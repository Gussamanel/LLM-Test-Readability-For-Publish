from __future__ import annotations
import os
import time
import random
from enum import Enum
from os import PathLike
import copy
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    PreTrainedModel,
    BitsAndBytesConfig,
)
from typing import Final, Optional, Any
from dotenv import load_dotenv

load_dotenv()

# MONKEY PATCH: Fix bitsandbytes incorrectly expecting torch attributes
if not hasattr(torch._C, "_has_xpu"):
    torch._C._has_xpu = False

if hasattr(torch, "compiler") and not hasattr(torch.compiler, "is_compiling"):
    torch.compiler.is_compiling = lambda: False
elif not hasattr(torch, "compiler"):
    import types
    torch.compiler = types.ModuleType("torch.compiler")
    torch.compiler.is_compiling = lambda: False

# =========================
# Exceptions
# =========================
class TokenError(Exception):
    """Base class for token-related exceptions in the model."""
    pass

class NegativeTokenCountError(TokenError):
    """Raised when the token count becomes negative."""
    def __init__(self, message="Negative token count: context window exceeded."):
        super().__init__(message)

class InsufficientAllowedTokensError(TokenError):
    """Raised when there are insufficient tokens for response generation."""
    def __init__(self, allowed_tokens: int):
        message = f"Insufficient allowed tokens. Minimum required is 1000. Allowed tokens: {allowed_tokens}."
        super().__init__(message)

class ModelLoadingException(Exception):
    def __init__(self, model_name_or_path: str | PathLike):
        super().__init__(f"{model_name_or_path} is being loaded.")

class UnsupportedModelException(Exception):
    def __init__(self, model_type: str):
        super().__init__(f"{model_type} is not supported right now.")

# =========================
# Model Types
# =========================
class ModelType(Enum):
    DEEPSEEK = "deepseek"
    OTHER = "other"

