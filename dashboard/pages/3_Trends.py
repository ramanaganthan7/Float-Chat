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
    apply_chart_theme, CHART_COLORS, SURFACE, SURFACE2, BORDER, TX, TX2, A3,
)

st.set_page_config(page_title="Trends | AlgoFloat", page_icon="", layout="wide")
inject_theme()
sidebar_brand()

_DATA_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sample_argo.csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(_DATA_CSV, parse_dates=["TIME"])
    return df.sort_values("TIME")

df = load_data()

page_header(
    icon_svg="""<svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.8">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
    </svg>""",
    title="Parameter Trends",
    subtitle="Time-series analysis, depth profiles, and cross-parameter correlations.",
)

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="
    font-size:0.68rem;font-weight:700;color:#8FACC8;
    text-transform:uppercase;letter-spacing:0.12em;
    padding:0.75rem 0 0.5rem;
    border-top:1px solid #1A3355;margin-top:0.5rem;
">Chart Controls</div>
""", unsafe_allow_html=True)

    param = st.selectbox(
        "Primary parameter",
        ["TEMP", "PSAL", "PRES"],
        format_func=lambda x: {"TEMP": "Temperature (°C)", "PSAL": "Salinity (PSU)", "PRES": "Pressure (dbar)"}[x],
    )

    all_platforms = sorted(df["PLATFORM_NUMBER"].unique())
    select_all = st.checkbox("All platforms", value=True)
    if select_all:
        platforms = all_platforms
    else:
        platforms = st.multiselect(
            "Platform(s)",
            options=all_platforms,
            default=all_platforms,
        )

    show_markers = st.checkbox("Show data points", value=False)

filtered = df[df["PLATFORM_NUMBER"].isin(platforms)] if platforms else df
_plabel = {"TEMP": "Temperature (°C)", "PSAL": "Salinity (PSU)", "PRES": "Pressure (dbar)"}

# ── Summary stats row ─────────────────────────────────────────────────────────
_label_style = "font-size:0.68rem;color:#8FACC8;text-transform:uppercase;letter-spacing:0.08em;"

c1, c2, c3, c4 = st.columns(4)
for col, lbl, val in [
    (c1, f"Min {param}", f"{filtered[param].min():.2f}"),
    (c2, f"Max {param}", f"{filtered[param].max():.2f}"),
    (c3, f"Mean {param}", f"{filtered[param].mean():.2f}"),
    (c4, f"Std Dev",      f"{filtered[param].std():.3f}"),
]:
    col.markdown(f"""
<div style="background:linear-gradient(135deg,#0A1628,#0D2240);border:1px solid #1A3355;
    border-radius:10px;padding:0.85rem 1rem;text-align:center;
    animation:fadeUp 0.4s ease both;">
  <div style="{_label_style}">{lbl}</div>
  <div style="font-size:1.35rem;font-weight:700;color:#00D4FF;">{val}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

# ── Time series ───────────────────────────────────────────────────────────────
section_header("Time Series", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
</svg>""")

fig_ts = px.line(
    filtered,
    x="TIME",
    y=param,
    color="PLATFORM_NUMBER",
    markers=show_markers,
    labels={"TIME": "Date / Time", param: _plabel[param], "PLATFORM_NUMBER": "Float"},
    color_discrete_sequence=CHART_COLORS,
)
apply_chart_theme(fig_ts, height=400)
fig_ts.update_layout(
    title=f"{_plabel[param]} over Time",
    xaxis_title="Date / Time",
    yaxis_title=_plabel[param],
    legend_title="Float ID",
)
st.plotly_chart(fig_ts, use_container_width=True)

st.divider()

# ── Depth profile + Box plot ──────────────────────────────────────────────────
col_depth, col_box = st.columns(2)

with col_depth:
    section_header("Depth Profile", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
    </svg>""")
    sample = filtered.sample(min(3000, len(filtered)), random_state=42)
    fig_depth = px.scatter(
        sample,
        x=param,
        y="PRES",
        color="PLATFORM_NUMBER",
        labels={"PRES": "Pressure (dbar)", param: _plabel[param], "PLATFORM_NUMBER": "Float"},
        opacity=0.65,
        color_discrete_sequence=CHART_COLORS,
    )
    fig_depth.update_yaxes(autorange="reversed")
    apply_chart_theme(fig_depth, height=400)
    fig_depth.update_layout(
        title=f"{_plabel[param]} vs Depth",
        xaxis_title=_plabel[param],
        yaxis_title="Pressure / Depth (dbar)",
        legend_title="Float ID",
    )
    st.plotly_chart(fig_depth, use_container_width=True)

