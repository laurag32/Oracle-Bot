import pandas as pd
from datetime import datetime, timedelta
from profit_logger import LOG_FILE
from telegram_notifier import notify

IDLE_THRESHOLD_HOURS = 1
MIN_NET_PROFIT_USD = 1

def check_idle_or_low_profit():
    try:
        df = pd.read_csv(LOG_FILE)
        if df.empty:
            notify("⚠️ Bot Idle: No transactions yet.")
            return
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        last_tx = df['timestamp'].max()
        if datetime.utcnow() - last_tx > timedelta(hours=IDLE_THRESHOLD_HOURS):
            notify(f"⚠️ Bot Idle: No activity in last {IDLE_THRESHOLD_HOURS}h")
        net_profit = df['profit_usd'].sum() - df['gas_spent_usd'].sum()
        if net_profit < MIN_NET_PROFIT_USD:
            notify(f"⚠️ Low Profit: Net profit today ${round(net_profit,2)}")
    except Exception as e:
        notify(f"Tracker Alerts Error: {e}")
