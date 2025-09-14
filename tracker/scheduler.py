import schedule
import time
from .profit_tracker import check_today_profit
from .tracker_alerts import check_idle_or_low_profit

def start_scheduler():
    schedule.every(6).hours.do(check_today_profit)
    schedule.every(1).hours.do(check_idle_or_low_profit)
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    start_scheduler()
