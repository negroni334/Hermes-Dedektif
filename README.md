# 🕵️‍♂️ Hermes Dedektif (Smart Contract Security AI Agent)

Hermes Dedektif, Akıllı Kontratlardaki (Smart Contracts) kritik siber güvenlik açıklarını ve mantıksal hataları tespit etmek için geliştirilmiş hibrit bir **Yapay Zeka ve Güvenlik Ajanıdır**.

## 🚀 Öne Çıkan Özellikler (Key Features)
- **Statik Analiz Motoru (Static Analysis):** Kod içerisindeki `tx.origin`, `selfdestruct` ve `block.timestamp` gibi kritik ve suistimale açık zafiyetleri milisaniyeler içinde yakalar.
- **Hibrit Yapay Zeka Desteği (Hybrid AI Layer):** Sunucu kaynaklı gecikmeleri ve API kesintilerini önlemek için **Hata Yönetimli (Fallback)** bir mimariye sahiptir. Çevrimiçi LLM API'si yanıt vermediğinde, yerel derin analiz motoru otomatik olarak devreye girer.
- **Esnek Dosya Okuma:** Dışarıdan yüklenen herhangi bir `.sol` (Solidity) dosyasını bağımsız olarak işleyebilir.

## 🛠️ Kurulum ve Çalıştırma (Installation)
# Gerekli bağımlılıkları yükleyin
py -m pip install requests

# Dedektifi çalıştırın
py main.py
