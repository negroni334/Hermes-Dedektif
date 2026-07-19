import os
import requests
from web3 import Web3

class HermesAuditor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
        self.api_url = "https://api.basescan.org/api"
        self.counter_file = "scan_counter.txt"

    def get_stats(self):
        if not os.path.exists(self.counter_file): return 1240
        with open(self.counter_file, "r") as f:
            try: return int(f.read())
            except: return 1240

    def increment_counter(self):
        count = self.get_stats() + 1
        with open(self.counter_file, "w") as f: f.write(str(count))

    def fetch_eth_price(self):
        try:
            url = "https://api.dexscreener.com/latest/dex/tokens/0x4200000000000000000000000000000000000006" # WETH Base
            data = requests.get(url, timeout=5).json()
            return float(data['pairs'][0]['priceUsd'])
        except: return 2500.0 # Hata durumunda sabit fiyat

    def fetch_wallet_balance(self, address):
        try:
            checksum_address = Web3.to_checksum_address(address.strip())
            balance_wei = self.w3.eth.get_balance(checksum_address)
            eth_amount = float(self.w3.from_wei(balance_wei, 'ether'))
            usd_value = eth_amount * self.fetch_eth_price()
            return eth_amount, usd_value
        except: return 0.0, 0.0

    def fetch_contract_source(self, address):
        params = {"module": "contract", "action": "getsourcecode", "address": address.strip().lower()}
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            data = response.json()
            if data.get("status") == "1" and data["result"][0].get("SourceCode"):
                return data["result"][0]["SourceCode"], "Verified"
            return "WALLET_OR_UNKNOWN", "Wallet"
        except: return "ERROR", "Error"

    def perform_audit(self, code):
        risky_patterns = ["setBlacklist", "blacklist", "setTax", "setFees", "renounceOwnership", "mint"]
        return [p for p in risky_patterns if p in code]