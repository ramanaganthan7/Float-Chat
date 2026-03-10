"""
graph.py — kept for backward compatibility.
The chatbot page now calls gemini_client + db directly.
This module is no longer used in the main workflow.
"""
import sys
import os

_DASHBOARD_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _DASHBOARD_DIR not in sys.path:
    sys.path.insert(0, _DASHBOARD_DIR)

from chatbot.prompt import SYSTEM_PROMPT
from chatbot.gemini_client import generate_sql
from db import run_query


class ChatState(dict):
    pass


def run_chat(user_prompt: str) -> dict:
    """Single-shot: generate SQL → execute → return result dict."""
    try:
        sql = generate_sql(user_prompt, SYSTEM_PROMPT)
    except Exception as e:
        return {"error": str(e), "df": None, "sql_query": ""}

    try:
        df = run_query(sql)
        return {"df": df, "sql_query": sql, "error": None}
    except Exception as e:
        return {"df": None, "sql_query": sql, "error": str(e)}