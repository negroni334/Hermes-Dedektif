import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
ai_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENAI_API_KEY"))

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

    def check_risky_functions(self, code):
        risky = ["setBlacklist", "blacklist", "setTax", "setFees", "renounceOwnership"]
        return [f for f in risky if f in code]

    def fetch_contract_source(self, address):
        params = {"chainid": "8453", "module": "contract", "action": "getsourcecode", "address": address, "apikey": self.api_key}
        try:
            res = requests.get(self.v2_api_url, params=params, timeout=10).json()
            if res.get("status") == "1": return res["result"][0].get("SourceCode"), "Verified"
        except: pass
        return None, None

    def ai_deep_audit(self, code):
        prompt = f"Analyze this contract for security. List risks. Code: {code[:3000]}"
        try:
            res = ai_client.chat.completions.create(model="google/gemini-2.5-flash", messages=[{"role": "user", "content": prompt}])
            return res.choices[0].message.content
        except: return "AI analysis temporarily unavailable."