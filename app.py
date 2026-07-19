import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes | Security Terminal", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.info("Founder: Baileys [NEGRONI]")
st.sidebar.metric("Global Scans", f"{auditor.get_stats()}+")

address = st.text_input("Target Contract Address (Base):")

if st.button("EXECUTE SCAN"):
    auditor.increment_counter()
    with st.spinner("Initializing deep scan..."):
        code, status = auditor.fetch_contract_source(address)
        
        if code == "NO_SOURCE":
            st.error("❌ CRITICAL: Contract address does not exist or has no public data on BaseScan.")
            st.info("💡 Not: Sadece 'Verified' kontratlar detaylı taramaya uygundur.")
        
        elif status == "ABI_ONLY":
            st.info("🔍 STATUS: Partially Verified (ABI available).")
            risks = auditor.perform_audit(code)
            if risks: 
                st.error(f"🚨 RISKY PATTERNS FOUND: {', '.join(risks)}")
            else: 
                st.success("✅ No suspicious patterns found in ABI.")
        
        else:
            risks = auditor.perform_audit(code)
            if risks:
                st.error(f"🚨 SECURITY THREATS IDENTIFIED: {', '.join(risks)}")
            else:
                st.success("✅ Clean Architecture - No common malicious patterns.")