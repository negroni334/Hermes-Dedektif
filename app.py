import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes Detective", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.info("Founder: Baileys [NEGRONI]")
st.sidebar.metric("Total Secured Assets", f"{auditor.get_stats()}+")

st.title("🌐 Security Audit Engine")
address = st.text_input("Enter Base Contract Address:")

if st.button("RUN DEEP ANALYSIS"):
    auditor.increment_counter()
    with st.spinner("Deep scanning..."):
        code, ctype = auditor.fetch_contract_source(address)
        risks = auditor.check_risky_functions(code or "")
        
        # Risk Alarmı
        if risks: st.error(f"🚨 RISKY FUNCTIONS: {', '.join(risks)}")
        
        # AI Derin Analiz
        report = auditor.ai_deep_audit(code or "")
        st.markdown("### 🤖 AI Audit Report")
        st.write(report)