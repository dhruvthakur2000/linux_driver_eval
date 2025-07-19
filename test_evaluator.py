from src.evaluator import evaluate_code

code_path = "generated_code/char_driver.c"
model_used = "mistral"
prompt_used = "char_driver.txt"

print(" Running Static Evaluation...")
report = evaluate_code(code_path, model_used, prompt_used)

print("\n Summary:")
for k, v in report.items():
    print(f" {k}: {v}")
