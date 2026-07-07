import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from main import auditor  # Ana analiz motorun

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="Hermes Detective | Web3 Security",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Gelişmiş Kurumsal & Canlı CSS (Siber Güvenlik Dashboard Teması)
st.markdown("""
    <style>
    /* Arka Plan Geçişi */
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b 0%, #0f172a 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Üst Başlık Alanı */
    .header-container {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Siber Kart Tasarımı (Glassmorphism) */
    .cyber-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
    }
    
    /* Giriş Alanı Özelleştirme */
    div[data-baseweb="input"] {
        background-color: #0f172a !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 0.3rem !important;
    }
    
    /* Buton Tasarımı (Neon Kırmızı/Turuncu Patlamalı) */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: 1px solid #ef4444 !important;
        padding: 0.8rem 2.5rem !important;
        width: 100%;
        box-shadow: 0 0 15px rgba(220, 38, 38, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 0 25px rgba(220, 38, 38, 0.7) !important;
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
    }
    
    /* Canlı Skor Gösterge Kartı */
    .score-box {
        text-align: center;
        padding: 2rem;
        border-radius: 16px;
        font-weight: bold;
        margin-top: 1rem;
    }
    .score-critical {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        color: #f87171;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
    }
    .score-medium {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
        color: #fbbf24;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
    }
    .score-low {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
        color: #34d399;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Üst Başlık Paneli (Göz Alıcı Karşılama)
st.markdown("""
    <div class="header-container">
        <h1 style='color: #3b82f6; margin: 0; font-size: 3rem; letter-spacing: 2px;'>🕵️‍♂️ HERMES DETECTIVE</h1>
        <p style='color: #94a3b8; font-size: 1.2rem; margin-top: 0.5rem;'>Autonomous Web3 Smart Contract Security Agent</p>
    </div>
""", unsafe_allow_html=True)

# 4. Yan Yana İki Sütunlu Düzen (Sol Taraf Giriş, Sağ Taraf Sonuçlar)
col_left, col_right = st.columns([2, 3], gap="large")

with col_left:
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Security Scanner")
    st.write("Analyze Base network smart contracts for compiler flaws, vulnerability vectors, and centralization risks instantly.")
    
    contract_address = st.text_input(
        "Target Contract Address",
        placeholder="Enter 0x... address"
    )
    
    run_audit = st.button("RUN SECURITY AUDIT")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if run_audit:
        if contract_address.strip() == "":
            st.warning("Please enter a valid contract address.")
        else:
            with st.spinner("🕵️‍♂️ Analyzing smart contract architecture..."):
                try:
                    pdf_path, score, holder_data = auditor(contract_address)
                    
                    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
                    st.markdown("### 📊 Audit Ledger Results")
                    
                    # Dinamik ve Canlı Skor Kutusu
                    if score >= 70:
                        st.markdown(f'<div class="score-box score-low"><h2 style="margin:0; font-size:2.5rem;">{score} / 100</h2><span style="font-size:1rem;">LOW RISK</span></div>', unsafe_allow_html=True)
                    elif score >= 40:
                        st.markdown(f'<div class="score-box score-medium"><h2 style="margin:0; font-size:2.5rem;">{score} / 100</h2><span style="font-size:1rem;">MEDIUM RISK</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="score-box score-critical"><h2 style="margin:0; font-size:2.5rem;">{score} / 100</h2><span style="font-size:1rem;">CRITICAL RISK</span></div>', unsafe_allow_html=True)
                    
                    # Cüzdan Dağılımı (Varsa)
                    if holder_data:
                        st.markdown("<br>➡️ **Top Holders Distribution:**", unsafe_allow_html=True)
                        df = pd.DataFrame(holder_data)
                        st.dataframe(df, use_container_width=True)
                    
                    # Rapor İndirme Butonu
                    if pdf_path and os.path.exists(pdf_path):
                        st.markdown("<br>", unsafe_allow_html=True)
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="📥 Download Standalone PDF Audit Report",
                                data=f,
                                file_name=os.path.basename(pdf_path),
                                mime="application/pdf"
                            )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"An error occurred during the audit: {str(e)}")
    else:
        # Butona basılmadan önce sağ tarafta duracak kurumsal bekleme ekranı
        st.markdown('<div class="cyber-card" style="text-align: center; padding: 4rem 2rem; color: #64748b;">', unsafe_allow_html=True)
        st.markdown("🌐 <br><br> *Waiting for target deployment address to execute active intelligence telemetry.*", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 5. Kurumsal Alt Bilgi ve Kurucu İmzası
st.markdown("""
    <br><hr style='border-color: rgba(59, 130, 246, 0.2);'>
    <div style='display: flex; justify-content: space-between; color: #475569; font-size: 0.85rem; padding: 0 1rem;'>
        <div>🚀 Powered by Hermes Agent Accelerated Architecture & Base Protocol</div>
        <div style='font-weight: bold; color: #3b82f6; letter-spacing: 0.5px;'>⚙️ Founder: Baileys (Negroni)</div>
    </div>
""", unsafe_allow_html=True)