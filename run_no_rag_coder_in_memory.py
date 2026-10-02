import os
import sys
import time
import argparse
from typing import List

try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3.dbapi2
except ImportError:
    pass

from dotenv import load_dotenv
load_dotenv()

from src.util import file_handler
from src.util import extractor
from src.util import prompts
from src.util import refactoring_manager
from src.util import pytest_runner
from src.util.data_analysis.data_collection import TestRunDataCollector
from src.util.dan.dan_integration import DANIntegrator

MODULE_BENCHMARK = [
    # codetiming
    {
        "name": "codetiming_timer",
        "module": "data/codetiming/codetiming_timer.py",
        "test": "data/codetiming/test_codetiming__timer.py"
    },
    # flutils
    {
        "name": "flutils_decorators",
        "module": "data/flutils.decorators/decorators.py",
        "test": "data/flutils.decorators/test_flutils_decorators.py"
    },
    {
        "name": "flutils_namedtupleutils",
        "module": "data/flutils.namedtupleutils/namedtupleutils.py",
        "test": "data/flutils.namedtupleutils/test_flutils_namedtupleutils.py"
    },
    {
        "name": "flutils_packages",
        "module": "data/flutils.packages/packages.py",
        "test": "data/flutils.packages/test_flutils_packages.py"
    },
    {
        "name": "flutils_cmd",
        "module": "data/flutils.setuputils.cmd/cmd.py",
        "test": "data/flutils.setuputils.cmd/test_flutils_setuputils_cmd.py"
    },
    # httpie
    {
        "name": "httpie_headers",
        "module": "data/httpie.output.formatters.headers/headers.py",
        "test": "data/httpie.output.formatters.headers/test_httpie_output_formatters_headers.py"
    },
    {
        "name": "httpie_plugins_base",
        "module": "data/httpie.plugins.base/base.py",
        "test": "data/httpie.plugins.base/test_httpie_plugins_base.py"
    },
    # py_backwards
    {
        "name": "py_backwards_transformers_base",
        "module": "data/py_backwards.transformers.base/base.py",
        "test": "data/py_backwards.transformers.base/test_py_backwards_transformers_base.py"
    },
    {
        "name": "py_backwards_dict_unpacking",
        "module": "data/py_backwards.transformers.dict_unpacking/dict_unpacking.py",
        "test": "data/py_backwards.transformers.dict_unpacking/test_py_backwards_transformers_dict_unpacking.py"
    },
    {
        "name": "py_backwards_return_from_generator",
        "module": "data/py_backwards.transformers.return_from_generator/return_from_generator.py",
        "test": "data/py_backwards.transformers.return_from_generator/test_py_backwards_transformers_return_from_generator.py"
    },
    {
        "name": "py_backwards_yield_from",
        "module": "data/py_backwards.transformers.yield_from/yield_from.py",
        "test": "data/py_backwards.transformers.yield_from/test_py_backwards_transformers_yield_from.py"
    },
    {
        "name": "py_backwards_helpers",
        "module": "data/py_backwards.utils.helpers/helpers.py",
        "test": "data/py_backwards.utils.helpers/test_py_backwards_utils_helpers.py"
    },
    # pymonet
    {
        "name": "pymonet_immutable_list",
        "module": "data/pymonet.immutable_list/immutable_list.py",
        "test": "data/pymonet.immutable_list/test_pymonet_immutable_list.py"
    },
    {
        "name": "pymonet_maybe",
        "module": "data/pymonet.maybe/maybe.py",
        "test": "data/pymonet.maybe/test_pymonet_maybe.py"
    },
    {
        "name": "pymonet_validation",
        "module": "data/pymonet.validation/validation.py",
        "test": "data/pymonet.validation/test_pymonet_validation.py"
    },
    # pypara
    {
        "name": "pypara_journaling",
        "module": "data/pypara.accounting.journaling/journaling.py",
        "test": "data/pypara.accounting.journaling/test_pypara_accounting_journaling.py"
    },
    # pytutils
    {
        "name": "pytutils_lazy_import",
        "module": "data/pytutils.lazy.lazy_import/lazy_import.py",
        "test": "data/pytutils.lazy.lazy_import/test_pytutils_lazy_lazy_import.py"
    },
    {
        "name": "pytutils_python",
        "module": "data/pytutils.python/python.py",
        "test": "data/pytutils.python/test_pytutils_python.py"
    },
]


