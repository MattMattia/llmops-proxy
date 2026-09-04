@echo off
title LLMOps Proxy - Inicio Silencioso
cd /d "%~dp0"

:: 1. Iniciar Ollama en segundo plano oculto
start /b ollama serve >nul 2>&1

:: 2. Iniciar FastAPI en segundo plano oculto
start /b cmd /c "call .venv\Scripts\activate.bat && uvicorn app.main:app --reload >nul 2>&1"

:: 3. Esperar 5 segundos a que carguen los servicios
timeout /t 5 /nobreak >nul

:: 4. Iniciar Streamlit (este abre el navegador automáticamente sin consola intrusiva)
start /b cmd /c "call .venv\Scripts\activate.bat && streamlit run app_ui.py"

exit