# =========================
# Model Wrapper (Base & Local)
# =========================
class Model:
    _SYSTEM_PROMPT: Final[str] = "You are a helpful AI assistant."
    _MODELS: Final[dict[str | PathLike, Model]] = {}

    def __init__(
        self,
        model_name: str,
        tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast = None,
        model: PreTrainedModel = None,
        max_new_tokens: int = 2048,
        context_window: int = 4096,
        temperature: float = 0.1,
        hf_token: str = None
    ):
        self.model_name = model_name.lower()
        self.tokenizer = tokenizer
        self.model = model
        self._max_new_tokens = max_new_tokens
        self._context_window = context_window
        self.temperature = temperature
        self.hf_token = hf_token

        if "deepseek" in self.model_name:
            self.type = ModelType.DEEPSEEK
        else:
            self.type = ModelType.OTHER

    @property
    def max_new_tokens(self) -> int:
        return self._max_new_tokens

    @max_new_tokens.setter
    def max_new_tokens(self, value: int) -> None:
        if value <= 0:
            raise ValueError("max_new_tokens must be positive.")
        self._max_new_tokens = value

    @property
    def context_window(self) -> int:
        return self._context_window

    @context_window.setter
    def context_window(self, value: int) -> None:
        if value <= 0:
            raise ValueError("context_window must be positive.")
        self._context_window = value

    # ---------------------
    # Response generation
    # ---------------------
    def get_response(
        self,
        history: list[dict[str, str]],
        prompt: str,
        *,
        dynamic_max_tokens: bool = True
    ) -> str:
        # 1. Update history
        history.append({"role": "user", "content": prompt})

        # 2. Tokenize / Format input
        input_ids = self.tokenizer.apply_chat_template(
            history, 
            add_generation_prompt=True, 
            return_tensors="pt"
        )
        
        # Ensure we are on the correct device (GPU if available)
        device = self.model.device
        input_ids = input_ids.to(device)

        if hasattr(input_ids, "keys") and "input_ids" in input_ids:
            input_ids = input_ids["input_ids"]

        # 3. Calculate max tokens
        total_input_tokens = input_ids.shape[1]
        
        if dynamic_max_tokens:
            max_allowed_tokens = self.context_window - total_input_tokens - 100
            if max_allowed_tokens < 0:
                raise NegativeTokenCountError()
            dynamic_max_new_tokens = min(2048, max(0, max_allowed_tokens))
        else:
            dynamic_max_new_tokens = min(2048, self.max_new_tokens)

        # 4. Generate
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids,
                max_new_tokens=dynamic_max_new_tokens,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # 5. Decode
        generated_tokens = outputs[0][total_input_tokens:]
        content = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)

        history.append({"role": "assistant", "content": content})
        return content

    # ---------------------
    # Token counting
    # ---------------------
    def count_tokens(self, history: list[dict[str, str]], prompt: str) -> int:
        history_copy = copy.deepcopy(history)
        history_copy.append({"role": "user", "content": prompt})
        input_ids = self.tokenizer.apply_chat_template(history_copy, add_generation_prompt=True, return_tensors="pt")
        if hasattr(input_ids, "keys") and "input_ids" in input_ids:
            input_ids = input_ids["input_ids"]
        return input_ids.shape[1]

    # ---------------------
    # Loading / caching
    # ---------------------
    @staticmethod
    def _get(model_name_or_path: str | PathLike) -> Model | None:
        return Model._MODELS.get(model_name_or_path)

    @staticmethod
    def get(
        model_name_or_path: str | PathLike,
        max_new_tokens: int = None,
        context_window: int = 16384,
        temperature: float = 0.1,
        hf_token: str = None
    ) -> 'Model | None':
        if model_name_or_path in Model._MODELS and Model._MODELS[model_name_or_path]:
            return Model._MODELS[model_name_or_path]

        m_path_str = str(model_name_or_path).lower()

        # Check if we should use DeepSeek API
        if "deepseek-v3" in m_path_str:
            return DeepSeekApiModel.load(
                model_name=str(model_name_or_path),
                temperature=temperature,
                max_new_tokens=max_new_tokens or 2048,
                context_window=context_window
            )

        # Check if we should use Chalmers Proxy (GPT-5 Mini or Claude 4.6 Sonnet)
        if "gpt" in m_path_str or "mini" in m_path_str:
            api_key = os.getenv("CHALMERS_GPT_API_KEY") or os.getenv("CHALMERS_API_KEY")
            base_url = os.getenv("CHALMERS_BASE_URL", "https://ai-gateway.portal.chalmers.se/llm/openai/v1")
            if not api_key:
                raise ValueError("CHALMERS_GPT_API_KEY or CHALMERS_API_KEY environment variable not set.")
            return ChalmersProxyModel.load(
                model_name="gpt-5-mini",
                api_key=api_key,
                base_url=base_url,
                temperature=temperature,
                max_new_tokens=max_new_tokens or 2048,
                context_window=context_window
            )

        if "claude" in m_path_str or "sonnet" in m_path_str:
            api_key = os.getenv("CHALMERS_CLAUDE_API_KEY") or os.getenv("CHALMERS_API_KEY")
            base_url = os.getenv("CHALMERS_BASE_URL", "https://ai-gateway.portal.chalmers.se/llm/openai/v1")
            if not api_key:
                raise ValueError("CHALMERS_CLAUDE_API_KEY or CHALMERS_API_KEY environment variable not set.")
            return ChalmersProxyModel.load(
                model_name="claude-sonnet-4-6",
                api_key=api_key,
                base_url=base_url,
                temperature=temperature,
                max_new_tokens=max_new_tokens or 2048,
                context_window=context_window
            )

        if max_new_tokens is None:
            raise ValueError("Cannot load model without max_new_tokens.")

        print(f"Loading local model: {model_name_or_path}...")
        
        token_arg = hf_token if hf_token else None

        tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path, 
            trust_remote_code=True, 
            token=token_arg
        )
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        try:
            import bitsandbytes
            has_bnb = True
        except ImportError:
            has_bnb = False

        load_in_4bit = False
        if has_bnb and "33b" in str(model_name_or_path).lower():
            load_in_4bit = True
            print("Usage of bitsandbytes detected: Enabling 4-bit quantization for memory efficiency.")
        
        device_map = "auto"
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            print(f"DEBUG: Found {device_count} GPUs.")
            if device_count == 1:
                 device_map = {"": 0}
                 print("DEBUG: Single GPU detected. Setting device_map={'': 0}")

        kwargs = {
            "device_map": device_map,
            "token": token_arg,
            "trust_remote_code": True
        }

        if load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
            kwargs["quantization_config"] = bnb_config
        else:
            kwargs["torch_dtype"] = torch.float16 if torch.cuda.is_available() else torch.float32

        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            **kwargs
        )
        model.eval()

        loaded_model = Model(
            tokenizer=tokenizer,
            model=model,
            model_name=str(model_name_or_path),
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            temperature=temperature,
            hf_token=hf_token
        )

        Model._MODELS[model_name_or_path] = loaded_model
        return loaded_model

