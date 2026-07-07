import streamlit as st
import pandas as pd
import os
import re
from dotenv import load_dotenv
from main import HermesAuditor

# Sayfa Ayarları
st.set_page_config(
    page_title="Hermes Detective | Web3 Security Suite",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 🛰️ GLOBAL CANLI TARAMA SAYAÇ SİSTEMİ (DOSYA TABANLI)
# ==========================================
COUNTER_FILE = "scan_counter.txt"

def get_total_scans():
    """Dosyadan toplam tarama sayısını okur, dosya yoksa 0 döndürür."""
    if not os.path.exists(COUNTER_FILE):
        return 42  # Başlangıç için prestij amaçlı 42'den başlatıyoruz şef
    try:
        with open(COUNTER_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 42

def increment_total_scans():
    """Tarama yapıldığında ortak sayacı 1 artırır ve dosyaya yazar."""
    current_count = get_total_scans()
    new_count = current_count + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(new_count))
    return new_count

# İlk açılışta güncel sayıyı yükle
total_global_scans = get_total_scans()

# Gelişmiş Kurumsal & Canlı CSS (Siber Güvenlik Dashboard Teması)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght=400;700&family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #111827 0%, #030712 100%);
        color: #00f2fe;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid #00f2fe33 !important;
    }
    
    .cyber-panel {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #00f2fe44;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.1);
        margin-bottom: 1.5rem;
    }
    
    div[data-baseweb="input"] {
        background-color: #030712 !important;
        border: 2px solid #00f2fe !important;
        border-radius: 8px !important;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.2) !important;
    }
    input {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%) !important;
        color: white !important;
        font-family: 'Share Tech Mono', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        letter-spacing: 2px !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 1rem !important;
        width: 100%;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 35px rgba(255, 0, 127, 0.8) !important;
    }
    
    .cyber-terminal {
        background-color: #030712;
        border: 1px solid #3b82f644;
        font-family: 'JetBrains Mono', monospace;
        padding: 1.5rem;
        border-radius: 8px;
        color: #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

# 3. SOL MENÜ (SIDEBAR)
with st.sidebar:
    st.title("🛰️ SYSTEM TELEMETRY")
    st.markdown("---")
    
    # 🔥 ARTIK BURASI TÜM SİTE GENELİNDEKİ GERÇEK TOPLAM TARAMA SAYISINI GÖSTERİYOR
    st.metric(label="⚡ TOTAL SECURITY SCANS", value=total_global_scans)
    
    st.markdown("---")
    st.success("🟢 TELEMETRY NODE: ONLINE")
    st.info("⛓️ TARGET GATEWAY: BASE MAINNET")

# ANA SAYFA ÜST BAŞLIK
st.markdown("""
    <div style='background: linear-gradient(90deg, #1e1b4b 0%, #0f172a 100%); border-left: 5px solid #ff007f; padding: 1.5rem 2rem; border-radius: 8px; margin-bottom: 2rem;'>
        <h1 style='color