import streamlit as st
import sys
import os

_DASH = os.path.dirname(os.path.abspath(__file__))
if _DASH not in sys.path:
    sys.path.insert(0, _DASH)

from utils.theme import inject_theme, sidebar_brand

st.set_page_config(
    page_title="AlgoFloat — Ocean Intelligence",
    page_icon="",
    layout="wide",
)

inject_theme()
sidebar_brand()

# ── Hero section ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    position:relative;overflow:hidden;
    padding:3.5rem 2.5rem 3rem;
    background:linear-gradient(135deg,#0A1628 0%,#0D2240 55%,#071626 100%);
    border:1px solid #1A3355;
    border-radius:16px;
    margin-bottom:2rem;
    animation:fadeUp 0.5s ease;
">
  <!-- ambient glow orbs -->
  <div style="
    position:absolute;top:-80px;right:-80px;width:360px;height:360px;
    background:radial-gradient(circle,rgba(0,148,198,0.13) 0%,transparent 70%);
    border-radius:50%;pointer-events:none;
  "></div>
  <div style="
    position:absolute;bottom:-100px;left:5%;width:280px;height:280px;
    background:radial-gradient(circle,rgba(0,198,184,0.10) 0%,transparent 70%);
    border-radius:50%;pointer-events:none;
  "></div>
  <!-- animated gradient bar at bottom -->
  <div style="
    position:absolute;bottom:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,#0094C6,#00C6B8,#00D4FF,#0094C6);
    background-size:200% 100%;
    animation:gradientShift 3.5s ease infinite;
  "></div>

  <div style="position:relative;z-index:1;max-width:700px;">
    <!-- live badge -->
    <div style="
        display:inline-flex;align-items:center;gap:0.45rem;
        background:rgba(0,212,255,0.09);
        border:1px solid rgba(0,212,255,0.22);
        border-radius:24px;
        padding:0.28rem 0.8rem;
        font-size:0.7rem;font-weight:700;color:#00D4FF;
        letter-spacing:0.08em;text-transform:uppercase;
        margin-bottom:1.25rem;
    ">
      <span style="
          width:7px;height:7px;border-radius:50%;background:#00D4FF;
          animation:pulseGlow 1.8s ease infinite;
          display:inline-block;
      "></span>
      Live Ocean Data
    </div>

    <h1 style="
        margin:0 0 0.8rem;
        font-size:clamp(1.9rem,3.5vw,2.8rem);
        font-weight:800;
        letter-spacing:-0.03em;
        background:linear-gradient(135deg,#E8F4FD 0%,#7ECEF4 45%,#00D4FF 100%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;
        line-height:1.15;
    ">
      AI-Powered ARGO<br>Ocean Data Explorer
    </h1>

    <p style="
        margin:0 0 2rem;
        color:#8FACC8;
        font-size:1rem;
        line-height:1.7;
    ">
      Real-time oceanographic insights from the global ARGO profiling float array.
      Explore temperature, salinity, and pressure across the world's oceans — powered
      by Gemini 2.0 Flash and natural language SQL.
    </p>

    <div style="display:flex;gap:0.6rem;flex-wrap:wrap;">
      <div style="
          padding:0.38rem 0.9rem;
          background:rgba(0,148,198,0.14);border:1px solid rgba(0,148,198,0.28);
          border-radius:24px;font-size:0.77rem;font-weight:600;color:#7ECEF4;
          display:flex;align-items:center;gap:0.4rem;
      ">
        <svg width="11" height="11" fill="none" viewBox="0 0 24 24" stroke="#7ECEF4" stroke-width="2.2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 7h16M4 12h16M4 17h16"/>
        </svg>
        SQLite Database
      </div>
      <div style="
          padding:0.38rem 0.9rem;
          background:rgba(0,198,184,0.11);border:1px solid rgba(0,198,184,0.24);
          border-radius:24px;font-size:0.77rem;font-weight:600;color:#00C6B8;
          display:flex;align-items:center;gap:0.4rem;
      ">
        <svg width="11" height="11" fill="none" viewBox="0 0 24 24" stroke="#00C6B8" stroke-width="2.2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
        Gemini 2.0 Flash
      </div>
      <div style="
          padding:0.38rem 0.9rem;
          background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.18);
          border-radius:24px;font-size:0.77rem;font-weight:600;color:#00D4FF;
          display:flex;align-items:center;gap:0.4rem;
      ">
        <svg width="11" height="11" fill="none" viewBox="0 0 24 24" stroke="#00D4FF" stroke-width="2.2">
          <circle cx="12" cy="12" r="10"/>
          <path stroke-linecap="round" d="M2 12h20M12 2a15.3 15.3 0 010 20M12 2a15.3 15.3 0 000 20"/>
        </svg>
        ARGO Float Array
      </div>
      <div style="
          padding:0.38rem 0.9rem;
          background:rgba(78,205,196,0.09);border:1px solid rgba(78,205,196,0.22);
          border-radius:24px;font-size:0.77rem;font-weight:600;color:#4ECDC4;
          display:flex;align-items:center;gap:0.4rem;
      ">
        <svg width="11" height="11" fill="none" viewBox="0 0 24 24" stroke="#4ECDC4" stroke-width="2.2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        Plotly Visualizations
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────────
_CARDS = [
    {
        "icon": """<svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.7">
          <rect x="3" y="3" width="7" height="7" rx="1.5"/>
          <rect x="14" y="3" width="7" height="7" rx="1.5"/>
          <rect x="3" y="14" width="7" height="7" rx="1.5"/>
          <rect x="14" y="14" width="7" height="7" rx="1.5"/>
        </svg>""",
        "title": "Overview",
        "desc": "Dataset statistics, KPI metrics, and full parameter distribution analysis across the ARGO dataset.",
        "color": "#00D4FF",
        "bg": "rgba(0,212,255,0.07)",
        "delay": "0.05s",
    },
    {
        "icon": """<svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.7">
          <circle cx="12" cy="12" r="9.5"/>
          <path stroke-linecap="round" d="M2.5 12 Q7 8.5 12 12 Q17 15.5 21.5 12"/>
          <path stroke-linecap="round" d="M12 2.5v19M4.2 4.2l15.6 15.6" opacity="0.4"/>
        </svg>""",
        "title": "Map",
        "desc": "Interactive global map of ARGO float positions with parameter-driven color overlays and filters.",
        "color": "#00C6B8",
        "bg": "rgba(0,198,184,0.07)",
        "delay": "0.12s",
    },
    {
        "icon": """<svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.7">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
        </svg>""",
        "title": "Trends",
        "desc": "Time-series analysis, depth profiles, and correlation views for temperature, salinity, and pressure.",
        "color": "#0094C6",
        "bg": "rgba(0,148,198,0.07)",
        "delay": "0.19s",
    },
    {
        "icon": """<svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.7">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-3 3-3-3z"/>
        </svg>""",
        "title": "Chatbot",
        "desc": "Natural language interface — ask anything about the data in plain English; Gemini writes the SQL.",
        "color": "#4ECDC4",
        "bg": "rgba(78,205,196,0.07)",
        "delay": "0.26s",
    },
]

cols = st.columns(4)
for col, card in zip(cols, _CARDS):
    with col:
        st.markdown(f"""
<div style="
    background:linear-gradient(135deg,#0A1628,#0D2240);
    border:1px solid #1A3355;
    border-radius:12px;
    padding:1.5rem 1.25rem 1.4rem;
    height:100%;
    position:relative;overflow:hidden;
    animation:fadeUp 0.4s ease {card['delay']} both;
    transition:transform 0.22s,box-shadow 0.22s,border-color 0.22s;
" onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 14px 36px rgba(0,148,198,0.22)';this.style.borderColor='{card['color']}55'"
  onmouseout="this.style.transform='';this.style.boxShadow='';this.style.borderColor='#1A3355'">
  <div style="
    position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,{card['color']},transparent);
  "></div>
  <div style="
    width:44px;height:44px;
    background:{card['bg']};
    border:1px solid {card['color']}30;
    border-radius:11px;
    display:flex;align-items:center;justify-content:center;
    margin-bottom:1rem;
  ">{card['icon']}</div>
  <div style="font-size:0.97rem;font-weight:700;color:#E8F4FD;margin-bottom:0.45rem;letter-spacing:-0.01em;">
    {card['title']}
  </div>
  <div style="font-size:0.8rem;color:#8FACC8;line-height:1.6;">
    {card['desc']}
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style="text-align:center;padding:0.25rem 0;animation:fadeIn 0.5s ease 0.4s both;">
  <span style="font-size:0.73rem;color:#3A5570;letter-spacing:0.04em;">
    Data: ARGO Global Float Array &nbsp;&middot;&nbsp; AI: Gemini 2.0 Flash &nbsp;&middot;&nbsp;
    Storage: SQLite &nbsp;&middot;&nbsp; Charts: Plotly
  </span>
</div>
""", unsafe_allow_html=True)
