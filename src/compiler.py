# src/compiler.py

import os
from src.logger import logger
from src.static_linter import lint_c_code

def evaluate_c_code(file_path: str, report_path: str) -> dict:
    """
    Runs custom static checks on the given C source file.
    Generates a report and returns the issues found.
    """
    try:
        logger.info(f" Starting static analysis on {file_path}")
        issues = lint_c_code(file_path, report_path)

        total_issues = sum(len(v) for v in issues.values())
        if total_issues == 0:
            logger.info(" No issues found in static analysis.")
        else:
            logger.warning(f" {total_issues} issues found during static analysis.")

        return issues

    except Exception as e:
        logger.error(f" Evaluation failed: {e}")
        return {}
