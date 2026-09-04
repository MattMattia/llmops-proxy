@echo off
title LLMOps Proxy - Inicio de Servicios
cd /d "%~dp0"

echo Iniciando servicio de Ollama...
start "Ollama" cmd /k "ollama serve"

echo Iniciando backend FastAPI...
start "FastAPI" cmd /k "call .venv\Scripts\activate.bat && uvicorn app.main:app --reload"

echo Esperando 5 segundos...
timeout /t 5 /nobreak >nul

echo Iniciando Streamlit...
start "Streamlit" cmd /k "call .venv\Scripts\activate.bat && streamlit run app_ui.py"

echo Todos los servicios iniciados.
pause