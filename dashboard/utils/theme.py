"""
theme.py — Shared production UI theme for AlgoFloat dashboard.
Provides: CSS injection, Plotly dark-ocean template, and HTML component helpers.
"""

import streamlit as st
import plotly.graph_objects as go

# ─── Design tokens ────────────────────────────────────────────────────────────
BG       = "#020B18"
SURFACE  = "#0A1628"
SURFACE2 = "#0D2240"
A1       = "#0094C6"   # ocean blue
A2       = "#00C6B8"   # teal
A3       = "#00D4FF"   # cyan
TX       = "#E8F4FD"   # text primary
TX2      = "#8FACC8"   # text secondary
BORDER   = "#1A3355"
OK       = "#00C896"
WARN     = "#FFB347"
ERR      = "#FF6B6B"

CHART_COLORS = [
    "#00D4FF", "#0094C6", "#00C6B8", "#4ECDC4",
    "#44A5E0", "#7ECEF4", "#1A6FA0", "#B8E4F9",
]

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:#020B18; --surface:#0A1628; --surface2:#0D2240;
    --a1:#0094C6; --a2:#00C6B8; --a3:#00D4FF;
    --tx:#E8F4FD; --tx2:#8FACC8; --border:#1A3355;
    --ok:#00C896; --warn:#FFB347; --err:#FF6B6B;
    --r:12px; --rs:8px;
    --sh:0 4px 24px rgba(0,148,198,0.10);
    --sh2:0 8px 32px rgba(0,148,198,0.20);
}

/* ── Core ── */
html, body, [class*="css"] {
    font-family:'Inter',sans-serif !important;
    background-color:var(--bg) !important;
    color:var(--tx) !important;
}
.stApp {
    background:linear-gradient(160deg,#020B18 0%,#040D1C 60%,#020B18 100%) !important;
}

/* ── Chrome hiding ── */
[data-testid="stDecoration"] { display:none !important; }
#MainMenu, footer, .viewerBadge_container__1QSob { display:none !important; }
header[data-testid="stHeader"] {
    background:rgba(2,11,24,0.88) !important;
    backdrop-filter:blur(14px) !important;
    border-bottom:1px solid var(--border) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#060F1E 0%,#030A14 100%) !important;
    border-right:1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top:0 !important; }
[data-testid="stSidebarNav"] { padding-top:0.5rem !important; }
[data-testid="stSidebarNav"] ul { gap:2px !important; }
[data-testid="stSidebarNav"] a {
    border-radius:var(--rs) !important;
    color:var(--tx2) !important;
    font-size:0.85rem !important;
    font-weight:500 !important;
    padding:0.55rem 1rem !important;
    transition:background 0.15s,color 0.15s,border 0.15s !important;
}
[data-testid="stSidebarNav"] a:hover {
    background:rgba(0,148,198,0.12) !important;
    color:var(--a3) !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background:rgba(0,148,198,0.18) !important;
    color:var(--a3) !important;
    border-left:3px solid var(--a3) !important;
    font-weight:700 !important;
}

/* ── Main block ── */
.main .block-container {
    padding:1.75rem 2.25rem 2.5rem !important;
    max-width:1440px !important;
}

/* ── Typography ── */
h1,h2,h3,h4,h5,h6 {
    font-family:'Inter',sans-serif !important;
    letter-spacing:-0.02em !important;
}
h1 { color:var(--tx) !important; font-size:1.8rem !important; font-weight:700 !important; }
h2 { color:var(--tx) !important; font-size:1.35rem !important; font-weight:700 !important; }
h3 { color:var(--a3) !important; font-size:1.05rem !important; font-weight:600 !important; }
p,li { color:var(--tx) !important; line-height:1.6 !important; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background:linear-gradient(135deg,var(--surface) 0%,var(--surface2) 100%) !important;
    border:1px solid var(--border) !important;
    border-radius:var(--r) !important;
    padding:1.25rem 1.25rem 1rem !important;
    box-shadow:var(--sh) !important;
    animation:fadeUp 0.4s ease both !important;
    transition:transform 0.2s ease,box-shadow 0.2s ease,border-color 0.2s !important;
    position:relative !important;
    overflow:hidden !important;
}
[data-testid="metric-container"]::before {
    content:'';
    position:absolute;
    top:0;left:0;right:0;
    height:2px;
    background:linear-gradient(90deg,var(--a1),var(--a2),var(--a3));
}
[data-testid="metric-container"]:hover {
    transform:translateY(-3px) !important;
    box-shadow:var(--sh2) !important;
    border-color:rgba(0,148,198,0.35) !important;
}
[data-testid="stMetricLabel"] > div {
    color:var(--tx2) !important;
    font-size:0.7rem !important;
    font-weight:700 !important;
    text-transform:uppercase !important;
    letter-spacing:0.1em !important;
}
[data-testid="stMetricValue"] > div {
    color:var(--a3) !important;
    font-size:1.9rem !important;
    font-weight:700 !important;
}
[data-testid="stMetricDelta"] { color:var(--ok) !important; }

/* Stagger animation on metric columns */
[data-testid="column"]:nth-child(1) [data-testid="metric-container"] { animation-delay:0.00s !important; }
[data-testid="column"]:nth-child(2) [data-testid="metric-container"] { animation-delay:0.08s !important; }
[data-testid="column"]:nth-child(3) [data-testid="metric-container"] { animation-delay:0.16s !important; }
[data-testid="column"]:nth-child(4) [data-testid="metric-container"] { animation-delay:0.24s !important; }

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    border:1px solid var(--border) !important;
    border-radius:var(--r) !important;
    overflow:hidden !important;
    box-shadow:var(--sh) !important;
}