def run_single_task(
    model: str,
    module_path_str: str,
    test_path_str: str,
    prompt_type: str,
    run_num: int,
    temperature: float = 1.0,
    version: str = "functions",
    job: int = 1,
    session: int = 1,
) -> bool:
    module_path = [module_path_str]
    test_path = test_path_str

    single_path = module_path[0]
    single_path_abs = os.path.abspath(single_path)
    if "httpie.plugins.base" in single_path_abs:
        module_name = "plugins_base.py"
    elif "py_backwards.transformers.base" in single_path_abs:
        module_name = "transformers_base.py"
    else:
        module_name = os.path.basename(single_path)

    output_dir, session_name = file_handler.setup_output_dir(
        model, job, session, temperature, version, module_name, prompt_type, run_num, no_rag=True
    )

    report_file = os.path.join(output_dir, "test_run_report.json")
    if os.path.exists(report_file):
        print(f"[SKIPPING] Report already exists: {report_file}")
        return True

    file_handler.pytest_runner_set_up(module_path, test_path, output_dir)
    print(f"\n--- Starting Task: {model} | {module_name} | {prompt_type} | run{run_num} ---")
    print(f"Output directory: {output_dir}")

    system_prompt = prompts.get_system_prompt_readability()
    refactor_mgr = refactoring_manager.RefactorManager(
        model_name=model,
        version=version,
        temperature=temperature,
        directory=output_dir,
        system_prompt=system_prompt,
        modules_paths=module_path,
        test_path=test_path,
        vectorstores=None,
        hf_token=os.getenv("HF_TOKEN"),
        prompt_type=prompt_type,
    )

    # 1. Imports
    import_info = refactor_mgr.get_and_save_new_imports()

    # 2. Refactor
    if "summarize" in version:
        refactor_mgr.run_summarize_functions()
    elif "function" in version:
        refactor_mgr.run_with_functions()
    elif "mix" in version:
        refactor_mgr.run_full_module()

    # 3. Pytest
    test_files = {
        "Original Test Results": test_path,
        "Refactored Test Results": refactor_mgr.refactored_file_path,
    }
    pytest_output_dir = os.path.join(output_dir, "pytest_results")
    os.makedirs(pytest_output_dir, exist_ok=True)

    failed_tests, test_summary, coverage_summary, test_ran_status, detailed_results = pytest_runner.run_pytest_and_log_results(
        test_files,
        module_path,
        pytest_output_dir,
        combined=False,
    )

    # 4. Collect results
    collector = TestRunDataCollector(output_dir, module_name=module_name)
    collector.set_llm_metadata(
        model_name=model,
        version=version,
        temperature=temperature,
        prompt_style=prompt_type,
        run_number=run_num,
    )

    before_results = {
        k: v for k, v in detailed_results.get("Original Test Results", {}).items()
        if k != "Collection Error"
    }
    refactored_raw = detailed_results.get("Refactored Test Results", {})
    if "Collection Error" in refactored_raw:
        after_results = {"collection_error": True}
    else:
        after_results = {k: v for k, v in refactored_raw.items()}

    test_summary_corrected = {
        **test_summary,
        "total_tests_before": len(before_results),
        "total_tests_after": len(after_results),
    }

    collector.set_test_summary(test_summary_corrected)
    collector.set_test_results("before_refactoring", before_results)
    collector.set_test_results("after_refactoring", after_results)
    collector.set_coverage_data(
        original_coverage=coverage_summary.get("Original Test Results", "N/A"),
        refactored_coverage=coverage_summary.get("Refactored Test Results", "N/A"),
    )

    # 5. DAN
    try:
        dan_integrator = DANIntegrator(model_name="microsoft/codebert-base-mlm")
        score_before = dan_integrator.compute_score(test_path, output_dir)
        score_after = dan_integrator.compute_score(refactor_mgr.refactored_file_path, output_dir)
        collector.set_dan_scores(score_before, score_after)
    except Exception as e:
        collector.set_dan_scores(None, None)

    collector.save()
    collector.save_json()
    print(f"[SUCCESS] Saved report to {report_file}")
    return True


def main():
    parser = argparse.ArgumentParser(description="In-memory No-RAG runner for DeepSeek Coder.")
    parser.add_argument("-m", "--model", default="deepseek-coder", help="Model name")
    parser.add_argument("--prompts", nargs="+", default=["base", "combined"], help="Prompt styles")
    parser.add_argument("-t", "--temperatures", nargs="+", type=float, default=[1.0], help="Temperatures")
    parser.add_argument("-r", "--runs", nargs="+", type=int, default=[1, 2, 3], help="Runs")
    parser.add_argument("-v", "--version", default="functions", help="Refactoring version")
    args = parser.parse_args()

    total_tasks = len(args.prompts) * len(args.temperatures) * len(args.runs) * len(MODULE_BENCHMARK)
    print("=" * 80)
    print(f" In-Memory No-RAG Evaluation for Model: {args.model}")
    print(f" Prompts: {args.prompts} | Temps: {args.temperatures} | Runs: {args.runs}")
    print(f" Total tasks: {total_tasks}")
    print("=" * 80)

    task_idx = 0
    start_time = time.time()
    success_count = 0
    fail_count = 0

    for prompt_type in args.prompts:
        for temp in args.temperatures:
            for run_num in args.runs:
                for target in MODULE_BENCHMARK:
                    task_idx += 1
                    print(f"\n>>> [{task_idx}/{total_tasks}] Processing {target['name']} ({prompt_type} | run{run_num})")
                    t_start = time.time()
                    try:
                        run_single_task(
                            model=args.model,
                            module_path_str=target["module"],
                            test_path_str=target["test"],
                            prompt_type=prompt_type,
                            run_num=run_num,
                            temperature=temp,
                            version=args.version,
                        )
                        elapsed = time.time() - t_start
                        print(f"    Finished in {elapsed:.1f}s")
                        success_count += 1
                    except Exception as e:
                        elapsed = time.time() - t_start
                        print(f"    [ERROR] Task failed after {elapsed:.1f}s: {e}")
                        import traceback
                        traceback.print_exc()
                        fail_count += 1

    total_time = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"Completed in {total_time/60:.2f} minutes (Success: {success_count}, Failed: {fail_count}).")
    print("=" * 80)


if __name__ == "__main__":
    main()
