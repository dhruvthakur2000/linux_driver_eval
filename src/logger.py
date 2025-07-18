import logging
import os

LOG_DIR = "logs"
LOG_FILE = "pipeline.log"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Remove all existing handlers first (especially for Jupyter / repeated imports)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# ✅ Set up logging ONLY to file (UTF-8 safe)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8")  # File logging only
    ]
)

logger = logging.getLogger(__name__)
