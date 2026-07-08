import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes Detective", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.info("Founder: Baileys [NEGRONI]")
st.sidebar.metric("Total Secured Assets", f"{auditor.get_stats()}+")

st.title("🌐 Security Audit Engine")
address = st.text_input("Enter Base Contract Address:")

if st.button("RUN ANALYSIS"):
    auditor.increment_counter()
    with st.spinner("Analyzing..."):
        code, ctype = auditor.fetch_contract_source(address)
        risks = auditor.check_risky_functions(code or "")
        
        if risks:
            st.error(f"🚨 CRITICAL: RISKY FUNCTIONS DETECTED: {', '.join(risks)}")
        else:
            st.success("✅ Architecture Verified.")