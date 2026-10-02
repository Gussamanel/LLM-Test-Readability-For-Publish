from __future__ import annotations
# main.py
import os
import re
import torch
import subprocess
import urllib.request
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any

from bs4 import BeautifulSoup
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import SystemMessage, HumanMessage
from .. import prompts

from .retrieval import RetrievalConfig, retrieve_context_multi
from .chunking import build_chunks, validate_chunks, preview_chunks, preview_first_code_chunk

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from langchain_huggingface import HuggingFacePipeline


# ============================================================
# 0) MULTI-REPO SPEC
# ============================================================

@dataclass(frozen=True)
class RepoSpec:
    repo_id: str
    repo_root: str
    persist_directory: str
    git_url: Optional[str] = None
    docs_urls: Tuple[str, ...] = ()


def ensure_repo_local(spec: RepoSpec) -> str:
    repo_root = os.path.abspath(spec.repo_root)

    if spec.git_url:
        if not os.path.isdir(repo_root) or not os.path.isdir(os.path.join(repo_root, ".git")):
            os.makedirs(os.path.dirname(repo_root), exist_ok=True)
            print(f"Cloning {spec.repo_id} from {spec.git_url} -> {repo_root}")
            subprocess.check_call(["git", "clone", spec.git_url, repo_root])
        else:
            if os.getenv("RAG_FORCE_PULL", "0") == "1":
                print(f"Pulling latest for {spec.repo_id} in {repo_root}")
                subprocess.check_call(["git", "-C", repo_root, "pull", "--ff-only"])
            else:
                print(f"Repo {spec.repo_id} already local at {repo_root}. Skipping pull (set RAG_FORCE_PULL=1 to force).")

    if not os.path.isdir(repo_root):
        raise FileNotFoundError(f"Repo root not found: {repo_root}")

    return repo_root


# ============================================================
# 1) LLM + EMBEDDINGS
# ============================================================

def load_llm(model_id: str = "deepseek-ai/deepseek-coder-6.7b-instruct") -> tuple[HuggingFacePipeline, AutoTokenizer]:
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    bnb_cfg = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_id, token=token, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_cfg,
        device_map="auto",
        token=token,
    )

    gen_pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=1024,        # smaller = less rambling, we had 350 before
        do_sample=False,
        return_full_text=False,
        truncation=True,
    )
    return HuggingFacePipeline(pipeline=gen_pipe), tokenizer


def load_embeddings():
    from langchain_nomic import NomicEmbeddings
    return NomicEmbeddings(model="nomic-embed-text-v1.5", dimensionality=768)


# ============================================================
# 2) INGESTION
# ============================================================

@dataclass
class IngestedFile:
    repo_id: str
    path: str
    text: str
    kind: str


def _read_text_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1", errors="ignore") as f:
            return f.read()


def ingest_repository(
    repo_root: str,
    repo_id: str,
    include_ext: Tuple[str, ...] = (".py", ".md", ".rst", ".txt"),
    exclude_dirs: Tuple[str, ...] = (".git", ".venv", "venv", "__pycache__", "dist", "build", ".mypy_cache"),
) -> List[IngestedFile]:
    repo_root = os.path.abspath(repo_root)
    out: List[IngestedFile] = []

    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for name in files:
            p = os.path.join(root, name)
            ext = os.path.splitext(name)[1].lower()
            if ext not in include_ext:
                continue

            text = _read_text_file(p).strip()
            if not text:
                continue

            kind = "code" if ext == ".py" else "doc"
            rel_path = os.path.relpath(p, repo_root)
            scoped_path = f"{repo_id}:{rel_path}"

            wrapped = f"search_document: FILE: {scoped_path}\nKIND: {kind}\n\n{text}"
            out.append(IngestedFile(repo_id=repo_id, path=scoped_path, text=wrapped, kind=kind))

    print(f"Ingested {len(out)} files from {repo_id} at {repo_root}")
    return out


