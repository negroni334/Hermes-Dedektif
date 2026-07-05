import re
import os

class HermesDedektif:
    def __init__(self):
        # Tarayacağımız kurallar
        self.guvenlik_kurallari = {
            "tx.origin": "KRİTİK UYARI: Kimlik doğrulamada 'tx.origin' kullanımı tespit edildi. Phishing saldırılarına yol açabilir! Yerine 'msg.sender' kullanılmalı.",
            "block.timestamp": "DÜŞÜK UYARI: 'block.timestamp' manipüle edilebilir, hassas rastgele sayı üretiminde kullanılmamalı.",
            "selfdestruct": "YÜKSEK UYARI: 'selfdestruct' fonksiyonu tespit edildi. Kontratın yok edilme ve fonların kilitlenme riski var."
        }

    def dosya_oku_ve_analiz_et(self, dosya_yolu):
        if not os.path.exists(dosya_yolu):
            print(f"❌ Hata: '{dosya_yolu}' dosyası bulunamadı!")
            return

        print(f"\n🕵️‍♂️ [Hermes Dedektif] '{dosya_yolu}' dosyası analiz ediliyor...\n")
        
        # Dosyayı aç ve oku
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            kontrat_kodu = f.read()

        bulgular = []
        satirlar = kontrat_kodu.split('\n')
        
        for satir_no, satir in enumerate(satirlar, 1):
            for kural, aciklama in self.guvenlik_kurallari.items():
                if kural in satir:
                    if not satir.strip().startswith("//"):
                        bulgular.append(f"📌 Satır {satir_no}: {aciklama}\n   👉 Kod: {satir.strip()}")

        if bulgular:
            print(f"🚨 Toplam {len(bulgular)} adet potansiyel risk tespit edildi:\n")
            for bulgu in bulgular:
                print(bulgu)
        else:
            print("✅ Harika! Temel güvenlik taramasında herhangi bir riskli kalıba rastlanmadı.")

if __name__ == "__main__":
    # Analiz etmek istediğimiz hedef dosya
    hedef_dosya = "test_kontrat.sol"
    
    dedektif = HermesDedektif()
    dedektif.dosya_oku_ve_analiz_et(hedef_dosya)
    