"""
AlgoFloat FastAPI backend.
Serves all data endpoints consumed by the React+Vite frontend.
Run: uvicorn backend.main:app --reload --port 8000
"""

from __future__ import annotations
import os
import sys
import math
import sqlite3

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Path setup ────────────────────────────────────────────────────────────────
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DASHBOARD = os.path.join(_ROOT, "dashboard")
if _DASHBOARD not in sys.path:
    sys.path.insert(0, _DASHBOARD)

from db import run_query, init_db, DB_PATH, CSV_PATH          # noqa: E402
from chatbot.gemini_client import generate_sql                 # noqa: E402
from chatbot.prompt import SYSTEM_PROMPT                       # noqa: E402

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="AlgoFloat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure DB exists on startup
if not os.path.exists(DB_PATH):
    init_db()


# ── Helpers ───────────────────────────────────────────────────────────────────
def _clean(obj):
    """Recursively replace NaN / Inf with None so JSON serialises."""
    if isinstance(obj, float):
        return None if (math.isnan(obj) or math.isinf(obj)) else obj
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean(v) for v in obj]
    return obj


def _df_records(df: pd.DataFrame) -> list[dict]:
    return _clean(df.to_dict(orient="records"))


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/api/overview")
def get_overview():
    df = pd.read_csv(CSV_PATH)

    # Platform summary
    platform_summary = (
        df.groupby("PLATFORM_NUMBER")
        .agg(
            cycles=("CYCLE_NUMBER", "nunique"),
            records=("N_POINTS", "count"),
            avg_temp=("TEMP", "mean"),
            avg_sal=("PSAL", "mean"),
            avg_pres=("PRES", "mean"),
        )
        .round(3)
        .reset_index()
    )

    return _clean({
        "total_records": int(len(df)),
        "unique_floats": int(df["PLATFORM_NUMBER"].nunique()),
        "avg_temp": round(float(df["TEMP"].mean()), 2),
        "avg_salinity": round(float(df["PSAL"].mean()), 2),
        "temp_values": df["TEMP"].dropna().tolist(),
        "psal_values": df["PSAL"].dropna().tolist(),
        "pres_values": df["PRES"].dropna().tolist(),
        "stats": df[["TEMP", "PSAL", "PRES"]].describe().round(4).to_dict(),
        "sample": _df_records(df.head(20)),
        "platform_summary": _df_records(platform_summary),
        "corr": df[["TEMP", "PSAL", "PRES"]].corr().round(3).to_dict(),
    })


@app.get("/api/map")
def get_map():
    df = pd.read_csv(CSV_PATH)
    cols = ["PLATFORM_NUMBER", "CYCLE_NUMBER", "TIME",
            "LATITUDE", "LONGITUDE", "TEMP", "PSAL", "PRES"]
    return _clean(df[cols].to_dict(orient="records"))


@app.get("/api/trends")
def get_trends():
    df = pd.read_csv(CSV_PATH, parse_dates=["TIME"])
    df = df.sort_values("TIME")
    df["TIME"] = df["TIME"].astype(str)
    cols = ["PLATFORM_NUMBER", "CYCLE_NUMBER", "TIME", "TEMP", "PSAL", "PRES"]
    return _clean(df[cols].to_dict(orient="records"))


class ChatRequest(BaseModel):
    prompt: str


@app.post("/api/chat")
def chat(body: ChatRequest):
    if not body.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    # 1 – Generate SQL
    try:
        sql = generate_sql(body.prompt, SYSTEM_PROMPT)
    except Exception as exc:
        return {"sql": None, "data": None, "columns": [], "row_count": 0,
                "error": f"Gemini error: {exc}"}

    # 2 – Execute SQL
    try:
        df = run_query(sql)
    except Exception as exc:
        return {"sql": sql, "data": None, "columns": [], "row_count": 0,
                "error": f"SQL error: {exc}"}

    df_head = df.head(100)
    return _clean({
        "sql": sql,
        "data": _df_records(df_head),
        "columns": df.columns.tolist(),
        "row_count": int(len(df)),
        "error": None,
    })


@app.get("/api/health")
def health():
    return {"status": "ok"}
