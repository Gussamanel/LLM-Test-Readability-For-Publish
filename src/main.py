try:
    import pysqlite3
    import sys
    sys.modules['sqlite3'] = pysqlite3.dbapi2
except ImportError:
    pass

from dotenv import load_dotenv
load_dotenv()

from .util import args_handler
from .util import file_handler
from .util import extractor
from .util import prompts
from .util import refactoring_manager
from .util import pytest_runner
from .util.data_analysis.data_collection import TestRunDataCollector
from .util.dan.dan_integration import DANIntegrator
#from .util.rag.rag import RepoSpec


import os
from typing import List

# -----------------------------
# Parse Arguments
# -----------------------------
args = args_handler.get_args()

module_path = args.paths
test_path = args.test_path
model = args.model
session = args.session
session_name = args.session_name
temperature = args.temperature
job = args.job
version = args.version
prompt_type = args.prompt_type
run = args.run

# -----------------------------
# Validation
# -----------------------------
if not module_path:
    raise ValueError("No module under test paths provided to extract functions from.")

if test_path is None:
    raise ValueError("No test path provided to extract functions from.")

# -----------------------------
# Load LLM system prompt
# -----------------------------
system_prompt = prompts.get_system_prompt_readability()

# -----------------------------
# Process each module
# -----------------------------

if isinstance(module_path, list):
    if len(module_path) == 0:
        raise ValueError("No module paths provided!")
    single_path = module_path[0]
else:
    single_path = module_path

# To handle cases where multiple files have the same name (e.g., base.py in different directories),
# we map each module path to a clean, unique module name that matches output/mini's structure.
single_path_abs = os.path.abspath(single_path)
if "httpie.plugins.base" in single_path_abs:
    module_name = "plugins_base.py"
elif "py_backwards.transformers.base" in single_path_abs:
    module_name = "transformers_base.py"
else:
    module_name = os.path.basename(single_path)

output_dir, session_name = file_handler.setup_output_dir(
    model, job, session, temperature, version, module_name, prompt_type, run, no_rag=args.no_rag
)

# Copy module and tests to output directory
file_handler.pytest_runner_set_up(module_path, test_path, output_dir)
print(f"Output directory: {output_dir}\n")

# -----------------------------
# RAG SETUP
# -----------------------------
vector_store = None
vectorstores = None
if not args.no_rag:
    from .util.rag.index_manager import RepoIndexManager, RepoSpec
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

    index_manager = RepoIndexManager(REPOS)
    vectorstores = index_manager.build()
else:
    print("RAG disabled by user flag.")

# -----------------------------
# Refactor manager
# -----------------------------
refactor_manager = refactoring_manager.RefactorManager(
    model_name=model,
    version=version,
    temperature=temperature,
    directory=output_dir,
    system_prompt=system_prompt,
    modules_paths=module_path,
    test_path=test_path,
    vectorstores=vectorstores, # Changed from vector_store
    hf_token=os.getenv("HF_TOKEN"),
    prompt_type=prompt_type,
)

# Generate imports
import_info = refactor_manager.get_and_save_new_imports()
print(import_info)

# Summarize functions / run with functions / full module
print(f"Running {version} script")
if "summarize" in version:
    refactor_manager.run_summarize_functions()
elif "function" in version:
    refactor_manager.run_with_functions()
elif "mix" in version:
    refactor_manager.run_full_module()

# -----------------------------
# Run pytest
# -----------------------------
test_files = {
    "Original Test Results": test_path,
    "Refactored Test Results": refactor_manager.refactored_file_path
}

pytest_output_dir = os.path.join(output_dir, "pytest_results")
os.makedirs(pytest_output_dir, exist_ok=True)

    # Run tests and collect detailed results, including collection errors
failed_tests, test_summary, coverage_summary, test_ran_status, detailed_results = pytest_runner.run_pytest_and_log_results(
    test_files,
    module_path,
    pytest_output_dir,
    combined=False
)

print("Failed tests:", failed_tests)

    # Refactor failed tests if any
#    refactor_manager.refactor_failed_test(failed_tests)

# -----------------------------
# Collect data
# -----------------------------
print(f"\nCollecting data for module: {module_path}\n")
collector = TestRunDataCollector(output_dir, module_name=module_name)

# LLM metadata
collector.set_llm_metadata(model_name=model, version=version, temperature=temperature, prompt_style=prompt_type, run_number=run)

# -----------------------------
# Filter results first
# -----------------------------
before_results = {
    k: v
    for k, v in detailed_results.get("Original Test Results", {}).items()
    if k != "Collection Error"  # remove any special keys
}

refactored_raw = detailed_results.get("Refactored Test Results", {})

# Final decision on after_results
if "Collection Error" in refactored_raw:
    after_results = {"collection_error": True}
else:
    after_results = {k: v for k, v in refactored_raw.items()}

# -----------------------------
# Compute summary after filtering
# -----------------------------
test_summary_corrected = {
    **test_summary,  # include original summary fields
    "total_tests_before": len(before_results),
    "total_tests_after": len(after_results),
}

collector.set_test_summary(test_summary_corrected)

# -----------------------------
# Store filtered results
# -----------------------------
collector.set_test_results("before_refactoring", before_results)
collector.set_test_results("after_refactoring", after_results)

# Coverage
collector.set_coverage_data(
    original_coverage=coverage_summary.get("Original Test Results", "N/A"),
    refactored_coverage=coverage_summary.get("Refactored Test Results", "N/A")
)

# -----------------------------
# DAN Scoring
# -----------------------------
print("\nComputing DAN Scores...")
try:
    dan_integrator = DANIntegrator(model_name="microsoft/codebert-base-mlm")
    
    # helper to handle list or string paths
    def get_score(path):
        if not path: return None
        if isinstance(path, list):
            path = path[0] # Take first for now, or average? simple approach: first
        return dan_integrator.compute_score(path, output_dir)

    score_before = get_score(test_path)
    score_after = get_score(refactor_manager.refactored_file_path)
    
    print(f"DAN Score Before: {score_before}")
    print(f"DAN Score After: {score_after}")
    
    collector.set_dan_scores(score_before, score_after)
    
except Exception as e:
    print(f"Failed to compute DAN scores: {e}")
    collector.set_dan_scores(None, None)

# Save reports
collector.save()
collector.save_json()