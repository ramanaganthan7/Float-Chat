import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

_DASH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _DASH not in sys.path:
    sys.path.insert(0, _DASH)

from chatbot.gemini_client import generate_sql
from chatbot.prompt import SYSTEM_PROMPT
from db import run_query, init_db, DB_PATH
from utils.theme import (
    inject_theme, sidebar_brand, page_header,
    apply_chart_theme, CHART_COLORS, SURFACE, SURFACE2, BORDER, A3,
)

st.set_page_config(page_title="Chatbot | AlgoFloat", page_icon="", layout="wide")
inject_theme()

# ── Extra chat-specific CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
/* User message bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background:linear-gradient(135deg,rgba(0,148,198,0.12),rgba(0,198,184,0.08)) !important;
    border-color:rgba(0,148,198,0.28) !important;
}
/* Assistant message bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background:linear-gradient(135deg,#0A1628,#0D2240) !important;
    border-color:#1A3355 !important;
}
/* Typed text in chat input */
[data-testid="stChatInputTextArea"] {
    background:#0A1628 !important;
    caret-color:#00D4FF !important;
}
/* Typing cursor blink */
@keyframes blink {
    0%,100% { opacity:1; }
    50%      { opacity:0; }
}
</style>
""", unsafe_allow_html=True)

sidebar_brand()

# ── Sidebar schema + examples ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="
    font-size:0.68rem;font-weight:700;color:#8FACC8;
    text-transform:uppercase;letter-spacing:0.12em;
    padding:0.75rem 0 0.5rem;
    border-top:1px solid #1A3355;margin-top:0.5rem;
">Table Schema</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="
    background:#060F1E;border:1px solid #1A3355;border-radius:8px;
    padding:0.75rem;font-family:'JetBrains Mono',monospace;
    font-size:0.72rem;color:#00D4FF;line-height:1.65;
">
  <span style="color:#8FACC8;">TABLE</span> argo_profiles<br>
  &nbsp;&nbsp;<span style="color:#4ECDC4;">N_POINTS</span><br>
  &nbsp;&nbsp;<span style="color:#4ECDC4;">CYCLE_NUMBER</span><br>
  &nbsp;&nbsp;<span style="color:#4ECDC4;">DATA_MODE</span><br>
  &nbsp;&nbsp;<span style="color:#4ECDC4;">DIRECTION</span><br>
  &nbsp;&nbsp;<span style="color:#4ECDC4;">PLATFORM_NUMBER</span><br>
  &nbsp;&nbsp;<span style="color:#00D4FF;">PRES</span> &nbsp;<span style="color:#44A5E0;">PSAL</span> &nbsp;<span style="color:#00C6B8;">TEMP</span><br>
  &nbsp;&nbsp;<span style="color:#4ECDC4;">LATITUDE &nbsp;LONGITUDE</span><br>
  &nbsp;&nbsp;<span style="color:#4ECDC4;">TIME</span><br>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="
    font-size:0.68rem;font-weight:700;color:#8FACC8;
    text-transform:uppercase;letter-spacing:0.12em;
    padding:0.75rem 0 0.5rem;
    border-top:1px solid #1A3355;margin-top:0.75rem;
">Example Queries</div>
""", unsafe_allow_html=True)

    _examples = [
        "Show the top 10 highest temperature readings",
        "Average salinity per platform",
        "List all floats and their cycle counts",
        "Show pressure vs temperature for platform 5906343",
        "Which float has the deepest observations?",
        "Find readings where TEMP > 28°C",
    ]
    for ex in _examples:
        st.markdown(f"""
<div style="
    padding:0.45rem 0.75rem;
    background:rgba(0,148,198,0.06);
    border:1px solid rgba(0,148,198,0.15);
    border-radius:6px;
    font-size:0.78rem;color:#8FACC8;
    margin-bottom:0.4rem;
    cursor:default;
    transition:background 0.15s;
" onmouseover="this.style.background='rgba(0,148,198,0.12)'"
  onmouseout="this.style.background='rgba(0,148,198,0.06)'">{ex}</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("Clear conversation"):
        st.session_state["messages"] = []
        st.rerun()

# ── Ensure DB ─────────────────────────────────────────────────────────────────
if not os.path.exists(DB_PATH):
    with st.spinner("Initialising database for the first time…"):
        init_db()

# ── Page header ───────────────────────────────────────────────────────────────
page_header(
    icon_svg="""<svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.8">
      <path stroke-linecap="round" stroke-linejoin="round"
        d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-3 3-3-3z"/>
    </svg>""",
    title="Chat with Ocean Data",
    subtitle="Ask anything in plain English — Gemini 2.0 Flash generates SQL and SQLite executes it instantly.",
)

# ── Status indicator ───────────────────────────────────────────────────────────
st.markdown("""
<div style="
    display:inline-flex;align-items:center;gap:0.5rem;
    padding:0.35rem 0.85rem;
    background:rgba(0,200,150,0.08);
    border:1px solid rgba(0,200,150,0.22);
    border-radius:24px;
    font-size:0.72rem;font-weight:600;color:#00C896;
    letter-spacing:0.05em;
    margin-bottom:1.25rem;
    animation:fadeUp 0.4s ease;
">
  <span style="width:7px;height:7px;border-radius:50%;background:#00C896;
    animation:pulseGlow 2s ease infinite;display:inline-block;"></span>
  Gemini 2.0 Flash connected
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ── Chat history ───────────────────────────────────────────────────────────────
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        content = msg["content"]
        if isinstance(content, str):
            st.markdown(content)
        elif isinstance(content, dict):
            _type = content.get("type")
            if _type == "dataframe":
                _df = pd.DataFrame(content["data"])
                st.markdown(f"""
<div style="
    display:inline-flex;align-items:center;gap:0.4rem;
    padding:0.3rem 0.8rem;
    background:rgba(0,200,150,0.1);border:1px solid rgba(0,200,150,0.25);
    border-radius:24px;font-size:0.75rem;font-weight:600;color:#00C896;
    margin-bottom:0.5rem;
">Returned {len(_df):,} rows</div>
""", unsafe_allow_html=True)
                st.dataframe(_df, use_container_width=True)
            elif _type == "error":
                st.error(content.get("message", "An error occurred."))

# ── Chat input ─────────────────────────────────────────────────────────────────
if prompt := st.chat_input("e.g. Show me temperature readings above 28°C …"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Step 1 — generate SQL
        with st.spinner("Generating SQL query…"):
            try:
                sql = generate_sql(prompt, SYSTEM_PROMPT)
            except Exception as e:
                sql = None
                err_msg = f"Could not reach Gemini API: {e}"
                st.error(err_msg)
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": {"type": "error", "message": err_msg},
                })

        if sql:
            with st.expander("Generated SQL", expanded=False):
                st.code(sql, language="sql")

            # Step 2 — execute
            with st.spinner("Running query against SQLite…"):
                try:
                    result_df = run_query(sql)
                except Exception as e:
                    result_df = None
                    err_msg = f"SQL execution error: {e}\n\nQuery:\n{sql}"
                    st.error(err_msg)
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": {"type": "error", "message": err_msg},
                    })

            if result_df is not None:
                if result_df.empty:
                    msg_text = "Query ran successfully but returned 0 rows. Try rephrasing your question."
                    st.info(msg_text)
                    st.session_state["messages"].append({"role": "assistant", "content": msg_text})
                else:
                    # Success badge
                    st.markdown(f"""
<div style="
    display:inline-flex;align-items:center;gap:0.45rem;
    padding:0.32rem 0.8rem;
    background:rgba(0,200,150,0.1);border:1px solid rgba(0,200,150,0.25);
    border-radius:24px;font-size:0.75rem;font-weight:600;color:#00C896;
    margin-bottom:0.6rem;animation:fadeUp 0.3s ease;
">
  <svg width="11" height="11" fill="none" viewBox="0 0 24 24" stroke="#00C896" stroke-width="2.5">
    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
  </svg>
  Returned {len(result_df):,} row{'s' if len(result_df) != 1 else ''}
</div>
""", unsafe_allow_html=True)

                    display_df = result_df.head(100)
                    st.dataframe(display_df, use_container_width=True)

                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": {
                            "type": "dataframe",
                            "data": display_df.to_dict(),
                        },
                    })

                    # Download button
                    st.download_button(
                        "Download CSV",
                        result_df.to_csv(index=False).encode("utf-8"),
                        "query_results.csv",
                        "text/csv",
                    )

                    # Auto-chart: time series if TIME column present
                    if "TIME" in result_df.columns:
                        sorted_df = result_df.sort_values("TIME")
                        numeric_candidates = (
                            ["TEMP", "PSAL", "PRES"]
                            + [c for c in result_df.select_dtypes("number").columns
                               if c not in ("TEMP", "PSAL", "PRES")]
                        )
                        for y_col in numeric_candidates:
                            if y_col in result_df.columns and y_col != "TIME":
                                color_col = "PLATFORM_NUMBER" if "PLATFORM_NUMBER" in result_df.columns else None
                                fig = px.line(
                                    sorted_df, x="TIME", y=y_col,
                                    color=color_col,
                                    markers=len(sorted_df) < 200,
                                    labels={"TIME": "Date / Time", y_col: y_col},
                                    color_discrete_sequence=CHART_COLORS,
                                )
                                apply_chart_theme(fig, height=360)
                                fig.update_layout(
                                    title=f"{y_col} over Time",
                                    xaxis_title="Date / Time",
                                    yaxis_title=y_col,
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                break

                    # Numeric scatter if two numeric columns + no TIME
                    elif len(result_df.select_dtypes("number").columns) >= 2:
                        num_cols = result_df.select_dtypes("number").columns.tolist()
                        x_col, y_col = num_cols[0], num_cols[1]
                        color_col = "PLATFORM_NUMBER" if "PLATFORM_NUMBER" in result_df.columns else None
                        fig = px.scatter(
                            result_df.head(500),
                            x=x_col, y=y_col,
                            color=color_col,
                            opacity=0.7,
                            labels={x_col: x_col, y_col: y_col},
                            color_discrete_sequence=CHART_COLORS,
                        )
                        apply_chart_theme(fig, height=340)
                        fig.update_layout(title=f"{x_col} vs {y_col}")
                        st.plotly_chart(fig, use_container_width=True)
