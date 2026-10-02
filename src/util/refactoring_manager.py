import os
import re
import time
from .model_lib import Model, NegativeTokenCountError, InsufficientAllowedTokensError, TokenError
from . import file_handler
from . import extractor
from datetime import datetime
from . import prompts
from io import StringIO
import pytest
import sys
from . import pytest_runner
from dotenv import load_dotenv
from .rag.langchain_model_adapter import LangChainModelAdapter
from langchain_openai import ChatOpenAI
from pathlib import Path
from typing import List
from .model_lib.models_thesis import Model


load_dotenv()

class RefactorManager:
    def __init__(
        self,
        model_name: str,
        version: str,
        system_prompt: str,
        temperature: float = 0.7,
        directory: str = "./DefaultDirectory/",
        test_path: str = None,
        modules_paths: List[str] = None,
        vectorstores=None,  # CHANGED: vector_store -> vectorstores
        hf_token: str = None,
        prompt_type: str = "base",
    ):
        """
        Initializes a RefactorManager using Hugging Face streaming for DeepSeek models.
        """
        if test_path is None and modules_paths is None:
            raise ValueError("Both 'test_path' and 'modules_paths' must be provided.")
        
        self.prompt_type = prompt_type

        # Determine model path and context window
        if model_name == "deepseek-coder":
            model_path = "deepseek-ai/deepseek-coder-33b-instruct"
            context_window = 16384
        elif model_name == "deepseek-v3":
            model_path = "deepseek-ai/DeepSeek-V3.2"
            context_window = 128000
        elif "gpt" in model_name.lower() or "mini" in model_name.lower():
            model_path = model_name
            context_window = 128000
        elif "claude" in model_name.lower() or "sonnet" in model_name.lower():
            model_path = model_name
            context_window = 200000
        else:
            raise ValueError(f"Unsupported model_name: {model_name}")

        max_new_tokens = 8192
        self._system_prompt = system_prompt or Model._SYSTEM_PROMPT
        self._temperature = temperature
        self._directory = directory
        self._log_dir = os.path.join(directory, "Log")
        os.makedirs(self._log_dir, exist_ok=True)

        # Hugging Face token (optional for API models)
        hf_token = os.getenv("HF_TOKEN") or hf_token

        # AGGRESSIVE MEMORY CLEANUP
        import gc
        import torch
        gc.collect()
        torch.cuda.empty_cache()

        self.model = Model.get(
            model_name_or_path=model_path,
            hf_token=hf_token,
            temperature=self._temperature,
            max_new_tokens=max_new_tokens,
        )

        # Load test modules
        self._modules_paths = [os.path.abspath(p) for p in modules_paths]
        self._modules = file_handler.get_modules_under_test(self._modules_paths)
        self._test_path = test_path
        self.old_imports, self._test_cases = extractor.extract_test_cases(test_path)

        # Synchronize model's system prompt and temperature
        self.model.system_prompt = self._system_prompt
        self.model.temperature = self._temperature

        # Other attributes
        self._new_imports = None
        self._log_responses_refactoring_path = None
        self._refactored_file_path = None
        self._functions = None
        self._summarized_functions = None
        self._version = version.lower()

        # Wrap with LangChain adapter if needed
        self.llm = LangChainModelAdapter(self.model)

        # Optional RAG
        # We now expect a dict of vectorstores and we pass the tokenizer too
        if vectorstores:
            from .rag.rag_refactorer import TestRefactorRAG
            self.rag = TestRefactorRAG(
                llm=self.llm, 
                vectorstores=vectorstores, 
                tokenizer=self.model.tokenizer,
                prompt_type=self.prompt_type
            )
        else:
            self.rag = None

        # Info printout
        info = f"""
        Model created: 
        Model name: {model_name}
        Model path: {model_path}
        Model temperature: {self.model.temperature}
        Model system prompt: {self.model.system_prompt}
        Version: {self._version}
        Context window: {context_window}
        Directory: {self._directory}
        Log directory: {self._log_dir}
        Modules paths: {self._modules_paths}
        Test path: {self._test_path}
        """
        print(info)

    
    ##############################################################################
    # Methods - helper functions
    ##############################################################################

    def get_model_temperature(self) -> float:
        """
        Retrieves the current temperature setting from the model.

        Returns:
        --------
        float - The model's temperature setting.
        """
        return self.model.temperature
    
    def count_tokens(self, prompt: str) -> int:
        """
        Counts the tokens for the provided prompt and the current system prompt
        using the model's tokenization.

        #Context window
        #LLama3 has 8000 token limit : https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct
        #LLama3.1 has 128 k token limit: 

        Parameters:
        -----------
        prompt: str - The user prompt to tokenize and count.

        Returns:
        --------
        int - The total number of tokens for the input and system prompt.
        """
        # Only include the system prompt and the latest user prompt in the message history
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Forward the counting to the model's token counter
        return self.model.count_tokens(messages, prompt)

    def get_response(self, prompt: str) -> str:
        """
        Generates a response from the model without using conversation history.

        Parameters:
        -----------
        prompt: str - The prompt to send to the model.

        Returns:
        --------
        str - The model's response.
        """
        # Sleep for 6 seconds to avoid API rate limits
        time.sleep(6)

        # Only include the system prompt and the latest user prompt in the message history
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        try:
            dynamic_max_tokens = True
            response = self.model.get_response(messages, prompt, dynamic_max_tokens=dynamic_max_tokens)
    
        except NegativeTokenCountError as err:
            print("Negative token count: Triggering summarization or alternative flow.")
            response = 0
    
        except InsufficientAllowedTokensError as err:
            print(f"Token limit exceeded. Allowed tokens: {err.allowed_tokens}.")
            response = 1
        
        except Exception as err:
            import traceback
            traceback.print_exc()
            print(f"Error during get_response: {err}")
            response = None
            
        return response
    
    def get_and_extract_response(self, user_prompt):
        response = self.get_response(user_prompt)
        extracted_response = extractor.extract_response(response)
        return response, extracted_response

    def get_and_save_new_imports(self, log_file_name="test_case_logs"):

        import_prompt = prompts.get_import_user_prompt(self.old_imports)

        new_imports_response = self.get_response(import_prompt)

        post_process_imports = extractor.extract_response(new_imports_response)
        
        self._new_imports = post_process_imports

        import_log_template = file_handler.get_log_imports_template(self.system_prompt, import_prompt, new_imports_response, post_process_imports)

        log_file_name = f"{log_file_name}.txt"
        
        log_file_path = file_handler.create_text_file(self._log_dir, log_file_name, import_log_template)

        self._log_responses_refactoring_path = log_file_path
        
        self._refactored_file_path = file_handler.create_refactored_python_file(self._directory, self._test_path, post_process_imports, self._version)

        info = f"""" 
        \n 
        ***********************\n
        ** New imports saved **\n
        ***********************\n
        Previous imports:  {self.old_imports}
        New imports:  {self._new_imports}
        \n
        Directory:  {self._directory}
        Refactored file path:  {self._refactored_file_path}
        Log directory:  {self._log_dir}
        Log file path:  {self._log_responses_refactoring_path}
        *******************************************************        
        \n\n\n
        """

        return info

    def log_model_response(self, user_prompt, response, refactored_test_case, counter = 0):
        log_response = file_handler.get_log_response_template(self.system_prompt, user_prompt, response, refactored_test_case, counter)

        log_file_path = file_handler.append_text_file(self._log_responses_refactoring_path, log_response)
        
        if log_file_path != self._log_responses_refactoring_path:
            raise ValueError("Error in summarize functions while appending first refactoring of test case to log file")

        info = f""""\n
        ***********************\n
        ** Loggin Response **\n
        ***********************\n
        response:  {response}   \n
        refactored_test_case:  {refactored_test_case}   \n\n
        Log file used:  {log_file_path}   \n
        *******************************************************
        \n\n\n
        """ 

        #print("\n", info)

        return log_file_path           

    
    def save_and_log_test_case(self, user_prompt, response, post_process_response=None, counter=0):
        if post_process_response is None:
            post_process_response = extractor.extract_response(response)  

        log_file_used = self.log_model_response(user_prompt, response, post_process_response)

        if log_file_used != self._log_responses_refactoring_path:
            raise ValueError("Error in saving and logging test case")

        refactored_file_path = file_handler.append_test_case(self._refactored_file_path,post_process_response)

        if isinstance(refactored_file_path, list):
            if len(refactored_file_path) != 1 or refactored_file_path[0] != self._refactored_file_path:
                raise ValueError("Error in appending test case to refactored file")
        else:
            if refactored_file_path != self._refactored_file_path:
                raise ValueError("Error in appending test case to refactored file")
        
        info = f""""\n
        ***********************\n
        ** New test case saved **\n
        ***********************\n
        post_process_response:  {post_process_response}   \n\n
        Refactored file path:  {refactored_file_path}   \n
        *******************************************************
        \n\n\n
        """
        print(info)


        # Summarize a dictionary of functions and returns a dictionary of the summarized functions
    def summarize_functions(self, used_functions=None):
        if used_functions is None:
            if self._functions is None:
                self._functions = extractor.extract_functions_from_files(self._modules_paths)
            
            functions = self._functions
        else:
            functions = used_functions

        summarized_functions = {}

        self.system_prompt = prompts.get_system_prompt_summary()

        sum_file_path = f'{self.log_dir}log_of_summary-of-functions.txt'

        with open(sum_file_path, 'w') as file:
            for name, function in functions.items():
                print(f"Summarizing function: {name}")
                user_prompt = f"Make a concise summary of this function:\n{function}\n"
                
                response = self.get_response(user_prompt)
                if response == 0 or response == 1:
                    functions_tokens = self.count_tokens(function)
                    raise ValueError(f"The total prompt is {functions_tokens} which is above the context windows of the choicen model ({self._context_window} tokens).")

                summarized_functions[name] = response
                log_summary = file_handler.get_log_summary_template(name, user_prompt, response)

                # Write to text file
                file.write(log_summary)

        self._summarized_functions = summarized_functions
        self.system_prompt = prompts.get_system_prompt_readability()

        return summarized_functions
    

    def last_prompt(self, refactored_test_case, counter=0):
        #Final prompt
            functions_names = extractor.extract_function_names(self._refactored_file_path)
        
            final_prompt = prompts.final_prompt(functions_names, refactored_test_case)

            response, refactored_test_case = self.get_and_extract_response(final_prompt)

            self.save_and_log_test_case(final_prompt, response,refactored_test_case)



    # Runs the summarize script, each test case is send to the model together with the text summariry of the funcions. The test case is extracted from the response and then it send again to the model together with the existing test functions names from the refactored file. The refactored file is updated with the new test case and the log file is updated with the response of the model.
    
    
    def assertion_cleanup(self, refactored_test_case):

        prompt = prompts.get_cleanup_user_prompt(refactored_test_case)

        response, cleaned_test_case = self.get_and_extract_response(prompt)

        _ = self.log_model_response(user_prompt=prompt, response=response, refactored_test_case=cleaned_test_case)

        return cleaned_test_case


    #Summarize one functions instead of all the functions. 
    def extract_one_tests_functions(self, test_case):
        version="functions"
        if self._functions is None:
            self._functions = extractor.extract_functions_from_files(self._modules_paths)

        all_functions, _ = extractor.extract_used_functions(test_case, self._functions)

        user_prompt = prompts.generate_first_prompt_for_one_test_case_functions(
            self._new_imports, test_case, all_functions, version
        )

        return  refactored
    
    ''''
    def refactor_failed_test(self, failed_tests):
        """Refactor failed tests or fix errors, save to new file, and return results"""
        if not failed_tests:
            print("No test failures or errors to address")
            return None, None

        try:
            # Determine the refactored file to work with
            if isinstance(self._refactored_file_path, list):
                if not self._refactored_file_path:
                    raise ValueError("Refactored file path list is empty.")
                refactored_path = self._refactored_file_path[0]
                print(f"Multiple refactored files provided. Using the first: {refactored_path}")
            else:
                refactored_path = self._refactored_file_path

            # Create updated file path with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_path = os.path.splitext(refactored_path)
            updated_file_path = f"{base_path[0]}_updated_{timestamp}{base_path[1]}"

            # Copy original content
            with open(refactored_path, "r") as f:
                original_content = f.read()
            with open(updated_file_path, "w") as f:
                f.write(original_content)

            # Detect import alias for the module under test to fix NameErrors
            # Look for: import module_name as alias OR from . import module_name as alias
            import_alias = "module_0" # Default fallback
            
            # Simple heuristic to find the module name from the file path
            # e.g., codetiming_timer.py -> codetiming_timer
            if self._modules_paths:
                module_name = os.path.basename(self._modules_paths[0]).replace(".py", "")
                
                # Check how it's imported in the test file
                # Pattern: import {module_name} as (\w+)
                match = re.search(f"import\\s+{module_name}\\s+as\\s+(\\w+)", original_content)
                if match:
                    import_alias = match.group(1)
                else:
                    # Pattern: from .* import {module_name} as (\w+)
                    match = re.search(f"from\\s+.*\\s+import\\s+{module_name}\\s+as\\s+(\\w+)", original_content)
                    if match:
                        import_alias = match.group(1)
                    else:
                        # If no alias, maybe it's imported directly?
                         if f"import {module_name}" in original_content:
                             import_alias = module_name

            print(f"Detected import alias/name: {import_alias}")

            # Set system prompt for pytest fixing
            self.model.system_prompt = prompts.get_system_prompt_pytest_fixer()

            # Handle collection errors first
            if "Collection Error" in failed_tests:
                error_info = failed_tests["Collection Error"]
                print(f"\nAddressing {error_info.get('type', 'unknown')} error")

                if error_info.get('type') == 'import_error':
                    fix_prompt = prompts.get_import_error_prompt(error_info)
                elif error_info.get('type') == 'syntax_error':
                    fix_prompt = prompts.get_syntax_error_prompt(error_info)
                else:
                    fix_prompt = (
                        f"Fix this error:\nType: {error_info.get('type', 'unknown')}\n"
                        f"Message: {error_info.get('message', '')}\n"
                        f"Traceback:\n{error_info['traceback']}\n"
                        "Provide a solution with corrected code in a Python block."
                    )

                llm_response = self.get_response(fix_prompt)
                if llm_response and isinstance(llm_response, str):
                    llm_response = extractor.extract_response(llm_response)

                    
                    # Fix module usage in response
                    if "module_0" in llm_response and import_alias != "module_0":
                         print(f"Replacing 'module_0' with '{import_alias}' in collection error fix")
                         llm_response = llm_response.replace("module_0", import_alias)

                    # Replace entire file content for collection errors
                    with open(updated_file_path, "w") as f:
                        f.write(llm_response)
                    print(f"Updated file created at: {updated_file_path}")

                # Skip normal test failures for collection errors
                return updated_file_path, self.run_pytest_on_updated_file(updated_file_path)

            # Handle normal test failures
            print("\nAddressing failed tests")

            module_content = None
            if self._modules_paths:
                try:
                    with open(self._modules_paths[0], 'r') as f:
                        module_content = f.read()
                except Exception as e:
                    print(f"Couldn't load module content: {str(e)}")

            for test_file, failures in failed_tests.items():
                if not failures:
                    continue

                print(f"Found {len(failures)} failures in {test_file}")

                for test_name, test_content in failures.items():
                    if not isinstance(test_content, str):
                        print(f"Skipping non-string test content: {test_name}")
                        continue

                    print(f"- Refactoring: {test_name}")

                    # Determine failure type
                    failure_type = None
                    if "AssertionError" in test_content:
                        failure_type = "AssertionError"
                    elif "Timeout" in test_content:
                        failure_type = "Timeout"

                    # Generate prompt with module context
                    fix_prompt = prompts.get_test_failure_prompt(
                        test_name=test_name,
                        test_content=test_content,
                        failed_module=module_content,
                        failure_type=failure_type
                    )
                    llm_response = self.get_response(fix_prompt)

                    if llm_response and isinstance(llm_response, str):
                        llm_response = extractor.extract_response(llm_response)

                        
                        # Fix module usage in response
                        if "module_0" in llm_response and import_alias != "module_0":
                             print(f"Replacing 'module_0' with '{import_alias}' in test fix")
                             llm_response = llm_response.replace("module_0", import_alias)

                        # Replace the old test in the file
                        with open(updated_file_path, "r") as f:
                            current_content = f.read()
                        
                        # Fallback if specific test content isn't found exactly (sometimes indentation/formatting differs)
                        if test_content not in current_content:
                             print(f"Warning: Exact test content match not found for {test_name}. Trying regex replacement.")
                             # Try to find the function definition by name and replace roughly
                             pattern = fr"def {test_name}\(\):.*?(?=\ndef |$)"
                             if re.search(pattern, current_content, re.DOTALL):
                                 updated_content = re.sub(pattern, llm_response, current_content, flags=re.DOTALL)
                             else:
                                 print(f"Could not find function {test_name} to replace.")
                                 updated_content = current_content
                        else:
                             updated_content = current_content.replace(test_content, llm_response)

                        with open(updated_file_path, "w") as f:
                            f.write(updated_content)

                        print(f"Updated test case: {test_name}")

            # Verify fixes
            print("\nValidating fixes...")
            verification_result = self.run_pytest_on_updated_file(updated_file_path)

            # Save verification results
            results_dir = os.path.join(self._directory, "verification_results")
            os.makedirs(results_dir, exist_ok=True)
            results_filename = f"verification_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            results_path = os.path.join(results_dir, results_filename)

            with open(results_path, 'w') as f:
                if not verification_result:
                    f.write("All test issues were resolved successfully!\n")
                    print("All issues resolved successfully!")
                else:
                    f.write(f"Found {len(verification_result)} remaining issues:\n\n")
                    for test_file, failures in verification_result.items():
                        f.write(f"File: {test_file}\n")
                        for test_name, error_info in failures.items():
                            f.write(f"- Test: {test_name}\n")
                            if isinstance(error_info, dict):
                                f.write(f"  Type: {error_info.get('type', 'unknown')}\n")
                                f.write(f"  Message: {error_info.get('message', '')}\n")
                                if 'context' in error_info:
                                    f.write(f"  Context:\n{error_info['context']}\n")
                            else:
                                f.write(f"  Error: {error_info}\n")
                        f.write("\n")
                    print(f"{len(verification_result)} issues remain after fixing")
            print(f"Verification results saved to: {results_path}")

            return updated_file_path, verification_result

        except Exception as e:
            print(f"Error during refactoring: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, None
       
    def run_pytest_on_updated_file(self, file_path):
        """Run pytest on updated file and return new failures"""
        captured_output = StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output

        try:
            # Ensure file_path is a list
            if isinstance(file_path, str):
                file_path = [file_path]

            exit_code = pytest.main([os.path.abspath(p) for p in file_path])
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        log_data = captured_output.getvalue()
        print(log_data)

        if exit_code == 0:
            print("\nAll refactored tests passed!")
            return None
        else:
            print("\nSome refactored tests still fail")
            return pytest_runner.extract_failed_tests(log_data, file_path)
    '''
    def sum_functions_for_one_test_case(self, test_case):
        version="summarize"
        if self._functions is None:
            self.functions = extractor.extract_functions_from_files(self._modules_paths)

        _, used_functions = extractor.extract_used_functions(test_case, self._functions)

        summarized_functions = self.summarize_functions(used_functions)

        all_summarized_functions = '\n'.join(summarized_functions.values()) + '\n'

        user_prompt = prompts.generate_first_prompt_for_one_test_case_functions(
            self._new_imports, test_case, all_summarized_functions, version
        )
        
        response, refactored = self.get_and_extract_response(user_prompt)

        self.log_model_response(user_prompt, response, refactored)
        
        return refactored
    

    ##############################################################################
    # Scripts
    # Script verrions:    ***Note: Version lower() in the constructor***
    #                   mix,       mix-cleanup 
    #                   summarize, summarize-cleanup
    #                   functions, functions-cleanup
    ##############################################################################


    def run_summarize_functions(self):
        if self.rag:
            print("\nRunning RAG-based refactoring (Summarize mode)...")
            counter = 1
            for test_case in self._test_cases:
                try:
                    raw_response = self.rag.refactor_raw(test_code=test_case, module_hint=self.old_imports)
                    refactored_test_case = extractor.extract_response(raw_response)
                    
                    self.log_model_response(f"RAG Retrieval for test case {counter}", raw_response, refactored_test_case, counter)
                    
                    if "cleanup" in self._version:
                        refactored_test_case = self.assertion_cleanup(refactored_test_case)
                    
                    self.last_prompt(refactored_test_case, counter)
                except Exception as e:
                    print(f"Error refactoring test case {counter} (Summarize RAG): {e}")
                
                counter += 1
            return "Summarize functions (RAG) completed"

        if self._summarized_functions == None:
            self._summarized_functions = self.summarize_functions()
  
        #Generate prompt using the summary of the functions
        test_case_prompts = prompts.generate_first_all_prompts_with_functions(self._new_imports, self._test_cases, self._summarized_functions, self._version)
        
        counter = 1

        for prompt in test_case_prompts:
            try:
                #First prompt
                response = self.get_response(prompt)
                if(response == 0 or response == 1):
                    raise ValueError("Token error in summarizing test cases")
                
                refactored_test_case = extractor.extract_response(response)

                self.log_model_response(prompt, response, refactored_test_case, counter)

                #Second prompt
                if self._refactored_file_path is None:
                    raise ValueError("Refactored file path is None")
                
                if "cleanup" in self._version:
                    refactored_test_case = self.assertion_cleanup(refactored_test_case)

                self.last_prompt(refactored_test_case, counter)
            except Exception as e:
                print(f"Error refactoring test case {counter} (Summarize): {e}")
        
            counter += 1
        

        return "Summarize functions completed"

    def run_with_functions(self):
        if self.rag:
            print("\nRunning RAG-based refactoring (Functions mode)...")
            counter = 1
            for test_case in self._test_cases:
                try:
                    # Assuming new imports are available in self._new_imports
                    extra_hint_imports = self._new_imports if self._new_imports else ""
                    raw_response = self.rag.refactor_raw(
                        test_code=test_case, 
                        module_hint=self.old_imports,
                        extra_hint=extra_hint_imports
                    )
                    refactored_test_case = extractor.extract_response(raw_response)
                    
                    self.log_model_response(f"RAG Retrieval for test case {counter}", raw_response, refactored_test_case, counter)

                    if "cleanup" in self._version:
                        refactored_test_case = self.assertion_cleanup(refactored_test_case)

                    self.last_prompt(refactored_test_case, counter)
                except Exception as e:
                    print(f"Error refactoring test case {counter} (Functions RAG): {e}")

                counter += 1
            return 

        if self._functions is None:
            self._functions = extractor.extract_functions_from_files(self._modules_paths)

        test_case_prompts = prompts.generate_first_all_prompts_with_functions(self._new_imports, self._test_cases, self._functions, version="functions")

        counter = 1
        for prompt in test_case_prompts:
            try:
                response = self.get_response(prompt)

                if response == 0 or response == 1:
                    print("\nTokens exceeded the context window limit. Trying with summarizing functions\n")
                    response = self.sum_functions_for_one_test_case(test_case_prompts[counter])
                    if response == 0 or response == 1:
                        raise ValueError(f"Token error in running with functions. \n During test: \n {test_case_prompts[counter]}")

                refactored_test_case = extractor.extract_response(response)

                if "cleanup" in self._version:
                    refactored_test_case = self.assertion_cleanup(refactored_test_case)

                self.last_prompt(refactored_test_case, counter)
            except Exception as e:
                print(f"Error refactoring test case {counter} (Functions): {e}")
            counter += 1


    def run_full_module(self):
        if self.rag:
            print("\nRunning RAG-based refactoring (Full Module mode)...")
            counter = 0
            for test_case in self._test_cases:
                try:
                    # Get the raw response from the RAG chain
                    raw_response = self.rag.refactor_raw(
                        test_code=test_case, 
                        module_hint=self.old_imports,
                        extra_hint=extra_hint_imports
                    )
                    refactored_test_case = extractor.extract_response(raw_response)
                    
                    self.log_model_response(f"RAG Retrieval for test case {counter+1}", raw_response, refactored_test_case, counter+1)

                    if "cleanup" in self._version:
                       refactored_test_case = self.assertion_cleanup(refactored_test_case)         

                    self.last_prompt(refactored_test_case, counter+1)  
                except Exception as e:
                    print(f"Error refactoring test case {counter+1} (Full Module RAG): {e}")

                counter += 1
            return "Full module refactored (RAG) completed"

        test_case_prompts = prompts.generate_first_prompts_with_module(self._new_imports, self._test_cases, self._modules)

        counter = 0
        for prompt in test_case_prompts:
            try:
                response = self.get_response(prompt)
                if response == 0 or response == 1:
                    print("\nTokens exceeded the context window limit. Trying with functions\n")
                    response = self.extract_one_tests_functions(test_case_prompts[counter])
                    if response == 0 or response == 1:
                        print("\nTokens exceeded the context window limit. Trying with summarizing functions\n")
                        response = self.sum_functions_for_one_test_case(test_case_prompts[counter])
                        if response == 0 or response == 1:
                            raise ValueError("Token error in running full module, after using functions and summarizing functions")        


                refactored_test_case = extractor.extract_response(response)

                if "cleanup" in self._version:
                   refactored_test_case = self.assertion_cleanup(refactored_test_case)         

                self.last_prompt(refactored_test_case)
            except Exception as e:
                print(f"Error refactoring test case {counter+1} (Full Module): {e}")
            counter += 1
        
        return "Full module refactored completed"


