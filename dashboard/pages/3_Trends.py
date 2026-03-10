import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Trends | FloatChat", layout="wide")
st.title("📈 Parameter Trends")

# ── Resolve CSV path relative to this file ──────────────────────────────────
_DATA_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sample_argo.csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(_DATA_CSV, parse_dates=["TIME"])
    return df.sort_values("TIME")

df = load_data()

# ── Sidebar controls ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔧 Controls")
    param = st.selectbox("Parameter", ["TEMP", "PSAL", "PRES"])
    platforms = st.multiselect(
        "Platform(s)",
        options=sorted(df["PLATFORM_NUMBER"].unique()),
        default=sorted(df["PLATFORM_NUMBER"].unique()),
    )

filtered = df[df["PLATFORM_NUMBER"].isin(platforms)] if platforms else df

# ── Main trend chart ─────────────────────────────────────────────────────────
fig = px.line(
    filtered,
    x="TIME",
    y=param,
    color="PLATFORM_NUMBER",
    title=f"{param} over Time",
    markers=True,
    labels={"TIME": "Date/Time", param: param, "PLATFORM_NUMBER": "Float"},
)
fig.update_layout(height=480)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Depth profile: PRES vs selected param ───────────────────────────────────
st.subheader(f"Depth Profile: Pressure vs {param}")
fig2 = px.scatter(
    filtered,
    x=param,
    y="PRES",
    color="PLATFORM_NUMBER",
    title=f"{param} vs Pressure (depth)",
    labels={"PRES": "Pressure (dbar)", param: param, "PLATFORM_NUMBER": "Float"},
)
fig2.update_yaxes(autorange="reversed")  # deeper = lower on plot
fig2.update_layout(height=420)
st.plotly_chart(fig2, use_container_width=True)
