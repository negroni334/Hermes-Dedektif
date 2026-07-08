import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes Detective", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.info("Founder: Baileys [NEGRONI]")
st.sidebar.metric("Total Scans", f"{auditor.get_stats()}+")

address = st.text_input("Enter Base Contract Address:")

if st.button("RUN ANALYSIS"):
    auditor.increment_counter()
    with st.spinner("Analyzing architecture..."):
        code, _ = auditor.fetch_contract_source(address)
        results = auditor.perform_audit(code or "")
        
        st.subheader("📊 Security Audit Report")
        for category, items in results.items():
            if items:
                st.error(f"🚨 {category} Detected: {', '.join(items)}")
            else:
                st.success(f"✅ {category}: Clean")