import os
import json
import re
from typing import Dict, Any
from datetime import datetime
from src.logger import logger


def extract_code_blocks(text: str)->str:
    matches = re.findall(r"```(?:[a-zA-Z]+\n)?(.*?)```", text, re.DOTALL)
    code="\n\n".join(matches) if matches else text.strip()
    logger.info("code extracted from response")
    return code


def save_generated_code(model_name: str, code: str,output_path: str = "generated_code"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(output_path, exist_ok=True)
    filename = f"{model_name}_{timestamp}.c"
    file_path = os.path.join(output_path, filename)
    with open(file_path, "w") as f:
        f.write(code)
    logger.info(f" Code saved to {file_path}")



def ensure_dir(path: str) -> None:
    if path:
        os.makedirs(path, exist_ok=True)



def save_json_report(data: Dict[str, Any], path: str) -> None:
    try:
        ensure_dir(os.path.dirname(path))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f" JSON report saved: {path}")
    except Exception as e:
        logger.error(f"Failed to save JSON report to {path}: {e}")

        

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()