def ingest_doc_urls(repo_id: str, urls: Tuple[str, ...]) -> List[IngestedFile]:
    docs: List[IngestedFile] = []

    for i, url in enumerate(urls, start=1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()
            text = soup.get_text("\n").strip()
            if not text:
                continue

            virtual_path = f"{repo_id}:DOC_URL:{i}"
            wrapped = (
                f"search_document: FILE: {virtual_path}\n"
                f"KIND: doc\n"
                f"SOURCE_URL: {url}\n\n"
                f"{text}"
            )

            docs.append(IngestedFile(repo_id=repo_id, path=virtual_path, text=wrapped, kind="doc"))

        except Exception as e:
            print(f"[WARN] Failed to ingest docs from {url}: {e}")

    return docs


# ============================================================
# 3) VECTOR STORE
# ============================================================

def build_or_load_vector_store(chunks: List[Document], embeddings: NomicEmbeddings, persist_directory: str) -> Chroma:
    if os.path.isdir(persist_directory) and os.listdir(persist_directory):
        print(f"Loading existing Chroma DB from {persist_directory}")
        return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    print(f"Building new Chroma DB in {persist_directory}")
    return Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)


def build_indexes_for_repos(repos: List[RepoSpec]) -> Dict[str, Chroma]:
    embeddings = load_embeddings()
    vectorstores: Dict[str, Chroma] = {}

    debug_ingest = os.getenv("RAG_DEBUG_INGEST", "0") == "1"

    for spec in repos:
        repo_root = ensure_repo_local(spec)

        files = ingest_repository(repo_root=repo_root, repo_id=spec.repo_id)
        if spec.docs_urls:
            doc_files = ingest_doc_urls(spec.repo_id, spec.docs_urls)
            print(f"Ingested {len(doc_files)} external docs for {spec.repo_id}")
            files.extend(doc_files)

        chunks = build_chunks(files)

        validate_chunks(chunks)

        
        if debug_ingest:
            preview_chunks(chunks, n=15)
            preview_first_code_chunk(chunks)

        vectorstores[spec.repo_id] = build_or_load_vector_store(
            chunks=chunks,
            embeddings=embeddings,
            persist_directory=spec.persist_directory,
        )

    return vectorstores


# ============================================================
# 4) OUTPUT ENFORCEMENT + GUARDS
# ============================================================

FINAL_BLOCK_RE = re.compile(r"<final_code>\s*(.*?)\s*</final_code>", re.S)
FINAL_UNTIL_CLOSE_RE = re.compile(r"^(.*?)\s*</final_code>", re.S)

def extract_final(text: str) -> str:
    """
    Prefer <final_code>...</final_code>. If the model only emits </final_code> (common),
    take everything before </final_code>. Otherwise return trimmed text.
    """
    m = FINAL_BLOCK_RE.search(text)
    if m:
        return m.group(1).strip()

    m2 = FINAL_UNTIL_CLOSE_RE.search(text.strip())
    if m2:
        return m2.group(1).strip()
    
    # Fallback: Check for markdown code blocks
    code_block_match = re.search(r'```(?:python)?\n(.*?)\n```', text, re.DOTALL | re.IGNORECASE)
    if code_block_match:
        return code_block_match.group(1).strip()

    return text.strip()


def semantic_guard(original: str, refactored: str) -> str:
    """
    Fail-closed checks to prevent the exact bad behavior
    (dropping asserts / removing start/stop / removing pytest.raises)
    """
    def has(s: str) -> bool:
        return s in original

    if "assert" in original and "assert" not in refactored:
        return original

    if "pytest.raises" in original and "pytest.raises" not in refactored:
        return original

    # If original explicitly calls start/stop, refactor must keep them.
    if ".start(" in original and ".start(" not in refactored:
        return original
    if ".stop(" in original and ".stop(" not in refactored:
        return original

    return refactored


# ============================================================
# 5) RAG CHAIN
# ============================================================