##############################################################################
    # Getter and Setters
##############################################################################

    @property
    def old_imports(self):
        return self._old_imports   

    @old_imports.setter
    def old_imports(self, old_imports):
        self._old_imports = old_imports 

    @property
    def test_cases(self):
        return self._test_cases

    @test_cases.setter
    def test_cases(self, test_cases):
        self._test_cases = test_cases

    @property
    def modules_paths(self):
        return self._modules_paths

    @property
    def system_prompt(self) -> str:
        """
        Retrieves the current system prompt.
        
        Returns:
        --------
        str - The system prompt.
        """
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, system_prompt: str) -> None:
        """
        Sets the system prompt for both the manager and the model. If an empty string is provided, resets to the default system prompt.

        Parameters:
        -----------
        system_prompt: str - The system prompt to set.
        """
        if not system_prompt:
            system_prompt = Model._SYSTEM_PROMPT
        
        self._system_prompt = system_prompt

        # Update the system prompt in the model as well
        self.model.system_prompt = system_prompt

    @property
    def temperature(self) -> float:
        """
        Retrieves the current temperature setting.
        
        Returns:
        --------
        float - The temperature setting.
        """
        return self._temperature

    @temperature.setter
    def temperature(self, temperature: float) -> None:
        """
        Sets the temperature for both the manager and the model.

        Parameters:
        -----------
        temperature: float - The temperature setting to apply.
        """
        self._temperature = temperature

        # Update the temperature in the model as well
        self.model.temperature = temperature

    @property
    def directory(self):
        return self._directory


    @property
    def new_imports(self):
        return self._new_imports

    @new_imports.setter
    def new_imports(self, new_imports):
        self._new_imports = new_imports
        
    @property
    def log_dir(self):
        return self._log_dir
    
    @log_dir.setter
    def log_dir(self, log_dir):
        self._log_dir = log_dir

    @property
    def log_responses_refactoring_path(self):
        return self._log_responses_refactoring_path
    
    @log_responses_refactoring_path.setter
    def log_responses_refactoring_path(self, log_responses_refactoring_path):
        self._log_responses_refactoring_path = log_responses_refactoring_path


    @property
    def refactored_file_path(self):
        return self._refactored_file_path
    
    @refactored_file_path.setter
    def refactored_file_path(self, refactored_file_path):
        self._refactored_file_path = refactored_file_path

    @property
    def version(self):
        return self._version
    
    @property
    def functions(self):
        return self._functions
    
    @functions.setter
    def functions(self, functions):
        self._functions = functions


    @version.setter
    def version(self, version):
        self._version = version
 ##############################################################################
 # Extra 
 ##############################################################################       

    def further_summarization(self, user_prompt, summary):


        currentUserPromptTokens = self.count_tokens(user_prompt)

        #Summary not extracted!!!!!!!!
        print("Further summarization needed, current tokens used in the user prompt: ", currentUserPromptTokens)


        # Check test case tokens
        test_case = extractor.extract_test_case_from_prompt(user_prompt)
        test_case_tokens = self.count_tokens(test_case)


        Max_test_case_tokens = self._context_window - 200
        if(test_case_tokens > Max_test_case_tokens):
            print("Test case tokens: ", test_case_tokens)
            print("Max test case tokens: ", Max_test_case_tokens)
            raise ValueError("Test case tokens exceeded the context window limit.")

        self.system_prompt = prompts.get_system_prompt_further_summarization()

        user_prompt = f"The previous summary is too large. Please condense the information further by providing only the core details. Here is the summary: {summary}\n"

        response = self.get_response(user_prompt)
        return response