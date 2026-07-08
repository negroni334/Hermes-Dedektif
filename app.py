import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes Detective", layout="wide")

# CSS - Karanlık mod
st.markdown("""
    <style>
    .stApp {background-color: #0E1117; color: white;}
    </style>
    """, unsafe_allow_html=True)

auditor = HermesAuditor()

# Sidebar
st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.info("Founder: Baileys [NEGRONI]")
st.sidebar.metric("Global Scans", auditor.get_global_count())

st.title("🌐 Security Audit Engine")
address = st.text_input("Enter Base Contract Address:")

if st.button("RUN ANALYSIS"):
    auditor.increment_counter()
    with st.spinner("Analyzing architecture..."):
        code, ctype = auditor.fetch_contract_source(address)
        dist = auditor.analyze_token_distribution(address)
        
        risks = auditor.check_risky_functions(code or "")
        rug = auditor.detect_rugpull_risk(dist)
        
        # Alarm sistemi
        if rug == "High" or risks:
            st.error("🚨 CRITICAL SECURITY ALERT: HIGH RISK DETECTED!")
            if risks: st.write(f"⚠️ Risky functions found: {', '.join(risks)}")
            if rug == "High": st.write("⚠️ Rugpull Alert: High holder concentration.")
        else:
            st.success("✅ Secure Architecture Verified.")

        st.markdown(f"**Audit Mode:** {ctype}")