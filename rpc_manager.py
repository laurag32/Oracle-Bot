from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()

RPCS = {
    "arbitrum": [os.getenv("RPC_ARB_1"), os.getenv("RPC_ARB_2")],
    "optimism": [os.getenv("RPC_OPT_1"), os.getenv("RPC_OPT_2")]
}

def get_web3(chain):
    for rpc in RPCS.get(chain, []):
        try:
            web3 = Web3(Web3.HTTPProvider(rpc))
            if web3.is_connected():
                return web3
        except:
            continue
    raise Exception(f"No RPCs available for {chain}")
