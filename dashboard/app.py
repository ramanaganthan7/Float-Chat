import streamlit as st

st.set_page_config(
    page_title="FloatChat — Ocean Dashboard",
    page_icon="",
    layout="wide",
)

st.title("🌊 FloatChat: AI-Powered ARGO Ocean Data Explorer")
st.markdown(
    """
    Welcome to **FloatChat** — an interactive dashboard built on top of real
    [ARGO float](https://argo.ucsd.edu/) ocean observations.

    Use the **sidebar** to navigate between pages:
    """
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("📊 **Overview**\nDataset summary, statistics & distributions.")
with col2:
    st.info("🗺️ **Map**\nInteractive global map of float locations.")
with col3:
    st.info("📈 **Trends**\nTime-series & depth profiles for key parameters.")
with col4:
    st.info("💬 **Chatbot**\nAsk questions in plain English — AI writes the SQL.")

st.divider()
st.caption("Data source: ARGO Global Float Array | Powered by Gemini AI + LangGraph + SQLite")
