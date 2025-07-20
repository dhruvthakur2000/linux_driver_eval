import os
import csv
import glob
from src.evaluator import evaluate_code
from src.logger import logger

GENERATED_DIR = "generated_code"
SUMMARY_DIR = "reports/summary"
SUMMARY_FILE = os.path.join(SUMMARY_DIR, "summary.csv")

def extract_model_prompt(filename: str):
    """
    Expected filename format: <prompt_name>_<model_name>.c
    E.g., char_driver_mistral.c → ('mistral', 'char_driver.txt')
    """
    name = os.path.basename(filename).replace(".c", "")
    parts = name.split("_")
    if len(parts) < 2:
        return "unknown", "unknown"
    model = parts[-1]
    prompt = "_".join(parts[:-1]) + ".txt"
    return model, prompt

def main():
    os.makedirs(SUMMARY_DIR, exist_ok=True)
    csv_fields = [
        "model", "prompt", "function_score",
        "missing_functions", "missing_includes",
        "suspicious_macros", "present_optional_components"
    ]

    results = []
    code_files = glob.glob(os.path.join(GENERATED_DIR, "*.c"))
    logger.info(f"Found {len(code_files)} files to evaluate.")

    for code_file in code_files:
        model, prompt = extract_model_prompt(code_file)
        result = evaluate_code(code_file, model, prompt)
        if result:
            results.append(result)

    with open(SUMMARY_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for row in results:
            writer.writerow({
                "model": row["model"],
                "prompt": row["prompt"],
                "function_score": row["function_score"],
                "missing_functions": "|".join(row["missing_functions"]),
                "missing_includes": "|".join(row["missing_includes"]),
                "suspicious_macros": "|".join(row["suspicious_macros"]),
                "present_optional_components": "|".join(row["present_optional_components"])
            })

    logger.info(f" Final summary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
