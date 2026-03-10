@echo off
IF "%1"=="dev" (
    uv run streamlit run dashboard/app.py --server.runOnSave true
) ELSE IF "%1"=="start" (
    uv run streamlit run dashboard/app.py
) ELSE (
    echo Usage: run.bat [start^|dev]
    echo   start  - run the app normally
    echo   dev    - run with auto-reload on save
)
