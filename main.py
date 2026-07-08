import os
import requests
from dotenv import load_dotenv

class HermesAuditor:
    def __init__(self):
        self.api_key = os.getenv("BASESCAN_API_KEY") or "YOUR_FALLBACK_API_KEY"
        self.v2_api_url = "https://api.basescan.org/api" # Base için doğru URL
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
        params = {"module": "contract", "action": "getsourcecode", "address": address, "apikey": self.api_key}
        try:
            res = requests.get(self.v2_api_url, params=params, timeout=10).json()
            if res.get("status") == "1":
                return res["result"][0].get("SourceCode"), "Verified"
        except: pass
        return None, None

    def perform_audit(self, code):
        risky_patterns = ["setBlacklist", "blacklist", "setTax", "setFees", "renounceOwnership", "mint", "transferOwnership"]
        return [p for p in risky_patterns if p in code]