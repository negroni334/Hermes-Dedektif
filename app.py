import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
# main.py içindeki dedektif sınıfımızı doğrudan içeri aktarıyoruz
from main import auditor

load_dotenv()

# Web Sitesi Sayfa Ayarları (Koyu Tema ve Tarayıcı Başlığı)
st.set_page_config(
    page_title="Hermes Smart Contract Security Detective",
    page_icon="🕵️‍♂️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Arayüz Başlıkları ve Görsel Tasarım
st.markdown("<h1 style='text-align: center; color: #1A365D;'>🕵️‍♂️ HERMES DETECTIVE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4A5568;'>Autonomous Web3 Smart Contract Security Agent</h3>", unsafe_allow_html=True)
st.markdown("---")

st.write("Enter any Base Blockchain contract address below to generate an objective, industry-grade security audit ledger.")

# Kullanıcı Giriş Alanı
contract_address = st.text_input("Base Contract Address (0x...)", placeholder="0x833589fCD6eDb6E08f4c7C32D4f71b54bda02913").strip()

if st.button("Run Security Audit", type="primary"):
    if not contract_address.startswith("0x") or len(contract_address) != 42:
        st.error("⚠️ Invalid address format. Please provide a valid 42-character Base network contract address.")
    else:
        with st.spinner("Analyzing network layers, tracking top holders, and processing AI audit ledger..."):
            # 1. Ağ katmanlarından kod veya bytecode katmanını çekelim
            code, code_type = auditor.fetch_contract_source(contract_address)
            if not code:
                code, code_type = auditor.fetch_contract_bytecode(contract_address)
            if not code:
                code = "HIDDEN_OR_EMPTY_TARGET"
                code_type = "Unknown / Unverified Structure (Kritik)"

            # 2. Canlı Cüzdan ve Dağılım Analizini Yapalım
            distribution_res = auditor.analyze_token_distribution(contract_address)

            # 3. Yapay Zeka Ceza Puanlaması ve Denetim Sürecini Tetikleyelim
            ai_report = auditor.ai_deep_audit(code, code_type, distribution_res, contract_address)

            # Raporlama için PDF dosya adını belirleyelim
            pdf_filename = f"Hermes_Web_Audit_{contract_address[:8]}.pdf"
            
            try:
                # PDF raporunu arka planda oluşturalım
                auditor.build_pdf_report(pdf_filename, contract_address, distribution_res, ai_report, code_type)
                
                # Ekranda Skor Gösterimi İçin Puanı Ayıklayalım
                import re
                score = "0"
                for line in ai_report.split("\n"):
                    if "Security Score" in line:
                        numbers = re.findall(r'\d+', line)
                        if numbers:
                            score = numbers[0]
                        break

                score_val = int(score)
                
                # Dinamik Renk Belirleme
                if score_val >= 75:
                    st.success(f"### 🎉 Overall Security Score: {score_val} / 100 (Low Risk)")
                elif score_val >= 50:
                    st.warning(f"### ⚠️ Overall Security Score: {score_val} / 100 (Medium Risk)")
                else:
                    st.error(f"### 🚨 Overall Security Score: {score_val} / 100 (CRITICAL RISK)")

                st.markdown("---")
                
                # Canlı Cüzdan Dağılım Verilerini Ekrana basalım
                st.subheader("1. Live Wallet & Token Distribution Ledger")
                for holder in distribution_res:
                    st.write(f"• {holder}")

                st.markdown("---")

                # İndirme Butonu Ekleyelim (Kullanıcı PDF olarak indirebilsin)
                with open(pdf_filename, "rb") as file:
                    st.download_button(
                        label="📥 Download Standalone PDF Audit Report",
                        data=file,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                # PDF oluştuktan sonra lokal temizlik yapalım
                if os.path.exists(pdf_filename):
                    os.remove(pdf_filename)

            except Exception as e:
                st.error(f"❌ An error occurred during report visualization: {str(e)}")

st.markdown("<br/><br/><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Powered by Hermes Agent Accelerated Architecture & Base Protocol</p>", unsafe_allow_html=True)