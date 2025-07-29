import re
from typing import Dict
from src.logger import logger
from src.utils import read_text

UNSAFE_FUNCS = [r"\bstrcpy\s*\(", r"\bsprintf\s*\(", r"\bgets\s*\("]
USER_COPY_FUNCS = [r"\bcopy_to_user\s*\(", r"\bcopy_from_user\s*\("]
LOCK_FUNCS = [r"\bDEFINE_MUTEX\s*\(", r"\bmutex_lock\s*\(", r"\bmutex_unlock\s*\("]


def scan_security_issues(file_path: str) -> Dict:
    logger.info(f" Security scan: {file_path}")
    res = {
        "metrics": {
            "buffer_safety": 1.0,
            "race_conditions": 0.6,
            "input_validation": 0.6,
            "resource_management": 0.7
        },
        "findings": {
            "unsafe_calls": [],
            "user_copy_calls": 0,
            "uses_mutex": False
        }
    }
    try:
        code = read_text(file_path)

        unsafe = [p for p in UNSAFE_FUNCS if re.search(p, code)]
        res["findings"]["unsafe_calls"] = unsafe
        if unsafe:
            res["metrics"]["buffer_safety"] -= 0.3

        user_copies = sum(1 for p in USER_COPY_FUNCS if re.search(p, code))
        res["findings"]["user_copy_calls"] = user_copies
        if user_copies > 0 and ("min(" in code or "BUFFER_SIZE" in code or "count" in code):
            res["metrics"]["input_validation"] += 0.2
        res["metrics"]["input_validation"] = min(1.0, res["metrics"]["input_validation"])

        uses_mutex = any(re.search(p, code) for p in LOCK_FUNCS)
        res["findings"]["uses_mutex"] = uses_mutex
        if uses_mutex:
            res["metrics"]["race_conditions"] += 0.2
        res["metrics"]["race_conditions"] = min(1.0, res["metrics"]["race_conditions"])

        if "kmalloc" in code or "kzalloc" in code:
            if "kfree" in code:
                res["metrics"]["resource_management"] += 0.1
            else:
                res["metrics"]["resource_management"] -= 0.2
        res["metrics"]["resource_management"] = max(0.0, min(1.0, res["metrics"]["resource_management"]))

        return res
    except Exception as e:
        logger.error(f"Security scan failed: {e}")
        return res
