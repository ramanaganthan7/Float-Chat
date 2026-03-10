import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os

# Ensure dashboard dir is on path so db / chatbot imports work
_DASH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _DASH not in sys.path:
    sys.path.insert(0, _DASH)

from chatbot.gemini_client import generate_sql
from chatbot.prompt import SYSTEM_PROMPT
from db import run_query, init_db, DB_PATH

st.set_page_config(page_title="Chatbot | FloatChat", layout="wide")
st.title("💬 Chat with Ocean Data")
st.caption(
    "Ask natural-language questions about the ARGO dataset — "
    "Gemini generates the SQL and SQLite runs it instantly."
)

# ── Ensure SQLite DB exists ──────────────────────────────────────────────────
if not os.path.exists(DB_PATH):
    with st.spinner("Initialising database for the first time…"):
        init_db()

# ── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ── Sidebar: schema hint ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Table Schema")
    st.code(
        "argo_profiles\n"
        "  N_POINTS, CYCLE_NUMBER, DATA_MODE,\n"
        "  DIRECTION, PLATFORM_NUMBER,\n"
        "  PRES, PSAL, TEMP,\n"
        "  LATITUDE, LONGITUDE, TIME",
        language="sql",
    )
    st.divider()
    st.markdown("**Example questions**")
    st.markdown(
        "- Show me the top 10 highest temperature readings\n"
        "- What is the average salinity per platform?\n"
        "- List all floats and their cycle counts\n"
        "- Show pressure vs temperature for platform 5906343"
    )
    if st.button("🗑️ Clear chat"):
        st.session_state["messages"] = []
        st.rerun()

# ── Display prior messages ───────────────────────────────────────────────────
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        content = msg["content"]
        if isinstance(content, str):
            st.markdown(content)
        elif isinstance(content, dict) and content.get("type") == "dataframe":
            st.dataframe(pd.DataFrame(content["data"]), use_container_width=True)

# ── User input ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("e.g. Show me temperature readings above 28°C …"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generating SQL…"):
            try:
                # Step 1 – ask Gemini to write the SQL (one call, no retries)
                sql = generate_sql(prompt, SYSTEM_PROMPT)
            except Exception as e:
                sql = None
                err = f"Gemini error: {e}"
                st.error(err)
                st.session_state["messages"].append({"role": "assistant", "content": err})

        if sql:
            with st.expander("🔍 Generated SQL", expanded=False):
                st.code(sql, language="sql")

            # Step 2 – run against SQLite
            try:
                df = run_query(sql)
            except Exception as e:
                df = None
                err = f"SQL execution error: {e}\n\nGenerated query:\n{sql}"
                st.error(err)
                st.session_state["messages"].append({"role": "assistant", "content": err})

            if df is not None:
                if df.empty:
                    msg = "Query ran successfully but returned 0 rows. Try a different question."
                    st.info(msg)
                    st.session_state["messages"].append({"role": "assistant", "content": msg})
                else:
                    st.success(f"✅ Returned **{len(df):,}** rows.")
                    st.dataframe(df.head(100), use_container_width=True)
                    st.session_state["messages"].append(
                        {"role": "assistant", "content": {
                            "type": "dataframe",
                            "data": df.head(100).to_dict(),
                        }}
                    )

                    # Download button
                    st.download_button(
                        "⬇️ Download CSV",
                        df.to_csv(index=False).encode("utf-8"),
                        "query_results.csv",
                        "text/csv",
                    )

                    # Auto-chart: pick first plottable numeric col vs TIME
                    if "TIME" in df.columns:
                        for y_col in ["TEMP", "PSAL", "PRES"] + list(df.select_dtypes("number").columns):
                            if y_col in df.columns and y_col != "TIME":
                                color = "PLATFORM_NUMBER" if "PLATFORM_NUMBER" in df.columns else None
                                fig = px.line(
                                    df.sort_values("TIME"),
                                    x="TIME", y=y_col,
                                    color=color,
                                    title=f"{y_col} over Time",
                                    markers=len(df) < 200,
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                break
