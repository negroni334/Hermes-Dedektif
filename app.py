import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes | Intelligence Terminal", layout="wide")
auditor = HermesAuditor()

st.sidebar.title("🕵️‍♂️ Hermes Intelligence")
st.sidebar.metric("Global Scans", f"{auditor.get_stats()}+")
st.sidebar.info("💡 Bu araç, herkese açık blokzincir verilerini analiz eder.")

address = st.text_input("Enter Target (Contract or Wallet):").strip()

if st.button("EXECUTE ANALYSIS"):
    if not address.startswith("0x"):
        st.error("❌ Geçersiz adres formatı! 0x ile başlamalı.")
    else:
        auditor.increment_counter()
        with st.spinner("Deep Scanning..."):
            
            # 1. BÖLÜM: HER ZAMAN BAKİYE GÖSTER (Cüzdan veya Kontrat fark etmez)
            st.subheader("💰 Varlık (Balance) Analizi")
            eth_bal, usd_val = auditor.fetch_wallet_balance(address)
            col1, col2 = st.columns(2)
            col1.metric("ETH Balance", f"{eth_bal:.6f} ETH")
            col2.metric("Portfolio Value (USD)", f"${usd_val:,.2f}")
            
            st.divider() # Araya şık bir çizgi atıyoruz
            
            # 2. BÖLÜM: GÜVENLİK SKORU (Sadece Kontratsa Çıkar)
            code, is_renounced = auditor.fetch_contract_details(address)
            
            if code == "IS_WALLET":
                st.info("ℹ️ Bu bir bireysel cüzdan (Wallet). Herhangi bir akıllı sözleşme kodu içermediği için güvenlik skoru aranmaz.")
            
            elif code == "UNVERIFIED_CONTRACT":
                st.warning("⚠️ Bu bir sözleşme adresi ancak kaynak kodu Basescan üzerinde doğrulanmamış (Unverified). Kod okunamadığı için risk skoru hesaplanamıyor.")
            
            else:
                score, risks = auditor.calculate_score(code)
                
                st.subheader("🛡️ Audit Score")
                st.progress(score / 100)
                st.metric("Security Score", f"100/{score}")
                
                if is_renounced:
                    st.success("✅ Owner Renounced: Sözleşme yetkileri iptal edilmiş (Güvenli).")
                else:
                    st.warning("⚠️ Owner Active: Sözleşme sahibi hala kontrol sahibi.")
                
                if risks:
                    st.error(f"🚨 Risks Detected: {', '.join(risks)}")
                else:
                    st.success("✅ Clean Code Architecture: No common malicious patterns found.")