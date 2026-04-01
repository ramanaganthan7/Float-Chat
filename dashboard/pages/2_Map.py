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

st.set_page_config(page_title="Map | AlgoFloat", page_icon="", layout="wide")
inject_theme()
sidebar_brand()

_DATA_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sample_argo.csv"
)

@st.cache_data
def load_data():
    return pd.read_csv(_DATA_CSV)

df = load_data()

page_header(
    icon_svg="""<svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.8">
      <circle cx="12" cy="12" r="9.5"/>
      <path stroke-linecap="round" d="M2.5 12 Q7 8.5 12 12 Q17 15.5 21.5 12"/>
      <path stroke-linecap="round" d="M12 2.5v19" opacity="0.35"/>
    </svg>""",
    title="Float Locations Map",
    subtitle="Interactive global map of ARGO profiling float positions. Filter by platform and colour by ocean parameter.",
)

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="
    font-size:0.68rem;font-weight:700;color:#8FACC8;
    text-transform:uppercase;letter-spacing:0.12em;
    padding:0.75rem 0 0.5rem;
    border-top:1px solid #1A3355;margin-top:0.5rem;
">Map Configuration</div>
""", unsafe_allow_html=True)

    color_by = st.selectbox(
        "Colour parameter",
        ["TEMP", "PSAL", "PRES"],
        format_func=lambda x: {"TEMP": "Temperature (°C)", "PSAL": "Salinity (PSU)", "PRES": "Pressure (dbar)"}[x],
    )

    map_style = st.selectbox(
        "Map style",
        ["carto-darkmatter", "open-street-map", "carto-positron"],
        format_func=lambda x: {
            "carto-darkmatter": "Dark Ocean",
            "open-street-map": "Street Map",
            "carto-positron": "Light Clean",
        }[x],
    )

    color_scale = st.selectbox(
        "Color scale",
        ["Viridis", "Plasma", "Turbo", "Blues", "Cividis"],
    )

    st.markdown("""
<div style="font-size:0.68rem;font-weight:700;color:#8FACC8;
    text-transform:uppercase;letter-spacing:0.12em;
    padding:0.75rem 0 0.5rem;border-top:1px solid #1A3355;margin-top:0.5rem;">
Platform Filter</div>
""", unsafe_allow_html=True)

    all_platforms = sorted(df["PLATFORM_NUMBER"].unique())
    select_all = st.checkbox("Select all platforms", value=True)
    if select_all:
        platforms = all_platforms
    else:
        platforms = st.multiselect(
            "Platform(s)",
            options=all_platforms,
            default=all_platforms[:3] if len(all_platforms) >= 3 else all_platforms,
        )

filtered = df[df["PLATFORM_NUMBER"].isin(platforms)] if platforms else df

# ── Map stats strip ───────────────────────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4)
_label_style = "font-size:0.68rem;color:#8FACC8;text-transform:uppercase;letter-spacing:0.08em;"
_val_style = "font-size:1.35rem;font-weight:700;color:#00D4FF;"

s1.markdown(f"""
<div style="background:linear-gradient(135deg,#0A1628,#0D2240);border:1px solid #1A3355;
    border-radius:10px;padding:0.85rem 1rem;text-align:center;">
  <div style="{_label_style}">Visible Records</div>
  <div style="{_val_style}">{len(filtered):,}</div>
</div>""", unsafe_allow_html=True)

s2.markdown(f"""
<div style="background:linear-gradient(135deg,#0A1628,#0D2240);border:1px solid #1A3355;
    border-radius:10px;padding:0.85rem 1rem;text-align:center;">
  <div style="{_label_style}">Active Floats</div>
  <div style="{_val_style}">{filtered['PLATFORM_NUMBER'].nunique():,}</div>
