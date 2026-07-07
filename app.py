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

with