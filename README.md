# 🕵️‍♂️ Hermes Dedektif (Smart Contract Security AI Agent)

Hermes Dedektif, Akıllı Kontratlardaki (Smart Contracts) kritik siber güvenlik açıklarını ve mantıksal hataları tespit etmek için geliştirilmiş hibrit bir Yapay Zeka ve Canlı Blockchain Güvenlik Ajanıdır.

## 🚀 Öne Çıkan Özellikler (Key Features)
- Canlı Base Ağı Entegrasyonu: Etherscan API V2 mimarisini kullanarak, Base ağındaki herhangi bir canlı kontrat adresini doğrudan blokzincirden çekip analiz eder.
- Statik Analiz Motoru: Kod içerisindeki tx.origin, selfdestruct ve block.timestamp gibi kritik ve suistimale açık zafiyetleri milisaniyeler içinde yakalar.
- Güvenli Mimari: .env desteği sayesinde gizli API anahtarlarınızı asla açık kaynak kodda deşifre etmez.

## 🛠️ Kurulum ve Çalıştırma (Installation)

Aşağıdaki komutları sırasıyla terminalinizde çalıştırarak projeyi kurabilirsiniz:

```bash
git clone [https://github.com/negroni334/Hermes-Dedektif.git](https://github.com/negroni334/Hermes-Dedektif.git)
cd Hermes-Dedektif
py -m pip install requests python-dotenv