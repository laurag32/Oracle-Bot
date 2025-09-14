import pandas as pd
from datetime import datetime
from telegram_notifier import notify
from profit_logger import LOG_FILE

def check_today_profit():
    try:
        df = pd.read_csv(LOG_FILE)
        today = datetime.utcnow().date()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        today_df = df[df['timestamp'].dt.date == today]
        if today_df.empty:
            notify("📊 Profit Tracker: No transactions today.")
            return
        total_profit = today_df['profit_usd'].sum()
        total_gas = today_df['gas_spent_usd'].sum()
        net = total_profit - total_gas
        message = f"📊 Today: {len(today_df)} tx | Profit: ${total_profit} | Gas: ${total_gas} | Net: ${net}"
        notify(message)
    except Exception as e:
        notify(f"Profit Tracker Error: {e}")