/* ── Buttons ── */
.stButton > button {
    background:linear-gradient(135deg,var(--a1),var(--a2)) !important;
    color:#fff !important;
    border:none !important;
    border-radius:var(--rs) !important;
    font-family:'Inter',sans-serif !important;
    font-weight:600 !important;
    font-size:0.85rem !important;
    letter-spacing:0.02em !important;
    padding:0.5rem 1.25rem !important;
    transition:all 0.2s ease !important;
    box-shadow:0 2px 12px rgba(0,148,198,0.25) !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 6px 20px rgba(0,148,198,0.4) !important;
}
.stButton > button:active { transform:translateY(0) !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background:rgba(0,148,198,0.10) !important;
    color:var(--a3) !important;
    border:1px solid rgba(0,148,198,0.3) !important;
    border-radius:var(--rs) !important;
    font-size:0.82rem !important;
    font-weight:600 !important;
    padding:0.45rem 1rem !important;
    transition:all 0.2s !important;
}
.stDownloadButton > button:hover {
    background:rgba(0,148,198,0.2) !important;
    transform:translateY(-1px) !important;
}

/* ── Selectbox / Multiselect ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background:var(--surface2) !important;
    border:1px solid var(--border) !important;
    border-radius:var(--rs) !important;
    color:var(--tx) !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div,
[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div {
    background:#0A1628 !important;
    border-color:#1A3355 !important;
}

/* ── Divider ── */
hr {
    border:none !important;
    border-top:1px solid var(--border) !important;
    margin:1.5rem 0 !important;
}

/* ── Alert boxes ── */
[data-testid="stAlert"] {
    border-radius:var(--r) !important;
    border-left-width:3px !important;
    font-size:0.875rem !important;
}
.stInfo    { background:rgba(0,148,198,0.07) !important; border-left-color:var(--a1) !important; }
.stSuccess { background:rgba(0,200,150,0.07) !important; border-left-color:var(--ok) !important; }
.stError   { background:rgba(255,107,107,0.07) !important; border-left-color:var(--err) !important; }
.stWarning { background:rgba(255,179,71,0.07) !important; border-left-color:var(--warn) !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background:var(--surface) !important;
    border:1px solid var(--border) !important;
    border-radius:var(--r) !important;
    overflow:hidden !important;
}
[data-testid="stExpander"] summary {
    color:var(--a3) !important;
    font-weight:600 !important;
    font-size:0.85rem !important;
    padding:0.75rem 1rem !important;
}
[data-testid="stExpander"] summary:hover {
    background:rgba(0,212,255,0.04) !important;
}

