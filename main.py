import re

class HermesDedektif:
    def __init__(self):
        # Taramak istediğimiz tehlikeli kalıplar ve açıklamaları
        self.guvenlik_kurallari = {
            "tx.origin": "KRİTİK UYARI: Kimlik doğrulamada 'tx.origin' kullanımı tespit edildi. Phishing (kimlik avı) saldırılarına yol açabilir! Yerine 'msg.sender' kullanılmalı.",
            "block.timestamp": "DÜŞÜK UYARI: 'block.timestamp' veya 'now' kullanımı tespit edildi. Madenciler (miners) tarafından manipüle edilebilir, hassas rastgele sayı üretiminde kullanılmamalı.",
            "selfdestruct": "YÜKSEK UYARI: 'selfdestruct' fonksiyonu tespit edildi. Kontratın tamamen yok edilme ve fonların kilitlenme riski var."
        }

    def kontrat_analiz_et(self, kontrat_kodu):
        print("\n🕵️‍♂️ [Hermes Dedektif] Analiz Başlatılıyor...\n")
        bulgular = []

        # Satır satır kodu incele
        satirlar = kontrat_kodu.split('\n')
        for satir_no, satir in enumerate(satirlar, 1):
            for kural, aciklama in self.guvenlik_kurallari.items():
                if kural in satir:
                    # Yorum satırlarını pas geçmek için basit bir kontrol
                    if not satir.strip().startswith("//"):
                        bulgular.append(f"📌 Satır {satir_no}: {aciklama}\n   👉 Kod: {satir.strip()}")

        # Sonuçları ekrana yazdır
        if bulgular:
            print(f"🚨 Toplam {len(bulgular)} adet potansiyel risk tespit edildi:\n")
            for bulgu in bulgular:
                print(bulgu)
        else:
            print("✅ Harika! Temel güvenlik taramasında herhangi bir riskli kalıba rastlanmadı.")

# Test amaçlı örnek bir akıllı kontrat kodu (Solidity)
ornek_kontrat = """
pragma solidity ^0.8.0;

contract GuvensizKontrat {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // Riskli Fonksiyon 1
    function transferEt(address alici) public {
        require(tx.origin == owner, "Yetkiniz yok!"); 
        payable(alici).transfer(address(this).balance);
    }

    // Riskli Fonksiyon 2
    function rastgeleSayiUret() public view returns (uint) {
        return uint(keccak256(abi.encodePacked(block.timestamp))); 
    }
}
"""

if __name__ == "__main__":
    dedektif = HermesDedektif()
    dedektif.kontrat_analiz_et(ornek_kontrat)
    