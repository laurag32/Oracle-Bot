import pandas as pd
from profit_logger import LOG_FILE

def get_daily_summary():
    df = pd.read_csv(LOG_FILE)
    if df.empty:
        return "No transactions logged yet."
    total_profit = df['profit_usd'].sum()
    total_gas = df['gas_spent_usd'].sum()
    net = total_profit - total_gas
    return f"Total Profit: ${round(total_profit,2)} | Gas Spent: ${round(total_gas,2)} | Net: ${round(net,2)}"
