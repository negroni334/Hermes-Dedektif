# 🕵️‍♂️ Hermes Dedektif (Smart Contract Security AI Agent)

Hermes Dedektif, Akıllı Kontratlardaki (Smart Contracts) kritik siber güvenlik açıklarını ve mantıksal hataları tespit etmek için geliştirilmiş hibrit bir Yapay Zeka ve Canlı Blockchain Güvenlik Ajanıdır.

## 🚀 Öne Çıkan Özellikler (Key Features)
- Canlı Base Ağı Entegrasyonu: Etherscan API V2 mimarisini kullanarak, Base ağındaki herhangi bir canlı kontrat adresini doğrudan blokzincirden çekip analiz eder.
- Statik Analiz Motoru: Kod içerisindeki tx.origin, selfdestruct ve block.timestamp gibi kritik ve suistimale açık zafiyetleri milisaniyeler içinde yakalar.
- Hibrit Yapay Zeka Desteği: Çevrimiçi LLM API'si yanıt vermediğinde veya yoğun olduğunda, yerel derin analiz motoru otomatik olarak devreye girer.
- Güvenli Mimari: .env desteği sayesinde gizli API anahtarlarınızı asla açık kaynak kodda deşifre etmez.

## 🛠️ Kurulum ve Çalıştırma (Installation)

1. Projeyi klonlayın:
git clone https://github.com/negroni334/Hermes-Dedektif.git

2. Proje klasörüne girin:
cd Hermes-Dedektif

3. Gerekli bağımlılıkları yükleyin:
py -m pip install requests python-dotenv

## 🔑 Yapılandırma (Configuration)
Klasör kökünde bir .env dosyası oluşturun ve Basescan API anahtarınızı ekleyin:
BASESCAN_API_KEY=your_api_key_here

## 🕵️‍♂️ Çalıştırma
Proji çalıştırmak için terminale şu komutu yazın:
py main.py

## 🎯 Hedef
Nous Research topluluğunda ve Base ekosisteminde yapay zeka tabanlı akıllı kontrat denetimini tamamen otonom hale getirmek.