with col_box:
    section_header("Distribution by Float", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
      <rect x="3" y="3" width="18" height="18" rx="2"/>
      <path stroke-linecap="round" d="M9 3v18M15 3v18M3 9h18M3 15h18"/>
    </svg>""")
    fig_box = px.box(
        filtered,
        x=filtered["PLATFORM_NUMBER"].astype(str),
        y=param,
        color=filtered["PLATFORM_NUMBER"].astype(str),
        labels={"x": "Platform", param: _plabel[param], "color": "Float"},
        color_discrete_sequence=CHART_COLORS,
    )
    apply_chart_theme(fig_box, height=400)
    fig_box.update_layout(
        title=f"{_plabel[param]} Distribution per Float",
        xaxis_title="Platform",
        yaxis_title=_plabel[param],
        showlegend=False,
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# ── T-S Diagram (oceanographic standard) ─────────────────────────────────────
section_header("T-S Diagram", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <circle cx="12" cy="12" r="4"/>
  <path stroke-linecap="round" d="M3 12h4m10 0h4M12 3v4m0 10v4"/>
</svg>""")

ts_sample = filtered.sample(min(4000, len(filtered)), random_state=7)
fig_ts_diag = px.scatter(
    ts_sample,
    x="PSAL",
    y="TEMP",
    color="PRES",
    color_continuous_scale=[[0, "#020B18"], [0.4, "#0094C6"], [0.75, "#00C6B8"], [1, "#00D4FF"]],
    labels={"PSAL": "Salinity (PSU)", "TEMP": "Temperature (°C)", "PRES": "Pressure (dbar)"},
    opacity=0.72,
)
apply_chart_theme(fig_ts_diag, height=380)
fig_ts_diag.update_layout(
    title="T-S Diagram: Temperature vs Salinity (coloured by Pressure/Depth)",
    xaxis_title="Salinity (PSU)",
    yaxis_title="Temperature (°C)",
)
fig_ts_diag.update_coloraxes(
    colorbar=dict(
        title=dict(text="Pressure (dbar)", font=dict(color=TX2, size=11)),
        tickfont=dict(color=TX2, size=10),
        outlinecolor=BORDER,
        thickness=14,
    )
)
st.plotly_chart(fig_ts_diag, use_container_width=True)

st.divider()

# ── Rolling mean overlay ──────────────────────────────────────────────────────
section_header("Rolling Mean Analysis", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
</svg>""")

if len(filtered) > 10:
    agg = filtered.groupby("TIME")[param].mean().reset_index()
    agg["rolling_mean"] = agg[param].rolling(window=min(10, max(3, len(agg) // 10)), min_periods=1).mean()

    fig_roll = go.Figure()
    fig_roll.add_trace(go.Scatter(
        x=agg["TIME"], y=agg[param],
        mode="lines", name="Raw mean",
        line=dict(color="#1A3355", width=1.5),
        opacity=0.7,
    ))
    fig_roll.add_trace(go.Scatter(
        x=agg["TIME"], y=agg["rolling_mean"],
        mode="lines", name="Rolling mean",
        line=dict(color=A3, width=2.5),
    ))
    apply_chart_theme(fig_roll, height=320)
    fig_roll.update_layout(
        title=f"Daily Mean {_plabel[param]} with Rolling Smooth",
        xaxis_title="Date / Time",
        yaxis_title=f"Mean {_plabel[param]}",
        legend_title="",
    )
    st.plotly_chart(fig_roll, use_container_width=True)
else:
    st.info("Not enough data points to render a rolling mean chart with current filters.")

st.caption(
    f"Showing {len(filtered):,} records from {filtered['PLATFORM_NUMBER'].nunique()} float(s). "
    f"Time range: {filtered['TIME'].min().date()} to {filtered['TIME'].max().date()}"
)
