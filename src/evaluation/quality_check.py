import re
from typing import Dict
from src.logger import logger
from src.utils import read_text

MAX_LINE_CHARS = 140
MIN_COMMENT_DENSITY = 0.05  # 5%


def _comment_density(code: str) -> float:
    lines = code.splitlines()
    if not lines:
        return 0.0
    comment_lines, block = 0, False
    for ln in lines:
        s = ln.strip()
        if s.startswith("//"):
            comment_lines += 1
        if "/*" in s:
            block = True
            comment_lines += 1
        elif block:
            comment_lines += 1
        if "*/" in s:
            block = False
    return comment_lines / max(1, len(lines))

def _long_line_count(code: str) -> int:
    return sum(1 for ln in code.splitlines() if len(ln) > MAX_LINE_CHARS)

def check_code_quality(file_path: str) -> Dict:
    logger.info(f" Code quality check: {file_path}")
    res = {
        "metrics": {
            "style_compliance": 1.0,
            "documentation": 1.0,
            "maintainability": 0.8
        },
        "findings": {
            "long_line_warnings": 0,
            "mixed_tabs_spaces": False
        }
    }
    try:
        code = read_text(file_path)
        long_lines = _long_line_count(code)
        res["findings"]["long_line_warnings"] = long_lines
        if long_lines > 0:
            res["metrics"]["style_compliance"] -= 0.1

        has_tabs = "\t" in code
        has_indented_spaces = bool(re.search(r"^\s{2,}\S", code, re.M))
        res["findings"]["mixed_tabs_spaces"] = has_tabs and has_indented_spaces
        if res["findings"]["mixed_tabs_spaces"]:
            res["metrics"]["style_compliance"] -= 0.05

        density = _comment_density(code)
        res["metrics"]["documentation"] = 1.0 if density >= MIN_COMMENT_DENSITY else 0.6

        if "goto" in code:
            res["metrics"]["maintainability"] -= 0.1

        res["metrics"]["style_compliance"] = max(0.0, res["metrics"]["style_compliance"])
        res["metrics"]["maintainability"] = max(0.0, res["metrics"]["maintainability"])

        return res
    except Exception as e:
        logger.error(f"Quality check failed: {e}")
        return res