def build_test_refactor_rag_chain(
    llm: BaseLanguageModel,
    vectorstores: Dict[str, Chroma],
    tokenizer,
    cfg: RetrievalConfig,
    model_max_input: int = 16384,
    prompt_type: str = "base",
):
    # Load readability guidelines
    try:
        guidelines_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "readability_guidelines.md")
        with open(guidelines_path, "r", encoding="utf-8") as f:
            readability_guidelines = f.read()
    except Exception as e:
        print(f"[WARN] Could not load readability guidelines: {e}")
        readability_guidelines = "Follow standard Python readability best practices."

    # ---------------------------------------------------------
    # PROMPT STRATEGIES
    # ---------------------------------------------------------
    # ------------------# 
    def _strategy_base(inputs):
        return [
            SystemMessage(content=prompts.get_system_prompt_constrained_instruction()),
            HumanMessage(content=prompts.base_user_prompt(
                inputs["context"], 
                inputs["test_code"], 
                # inputs["readability_guidelines"],
                inputs["imports"]
            ))
        ]
    # ------------------# 
    def _strategy_combined(inputs):
        return [
            SystemMessage(content=prompts.get_system_prompt_constrained_instruction()),
            HumanMessage(content=prompts.combined_user_prompt(
                inputs["context"], 
                inputs["test_code"], 
                # inputs["readability_guidelines"],
                inputs["imports"]
            ))
        ]
    # ------------------# 
    # ------------------# 
    def _strategy_self_critique(inputs):
        return [
            SystemMessage(content=prompts.get_system_prompt_self_critique()),
            HumanMessage(content=prompts.get_self_critique_user_prompt(
                inputs["context"], 
                inputs["test_code"], 
                # inputs["readability_guidelines"],
                inputs["imports"]
            ))
        ]
    # ------------------# 

    # ------------------# 
    def _strategy_constrained(inputs):
        return [
            SystemMessage(content=prompts.get_system_prompt_constrained_instruction()),
            HumanMessage(content=prompts.get_constrained_instruction_user_prompt(
                inputs["context"], 
                inputs["test_code"], 
                #inputs["readability_guidelines"],
                inputs["imports"]
            ))
        ]
    # ------------------# 

    # ------------------# 
    def _strategy_base_rag(inputs):
        # Use simple base prompt from prompts.py
        formatted = prompts.get_rag_base_prompt(
            readability_guidelines=inputs["readability_guidelines"],
            context=inputs["context"],
            imports=inputs["imports"],
            test_code=inputs["test_code"]
        )
        return [HumanMessage(content=formatted)]
    # ------------------# 

    # ------------------# 
    def _strategy_loose_self_critique(inputs):
        return [
            SystemMessage(content=prompts.get_system_prompt_self_critique()),
            HumanMessage(content=prompts.get_loose_self_critique_user_prompt(
                inputs["context"], 
                inputs["test_code"], 
                inputs["imports"]
            ))
        ]
    # ------------------# 

    def _strategy_chain_of_thought(inputs):
        return prompts.get_cot_user_prompt(
            inputs["context"],
            inputs["test_code"],
            inputs["imports"]
        )

    PROMPT_STRATEGIES = {
        "self_critique": _strategy_self_critique,
        "base": _strategy_base,
        "combined": _strategy_combined,
        "constrained": _strategy_constrained,
        "loose_self_critique": _strategy_loose_self_critique,
        "chain_of_thought": _strategy_chain_of_thought,
        "base_rag": _strategy_base_rag,
    }

    # dynamic dispatch
    def generate_prompt(inputs):
        # Selects the strategy based on prompt_type (defaults to "base")
        strategy = PROMPT_STRATEGIES.get(prompt_type, _strategy_base)
        return strategy(inputs)

    def _get_context(x):
        context_str = retrieve_context_multi(
            vectorstores=vectorstores,
            test_code=x["test_code"],
            tokenizer=tokenizer,
            module_hint=x.get("module_hint", ""),
            extra_hint=x.get("extra_hint", ""),
            cfg=cfg,
            max_input_tokens=model_max_input,
            reserved_for_generation=1500, # Increased reserve for guidelines + context
        )
        print(f"\n[DEBUG] Retrieved Context for test:\n{context_str[:1000]}...\n(Total chars: {len(context_str)})")
        return context_str

    rag_inputs = RunnableParallel(
        context=_get_context,
        test_code=lambda x: x["test_code"],
        imports=lambda x: x.get("extra_hint", ""),
        readability_guidelines=lambda _: readability_guidelines,
    )

    return rag_inputs | generate_prompt | llm | StrOutputParser()


