import os
import re
import json
from src.logger import logger

REQUIRED_FUNCTIONS = ['open', 'read', 'write', 'release']
REQUIRED_INCLUDES = ['<linux/fs.h>', '<linux/init.h>', '<linux/module.h>']
SUSPICIOUS_MACROS = ['EIO', 'EFAULT', 'copy_to_user']
OPTIONAL_COMPONENTS = ['file_operations', 'init', 'exit', 'register_chrdev']

def evaluate_code(file_path: str, model_name: str, prompt_used: str, output_path="reports/metrics"):
    try:
        with open(file_path, "r") as f:
            code = f.read()
    except Exception as e:
        logger.error(f" Failed to read code: {e}")
        return

    result = {
        "model": model_name,
        "prompt": prompt_used,
        "missing_functions": [],
        "missing_includes": [],
        "suspicious_macros": [],
        "present_optional_components": [],
        "function_score": 0
    }

    # Check for required functions
    for func in REQUIRED_FUNCTIONS:
        pattern = rf"{func}\s*\("
        if not re.search(pattern, code):
            result["missing_functions"].append(func)

    # Check for required includes
    for inc in REQUIRED_INCLUDES:
        if inc not in code:
            result["missing_includes"].append(inc)

    # Check for suspicious macros
    for macro in SUSPICIOUS_MACROS:
        if macro in code:
            result["suspicious_macros"].append(macro)

    # Check for optional structure
    for component in OPTIONAL_COMPONENTS:
        if component in code:
            result["present_optional_components"].append(component)

    # Score: 10 - 1 for each missing function, max 10
    result["function_score"] = 10 - len(result["missing_functions"])
    result["function_score"] = max(0, result["function_score"])  # No negative scores

    # Save report
    os.makedirs(output_path, exist_ok=True)
    report_file = os.path.join(output_path, f"{os.path.basename(file_path).replace('.c', '')}_{model_name}.json")
    with open(report_file, "w") as f:
        json.dump(result, f, indent=4)

    logger.info(f"Evaluation report saved to {report_file}")
    return result
