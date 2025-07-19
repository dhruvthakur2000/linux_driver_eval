import os
import re
from datetime import datetime
from src.logger import logger


def extract_code_blocks(text: str)->str:
    matches = re.findall(r"```(?:[a-zA-Z]+\n)?(.*?)```", response, re.DOTALL)
    code="\n\n".join(matches) if matches else text.strip()
    logger.info("code extracted from response")
    return code


def save_generated_code(model_name: str, code: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{model_name}_{timestamp}.c"
    path = os.path.join("generated_code", filename)

    with open(path, "w") as f:
        f.write(code)
    logger.info(f" Code saved to {path}")