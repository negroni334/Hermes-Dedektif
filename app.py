import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes Detective", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.info("Founder: Baileys [NEGRONI]")
st.sidebar.metric("Global Scans", f"{auditor.get_stats()}+")

address = st.text_input("Enter Base Contract Address:")

if st.button("RUN ANALYSIS"):
    if not address:
        st.warning("Lütfen geçerli bir adres gir.")
    else:
        auditor.increment_counter()
        with st.spinner("Analyzing architecture..."):
            code, status = auditor.fetch_contract_source(address)
            if code:
                risks = auditor.perform_audit(code)
                if risks:
                    st.error(f"🚨 RISKY FUNCTIONS: {', '.join(risks)}")
                else:
                    st.success("✅ Architecture Verified.")
            else:
                st.error("❌ Veri çekilemedi. API Anahtarını veya Adresi kontrol et.")