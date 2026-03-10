import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Overview | FloatChat", layout="wide")
st.title("📊 Dataset Overview")

# ── Resolve CSV path relative to this file ──────────────────────────────────
_DATA_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sample_argo.csv"
)

@st.cache_data
def load_data():
    return pd.read_csv(_DATA_CSV)

df = load_data()

# ── KPI metrics row ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", f"{len(df):,}")
col2.metric("Floats", df["PLATFORM_NUMBER"].nunique())
col3.metric("Avg Temp (°C)", f"{df['TEMP'].mean():.2f}")
col4.metric("Avg Salinity", f"{df['PSAL'].mean():.2f}")

st.divider()

# ── Dataset snapshot ────────────────────────────────────────────────────────
st.subheader("Dataset Snapshot")
st.dataframe(df.head(20), use_container_width=True)

st.divider()

# ── Statistics ──────────────────────────────────────────────────────────────
st.subheader("Basic Statistics")
numeric_cols = ["TEMP", "PSAL", "PRES"]
st.dataframe(df[numeric_cols].describe(), use_container_width=True)

st.divider()

# ── Distribution charts ─────────────────────────────────────────────────────
st.subheader("Parameter Distributions")
chart_col1, chart_col2, chart_col3 = st.columns(3)
with chart_col1:
    fig = px.histogram(df, x="TEMP", nbins=40, title="Temperature Distribution",
                       color_discrete_sequence=["#0077B6"])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with chart_col2:
    fig = px.histogram(df, x="PSAL", nbins=40, title="Salinity Distribution",
                       color_discrete_sequence=["#00B4D8"])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with chart_col3:
    fig = px.histogram(df, x="PRES", nbins=40, title="Pressure Distribution",
                       color_discrete_sequence=["#90E0EF"])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
