"""uv run start.py  →  launches the Streamlit app"""
import subprocess, sys
subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard/app.py"], check=True)
