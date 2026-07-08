import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes Detective", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.info("Founder: Baileys [NEGRONI]")
st.sidebar.metric("Global Scans", f"{auditor.get_stats()}+")

address = st.text_input("Enter Base Contract Address:")

if st.button("RUN ANALYSIS"):
    auditor.increment_counter()
    with st.spinner("Analyzing..."):
        code, status = auditor.fetch_contract_source(address)
        if code is not None:
            risks = auditor.perform_audit(code)
            if risks:
                st.error(f"🚨 RISKY FUNCTIONS: {', '.join(risks)}")
            else:
                st.success("✅ Architecture Verified.")
        else:
            st.error(f"❌ Veri çekilemedi: {status}")
            st.info("İpucu: Adresin Base ağında olduğundan emin ol ve 0x ile başladığını kontrol et.")