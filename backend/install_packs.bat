@echo off
REM One-time: install Argos offline models (en, zh, ja, de pairs).
REM Double-click this file from Explorer, or run from cmd in the backend folder.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
  echo [ERROR] Virtual environment not found.
  echo Create it first in this folder:
  echo   python -m venv venv
  echo   venv\Scripts\activate
  echo   pip install -r requirements.txt
  pause
  exit /b 1
)

echo Running install_language_packs.py ...
echo This may take a long time and download several hundred MB.
echo.

venv\Scripts\python.exe scripts\install_language_packs.py

echo.
pause
