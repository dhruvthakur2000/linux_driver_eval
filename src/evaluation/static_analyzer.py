# src/static_analyzer.py
import re
from typing import Dict, List
from src.logger import logger

# ---- Heuristic rule sets ----
REQUIRED_INCLUDES = [
    r"<linux/module.h>", r"<linux/fs.h>",
    r"<linux/uaccess.h>", r"<linux/cdev.h>"
]

REQUIRED_FUNCS = ["open", "read", "write", "release"]
REQUIRED_KERNEL_MACROS = ["THIS_MODULE", "module_init", "module_exit", "MODULE_LICENSE"]

FILE_OPS_STRUCT_RX = r"struct\s+file_operations\s+[a-zA-Z_]\w*\s*=\s*\{"

# Security patterns
UNSAFE_FUNCS = [r"\bstrcpy\s*\(", r"\bsprintf\s*\(", r"\bgets\s*\("]
DISCOURAGED_FUNCS = [r"\bstrcat\s*\(", r"\bmemcpy\s*\("]
USER_COPY_FUNCS = [r"\bcopy_to_user\s*\(", r"\bcopy_from_user\s*\("]

# Concurrency / locking
MUTEX_USE = [r"\bDEFINE_MUTEX\s*\(", r"\bmutex_lock\s*\(", r"\bmutex_unlock\s*\("]
SPINLOCK_USE = [r"\bspin_lock\s*\(", r"\bspin_unlock\s*\("]

# Style / quality
MAX_LINE_CHARS = 140
MIN_COMMENT_DENSITY = 0.05  # 5% of lines as comments considered ok for a simple driver


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _count_matches(code: str, patterns: List[str]) -> int:
    return sum(1 for p in patterns if re.search(p, code))


def _missing_items(code: str, items: List[str]) -> List[str]:
    missing = []
    for inc in items:
        if inc.startswith("<") and inc not in code:
            missing.append(inc)
        elif inc in REQUIRED_KERNEL_MACROS and inc not in code:
            missing.append(inc)
    return missing


def _has_file_ops_struct(code: str) -> bool:
    return bool(re.search(FILE_OPS_STRUCT_RX, code))


def _has_required_functions(code: str) -> List[str]:
    missing = []
    for fn in REQUIRED_FUNCS:
        if not re.search(rf"\b{fn}\s*\(", code):
            missing.append(fn)
    return missing


def _comment_density(code: str) -> float:
    lines = code.splitlines()
    if not lines:
        return 0.0
    comment_lines = 0
    block = False
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


def _long_lines_warnings(code: str) -> int:
    return sum(1 for ln in code.splitlines() if len(ln) > MAX_LINE_CHARS)


def _has_bounds_checks_near_user_copies(code: str) -> bool:
    """
    Very light heuristic:
    If copy_to_user/copy_from_user appears and we see a min()/bounds-like expression
    or BUFFER_SIZE/count checks in the same function or nearby lines, reward it.
    """
    # crude window around copy_* lines
    lines = code.splitlines()
    idxs = [i for i, ln in enumerate(lines) if re.search(r"copy_(to|from)_user\s*\(", ln)]
    if not idxs:
        return False
    for i in idxs:
        window = "\n".join(lines[max(0, i-6): i+6])
        if re.search(r"\bmin\s*\(", window) or re.search(r"BUFFER_SIZE|count|f_pos|pos|remaining", window):
            return True
    return False


