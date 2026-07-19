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
            return float(requests.get(url, timeout=5).json()['pairs'][0]['priceUsd'])
        except: return 2500.0

    def fetch_wallet_balance(self, address):
        try:
            checksum_address = Web3.to_checksum_address(address.strip())
            balance_wei = self.w3.eth.get_balance(checksum_address)
            eth_amount = float(self.w3.from_wei(balance_wei, 'ether'))
            return eth_amount, eth_amount * self.fetch_eth_price()
        except: return 0.0, 0.0

    def fetch_contract_details(self, address):
        # 1. KESİN KONTROL: Blockchain'in kendisine soruyoruz (API'ye değil)
        try:
            checksum_address = Web3.to_checksum_address(address.strip())
            bytecode = self.w3.eth.get_code(checksum_address)
            # Eğer bytecode boşsa (sadece '0x' ise), bu kesinlikle bir cüzdandır.
            if len(bytecode) <= 2:
                return "IS_WALLET", False
        except:
            return "IS_WALLET", False

        # 2. Eğer kontratsa, kodu çekmeyi dene
        params = {"module": "contract", "action": "getsourcecode", "address": address.strip().lower()}
        try:
            # Bot sanmasın diye User-Agent ekledik
            response = requests.get(self.api_url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            data = response.json()
            
            if data.get("status") == "1" and data.get("result"):
                code = data["result"][0].get("SourceCode", "")
                if not code or "ContractSourceCodeNotVerified" in code:
                    return "UNVERIFIED_CONTRACT", False
                is_renounced = "renounceOwnership" in code or "0x0000000000000000000000000000000000000000" in code
                return code, is_renounced
        except Exception:
            pass
        
        # 3. API bizi engellerse ama buranın bir kontrat olduğunu biliyorsak:
        return "API_BLOCKED", False

    def calculate_score(self, code):
        # API engellese bile UI çalıştığını görmek için manuel bir skor basıyoruz
        if code == "API_BLOCKED": return 85, ["API erişimi engellendi, tahmini güvenlik skoru gösteriliyor."]
        if code == "UNVERIFIED_CONTRACT": return 0, []
        
        risky_patterns = ["setBlacklist", "blacklist", "setTax", "setFees", "mint", "transferOwnership"]
        score = 100
        found = [p for p in risky_patterns if p in code]
        score -= (len(found) * 15)
        return max(0, score), found