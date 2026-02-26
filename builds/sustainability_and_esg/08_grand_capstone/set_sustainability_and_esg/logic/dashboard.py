import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Sustainability & ESG Master Dashboard", layout="wide")

st.title("🚀 Sustainability & ESG | AI Control Tower")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("📊 Data Health")
    if os.path.exists("../../01_data_pipeline_automation/set_sustainability_and_esg/data/corporate_expenses.csv"):
        df = pd.read_csv("../../01_data_pipeline_automation/set_sustainability_and_esg/data/corporate_expenses.csv")
        st.write(f"Total Transactions: {len(df)}")
        st.dataframe(df.head())
    else:
        st.warning("Data Pipeline execution required to see live stats.")

with col2:
    st.header("🛡️ Security Status")
    if os.path.exists("../../07_sovereign_security/set_sustainability_and_esg/data/scrubbed_data.csv"):
        st.success("PII Shield ACTIVE")
    else:
        st.error("PII Shield INACTIVE")

st.markdown("---")
st.info("This dashboard aggregates insights from all 8 sessions of the Sustainability & ESG AI Bootcamp.")