def analyze_code(file_path: str) -> Dict:
    """
    Returns a dict of:
      - findings (missing includes/functions/macros, unsafe calls, etc.)
      - normalized metrics buckets in keys: functionality, security, code_quality, performance, advanced
    """
    logger.info(f"🔎 Static analysis of {file_path}")
    code = _read(file_path)

    missing_includes = _missing_items(code, REQUIRED_INCLUDES)
    missing_macros = _missing_items(code, REQUIRED_KERNEL_MACROS)
    missing_funcs = _has_required_functions(code)
    has_file_ops = _has_file_ops_struct(code)

    unsafe_found = [p for p in UNSAFE_FUNCS if re.search(p, code)]
    discouraged_found = [p for p in DISCOURAGED_FUNCS if re.search(p, code)]
    user_copy_calls = _count_matches(code, USER_COPY_FUNCS)
    has_mutex = _count_matches(code, MUTEX_USE) > 0
    has_spin = _count_matches(code, SPINLOCK_USE) > 0

    comment_ratio = _comment_density(code)
    long_line_warns = _long_lines_warnings(code)

    # ---- Normalize to 0..1 buckets ----
    # Functionality
    base_ops = 1.0 - (len(missing_funcs) / max(1, len(REQUIRED_FUNCS)))
    if not has_file_ops:
        base_ops *= 0.7  # penalize missing struct file_operations

    # Error handling heuristic: if copy_to/from_user exists and bounds heuristics are present => better
    error_handling = 0.5
    if user_copy_calls > 0:
        error_handling = 0.7 if _has_bounds_checks_near_user_copies(code) else 0.4
    if "return -EFAULT" in code or "return -EINVAL" in code or "goto" in code:
        error_handling = min(1.0, error_handling + 0.1)

    edge_cases = 0.5
    if "min(" in code or "memmove(" in code or "KMALLOC" in code or "kzalloc" in code:
        edge_cases = 0.6
    if "mutex_lock" in code and "mutex_unlock" in code:
        edge_cases += 0.1
    edge_cases = min(edge_cases, 1.0)

    functionality = {
        "basic_operations": round(max(0.0, min(1.0, base_ops)), 2),
        "error_handling": round(max(0.0, min(1.0, error_handling)), 2),
        "edge_cases": round(max(0.0, min(1.0, edge_cases)), 2),
    }

    # Security
    buffer_safety = 1.0
    if unsafe_found:
        buffer_safety -= 0.3
    if not _has_bounds_checks_near_user_copies(code):
        buffer_safety -= 0.2
    buffer_safety = max(0.0, buffer_safety)

    race_conditions = 0.6
    if has_mutex or has_spin:
        race_conditions += 0.2
    if "interrupt" in code or "irq" in code:
        # without locks in IRQ paths we'd penalize, but keep heuristic light
        race_conditions -= 0.1
    race_conditions = max(0.0, min(1.0, race_conditions))

    input_validation = 0.6
    if "copy_from_user" in code and ("count" in code or "BUFFER_SIZE" in code):
        input_validation += 0.2
    if "if (" in code and ("< 0" in code or "> BUFFER_SIZE" in code):
        input_validation += 0.1
    input_validation = max(0.0, min(1.0, input_validation))

    security = {
        "buffer_safety": round(buffer_safety, 2),
        "race_conditions": round(race_conditions, 2),
        "input_validation": round(input_validation, 2),
    }

    # Code Quality
    style = 1.0
    if missing_includes:
        style -= 0.15
    if long_line_warns > 0:
        style -= 0.1
    style = max(0.0, style)

    documentation = 1.0 if comment_ratio >= MIN_COMMENT_DENSITY else 0.6
    maintainability = 0.8
    if "goto" in code:
        maintainability -= 0.1
    if len(code) > 6000:
        maintainability -= 0.1
    maintainability = max(0.0, maintainability)

    code_quality = {
        "style_compliance": round(style, 2),
        "documentation": round(documentation, 2),
        "maintainability": round(maintainability, 2),
    }

    # Performance (very light heuristics for a char driver)
    efficiency = 0.8
    if "memset" in code or "memcpy" in code:
        efficiency -= 0.05
    scalability = 0.7  # neutral default for simple drivers
    memory_usage = 0.9 if "BUFFER_SIZE" in code and "1024" in code else 0.8

    performance = {
        "efficiency": round(max(0.0, efficiency), 2),
        "scalability": round(max(0.0, scalability), 2),
        "memory_usage": round(max(0.0, memory_usage), 2),
    }

    # Advanced features (presence flags → small bonus if present)
    device_tree = 1.0 if "of_match_table" in code else 0.0
    power_mgmt = 1.0 if "suspend" in code and "resume" in code else 0.0
    debug_support = 1.0 if ("dev_dbg" in code or "debugfs" in code or "proc_create" in code) else 0.0

    advanced = {
        "device_tree": device_tree,
        "power_management": power_mgmt,
        "debug_support": debug_support,
    }

    findings = {
        "missing_includes": missing_includes,
        "missing_functions": missing_funcs,
        "missing_macros": [m for m in REQUIRED_KERNEL_MACROS if m in missing_macros],
        "unsafe_calls": [p for p in UNSAFE_FUNCS if re.search(p, code)],
        "discouraged_calls": [p for p in DISCOURAGED_FUNCS if re.search(p, code)],
        "has_file_operations_struct": has_file_ops,
        "uses_mutex": has_mutex,
        "uses_spinlock": has_spin,
        "comment_density": round(comment_ratio, 3),
        "long_line_warnings": long_line_warns,
        "user_copy_calls": user_copy_calls,
    }

    metrics = {
        "functionality": functionality,
        "security": security,
        "code_quality": code_quality,
        "performance": performance,
        "advanced": advanced,
        "findings": findings,
    }

    logger.info(" Static analysis completed.")
    return metrics