</div>""", unsafe_allow_html=True)

s3.markdown(f"""
<div style="background:linear-gradient(135deg,#0A1628,#0D2240);border:1px solid #1A3355;
    border-radius:10px;padding:0.85rem 1rem;text-align:center;">
  <div style="{_label_style}">Avg {color_by}</div>
  <div style="{_val_style}">{filtered[color_by].mean():.2f}</div>
</div>""", unsafe_allow_html=True)

s4.markdown(f"""
<div style="background:linear-gradient(135deg,#0A1628,#0D2240);border:1px solid #1A3355;
    border-radius:10px;padding:0.85rem 1rem;text-align:center;">
  <div style="{_label_style}">{color_by} Range</div>
  <div style="{_val_style}">{filtered[color_by].min():.1f} – {filtered[color_by].max():.1f}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

# ── Main map ──────────────────────────────────────────────────────────────────
_param_labels = {"TEMP": "Temp (°C)", "PSAL": "Salinity", "PRES": "Pressure (dbar)"}

fig = px.scatter_mapbox(
    filtered,
    lat="LATITUDE",
    lon="LONGITUDE",
    color=color_by,
    size_max=8,
    hover_name="PLATFORM_NUMBER",
    hover_data={
        "CYCLE_NUMBER": True,
        "TIME": True,
        "TEMP": ":.2f",
        "PSAL": ":.3f",
        "PRES": ":.1f",
        "LATITUDE": ":.4f",
        "LONGITUDE": ":.4f",
    },
    zoom=1.5,
    height=580,
    mapbox_style=map_style,
    color_continuous_scale=color_scale,
    labels={color_by: _param_labels.get(color_by, color_by)},
)
fig.update_layout(
    paper_bgcolor=SURFACE,
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    coloraxis_colorbar=dict(
        title=dict(text=_param_labels.get(color_by, color_by), font=dict(color=TX2, size=11)),
        tickfont=dict(color=TX2, size=10),
        outlinecolor=BORDER,
        thickness=14,
        bgcolor="rgba(10,22,40,0.85)",
        len=0.7,
    ),
    hoverlabel=dict(
        bgcolor=SURFACE2,
        bordercolor="#0094C6",
        font=dict(color="#E8F4FD", family="Inter, sans-serif", size=12),
    ),
)
fig.update_traces(marker=dict(opacity=0.82, sizemin=4))

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Geographic distribution ───────────────────────────────────────────────────
section_header("Geographic Distribution", icon_svg="""<svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="#8FACC8" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
  <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
</svg>""")

col_lat, col_lon = st.columns(2)

with col_lat:
    fig_lat = px.histogram(
        filtered, x="LATITUDE", nbins=40,
        title="Latitude Distribution",
        color_discrete_sequence=[CHART_COLORS[0]],
    )
    fig_lat.update_traces(marker_line_width=0, opacity=0.85)
    apply_chart_theme(fig_lat, height=280)
    fig_lat.update_layout(showlegend=False, xaxis_title="Latitude (°)", yaxis_title="Count")
    st.plotly_chart(fig_lat, use_container_width=True)

with col_lon:
    fig_lon = px.histogram(
        filtered, x="LONGITUDE", nbins=40,
        title="Longitude Distribution",
        color_discrete_sequence=[CHART_COLORS[2]],
    )
    fig_lon.update_traces(marker_line_width=0, opacity=0.85)
    apply_chart_theme(fig_lon, height=280)
    fig_lon.update_layout(showlegend=False, xaxis_title="Longitude (°)", yaxis_title="Count")
    st.plotly_chart(fig_lon, use_container_width=True)

st.caption(
    f"Displaying {len(filtered):,} observations from "
    f"{filtered['PLATFORM_NUMBER'].nunique()} float(s). "
    f"Lat range: {filtered['LATITUDE'].min():.2f}° to {filtered['LATITUDE'].max():.2f}°  |  "
    f"Lon range: {filtered['LONGITUDE'].min():.2f}° to {filtered['LONGITUDE'].max():.2f}°"
)
