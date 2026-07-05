# 🕵️‍♂️ Hermes Dedektif (Smart Contract Security AI Agent)

Hermes Dedektif, Akıllı Kontratlardaki (Smart Contracts) kritik siber güvenlik açıklarını ve mantıksal hataları tespit etmek için geliştirilmiş hibrit bir **Yapay Zeka ve Canlı Blockchain Güvenlik Ajanıdır**.

## 🚀 Öne Çıkan Özellikler (Key Features)
- **Canlı Base Ağı Entegrasyonu (Live Base Network Tarama):** Etherscan API V2 mimarisini kullanarak, Base ağındaki herhangi bir canlı kontrat adresini (Örn: USDC, WETH) doğrudan blokzincirden çekip analiz eder.
- **Statik Analiz Motoru (Static Analysis):** Kod içerisindeki `tx.origin`, `selfdestruct` ve `block.timestamp` gibi kritik ve suistimale açık zafiyetleri milisaniyeler içinde yakalar.
- **Hibrit Yapay Zeka Desteği (Hybrid AI Layer):** Sunucu kaynaklı gecikmeleri ve API kesintilerini önlemek için **Hata Yönetimli (Fallback)** bir mimariye sahiptir. Çevrimiçi LLM API'si yanıt vermediğinde veya yoğun olduğunda, yerel derin analiz motoru otomatik olarak devreye girer.
- **Güvenli Mimari:** `.env` desteği sayesinde gizli API anahtarlarınızı asla açık kaynak kodda deşifre etmez.

## 🛠️ Kurulum ve Çalıştırma (Installation)
