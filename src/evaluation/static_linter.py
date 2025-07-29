import re
from typing import Dict
from src.logger import logger
from src.utils import read_text


REQUIRED_FUNCTIONS = ['open', 'read', 'write', 'release']
REQUIRED_INCLUDES = ['<linux/fs.h>', '<linux/init.h>', '<linux/module.h>']
SUSPICIOUS_MACROS = ['EIO', 'EFAULT', 'copy_to_user']
REQUIRED_TYPES = ['ssize_t', 'loff_t', 'size_t']


def lint_c_code(file_path: str) -> Dict:
    logger.info(f" Static lint: {file_path}")
    issues = {
        "missing_functions": [],
        "missing_types": [],
        "suspicious_macros": [],
        "missing_includes": [],
        "issues_count": 0
    }
    try:
        code = read_text(file_path)

        for fn in REQUIRED_FUNCTIONS:
            if not re.search(rf"\b{fn}\s*\(", code):
                issues["missing_functions"].append(fn)

        for typ in REQUIRED_TYPES:
            if typ not in code:
                issues["missing_types"].append(typ)

        for macro in SUSPICIOUS_MACROS:
            if macro in code and f"#define {macro}" not in code:
                issues["suspicious_macros"].append(macro)

        for header in REQUIRED_INCLUDES:
            if header not in code:
                issues["missing_includes"].append(header)

        issues["issues_count"] = (
            len(issues["missing_functions"]) +
            len(issues["missing_types"]) +
            len(issues["suspicious_macros"]) +
            len(issues["missing_includes"])
        )
        logger.info(f"Static lint complete: {issues['issues_count']} issue(s)")
        return issues
    except Exception as e:
        logger.error(f"Static linting failed: {e}")
        return issues
