import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from main import auditor  # Ana analiz motorun

# 1. Sayfa Ayarlarını Kurumsal Yapalım
st.set_page_config(
    page_title="Hermes Detective | Web3 Security",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Özel Kurumsal CSS Teması (Göz Alıcı Siber Güvenlik Modu)
st.markdown("""
    <style>
    /* Arka plan ve genel yazı renkleri */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    /* Input kutusunun tasarımı */
    div[data-baseweb="input"] {
        background-color: #1e293b !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 10px !important;
    }
    
    /* Run Security Audit Butonu Tasarımı */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ef4444 0%, #cc1111 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Başlık Alanı
col1, col2 = st.columns([1, 8])
with col1:
    st.markdown("<h1 style='font-size: 4.5rem; margin:0;'>🕵️‍♂️</h1>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 style='color: #3b82f6; margin-bottom: 0; padding-top: 10px;'>HERMES DETECTIVE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1.1rem; margin-top:0;'>Autonomous Web3 Smart Contract Security Agent</p>", unsafe_allow_html=True)

st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)

# 4. Arama Alanı
st.markdown("### 🔍 Scan Smart Contract")
contract_address = st.text_input(
    "Base Contract Address (0x...)",
    placeholder="Enter Base Blockchain contract address to generate an objective, industry-grade security audit ledger."
)

# 5. Buton ve Backend Mantığı (Motorun Çalıştığı Yer)
if st.button("Run Security Audit"):
    if contract_address.strip() == "":
        st.warning("Please enter a valid contract address.")
    else:
        with st.spinner("🕵️‍♂️ Hermes Detective is analyzing the contract architecture, holder distributions, and compiler vulnerabilities..."):
            try:
                # main.py içindeki auditor fonksiyonunu tetikliyoruz
                pdf_path, score, holder_data = auditor(contract_address)
                
                st.markdown("---")
                st.success("Audit Completed Successfully!")
                
                # Skor Gösterimi
                if score >= 70:
                    st.metric(label="Security Score", value=f"{score} / 100", delta="LOW RISK", delta_color="normal")
                elif score >= 40:
                    st.metric(label="Security Score", value=f"{score} / 100", delta="MEDIUM RISK", delta_color="off")
                else:
                    st.metric(label="Security Score", value=f"{score} / 100", delta="- CRITICAL RISK", delta_color="inverse")
                
                # Cüzdan Dağılım Tablosu
                if holder_data:
                    st.markdown("### 📊 Top Token Holders Distribution")
                    df = pd.DataFrame(holder_data)
                    st.dataframe(df, use_container_width=True)
                
                # PDF İndirme Butonu
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Standalone PDF Audit Report",
                            data=f,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error(f"An error occurred during the audit: {str(e)}")

# 6. Kurumsal Alt Bilgi ve Kurucu İmzası (Founder: Baileys)
st.markdown("""
    <br><br><hr style='border-color: #334155;'>
    <div style='display: flex; justify-content: space-between; color: #475569; font-size: 0.85rem;'>
        <div>🚀 Powered by Hermes Agent Accelerated Architecture & Base Protocol</div>
        <div style='font-weight: bold; color: #3b82f6;'>⚙️ Founder: Baileys {NEGRONI]</div>
    </div>
""", unsafe_allow_html=True)