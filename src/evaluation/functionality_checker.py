import re
from typing import Dict
from src.logger import logger
from src.utils import read_text

REQ_FUNCS = ["open", "read", "write", "release"]
FILE_OPS_STRUCT_RX = r"struct\s+file_operations\s+[a-zA-Z_]\w*\s*=\s*\{"


def check_driver_apis(file_path: str) -> Dict:
    """
    Returns normalized functionality metrics + findings.
    """
    logger.info(f" Functionality check: {file_path}")
    data = {
        "metrics": {
            "basic_operations": 0.0,
            "error_handling": 0.5,
            "edge_cases": 0.5,
            "kernel_integration": 0.0
        },
        "findings": {
            "missing_functions": [],
            "has_file_operations_struct": False
        }
    }
    try:
        code = read_text(file_path)

        missing = []
        for fn in REQ_FUNCS:
            if not re.search(rf"\b{fn}\s*\(", code):
                missing.append(fn)
        data["findings"]["missing_functions"] = missing

        base = 1.0 - (len(missing) / max(1, len(REQ_FUNCS)))
        data["metrics"]["basic_operations"] = round(max(0.0, base), 2)

        has_file_ops = bool(re.search(FILE_OPS_STRUCT_RX, code))
        data["findings"]["has_file_operations_struct"] = has_file_ops
        ki = base
        if not has_file_ops:
            ki *= 0.7
        data["metrics"]["kernel_integration"] = round(max(0.0, min(1.0, ki)), 2)

        eh = 0.5
        if "copy_to_user" in code or "copy_from_user" in code:
            eh += 0.1
        if "-EFAULT" in code or "-EINVAL" in code:
            eh += 0.1
        data["metrics"]["error_handling"] = round(min(1.0, eh), 2)

        ec = 0.5
        if "min(" in code or "memmove(" in code:
            ec += 0.1
        data["metrics"]["edge_cases"] = round(min(1.0, ec), 2)

        return data
    except Exception as e:
        logger.error(f"Functionality check failed: {e}")
        return data
