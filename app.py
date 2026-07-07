import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from main import auditor  # Ana analiz motorun

# ==========================================
# 📊 GEÇİCİ VERİ TABANI (CANLI SAYAÇ SİSTEMİ)
# ==========================================
if "total_scans" not in st.session_state:
    st.session_state["total_scans"] = 42

if "visitor_log" not in st.session_state:
    st.session_state["visitor_log"] = {
        "24h_visitors": 118,
        "live_nodes": 7
    }

# Sayfa Ayarları (Geniş Ekran)
st.set_page_config(
    page_title="Hermes Detective | Web3 Security Suite",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gelişmiş Kurumsal & Canlı CSS (Siber Güvenlik Dashboard Teması)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Share+Tech+Mono&display=swap');
    
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
    
    .counter-widget {
        background: #030712; 
        padding: 1rem; 
        border-radius: 8px; 
        border: 1px solid #ff007f44; 
        margin-bottom: 1rem;
        box-shadow: inset 0 0 10px rgba(255, 0, 127, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 3. SOL MENÜ (SIDEBAR)
with st.sidebar:
    st.markdown("<h2 style='color:#ff007f; font-family:\"Share Tech Mono\";'>🛰️ SYSTEM TELEMETRY</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    visitors = st.session_state["visitor_log"]["24h_visitors"]
    total_scans = st.session_state["total_scans"]
    
    st.markdown(f"""
        <div class="counter-widget">
            <p style='margin:0; color:#94a3b8; font-size:0.8rem;'>🫵 24H UNIQUE VISITORS</p>
            <h2 style='margin:0; color:#00f2fe; font-family:"Share Tech Mono"; font-size:2.2rem;'>{visitors}</h2>
        </div>
        <div class="counter-widget">
            <p style='margin:0; color:#94a3b8; font-size:0.8rem;'>⚡ TOTAL SECURITY SCANS</p>
            <h2 style='margin:0; color:#ff007f; font-family:"Share Tech Mono"; font-size:2.2rem;'>{total_scans}</h2>
        </div>
    """, unsafe_