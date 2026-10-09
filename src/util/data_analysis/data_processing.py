import os
import re
import pandas as pd

def parse_summary(summary_str):
    """Extract Total, Passed, Failed counts from summary text (very flexible)."""
    if pd.isna(summary_str):
        return {"total": None, "passed": None, "failed": None}

    # Normalize input
    s = str(summary_str).lower().replace(",", " ").replace(";", " ").replace("|", " ")

    # Use regex to capture numbers even with flexible labels
    total_match = re.search(r"total[^0-9]*([0-9]+)", s)
    pass_match = re.search(r"pass[^0-9]*([0-9]+)", s)
    fail_match = re.search(r"fail[^0-9]*([0-9]+)", s)

    total = int(total_match.group(1)) if total_match else None
    passed = int(pass_match.group(1)) if pass_match else None
    failed = int(fail_match.group(1)) if fail_match else None

    return {"total": total, "passed": passed, "failed": failed}


def summarize_csvs(input_folder: str, output_file: str):
    summary_data = []

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".csv"):
                file_path = os.path.join(root, filename)
                try:
                    df = pd.read_csv(file_path)

                    # Try to infer module name
                    module_name = df.get("Module name", [os.path.basename(root)])[0]

                    # Extract coverage values
                    orig_cov = df.get("original_coverage", [None])[0]
                    refac_cov = df.get("refactored_coverage", [None])[0]

                    # Compute coverage difference
                    coverage_diff = (
                        refac_cov - orig_cov
                        if pd.notna(orig_cov) and pd.notna(refac_cov)
                        else None
                    )

                    # Parse test summaries
                    orig_summary = parse_summary(df.get("summary_Original Test Results", [None])[0])
                    refac_summary = parse_summary(df.get("summary_Refactored Test Results", [None])[0])

                    # Compute test differences
                    tests_diff = (
                        refac_summary["total"] - orig_summary["total"]
                        if orig_summary["total"] is not None and refac_summary["total"] is not None
                        else None
                    )
                    passed_diff = (
                        refac_summary["passed"] - orig_summary["passed"]
                        if orig_summary["passed"] is not None and refac_summary["passed"] is not None
                        else None
                    )
                    failed_diff = (
                        refac_summary["failed"] - orig_summary["failed"]
                        if orig_summary["failed"] is not None and refac_summary["failed"] is not None
                        else None
                    )

                    summary_data.append({
                        "Module name": module_name,
                        "Coverage Difference": coverage_diff,
                        "Number of Tests Difference": tests_diff,
                        "Number of Passed Difference": passed_diff,
                        "Number of Failed Difference": failed_diff
                    })

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    if not summary_data:
        print("No valid CSV files found.")
        return

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_file, index=False)
    print(f"Summary saved to: {output_file}")
    print(f"Processed {len(summary_data)} modules.")


if __name__ == "__main__":
    input_folder = "output/no_rag"  # change this
    output_file = "summary.csv"
    summarize_csvs(input_folder, output_file)
