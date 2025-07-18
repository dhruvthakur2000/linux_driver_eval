import subprocess
import os
from src.logger import logger

def compile_code(source_path: str, model_name: str) -> tuple:
    """
    Compiles the C file and saves output to logs.
    Returns (True/False, output_text)
    """
    file_name = os.path.basename(source_path).replace(".c", "")
    log_dir = os.path.join("reports", "compilation_logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{file_name}.log")

    output_path = source_path.replace(".c", ".o")
    compile_cmd = ["gcc", "-Wall", "-Werror", "-c", source_path, "-o", output_path]

    try:
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        output = result.stdout + result.stderr

        with open(log_file, "w") as f:
            f.write(output)

        if result.returncode == 0:
            logger.info(f" Compilation successful for {source_path}")
            return True, output
        else:
            logger.warning(f" Compilation failed for {source_path}")
            return False, output

    except Exception as e:
        logger.error(f" Compiler crashed: {e}")
        return False, str(e)
