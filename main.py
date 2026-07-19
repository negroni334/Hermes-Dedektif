import os
import requests

class HermesAuditor:
    def __init__(self):
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

    def fetch_contract_source(self, address):
        params = {"module": "contract", "action": "getsourcecode", "address": address}
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            data = response.json()
            if data.get("status") == "1" and data["result"][0].get("SourceCode"):
                return data["result"][0]["SourceCode"], "Verified"
            return "WALLET_OR_UNKNOWN", "Wallet"
        except:
            return "ERROR", "Error"

    def fetch_wallet_balance(self, address):
        params = {"module": "account", "action": "balance", "address": address, "tag": "latest"}
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            data = response.json()
            if data.get("status") == "1":
                return float(data["result"]) / 1e18
            return 0.0
        except: return 0.0

    def perform_audit(self, code):
        risky_patterns = ["setBlacklist", "blacklist", "setTax", "setFees", "renounceOwnership", "mint"]
        return [p for p in risky_patterns if p in code]