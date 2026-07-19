import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes Detective", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.info("Founder: Baileys [NEGRONI]")
st.sidebar.metric("Global Scans", f"{auditor.get_stats()}+")

address = st.text_input("Enter Base Contract Address:")

if st.button("EXECUTE SCAN"):
    auditor.increment_counter()
    with st.spinner("Initializing deep scan..."):
        code, status = auditor.fetch_contract_source(address)
        
        # EĞER HİÇBİR ŞEY BULAMAZSA
        if code == "NO_SOURCE":
            st.warning("⚠️ CONTRACT STATUS: Unverified. Source code and ABI unavailable.")
        elif status == "ABI_ONLY":
            st.info("🔍 STATUS: Partially Verified (ABI available).")
            # ABI içinde riskli fonksiyon isimlerini ara
            risks = auditor.perform_audit(code)
            if risks: st.error(f"🚨 RISKY PATTERNS FOUND: {', '.join(risks)}")
            else: st.success("✅ No suspicious patterns found in ABI.")
        else:
            risks = auditor.perform_audit(code)
            # ... (diğer kodun aynı)