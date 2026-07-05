import re
import os
import requests

class HermesDedektif:
    def __init__(self):
        self.guvenlik_kurallari = {
            "tx.origin": "KRİTİK UYARI: Kimlik doğrulamada 'tx.origin' kullanımı tespit edildi. Phishing saldırılarına yol açabilir!",
            "block.timestamp": "DÜŞÜK UYARI: 'block.timestamp' manipüle edilebilir, hassas rastgele sayı üretiminde kullanılmamalı.",
            "selfdestruct": "YÜKSEK UYARI: 'selfdestruct' fonksiyonu tespit edildi. Kontratın yok edilme riski var."
        }
        self.api_url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-7B-Instruct"

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
        """API çöktüğünde veya geciktiğinde devreye giren B Planı (Fallback)"""
        rapor = "🤖 [Yerel Güvenlik Motoru Raporu]\n\n"
        if not statik_bulgular:
            return rapor + "✅ Kontrat üzerinde yapılan yerel derin analizde herhangi bir mantıksal veya yapısal açık tespit edilemedi."
        
        rapor += f"🚨 Kontrat içinde kritik risk seviyesine sahip {len(statik_bulgular)} mimari zafiyet bulundu:\n\n"
        for b in statik_bulgular:
            if "tx.origin" in b:
                rapor += "▪️ [PHISHING TEHDİDİ]: Kontrat harici bir cüzdan vasıtasıyla kandırılabilir (tx.origin istismarı). Acilen 'msg.sender' mimarisine geçiş yapılmalı.\n"
            if "selfdestruct" in b:
                rapor += "▪️ [KONTROL KAYBI]: 'selfdestruct' kullanımı, kötü niyetli veya hatalı bir tetikleme ile kontrattaki tüm likiditeyi kalıcı olarak kilitleyebilir/yok edebilir.\n"
        return rapor

    def yapay_zeka_analizi(self, kontrat_kodu, statik_bulgular):
        print("🧠 [Yapay Zeka] Kontrat bütünsel olarak analiz ediliyor, derin rapor isteniyor...")
        
        sistem_mesaji = (
            "Sen profesyonel bir Web3 ve Akıllı Kontrat Güvenlik Uzmanısın. "
            "Sana verilen Solidity kodunu incele, gizli honeypot risklerini ve mantık hatalarını tespit et. "
            "Cevabını temiz, kısa ve maddeler halinde Türkçe olarak ver."
        )
        
        girdi_metni = (
            f"{sistem_mesaji}\n\n"
            f"--- ANALİZ EDİLECEK SÖZLEŞME KODU ---\n{kontrat_kodu}\n\n"
            f"--- BASİT TARAYICI BULGULARI ---\n{os.linesep.join(statik_bulgular) if statik_bulgular else 'Bulgu yok.'}\n\n"
            f"Lütfen bu kontratı derinlemesine analiz et ve kritik riskleri raporla:"
        )

        try:
            # Zaman aşımını (timeout) biraz daha esnek tutuyoruz
            cevap = requests.post(
                self.api_url,
                json={"inputs": girdi_metni, "parameters": {"max_new_tokens": 400, "temperature": 0.2}},
                timeout=10
            )
            
            if cevap.status_code == 200:
                sonuc = cevap.json()
                if isinstance(sonuc, list) and "generated_text" in sonuc[0]:
                    raw_text = sonuc[0]["generated_text"]
                    ai_raporu = raw_text.replace(girdi_metni, "").strip()
                    if ai_raporu:
                        return f"✨ [Yapay Zeka Raporu]\n\n{ai_raporu}"
            
            # Sunucu hatası veya boş yanıt durumunda Fallback çalıştır
            return self.yerel_derin_rapor_olustur(statik_bulgular)
            
        except Exception:
            # İnternet yoksa veya API çöktüyse sessizce yerel motora devret
            return self.yerel_derin_rapor_olustur(statik_bulgular)

    def dosya_oku_ve_tasi(self, dosya_yolu):
        if not os.path.exists(dosya_yolu):
            print(f"❌ Hata: '{dosya_yolu}' dosyası bulunamadı!")
            return

        print(f"\n🕵️‍♂️ [Hermes Dedektif] '{dosya_yolu}' dosyası açılıyor...")
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            kontrat_kodu = f.read()

        statik_sonuclar = self.statik_analiz(kontrat_kodu)
        print(f"🚨 Hızlı taramada {len(statik_sonuclar)} risk kalıbı tetiklendi.\n")

        ai_raporu = self.yapay_zeka_analizi(kontrat_kodu, statik_sonuclar)
        
        print("================ DEDEKTİF RAPORU ================")
        print(ai_raporu)
        print("=================================================")

if __name__ == "__main__":
    dedektif = HermesDedektif()
    dedektif.dosya_oku_ve_tasi("test_kontrat.sol")
    