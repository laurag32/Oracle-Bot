import time
from datetime import datetime

def timestamp():
    """
    Returns the current UTC timestamp as a string.
    Example: "2025-09-14 19:45:00"
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def sleep_with_countdown(seconds):
    """
    Sleep with a console countdown.
    Example: sleep_with_countdown(10)
    """
    for i in range(seconds, 0, -1):
        print(f"Sleeping {i}s...", end="\r")
        time.sleep(1)
    print(" " * 20, end="\r")
