import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes | Intelligence Terminal", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Intelligence")
st.sidebar.metric("Global Scans", f"{auditor.get_stats()}+")
st.sidebar.info("💡 Bu araç, herkese açık blokzincir verilerini analiz eder; varlık güvenliğini artırmaya odaklanır.")

address = st.text_input("Enter Target Address (Base Mainnet):").strip()

if st.button("EXECUTE ANALYSIS"):
    if not address.startswith("0x"):
        st.error("❌ Geçersiz adres formatı! 0x ile başlamalı.")
    else:
        auditor.increment_counter()
        with st.spinner("Analyzing On-Chain Data..."):
            code, status = auditor.fetch_contract_source(address)
            
            if code == "WALLET_OR_UNKNOWN":
                st.subheader("👤 Cüzdan Profil Analizi")
                eth_bal, usd_val = auditor.fetch_wallet_balance(address)
                col1, col2 = st.columns(2)
                col1.metric("ETH Balance", f"{eth_bal:.6f} ETH")
                col2.metric("Portfolio Value (USD)", f"${usd_val:,.2f}")
            elif code == "ERROR":
                st.error("❌ API Bağlantı Hatası.")
            else:
                risks = auditor.perform_audit(code)
                if risks:
                    st.error(f"🚨 RISKY PATTERNS FOUND: {', '.join(risks)}")
                else:
                    st.success("✅ Clean Architecture: No common malicious patterns found.")