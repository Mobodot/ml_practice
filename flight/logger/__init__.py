import os
import logging
from datetime import datetime


CURRENT_TIME_STAMP = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
LOG_FILE = f"{CURRENT_TIME_STAMP}.log"
LOG_DIR = "flight_logs"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] - %(levelname)s: [%(message)s]",
    level=logging.INFO
)
