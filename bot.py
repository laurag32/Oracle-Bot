import time
import threading
from web3 import Web3
from dotenv import load_dotenv
import os
from rpc_manager import get_web3
from telegram_notifier import notify
import pandas as pd
from datetime import datetime
from tracker.scheduler import start_scheduler

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
DRY_RUN = os.getenv("DRY_RUN") == "true"
MIN_PROFIT_USD = float(os.getenv("MIN_PROFIT_USD", 1))

with open("watchers.json", "r") as f:
    import json
    watchers = json.load(f)

# Start tracker scheduler in separate thread
threading.Thread(target=start_scheduler, daemon=True).start()

def main_loop():
    while True:
        for watcher in watchers:
            chain = watcher["chain"]
            address = watcher["address"]
            func = watcher["function"]
            bounty = watcher.get("bounty", 0.5)

            web3 = get_web3(chain)

            try:
                contract = web3.eth.contract(address=Web3.to_checksum_address(address), abi=[{
                    "constant": False,
                    "inputs": [],
                    "name": func,
                    "outputs": [],
                    "payable": False,
                    "stateMutability": "nonpayable",
                    "type": "function"
                }])

                gas_estimate = contract.functions[func]().estimateGas({'from': PUBLIC_ADDRESS})
                gas_price = web3.eth.gas_price

                tx_cost_usd = (gas_estimate * gas_price / 1e18) * get_eth_price(chain)
                if tx_cost_usd > bounty:
                    continue

                if not DRY_RUN:
                    tx = contract.functions[func]().buildTransaction({
                        'from': PUBLIC_ADDRESS,
                        'nonce': web3.eth.get_transaction_count(PUBLIC_ADDRESS),
                        'gas': gas_estimate,
                        'gasPrice': gas_price
                    })
                    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
                    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                else:
                    tx_hash = "DRY_RUN"

                profit_usd = bounty
                log_transaction(chain, tx_hash, profit_usd, tx_cost_usd)

                notify(f"✅ Executed {func} on {watcher['name']} ({chain}) | Profit: ${profit_usd}")

            except Exception as e:
                print(f"Error with {watcher['name']}: {e}")
                continue

        time.sleep(60)

def log_transaction(chain, tx_hash, profit_usd, gas_spent_usd):
    import csv
    import os
    log_file = "logs/profit_log.csv"
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp","chain","tx_hash","profit_usd","gas_spent_usd"])
        writer.writerow([datetime.utcnow(), chain, tx_hash, profit_usd, gas_spent_usd])

def get_eth_price(chain):
    # Placeholder: return 1 USD per ETH for simplicity, replace with actual price feed
    return 1

if __name__ == "__main__":
    main_loop()
