# src/logger.py (or utils/logger.py)

import logging
import os

def get_logger(name: str) -> logging.Logger:


    # Step 1: Create a logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Step 2: Create a logger instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Step 3: Define console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_format)

    # Step 4: Define file handler
    file_path = os.path.join(log_dir, f"{name}.log")
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_format)

    # Step 5: Attach handlers if not already added
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
