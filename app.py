import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes | Security Terminal", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.metric("Global Scans", f"{auditor.get_stats()}+")

address = st.text_input("Enter Target Address (Base):").strip()

if st.button("EXECUTE SCAN"):
    if not address.startswith("0x"):
        st.error("❌ Geçersiz adres formatı! 0x ile başlamalı.")
    else:
        auditor.increment_counter()
        with st.spinner("Analyzing..."):
            code, status = auditor.fetch_contract_source(address)
            
            if code == "WALLET_OR_UNKNOWN":
                st.info("👤 Cüzdan Tespiti: Bu adres bir akıllı sözleşme değil, cüzdan (EOA).")
                balance = auditor.fetch_wallet_balance(address)
                st.metric("Cüzdan Bakiyesi", f"{balance:.8f} ETH")
                if balance == 0:
                    st.warning("⚠️ Bakiye 0 görünüyor. API Key'in çalışıp çalışmadığını kontrol et.")
            elif code == "ERROR":
                st.error("❌ API Bağlantı Hatası.")
            else:
                risks = auditor.perform_audit(code)
                if risks:
                    st.error(f"🚨 RISKY PATTERNS FOUND: {', '.join(risks)}")
                else:
                    st.success("✅ Clean Architecture: No common malicious patterns found.")