/* ── Code blocks ── */
.stCode, pre, code {
    background:#060F1E !important;
    border:1px solid var(--border) !important;
    border-radius:var(--rs) !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:0.8rem !important;
    color:var(--a3) !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background:var(--surface) !important;
    border:1px solid var(--border) !important;
    border-radius:var(--r) !important;
    padding:0.85rem 1rem !important;
    margin-bottom:0.6rem !important;
    animation:fadeUp 0.3s ease both !important;
    transition:border-color 0.2s !important;
}
[data-testid="stChatMessage"]:hover {
    border-color:rgba(0,148,198,0.3) !important;
}

/* ── Chat input ── */
[data-testid="stChatInputTextArea"] {
    background:var(--surface2) !important;
    border:1px solid var(--border) !important;
    border-radius:24px !important;
    color:var(--tx) !important;
    font-family:'Inter',sans-serif !important;
    font-size:0.9rem !important;
    transition:border-color 0.2s,box-shadow 0.2s !important;
}
[data-testid="stChatInputTextArea"]:focus {
    border-color:var(--a3) !important;
    box-shadow:0 0 0 3px rgba(0,212,255,0.12) !important;
}

/* ── Spinner ── */
.stSpinner > div > div {
    border-top-color:var(--a3) !important;
    border-right-color:var(--a3) !important;
}

/* ── Caption ── */
.stCaption, [data-testid="stCaption"] {
    color:var(--tx2) !important;
    font-size:0.78rem !important;
}

/* ── Plotly chart containers ── */
[data-testid="stPlotlyChart"] {
    border:1px solid var(--border) !important;
    border-radius:var(--r) !important;
    overflow:hidden !important;
    box-shadow:var(--sh) !important;
    animation:fadeUp 0.45s ease both !important;
}

/* ── Sidebar text ── */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color:var(--tx2) !important;
    font-size:0.68rem !important;
    font-weight:700 !important;
    text-transform:uppercase !important;
    letter-spacing:0.12em !important;
    margin-bottom:0.4rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:var(--a1); }

