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
            url = "https://api.dexscreener.com/latest/dex/tokens/0x4200000000000000000000000000000000000006"
            data = requests.get(url, timeout=5).json()
            return float(data['pairs'][0]['priceUsd'])
        except: return 2500.0

    def fetch_wallet_balance(self, address):
        try:
            checksum_address = Web3.to_checksum_address(address.strip())
            balance_wei = self.w3.eth.get_balance(checksum_address)
            eth_amount = float(self.w3.from_wei(balance_wei, 'ether'))
            return eth_amount, eth_amount * self.fetch_eth_price()
        except: return 0.0, 0.0

    def fetch_contract_details(self, address):
        params = {
            "module": "contract", 
            "action": "getsourcecode", 
            "address": address.strip().lower()
        }
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            data = response.json()
            
            if data.get("status") == "1" and data.get("result"):
                code = data["result"][0].get("SourceCode", "")
                
                # Kod boşsa veya doğrulanmamışsa özel durum döndür
                if not code or "ContractSourceCodeNotVerified" in code:
                    return "UNVERIFIED_CONTRACT", False
                    
                is_renounced = "renounceOwnership" in code or "0x0000000000000000000000000000000000000000" in code
                return code, is_renounced
            
            return None, False
        except Exception:
            return None, False

    def calculate_score(self, code):
        if code == "UNVERIFIED_CONTRACT" or code is None: 
            return 0, []
        risky_patterns = ["setBlacklist", "blacklist", "setTax", "setFees", "mint", "transferOwnership"]
        score = 100
        found = [p for p in risky_patterns if p in code]
        score -= (len(found) * 15)
        return max(0, score), found