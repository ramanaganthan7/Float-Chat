import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Map | FloatChat", layout="wide")
st.title("🗺️ Float Locations Map")

# ── Resolve CSV path relative to this file ──────────────────────────────────
_DATA_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sample_argo.csv"
)

@st.cache_data
def load_data():
    return pd.read_csv(_DATA_CSV)

df = load_data()

# ── Sidebar filters ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔧 Filters")
    color_by = st.selectbox("Colour by", ["TEMP", "PSAL", "PRES"])
    platforms = st.multiselect(
        "Platform(s)",
        options=sorted(df["PLATFORM_NUMBER"].unique()),
        default=sorted(df["PLATFORM_NUMBER"].unique()),
    )

filtered = df[df["PLATFORM_NUMBER"].isin(platforms)] if platforms else df

fig = px.scatter_mapbox(
    filtered,
    lat="LATITUDE",
    lon="LONGITUDE",
    color=color_by,
    hover_data=["PLATFORM_NUMBER", "CYCLE_NUMBER", "TIME", "TEMP", "PSAL", "PRES"],
    zoom=2,
    height=600,
    mapbox_style="open-street-map",
    title=f"ARGO Float Locations — coloured by {color_by}",
    color_continuous_scale="Viridis",
)
fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})

st.plotly_chart(fig, use_container_width=True)

st.caption(f"Showing {len(filtered):,} records from {filtered['PLATFORM_NUMBER'].nunique()} float(s).")
