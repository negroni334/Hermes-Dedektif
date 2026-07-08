import streamlit as st
from main import HermesAuditor

st.set_page_config(page_title="Hermes Enterprise", layout="wide")
st.markdown("<style>.stApp {background-color: #050505; color: white;}</style>", unsafe_allow_html=True)

auditor = HermesAuditor()

st.title("HERMES | Enterprise Security")
st.sidebar.metric("Total Secured Assets", f"{auditor.get_stats()}+")
st.sidebar.info("Founder: Baileys [NEGRONI]")

address = st.text_input("Enter Contract Address:")

if st.button("INITIALIZE DEEP SCAN"):
    auditor.increment_counter()
    with st.spinner("Analyzing..."):
        data = auditor.run_analysis(address)
        
        c1, c2 = st.columns(2)
        c1.metric("Security Score", f"{data['score']}/100")
        c2.metric("Risk Status", "CRITICAL" if data['risks'] else "SECURE")
        
        if data['risks']:
            st.error(f"🚨 RISKY FUNCTIONS FOUND: {', '.join(data['risks'])}")
        st.success("Analysis Complete.")