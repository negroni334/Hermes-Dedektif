import re
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HermesDedektif:
    def __init__(self):
        self.guvenlik_kurallari = {
            "tx.origin": "KRİTİK UYARI: Kimlik doğrulamada 'tx.origin' kullanımı tespit edildi. Phishing saldırılarına yol açabilir!",
            "block.timestamp": "DÜŞÜK UYARI: 'block.timestamp' manipüle edilebilir, hassas rastgele sayı üretiminde kullanılmamalı.",
            "selfdestruct": "YÜKSEK UYARI: 'selfdestruct' fonksiyonu tespit edildi. Kontratın yok edilme riski var."
        }
        self.api_key = os.getenv("BASESCAN_API_KEY")
        # Yeni Nesil Etherscan API V2 Merkezi Adresi
        self.v2_api_url = "https://api.etherscan.io/v2/api"

    def base_agindan_kontrat_cek(self, kontrat_adresi):
        print(f"🌐 [Base Ağı V2 API] {kontrat_adresi} adresindeki kontrat kodu çekiliyor...")
        
        params = {
            "chainid": "8453", # Base Ağının Resmi ID'si
            "module": "contract",
            "action": "getsourcecode",
            "address": kontrat_adresi,
            "apikey": self.api_key
        }
        
        try:
            cevap = requests.get(self.v2_api_url, params=params, timeout=15)
            if cevap.status_code == 200:
                data = cevap.json()
                
                if data.get("status") == "1" and data.get("result"):
                    source_code = data["result"][0].get("SourceCode")
                    if source_code:
                        return source_code
                    
                print(f"⚠️ API Yanıt Mesajı: {data.get('message')} | Detay: {data.get('result')}")
                return None
            else:
                print(f"❌ API Bağlantı Hatası: Kod {cevap.status_code}")
                return None
        except Exception as e:
            print(f"❌ Bağlantı sırasında bir hata oluştu: {str(e)}")
            return None

    def statik_analiz(self, kontrat_kodu):
        bulgular = []
        satirlar = kontrat_kodu.split('\n')
        for satir_no, satir in enumerate(satirlar, 1):
            for kural, aciklama in self.guvenlik_kurallari.items():
                if kural in satir:
                    if not satir.strip().startswith("//"):
                        bulgular.append(f"📌 Satır {satir_no}: {aciklama} -> Kod: {satir.strip()}")
        return bulgular

    def yerel_derin_rapor_olustur(self, statik_bulgular):
        rapor = "🤖 [Yerel Güvenlik Motoru Raporu]\n\n"
        if not statik_bulgular:
            return rapor + "✅ Yapılan derin analizde herhangi bir zafiyet kalıbına rastlanmadı."
        
        rapor += f"🚨 Kontrat içinde {len(statik_bulgular)} mimari zafiyet bulundu:\n\n"
        for b in statik_bulgular:
            if "tx.origin" in b:
                rapor += "▪️ [PHISHING TEHDİDİ]: tx.origin istismarı riski. msg.sender kullanılmalı.\n"
            if "selfdestruct" in b:
                rapor += "▪️ [KONTROL KAYBI]: selfdestruct riski. Fonlar kalıcı olarak kilitlenebilir.\n"
        return rapor

    def analiz_et(self, kontrat_kodu):
        statik_sonuclar = self.statik_analiz(kontrat_kodu)
        print(f"🚨 Hızlı taramada {len(statik_sonuclar)} risk kalıbı tetiklendi.\n")
        
        rapor = self.yerel_derin_rapor_olustur(statik_sonuclar)
        print("================ DEDEKTİF RAPORU ================")
        print(rapor)
        print("=================================================")

if __name__ == "__main__":
    dedektif = HermesDedektif()
    
    # Base ağındaki USDC kontrat adresi
    hedef_canli_kontrat = "0x833589fCD6eDb6E08f4c7C32D4f71b54bda02913" 
    
    kod = dedektif.base_agindan_kontrat_cek(hedef_canli_kontrat)
    if kod:
        dedektif.analiz_et(kod)
        