# =========================
# DeepSeek API Model
# =========================
class DeepSeekApiModel(Model):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        base_url: str = "https://api.deepseek.com",
        tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast = None,
        max_new_tokens: int = 8192,
        context_window: int = 128000,
        temperature: float = 1.0,
    ):
        super().__init__(
            model_name=model_name,
            tokenizer=tokenizer,
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            temperature=temperature
        )
        from openai import OpenAI
        self.client = OpenAI(
            base_url=base_url, 
            api_key=api_key,
            timeout=180.0,
            max_retries=10
        )

    @classmethod
    def load(
        cls,
        model_name: str,
        temperature: float = 1.0,
        max_new_tokens: int = 8192,
        context_window: int = 128000
    ) -> DeepSeekApiModel:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set.")

        try:
            tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-33b-instruct", trust_remote_code=True)
        except Exception:
            print("Warning: Could not load local tokenizer for DeepSeekApiModel. Token counting may be inaccurate.")
            tokenizer = None

        instance = cls(
            model_name=model_name,
            api_key=api_key,
            tokenizer=tokenizer,
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            temperature=temperature
        )
        Model._MODELS[model_name] = instance
        return instance

    def get_response(
        self,
        history: list[dict[str, str]],
        prompt: str,
        *,
        dynamic_max_tokens: bool = True
    ) -> str:
        history.append({"role": "user", "content": prompt})

        print(f"Calling DeepSeek API for model: {self.model_name}...")
        
        # Use official deepseek-chat model
        api_model_name = "deepseek-chat"

        max_retries = 5
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=api_model_name,
                    messages=history,
                    temperature=self.temperature,
                    max_tokens=self.max_new_tokens,
                    stream=True
                )

                full_content = ""
                
                print(f"Receiving stream (attempt {attempt + 1}): ", end="", flush=True)
                for chunk in completion:
                    if not getattr(chunk, "choices", None):
                        continue
                    
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        full_content += content
                        print(content, end="", flush=True)
                print("\nStream finished.")

                # Store full response in history
                history.append({"role": "assistant", "content": full_content})
                return full_content

            except Exception as e:
                import openai
                if isinstance(e, (openai.InternalServerError, openai.APITimeoutError, openai.RateLimitError)):
                    if attempt < max_retries - 1:
                        delay = (base_delay ** attempt) + random.uniform(0, 1)
                        print(f"\nAPI Error (attempt {attempt + 1}): {e}. Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                        continue
                
                print(f"\nTerminal API Error: {e}")
                raise e

    def count_tokens(self, history: list[dict[str, str]], prompt: str) -> int:
        if self.tokenizer:
            return super().count_tokens(history, prompt)
        return len(str(history)) // 3

# =========================
# Nvidia API Model
# =========================
class NvidiaApiModel(Model):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast = None,
        max_new_tokens: int = 8192,
        context_window: int = 128000,
        temperature: float = 1.0,
    ):
        super().__init__(
            model_name=model_name,
            tokenizer=tokenizer,
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            temperature=temperature
        )
        from openai import OpenAI
        self.client = OpenAI(
            base_url=base_url, 
            api_key=api_key,
            timeout=180.0,
            max_retries=10
        )

    @classmethod
    def load(
        cls,
        model_name: str,
        temperature: float = 1.0,
        max_new_tokens: int = 8192,
        context_window: int = 128000
    ) -> NvidiaApiModel:
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            raise ValueError("NVIDIA_API_KEY environment variable not set.")

        # Use a compatible tokenizer for local counting if possible, 
        # otherwise we can use a generic one or just trust the API
        # For now, let's try to load the deepseek-v3 tokenizer if available, 
        # or fall back to a common one like deepseek-coder-33b-instruct which is likely already cached.
        try:
            tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-33b-instruct", trust_remote_code=True)
        except Exception:
            print("Warning: Could not load local tokenizer for NvidiaApiModel. Token counting may be inaccurate.")
            tokenizer = None

        instance = cls(
            model_name=model_name,
            api_key=api_key,
            tokenizer=tokenizer,
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            temperature=temperature
        )
        Model._MODELS[model_name] = instance
        return instance

    def get_response(
        self,
        history: list[dict[str, str]],
        prompt: str,
        *,
        dynamic_max_tokens: bool = True
    ) -> str:
        history.append({"role": "user", "content": prompt})

        print(f"Calling NVIDIA API for model: {self.model_name}...")
        
        # Determine actual model name to use from the path
        api_model_name = self.model_name
        if api_model_name == "deepseek-v3":
             api_model_name = "deepseek-ai/deepseek-v3.2"

        max_retries = 5
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=api_model_name,
                    messages=history,
                    temperature=self.temperature,
                    top_p=0.95,
                    max_tokens=self.max_new_tokens,
                    extra_body={"chat_template_kwargs": {"thinking": True}},
                    stream=True
                )

                full_content = ""
                reasoning_tokens = ""
                
                print(f"Receiving stream (attempt {attempt + 1}): ", end="", flush=True)
                for chunk in completion:
                    if not getattr(chunk, "choices", None):
                        continue
                    
                    # Handle reasoning content
                    reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
                    if reasoning:
                        reasoning_tokens += reasoning
                        # If we want to show reasoning in logs, we can print it here
                        # print(reasoning, end="", flush=True) 

                    # Handle normal content
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        full_content += content
                        print(content, end="", flush=True)
                print("\nStream finished.")

                # Store full response in history
                history.append({"role": "assistant", "content": full_content})
                return full_content

            except Exception as e:
                import openai
                if isinstance(e, (openai.InternalServerError, openai.APITimeoutError, openai.RateLimitError)):
                    if attempt < max_retries - 1:
                        delay = (base_delay ** attempt) + random.uniform(0, 1)
                        print(f"\nAPI Error (attempt {attempt + 1}): {e}. Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                        continue
                
                # If it's a terminal error or we ran out of retries, re-raise
                print(f"\nTerminal API Error: {e}")
                raise e

    def count_tokens(self, history: list[dict[str, str]], prompt: str) -> int:
        if self.tokenizer:
            return super().count_tokens(history, prompt)
        # Fallback if no tokenizer
        return len(str(history)) // 3 # Very rough estimate

# =========================
# Chalmers API Model
# =========================
class ChalmersProxyModel(Model):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        base_url: str = "https://anast.ita.chalmers.se:4100/v1",
        tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast = None,
        max_new_tokens: int = 8192,
        context_window: int = 128000,
        temperature: float = 1.0,
    ):
        super().__init__(
            model_name=model_name,
            tokenizer=tokenizer,
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            temperature=temperature
        )
        from openai import OpenAI
        import httpx
        self.client = OpenAI(
            base_url=base_url, 
            api_key=api_key,
            timeout=180.0,
            max_retries=10,
            http_client=httpx.Client(verify=False)
        )

    @classmethod
    def load(
        cls,
        model_name: str,
        api_key: str,
        base_url: str = "https://ai-gateway.portal.chalmers.se/llm/openai/v1",
        temperature: float = 1.0,
        max_new_tokens: int = 8192,
        context_window: int = 128000
    ) -> "ChalmersProxyModel":
        try:
            import tiktoken
            tokenizer = tiktoken.get_encoding("cl100k_base")
        except Exception:
            tokenizer = None

        instance = cls(
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            tokenizer=tokenizer,
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            temperature=temperature
        )
        Model._MODELS[model_name] = instance
        return instance

    def get_response(
        self,
        history: list[dict[str, str]],
        prompt: str,
        *,
        dynamic_max_tokens: bool = True
    ) -> str:
        history.append({"role": "user", "content": prompt})

        print(f"Calling Chalmers API for model: {self.model_name}...")
        
        # GPT-5 mini on this proxy only supports temperature=1
        actual_temp = self.temperature
        if "gpt-5-mini" in self.model_name.lower():
            actual_temp = 1.0

        max_retries = 5
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                kwargs = {
                    "model": self.model_name,
                    "messages": history,
                    "temperature": actual_temp,
                    "stream": True
                }
                if "gpt-5-mini" in self.model_name.lower() or "mini" in self.model_name.lower():
                    kwargs["max_completion_tokens"] = self.max_new_tokens
                else:
                    kwargs["max_tokens"] = self.max_new_tokens

                completion = self.client.chat.completions.create(**kwargs)

                full_content = ""
                
                print(f"Receiving stream (attempt {attempt + 1}): ", end="", flush=True)
                for chunk in completion:
                    if not getattr(chunk, "choices", None):
                        continue
                    
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        full_content += content
                        print(content, end="", flush=True)
                print("\nStream finished.")

                history.append({"role": "assistant", "content": full_content})
                return full_content

            except Exception as e:
                import openai
                if isinstance(e, (openai.InternalServerError, openai.APITimeoutError, openai.RateLimitError)):
                    if attempt < max_retries - 1:
                        delay = (base_delay ** attempt) + random.uniform(0, 1)
                        print(f"\nAPI Error (attempt {attempt + 1}): {e}. Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                        continue
                
                print(f"\nTerminal API Error: {e}")
                raise e

    def count_tokens(self, history: list[dict[str, str]], prompt: str) -> int:
        if self.tokenizer:
            try:
                full_text = "\n".join(m.get("content", "") for m in history) + "\n" + prompt
                return len(self.tokenizer.encode(full_text))
            except Exception:
                pass
        return len(str(history) + prompt) // 3 # Fallback estimate

# =========================
# Session
# =========================
class Session:
    _SESSIONS: dict[str, Session] = {}

    def __init__(
        self,
        name: str,
        model_name_or_path: str | PathLike,
        *,
        max_new_tokens: int,
        system_prompt: str,
        context_window: int = 16384,
        temperature: float = 0.1
    ):
        self.name = name
        self.model = Model.get(
            model_name_or_path,
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            temperature=temperature,
        )
        if not self.model:
            raise ModelLoadingException(model_name_or_path)

        self._system_prompt = system_prompt
        self._history = [{"role": "system", "content": system_prompt}]

    @staticmethod
    def create(
        name: str,
        model_name_or_path: str | PathLike,
        max_new_tokens: int,
        system_prompt: str = Model._SYSTEM_PROMPT,
        temperature: float = 0.1
    ) -> Session:
        session = Session.get(name)
        if session:
            return session

        session = Session(name, model_name_or_path, max_new_tokens, system_prompt, temperature)
        Session._SESSIONS[name] = session
        return session

    @staticmethod
    def get(name: str) -> Session | None:
        return Session._SESSIONS.get(name)

    @property
    def system_prompt(self) -> str:
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, system_prompt: str) -> None:
        if not system_prompt:
            system_prompt = Model._SYSTEM_PROMPT
        self._system_prompt = system_prompt
        self._history[0] = {"role": "system", "content": self._system_prompt}

    def prompt(self, prompt: str) -> str:
        return self.model.get_response(self._history, prompt, dynamic_max_tokens=True)

    def clear(self) -> None:
        self._history = [{"role": "system", "content": self._system_prompt}]

    @property
    def history(self) -> list[dict[str, str]]:
        return copy.deepcopy(self._history)

    def delete(self) -> None:
        del Session._SESSIONS[self.name]