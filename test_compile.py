# test_static_eval.py

from src.compiler import evaluate_c_code

# Paths
code_path = "generated_code/char_driver.c"
report_path = "reports/lint_logs"

print(" Running Static Analysis for LLM-generated Linux Driver Code...")
issues = evaluate_c_code(code_path, report_path)

print("\n Issue Summary:")
for category, entries in issues.items():
    print(f"  {category}: {len(entries)} issue(s)")
    for item in entries:
        print(f"    - {item}")
