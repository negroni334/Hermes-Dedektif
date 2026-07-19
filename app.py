import streamlit as st
from main import HermesAuditor

# Sayfa ayarları
st.set_page_config(page_title="Hermes | Security Terminal", layout="wide")
auditor = HermesAuditor()

# Sidebar
st.sidebar.title("🕵️‍♂️ Hermes Detective")
st.sidebar.info("Founder: Baileys [NEGRONI]")
st.sidebar.metric("Global Scans", f"{auditor.get_stats()}+")

address = st.text_input("Enter Target Address (Base):")

if st.button("EXECUTE SCAN"):
    if not address.startswith("0x"):
        st.error("❌ Geçersiz adres formatı! 0x ile başlamalı.")
    else:
        auditor.increment_counter()
        with st.spinner("Analyzing address..."):
            code, status = auditor.fetch_contract_source(address)
            
            # Sonuç değerlendirme
            if code == "WALLET_OR_UNKNOWN":
                st.info("👤 Cüzdan Adresi: Bu adres bir akıllı sözleşme değil, cüzdan (EOA). Tarama yapılamaz.")
            elif code == "NO_SOURCE":
                st.warning("⚠️ Sözleşme doğrulanmamış (Unverified). Kaynak kodu herkese açık değil.")
            elif code == "ERROR":
                st.error("❌ API Bağlantı Hatası: Lütfen tekrar deneyin.")
            else:
                risks = auditor.perform_audit(code)
                if risks:
                    st.error(f"🚨 RISKY FUNCTIONS DETECTED: {', '.join(risks)}")
                else:
                    st.success("✅ Clean Architecture: No common malicious patterns found.")