@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    echo No se encontro el entorno virtual .venv
    echo Crea el entorno con: python -m venv .venv
    pause
    exit /b 1
)
.venv\Scripts\python.exe -m uvicorn src.main:app --reload
