import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes Detective", layout="wide")
auditor = HermesAuditor()

st.title("🕵️‍♂️ Hermes Security Detective")
address = st.text_input("Enter Base Contract Address:")

if st.button("Analyze Contract"):
    with st.spinner("Analyzing..."):
        code, code_type = auditor.fetch_contract_source(address)
        distribution = auditor.analyze_token_distribution(address)
        
        # Risk Alarm Sistemi
        risks = auditor.check_risky_functions(code or "")
        rug_risk = auditor.detect_rugpull_risk(distribution)
        
        if rug_risk == "High" or len(risks) > 0:
            st.error("🚨 CRITICAL SECURITY ALERT: HIGH RISK DETECTED!")
            if risks: st.write(f"⚠️ Risky functions: {', '.join(risks)}")
            if rug_risk == "High": st.write("⚠️ Rugpull Alert: High holder concentration.")
        else:
            st.success("✅ No major risks detected.")

        report = auditor.ai_deep_audit(code or "", code_type, distribution)
        st.markdown(report)