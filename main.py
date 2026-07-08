import os
import requests

class HermesAuditor:
    def __init__(self):
        # API anahtarı olmadan da çalışan genel endpoint
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
        # API anahtarı zorunlu değil, bazen boş bırakmak daha iyi çalışır
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address
        }
        try:
            response = requests.get(self.api_url, params=params, timeout=15)
            data = response.json()
            if data.get("status") == "1":
                return data["result"][0].get("SourceCode", ""), "Verified"
        except Exception as e:
            return None, str(e)
        return None, "Not Found"

    def perform_audit(self, code):
        risky_patterns = ["setBlacklist", "blacklist", "setTax", "setFees", "renounceOwnership"]
        return [p for p in risky_patterns if p in code]