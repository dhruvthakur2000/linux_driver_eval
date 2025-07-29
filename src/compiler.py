import os
import subprocess
from datetime import datetime
from pathlib import Path
from src.logger import logger

def _to_wsl_path(win_path: str) -> str:
    p = Path(win_path).resolve()
    drive = p.drive.replace(":", "").lower()
    parts = "/".join(p.parts[1:])  # drop drive letter
    return f"/mnt/{drive}/{parts}".replace("\\", "/")

def compile_code(file_path: str) -> dict:
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(file_path))[0]
    log_file = os.path.join(logs_dir, f"{base}_compile_{ts}.log")

    # Paths for both Windows and WSL
    include_dir = os.path.abspath("mock_linux_headers")

    # If you installed gcc in WSL, call via `wsl` and convert paths
    use_wsl = True
    if use_wsl:
        wsl_file = _to_wsl_path(file_path)
        wsl_inc  = _to_wsl_path(include_dir)
        cmd = ["wsl", "gcc", "-Wall", "-Wextra", "-fsyntax-only", "-I", wsl_inc, wsl_file]
        pretty_cmd = " ".join(cmd)
    else:
        cmd = ["gcc", "-Wall", "-Wextra", "-fsyntax-only", "-I", include_dir, file_path]
        pretty_cmd = " ".join(cmd)

    logger.info(f"Compiling {file_path} using gcc...")
    logger.debug(f"Command: {pretty_cmd}")

    result = {"success": False, "warnings_count": 0, "errors_count": 0, "log_file": log_file}
    with open(log_file, "w", encoding="utf-8", errors="ignore") as f:
        try:
            proc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, text=True)
        except FileNotFoundError as e:
            logger.error(f"gcc not found: {e}")
            f.write(f"error: gcc not found: {e}\n")
            result["errors_count"] = 1
            return result

    # Parse the log for warnings/errors
    try:
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            log = f.read()
        result["warnings_count"] = log.count("warning:")
        result["errors_count"]   = log.count("error:")
    except Exception:
        pass

    result["success"] = (proc.returncode == 0)

    if result["success"]:
        logger.info(f"✅ Compilation successful with {result['warnings_count']} warnings.")
    else:
        logger.warning(f"⚠️ Compilation failed with {result['errors_count']} errors and {result['warnings_count']} warnings.")

    return result
