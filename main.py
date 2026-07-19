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
        # API anahtarı gerekebilir, ancak genel sorgu limitlerinde bazen kısıtlıyor olabilir
        params = {
            "module": "contract", 
            "action": "getsourcecode", 
            "address": address.strip().lower()
        }
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            data = response.json()
            
            # Hata ayıklama için terminale yazdıralım
            print(f"DEBUG DATA: {data}") 
            
            if data.get("status") == "1":
                result = data["result"][0]
                code = result.get("SourceCode", "")
                if not code: return "NO_CODE", False
                
                is_renounced = "renounceOwnership" in code or "0x0000000000000000000000000000000000000000" in code
                return code, is_renounced
            return None, False
        except Exception as e:
            print(f"HATA: {e}")
            return None, False

    def calculate_score(self, code):
        if code == "NO_CODE": return 0, []
        risky_patterns = ["setBlacklist", "blacklist", "setTax", "setFees", "mint", "transferOwnership"]
        score = 100
        found = [p for p in risky_patterns if p in code]
        score -= (len(found) * 15)
        return max(0, score), found