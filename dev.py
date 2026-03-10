"""uv run dev.py  →  launches the Streamlit app with auto-reload on save"""
import subprocess, sys
subprocess.run(
    [sys.executable, "-m", "streamlit", "run", "dashboard/app.py", "--server.runOnSave", "true"],
    check=True,
)
