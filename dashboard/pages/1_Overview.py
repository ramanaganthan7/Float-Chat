import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

_DASH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _DASH not in sys.path:
    sys.path.insert(0, _DASH)

from utils.theme import (
    inject_theme, sidebar_brand, page_header, section_header,
    apply_chart_theme, CHART_COLORS, SURFACE, SURFACE2, BORDER, TX2, A3,
)

st.set_page_config(page_title="Overview | AlgoFloat", page_icon="", layout="wide")
inject_theme()
sidebar_brand()

_DATA_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sample_argo.csv"
)

@st.cache_data
def load_data():
    return pd.read_csv(_DATA_CSV)

df = load_data()

# ── Page header ───────────────────────────────────────────────────────────────
page_header(
    icon_svg="""<svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.8">
      <rect x="3" y="3" width="7" height="7" rx="1.5"/>
      <rect x="14" y="3" width="7" height="7" rx="1.5"/>
      <rect x="3" y="14" width="7" height="7" rx="1.5"/>
      <rect x="14" y="14" width="7" height="7" rx="1.5"/>
    </svg>""",
    title="Dataset Overview",
    subtitle="Summary statistics, KPI metrics, and parameter distributions across the ARGO dataset.",
)

# ── KPI Metrics ───────────────────────────────────────────────────────────────
section_header("Key Metrics", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
</svg>""")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Records",   f"{len(df):,}")
c2.metric("Unique Floats",   f"{df['PLATFORM_NUMBER'].nunique():,}")
c3.metric("Avg Temp (°C)",   f"{df['TEMP'].mean():.2f}")
c4.metric("Avg Salinity",    f"{df['PSAL'].mean():.2f}")

st.divider()

# ── Dataset snapshot ──────────────────────────────────────────────────────────
section_header("Dataset Snapshot", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M3 14h18M10 3v18M14 3v18"/>
</svg>""")

st.dataframe(
    df.head(20).style.background_gradient(
        cmap="Blues", subset=["TEMP", "PSAL", "PRES"]
    ),
    use_container_width=True,
    height=340,
)

st.divider()

# ── Statistics ────────────────────────────────────────────────────────────────
section_header("Descriptive Statistics", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4v16"/>
</svg>""")

numeric_cols = ["TEMP", "PSAL", "PRES"]
stats_df = df[numeric_cols].describe().round(4)
st.dataframe(stats_df, use_container_width=True)

st.divider()

# ── Distribution Charts ───────────────────────────────────────────────────────
section_header("Parameter Distributions", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"/>
  <path stroke-linecap="round" stroke-linejoin="round" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"/>
</svg>""")

col1, col2, col3 = st.columns(3)

with col1:
    fig = px.histogram(
        df, x="TEMP", nbins=45,
        title="Temperature (°C)",
        color_discrete_sequence=[CHART_COLORS[0]],
    )
    fig.update_traces(marker_line_width=0, opacity=0.85)
    apply_chart_theme(fig, height=340)
    fig.update_layout(
        showlegend=False,
        xaxis_title="Temperature (°C)",
        yaxis_title="Count",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(
        df, x="PSAL", nbins=45,
        title="Salinity (PSU)",
        color_discrete_sequence=[CHART_COLORS[1]],
    )
    fig.update_traces(marker_line_width=0, opacity=0.85)
    apply_chart_theme(fig, height=340)
    fig.update_layout(
        showlegend=False,
        xaxis_title="Salinity (PSU)",
        yaxis_title="Count",
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = px.histogram(
        df, x="PRES", nbins=45,
        title="Pressure (dbar)",
        color_discrete_sequence=[CHART_COLORS[2]],
    )
    fig.update_traces(marker_line_width=0, opacity=0.85)
    apply_chart_theme(fig, height=340)
    fig.update_layout(
        showlegend=False,
        xaxis_title="Pressure (dbar)",
        yaxis_title="Count",
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Correlation matrix ────────────────────────────────────────────────────────
section_header("Parameter Correlation Matrix", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm0 8a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zm12 0a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"/>
</svg>""")

col_left, col_right = st.columns([1, 1])

with col_left:
    corr = df[numeric_cols].corr().round(3)
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.columns.tolist(),
        colorscale=[
            [0.0, "#020B18"], [0.3, "#0A1628"],
            [0.5, "#0094C6"], [0.75, "#00C6B8"],
            [1.0, "#00D4FF"],
        ],
        text=corr.values.round(3),
        texttemplate="%{text}",
        textfont={"size": 14, "color": "#E8F4FD"},
        showscale=True,
        zmin=-1, zmax=1,
        colorbar=dict(
            tickfont=dict(color=TX2),
            outlinecolor=BORDER,
            thickness=14,
        ),
    ))
    apply_chart_theme(fig_corr, height=340)
    fig_corr.update_layout(title="TEMP / PSAL / PRES Correlation")
    st.plotly_chart(fig_corr, use_container_width=True)

with col_right:
    fig_scatter = px.scatter(
        df.sample(min(2000, len(df)), random_state=42),
        x="TEMP", y="PSAL",
        color="PRES",
        title="Temperature vs Salinity (coloured by Pressure)",
        labels={"TEMP": "Temperature (°C)", "PSAL": "Salinity (PSU)", "PRES": "Pressure (dbar)"},
        color_continuous_scale="Blues",
        opacity=0.65,
    )
    apply_chart_theme(fig_scatter, height=340)
    fig_scatter.update_coloraxes(
        colorbar=dict(tickfont=dict(color=TX2), outlinecolor=BORDER, thickness=14)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ── Per-platform summary ──────────────────────────────────────────────────────
section_header("Per-Float Summary", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0"/>
</svg>""")

platform_summary = (
    df.groupby("PLATFORM_NUMBER")
    .agg(
        Cycles=("CYCLE_NUMBER", "nunique"),
        Records=("N_POINTS", "count"),
        Avg_Temp=("TEMP", "mean"),
        Avg_Sal=("PSAL", "mean"),
        Avg_Pres=("PRES", "mean"),
        Min_Lat=("LATITUDE", "min"),
        Max_Lat=("LATITUDE", "max"),
    )
    .round(3)
    .reset_index()
)

fig_bar = px.bar(
    platform_summary,
    x=platform_summary["PLATFORM_NUMBER"].astype(str),
    y="Records",
    color="Avg_Temp",
    title="Records per Float (coloured by Avg Temp)",
    labels={"x": "Platform", "Records": "Record Count", "Avg_Temp": "Avg Temp (°C)"},
    color_continuous_scale=[[0, "#0A1628"], [0.5, "#0094C6"], [1, "#00D4FF"]],
)
apply_chart_theme(fig_bar, height=320)
fig_bar.update_coloraxes(
    colorbar=dict(tickfont=dict(color=TX2), outlinecolor=BORDER, thickness=14)
)
st.plotly_chart(fig_bar, use_container_width=True)

st.dataframe(platform_summary, use_container_width=True)

st.caption(f"Dataset: {len(df):,} records · {df['PLATFORM_NUMBER'].nunique()} floats · Source: ARGO Global Float Array")
