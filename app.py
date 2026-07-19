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
            st.error("❌ CRITICAL: Contract address does not exist or has no public data on BaseScan.")
            st.info("💡 Not: Sadece 'Verified' kontratlar detaylı taramaya uygundur.")
        elif status == "ABI_ONLY":
            # ... (ABI kısmı)