# ============================================================
# 6) MAIN
# ============================================================

if __name__ == "__main__":
    REPOS: List[RepoSpec] = [
        RepoSpec(
            repo_id="codetiming",
            git_url="https://github.com/realpython/codetiming.git",
            repo_root="./repos/codetiming",
            persist_directory="./chroma_indexes/codetiming",
            docs_urls=("https://pypi.org/project/codetiming/",),
        ),
        RepoSpec(
            repo_id="flutils",
            git_url="https://gitlab.com/finite-loop/flutils.git",
            repo_root="./repos/flutils",
            persist_directory="./chroma_indexes/flutils",
            docs_urls=("https://pypi.org/project/flutils/",),
        ),
        RepoSpec(
            repo_id="httpie",
            git_url="https://github.com/httpie/cli.git",
            repo_root="./repos/httpie",
            persist_directory="./chroma_indexes/httpie",
            docs_urls=("https://httpie.io/docs",),
        ),
        RepoSpec(
            repo_id="py-backwards",
            git_url="https://github.com/nvbn/py-backwards.git",
            repo_root="./repos/py-backwards",
            persist_directory="./chroma_indexes/py-backwards",
            docs_urls=("https://pypi.org/project/py-backwards/",),
        ),
        RepoSpec(
            repo_id="pymonet",
            git_url="https://github.com/przemyslawjanpietrzak/pyMonet.git",
            repo_root="./repos/pymonet",
            persist_directory="./chroma_indexes/pymonet",
            docs_urls=("https://pypi.org/project/pymonet/",),
        ),
        RepoSpec(
            repo_id="pyutils",
            git_url="https://github.com/scottgasch/pyutils.git",
            repo_root="./repos/pyutils",
            persist_directory="./chroma_indexes/pyutils",
            docs_urls=("https://pypi.org/project/pyutils/",),
        ),
    ]

    vectorstores = build_indexes_for_repos(REPOS)
    llm, tokenizer = load_llm()

    generated_test_code = """
import pytest
from codetiming import Timer

def test_something():
    t = Timer()
    t.start()
    t.stop()
    assert t.last > 0
"""

    """
    import pytest
    from flutils.strutils import camel_to_underscore, underscore_to_camel

    def test_camel_and_underscore_conversions():
        assert camel_to_underscore("FooBar") == "foo_bar"
        assert underscore_to_camel("foo_bar") == "fooBar"
        assert underscore_to_camel("_one__two___", lower_first=False) == "OneTwo"
    """
    cfg = RetrievalConfig(
        search_type="mmr",
        k_code=4,
        k_docs=2,
        fetch_k=20,
        lambda_mult=0.4,
        include_docs=True,
        max_code_total=8,
        max_docs_total=2,
        max_chars_per_doc=1200,
    )

    rag_refactor = build_test_refactor_rag_chain(
        llm=llm,
        vectorstores=vectorstores,
        tokenizer=tokenizer,
        cfg=cfg,
        model_max_input=16384,
    )

    raw = rag_refactor.invoke({
        "test_code": generated_test_code,
        "module_hint": "codetiming timer logic",
        "extra_hint": "standard pytest structure",
    })

    final = extract_final(raw)
    final = semantic_guard(generated_test_code, final)

    print("-" * 30)
    print("REFACTORED TEST CODE:")
    print("-" * 30)
    print(final)
    