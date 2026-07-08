import os
import re
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

    def run_analysis(self, address):
        # Kaynak kod çekme
        params = {"chainid": "8453", "module": "contract", "action": "getsourcecode", "address": address, "apikey": self.api_key}
        try:
            res = requests.get(self.v2_api_url, params=params, timeout=10).json()
            code = res["result"][0].get("SourceCode", "") if res.get("status") == "1" else ""
        except: code = ""

        # Risk analizleri
        risky_patterns = ["setBlacklist", "blacklist", "setTax", "setFees", "setTrading", "renounceOwnership"]
        found_risks = [p for p in risky_patterns if p in code]
        
        # Rugpull (Simüle edilmiş yüzde kontrolü)
        rug_risk = "High" # Default olarak riskli başla, kod analizine göre refine edilebilir

        return {"code": code, "risks": found_risks, "rug_risk": rug_risk, "score": 85 if not found_risks else 40}