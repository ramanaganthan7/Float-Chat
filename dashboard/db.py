import sqlite3
import pandas as pd
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_BASE_DIR, "..", "data")
CSV_PATH = os.path.join(_DATA_DIR, "sample_argo.csv")
DB_PATH = os.path.join(_DATA_DIR, "argo.db")


def init_db():
    """Load CSV into SQLite database, replacing existing data."""
    df = pd.read_csv(CSV_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("argo_profiles", conn, if_exists="replace", index=False)
    conn.close()


def get_connection():
    if not os.path.exists(DB_PATH):
        init_db()
    return sqlite3.connect(DB_PATH)


def run_query(query: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()
    return df


# Ensure DB is initialised on import
if not os.path.exists(DB_PATH):
    init_db()
