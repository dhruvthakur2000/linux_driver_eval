import os
import argparse
import json
from datetime import datetime

from src.logger import logger
from src.compiler import compile_code
from src.evaluation.static_linter import lint_c_code
from src.evaluation.functionality_checker import check_driver_apis
from src.evaluation.security_check import scan_security_issues
from src.evaluation.quality_check import check_code_quality
from src.evaluation.adv_feature import check_advanced_features
from src.metrics import score_all


def evaluate_file(file_path: str, output_dir: str) -> None:
    logger.info(f" Evaluating: {file_path}")

    evaluation_data = {
        "file": file_path,
        "timestamp": datetime.now().isoformat(),
    }

    try:
        # 1. Compilation
        compilation_result = compile_code(file_path)
        evaluation_data["compilation"] = compilation_result

        # 2. Static Lint
        lint_result = lint_c_code(file_path)
        evaluation_data["static_analysis"] = lint_result

        # 3. Functionality
        func_result = check_driver_apis(file_path)
        evaluation_data["functionality"] = func_result

        # 4. Security
        security_result = scan_security_issues(file_path)
        evaluation_data["security"] = security_result

        # 5. Code Quality
        quality_result = check_code_quality(file_path)
        evaluation_data["code_quality"] = quality_result

        # 6. Advanced Features
        advanced_result = check_advanced_features(file_path)
        evaluation_data["advanced_features"] = advanced_result

        # 7. Scoring (calculate total score)
        scores = score_all(evaluation_data)
        evaluation_data["overall_score"] = scores

        # 8. Save JSON report
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.splitext(os.path.basename(file_path))[0]
        report_path = os.path.join(output_dir, f"{filename}_evaluation.json")
        with open(report_path, "w") as f:
            json.dump(evaluation_data, f, indent=4)

        logger.info(f"Evaluation report saved to {report_path}")


    except Exception as e:
        logger.error(f"Evaluation failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate Linux driver C code")
    parser.add_argument("--file", "-f", required=True, help="Path to the C file")
    parser.add_argument("--output", "-o", default="reports", help="Reports output dir")
    args = parser.parse_args()

    evaluate_file(args.file, args.output)
    logger.info(f" Evaluation complete. Report saved to {args.output}")



if __name__ == "__main__":
    main()