/* ── Keyframes ── */
@keyframes fadeUp {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeIn {
    from { opacity:0; }
    to   { opacity:1; }
}
@keyframes gradientShift {
    0%,100% { background-position:0% 50%; }
    50%      { background-position:100% 50%; }
}
@keyframes pulseGlow {
    0%,100% { box-shadow:0 0 12px rgba(0,212,255,0.2); }
    50%      { box-shadow:0 0 28px rgba(0,212,255,0.5); }
}
@keyframes spin {
    to { transform:rotate(360deg); }
}
"""


def inject_theme() -> None:
    """Inject global CSS into the Streamlit page."""
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


def apply_chart_theme(fig: go.Figure, height: int = 440) -> go.Figure:
    """Apply the dark ocean Plotly theme to any figure."""
    fig.update_layout(
        height=height,
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE2,
        font=dict(family="Inter, sans-serif", color=TX, size=12),
        colorway=CHART_COLORS,
        xaxis=dict(
            gridcolor=BORDER,
            linecolor=BORDER,
            tickcolor=TX2,
            title_font=dict(color=TX2),
            tickfont=dict(color=TX2),
            showgrid=True,
        ),
        yaxis=dict(
            gridcolor=BORDER,
            linecolor=BORDER,
            tickcolor=TX2,
            title_font=dict(color=TX2),
            tickfont=dict(color=TX2),
            showgrid=True,
        ),
        legend=dict(
            bgcolor="rgba(10,22,40,0.85)",
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(color=TX2, size=11),
        ),
        title_font=dict(color=TX, size=13, family="Inter, sans-serif"),
        margin=dict(l=12, r=12, t=44, b=12),
        hoverlabel=dict(
            bgcolor=SURFACE2,
            bordercolor=A1,
            font=dict(color=TX, family="Inter, sans-serif", size=12),
        ),
    )
    return fig


def page_header(icon_svg: str, title: str, subtitle: str = "") -> None:
    """Styled page header with gradient title and icon badge."""
    sub_html = (
        f'<p style="margin:0.3rem 0 0;color:#8FACC8;font-size:0.88rem;">{subtitle}</p>'
        if subtitle else ""
    )
    st.markdown(f"""
<div style="
    display:flex;align-items:center;gap:1rem;
    padding:1.25rem 0 1rem;
    border-bottom:1px solid #1A3355;
    margin-bottom:1.5rem;
    animation:fadeUp 0.35s ease;
">
  <div style="
    width:46px;height:46px;flex-shrink:0;
    background:linear-gradient(135deg,#0094C6,#00C6B8);
    border-radius:11px;
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 4px 16px rgba(0,148,198,0.35);
  ">{icon_svg}</div>
  <div>
    <h1 style="
      margin:0;font-size:1.6rem;font-weight:800;
      background:linear-gradient(135deg,#E8F4FD 0%,#7ECEF4 50%,#00D4FF 100%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      background-clip:text;letter-spacing:-0.025em;
    ">{title}</h1>
    {sub_html}
  </div>
</div>
""", unsafe_allow_html=True)


def section_header(text: str, icon_svg: str = "") -> None:
    """Styled section divider with optional icon."""
    icon_part = f'<span style="display:inline-flex;">{icon_svg}</span>' if icon_svg else ""
    st.markdown(f"""
<div style="
    display:flex;align-items:center;gap:0.5rem;
    margin:1.75rem 0 0.85rem;
    padding-bottom:0.55rem;
    border-bottom:1px solid #1A3355;
    animation:fadeIn 0.3s ease;
">
  {icon_part}
  <span style="
    font-size:0.72rem;font-weight:700;color:#8FACC8;
    text-transform:uppercase;letter-spacing:0.12em;
  ">{text}</span>
</div>
""", unsafe_allow_html=True)


def sidebar_brand() -> None:
    """Render the AlgoFloat brand block at the top of the sidebar."""
    st.sidebar.markdown("""
<div style="
    padding:1.5rem 1rem 1.25rem;
    border-bottom:1px solid #1A3355;
    margin-bottom:0.25rem;
    text-align:center;
">
  <div style="
    display:inline-flex;align-items:center;gap:0.6rem;
    padding:0.55rem 1.1rem;
    background:linear-gradient(135deg,rgba(0,148,198,0.14),rgba(0,198,184,0.14));
    border:1px solid rgba(0,212,255,0.18);
    border-radius:10px;
  ">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="12" r="9.5" stroke="#00D4FF" stroke-width="1.4"/>
      <path d="M2.5 12 Q7 8 12 12 Q17 16 21.5 12" stroke="#00D4FF" stroke-width="1.4" stroke-linecap="round" fill="none"/>
      <path d="M2.5 12 Q7 16 12 12 Q17 8 21.5 12" stroke="#00C6B8" stroke-width="1.4" stroke-linecap="round" fill="none"/>
      <circle cx="12" cy="7.5" r="1.5" fill="#00D4FF"/>
    </svg>
    <span style="font-size:0.97rem;font-weight:700;color:#E8F4FD;letter-spacing:-0.01em;">AlgoFloat</span>
  </div>
  <div style="font-size:0.67rem;color:#4A6888;margin-top:0.45rem;letter-spacing:0.06em;text-transform:uppercase;">
    Ocean Intelligence Platform
  </div>
</div>
""", unsafe_allow_html=True)


def badge(text: str, color: str = A3) -> str:
    """Return an inline HTML badge span."""
    return (
        f'<span style="display:inline-block;padding:0.2rem 0.6rem;'
        f'background:{color}18;border:1px solid {color}40;'
        f'border-radius:20px;font-size:0.72rem;font-weight:600;color:{color};">'
        f'{text}</span>'
    )
