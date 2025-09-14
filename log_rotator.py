import os
from datetime import datetime
import shutil
from profit_logger import LOG_FILE

def rotate_logs():
    if not os.path.exists(LOG_FILE):
        return "No log file to rotate."
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    dest = f"logs/profit_log_{date_str}.csv"
    shutil.copy(LOG_FILE, dest)
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,chain,tx_hash,profit_usd,gas_spent_usd\n")
    return f"Log rotated: {dest}"
