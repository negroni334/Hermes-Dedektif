import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HermesAuditor:
    def __init__(self):
        self.api_key = os.getenv("BASESCAN_API_KEY")
        self.v2_api_url = "https://api.etherscan.io/v2/api"
        self.counter_file = "scan_counter.txt"

    def get_stats(self):
        if not os.path.exists(self.counter_file): return 1240
        with open(self.counter_file, "r") as f:
            try: return int(f.read())
            except: return 1240

    def increment_counter(self):
        count = self.get_stats() + 1
        with open(self.counter_file, "w") as f: f.write(str(count))

    def perform_audit(self, code):
        risky_patterns = {
            "Honeypot": ["setBlacklist", "blacklist", "setTrading", "disableTrading"],
            "RugPull Risk": ["renounceOwnership", "setTax", "setFees"]
        }
        found = {"Honeypot": [], "RugPull Risk": []}
        for category, patterns in risky_patterns.items():
            for p in patterns:
                if p in code: found[category].append(p)
        return found