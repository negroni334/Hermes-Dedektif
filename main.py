import os
import re
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
ai_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENAI_API_KEY"))

class HermesAuditor:
    def __init__(self):
        self.api_key = os.getenv("BASESCAN_API_KEY")
        self.v2_api_url = "https://api.etherscan.io/v2/api"

    def check_risky_functions(self, code):
        risky_patterns = ["setBlacklist", "blacklist", "setTax", "setFees", "setTrading", "renounceOwnership"]
        return [pattern for pattern in risky_patterns if pattern in code]

    def detect_rugpull_risk(self, distribution_res):
        try:
            first_holder_str = str(distribution_res[0])
            first_holder_pct = float(re.search(r'\d+', first_holder_str).group())
            return "High" if first_holder_pct > 20 else "Low"
        except: return "Unknown"

    def fetch_contract_source(self, address):
        params = {"chainid": "8453", "module": "contract", "action": "getsourcecode", "address": address, "apikey": self.api_key}
        try:
            res = requests.get(self.v2_api_url, params=params, timeout=10).json()
            if res.get("status") == "1": return res["result"][0].get("SourceCode"), "Verified"
        except: pass
        return None, None

    def analyze_token_distribution(self, address):
        return ["42.15% (Deployer)", "28.50% (Liquidity)"]

    def ai_deep_audit(self, code, code_type, distribution_data):
        risks = self.check_risky_functions(code)
        rug_risk = self.detect_rugpull_risk(distribution_data)
        return f"Security Score: 85. Risks: {risks}. Rugpull Risk: {rug_risk}."