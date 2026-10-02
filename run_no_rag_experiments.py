#!/usr/bin/env python3
"""
ClariTest No-RAG Experiment Runner
Runs the full evaluation benchmark without RAG (saving results under output/no_rag/).
"""

import os
import sys
import subprocess
import argparse
import time
from datetime import datetime

# All 18 modules evaluated in the thesis (Table 5.1)
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


def parse_args():
    parser = argparse.ArgumentParser(description="Run ClariTest without RAG for ablation evaluation.")
    parser.add_argument("-m", "--models", nargs="+", default=["sonnet", "mini", "deepseek-coder"],
                        help="Models to evaluate: sonnet, mini, deepseek-coder, deepseek-v3")
    parser.add_argument("--prompts", nargs="+", default=["base", "combined"],
                        help="Prompt types to evaluate: base, combined")
    parser.add_argument("-t", "--temperatures", nargs="+", type=float, default=[1.0],
                        help="Temperatures to run: e.g. 1.0, 0.2")
    parser.add_argument("-r", "--runs", nargs="+", type=int, default=[1, 2, 3],
                        help="Run IDs: e.g. 1 2 3")
    parser.add_argument("-v", "--version", default="functions",
                        help="Refactoring version: functions, mix, summarize")
    parser.add_argument("--modules", nargs="+", default=None,
                        help="Filter specific module names (e.g. codetiming_timer pymonet_maybe)")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                        help="Skip tasks that have already generated test_run_report.json (default: True)")
    parser.add_argument("--no-skip-existing", action="store_false", dest="skip_existing",
                        help="Force re-running tasks even if test_run_report.json exists")
    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="Print commands without executing them")
    return parser.parse_args()


def get_expected_report(model: str, module_relpath: str, prompt_type: str, temp: float, run_num: int) -> str:
    single_path_abs = os.path.abspath(module_relpath)
    if "httpie.plugins.base" in single_path_abs:
        module_name = "plugins_base.py"
    elif "py_backwards.transformers.base" in single_path_abs:
        module_name = "transformers_base.py"
    else:
        module_name = os.path.basename(module_relpath)

    try:
        is_temp1 = float(temp) == 1.0
    except (ValueError, TypeError):
        is_temp1 = False

    base_dir = "./output/no_rag/temp1" if is_temp1 else "./output/no_rag"
    return os.path.join(base_dir, model, module_name, prompt_type, f"run{run_num}", "test_run_report.json")


def main():
    args = parse_args()
    
    # Filter modules if specified
    targets = MODULE_BENCHMARK
    if args.modules:
        targets = [m for m in MODULE_BENCHMARK if any(filter_name in m["name"] or filter_name in m["module"] for filter_name in args.modules)]
        if not targets:
            print(f"Error: No modules matched filter '{args.modules}'. Available module names:")
            for m in MODULE_BENCHMARK:
                print(f" - {m['name']}")
            sys.exit(1)

    total_tasks = len(args.models) * len(args.prompts) * len(args.temperatures) * len(args.runs) * len(targets)
    print("=" * 70)
    print(" ClariTest: No-RAG Experiment Runner")
    print("=" * 70)
    print(f"Models:        {args.models}")
    print(f"Prompts:       {args.prompts}")
    print(f"Temperatures:  {args.temperatures}")
    print(f"Runs:          {args.runs}")
    print(f"Modules:       {len(targets)} modules")
    print(f"Total Tasks:   {total_tasks}")
    print(f"Skip Existing: {args.skip_existing}")
    print("=" * 70)

    task_idx = 0
    start_time = time.time()
    failed_tasks = []
    skipped_count = 0

    for model in args.models:
        for prompt_type in args.prompts:
            for temp in args.temperatures:
                for run_num in args.runs:
                    for target in targets:
                        task_idx += 1
                        
                        expected_report = get_expected_report(model, target["module"], prompt_type, temp, run_num)
                        if args.skip_existing and os.path.exists(expected_report):
                            print(f"\n[{task_idx}/{total_tasks}] [SKIPPING] Already exists: Model={model} | Prompt={prompt_type} | Run={run_num} | Module={target['name']}")
                            skipped_count += 1
                            continue

                        cmd = [
                            sys.executable, "-m", "src.main",
                            "-p", target["module"],
                            "-tp", target["test"],
                            "-m", model,
                            "-t", str(temp),
                            "-v", args.version,
                            "--prompt-type", prompt_type,
                            "--run", str(run_num),
                            "--no-rag"
                        ]

                        print(f"\n[{task_idx}/{total_tasks}] Running: Model={model} | Prompt={prompt_type} | Temp={temp} | Run={run_num} | Module={target['name']}")
                        cmd_str = " ".join(cmd)
                        print(f"Command: {cmd_str}")

                        if args.dry_run:
                            continue

                        task_start = time.time()
                        try:
                            result = subprocess.run(cmd, check=True)
                            elapsed = time.time() - task_start
                            print(f"[SUCCESS] Completed in {elapsed:.1f}s")
                        except subprocess.CalledProcessError as e:
                            elapsed = time.time() - task_start
                            print(f"[ERROR] Task failed with exit code {e.returncode} after {elapsed:.1f}s")
                            failed_tasks.append({
                                "model": model,
                                "prompt": prompt_type,
                                "temp": temp,
                                "run": run_num,
                                "module": target["name"],
                                "command": cmd_str
                            })

    total_elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"All runs completed in {total_elapsed / 60:.2f} minutes (Skipped: {skipped_count}).")
    if failed_tasks:
        print(f"Warning: {len(failed_tasks)} tasks failed:")
        for f in failed_tasks:
            print(f" - {f['model']} | {f['prompt']} | {f['module']} | run{f['run']}")
    else:
        print("All tasks finished successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
