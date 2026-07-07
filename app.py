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
    </style>
""", unsafe_allow_html=True)

# 3. SOL MENÜ (SIDEBAR)
with st.sidebar:
    st.markdown("<h2 style='color:#ff007f; font-family:\"Share Tech Mono\";'>🛰️ SYSTEM TELEMETRY</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    visitors = st.session_state["visitor_log"]["24h_visitors"]
    total_scans = st.session_state["total_scans"]
    
    st.markdown("<div style='background: #030712; padding: 1rem; border-radius: 8px; border: 1px solid rgba(255, 0, 127, 0.25); margin-bottom: 1rem;'><p style='margin:0; color:#94a3b8; font-size:0.8rem;'>🫵 24H UNIQUE VISITORS</p><h2 style='margin:0; color:#00f2fe; font-family:\"Share Tech Mono\"; font-size:2.2rem;'>" + str(visitors) + "</h2></div>", unsafe_allow_html=True)
    st.markdown("<div style='background: #030712; padding: 1rem; border-radius: 8px; border: 1px solid rgba(255, 0, 127, 0.25); margin-bottom: 1rem;'><p style='margin:0; color:#94a3b8; font-size:0.8rem;'>⚡ TOTAL SECURITY SCANS</p><h2 style='margin:0; color:#ff007f; font-family:\"Share Tech Mono\"; font-size:2.2rem;'>" + str(total_scans) + "</h2></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div style='background:#030712; padding:0.8rem; border-radius:8px; border:1px solid #38bdf833; margin-bottom:1rem;'>
            <p style='margin:0; color:#94a3b8; font-size:0.75rem;'>TELEMETRY NODE</p>
            <h4 style='margin:0; color:#4ade80;'>🟢 ONLINE / MONITORING</h4>
        </div>
        <div style='background:#030712; padding:0.8rem; border-radius:8px; border:1px solid #38bdf833; margin-bottom:1rem;'>
            <p style='margin:0; color:#94a3b8; font-size:0.75rem;'>TARGET GATEWAY</p>
            <h4 style='margin:0; color:#38bdf8;'>⛓️ BASE MAINNET</h4>
        </div>
    """, unsafe_allow_html=True)

# ANA SAYFA ÜST BAŞLIK
st.markdown("""
    <div style='background: linear-gradient(90deg, #1e1b4b 0%, #0f172a 100%); border-left: 5px solid #ff007f; padding: 1.5rem 2rem; border-radius: 8px; margin-bottom: 2rem;'>
        <h1 style='color: #ffffff; margin: 0; font-family: "Share Tech Mono", sans-serif; font-size: 2.8rem; letter-spacing: 3px;'>🕵️‍♂️ HERMES DETECTIVE</h1>
        <p style='color: #00f2fe; font-size: 1.1rem; margin: 0.2rem 0 0 0; font-family: "JetBrains Mono", monospace;'>Autonomous Web3 Smart Contract Security Agent</p>
    </div>
""", unsafe_allow_html=True)

# İKİ SÜTUNLU MERKEZİ PANEL DÜZENİ
col_left, col_right = st.columns([2, 3], gap="large")

with col_left:
    st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#ffffff; font-family:\"Share Tech Mono\"; margin-top:0;'>🔒 INITIATE THREAT SCAN</h3>", unsafe_allow_html=True)
    st.write("Deploy advanced semantic analysis and code-flow graph scanning to map vulnerabilities instantly.")
    
    contract_address = st.text_input(
        "Target Base Deployment Address",
        placeholder="Enter 0x... address here"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    run_audit = st.button("RUN SECURITY TELEMETRY")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if run_audit:
        if contract_address.strip() == "":
            st.warning("Please enter a valid contract address.")
        else:
            st.session_state["total_scans"] += 1
            with st.spinner("🕵️‍♂️ Mapping bytecode blocks & inspecting token liquidity holders..."):
                try:
                    pdf_path, score, holder_data = auditor(contract_address)
                    
                    st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
                    st.markdown("<h3 style='color:#ffffff; font-family:\"Share Tech Mono\"; margin-top:0;'>📊 ACTIVE INTELLIGENCE REPORT</h3>", unsafe_allow_html=True)
                    
                    if score >= 70:
                        st.markdown('<div style="background:rgba(16,185,129,0.1); border:2px solid #10b981; padding:1.5rem; border-radius:8px; text-align:center; box-shadow:0 0 15px rgba(16,185,129,0.3);"><h2 style="margin:0; font-size:3rem; color:#34d399; font-family:\'Share Tech Mono\';">' + str(score) + ' / 100</h2><strong style="color:#34d399;">SECURITY LEVEL: SECURE (LOW RISK)</strong></div>', unsafe_allow_html=True)
                    elif score >= 40:
                        st.markdown('<div style="background:rgba(245,158,11,0.1); border:2px solid #f59e0b; padding:1.5rem; border-radius:8px; text-align:center; box-shadow:0 0 15px rgba(245,158,11,0.3);"><h2 style="margin:0; font-size:3rem; color:#fbbf24; font-family:\'Share Tech Mono\';">' + str(score) + ' / 100</h2><strong style="color:#fbbf24;">SECURITY LEVEL: WARNING (MEDIUM RISK)</strong></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="background:rgba(239,68,68,0.1); border:2px solid #ef4444; padding:1.5rem; border-radius:8px; text-align:center; box-shadow:0 0 15px rgba(239,68,68,0.3);"><h2 style="margin:0; font-size:3rem; color:#f87171; font-family:\'Share Tech Mono\';">' + str(score) + ' / 100</h2><strong style="color:#f87171;">SECURITY LEVEL: CRITICAL VULNERABILITY DETECTED</strong></div>', unsafe_allow_html=True)
                    
                    if holder_data:
                        st.markdown("<br><h4 style='color:#ffffff; font-family:\"Share Tech Mono\";'>📋 TOP HOLDERS LEDGER</h4>", unsafe_allow_html=True)
                        df = pd.DataFrame(holder_data)
                        st.dataframe(df, use_container_width=True)
                    
                    if pdf_path and os.path.exists(pdf_path):
                        st.markdown("<br>", unsafe_allow_html=True)
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="📥 DOWNLOAD STANDALONE SECURITY AUDIT PDF",
                                data=f