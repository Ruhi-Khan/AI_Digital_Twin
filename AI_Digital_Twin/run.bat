@echo off

cd /d "%~dp0"

echo.
echo ==========================================
echo      AI DIGITAL TWIN OF THE INTERNET
echo ==========================================
echo.

python -m uvicorn app.main:app --reload

pause