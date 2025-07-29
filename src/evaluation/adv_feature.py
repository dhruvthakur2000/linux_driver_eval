from typing import Dict
from src.logger import logger
from src.utils import read_text

def check_advanced_features(file_path: str) -> Dict:
    """
    Checks for device tree, power management, debugging hooks.
    Returns presence metrics in 0..1.
    """
    logger.info(f" Advanced features check: {file_path}")
    res = {
        "metrics": {
            "device_tree": 0.0,
            "power_management": 0.0,
            "debug_support": 0.0
        },
        "findings": {}
    }
    try:
        code = read_text(file_path)
        if "of_match_table" in code:
            res["metrics"]["device_tree"] = 1.0
        if "suspend" in code and "resume" in code:
            res["metrics"]["power_management"] = 1.0
        if ("dev_dbg" in code) or ("debugfs" in code) or ("proc_create" in code):
            res["metrics"]["debug_support"] = 1.0
        return res
    except Exception as e:
        logger.error(f"Advanced feature check failed: {e}")
        return res
