import subprocess
import sys
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def start():
    """uv run start — launch the Streamlit app normally."""
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run",
         os.path.join(_ROOT, "dashboard", "app.py")],
        check=True,
    )


def dev():
    """uv run dev — launch the Streamlit app with auto-reload on save."""
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run",
         os.path.join(_ROOT, "dashboard", "app.py"),
         "--server.runOnSave", "true"],
        check=True,
    )
