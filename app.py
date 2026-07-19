import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes | Security Audit", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Security")
address = st.text_input("Enter Target (Contract or Wallet):").strip()

if st.button("RUN FULL AUDIT"):
    auditor.increment_counter()
    if address.startswith("0x"):
        with st.spinner("Deep Scanning..."):
            code, is_renounced = auditor.fetch_contract_details(address)
            
            if code is None:
                st.info("👤 Cüzdan Tespiti: Bakiye analizi yapılıyor...")
                eth, usd = auditor.fetch_wallet_balance(address)
                st.metric("Balance", f"{eth:.6f} ETH", f"${usd:,.2f}")
            else:
                score, risks = auditor.calculate_score(code)
                st.subheader("🛡️ Audit Score")
                st.progress(score / 100)
                st.metric("Security Score", f"{score}/100")
                
                if is_renounced:
                    st.success("✅ Owner Renounced: Sözleşme yetkileri iptal edilmiş (Güvenli).")
                else:
                    st.warning("⚠️ Owner Active: Sözleşme sahibi hala kontrol sahibi.")
                
                if risks:
                    st.error(f"🚨 Risks Detected: {', '.join(risks)}")
                else:
                    st.success("✅ Clean Code Architecture.")