@echo off
echo Starting CodeEcho Development Environment...

echo.
echo [1/3] Activating Python virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [2/3] Starting Backend Server...
start "CodeEcho Backend" cmd /k "cd CodeEcho-app\backend\src && python main.py"

echo.
echo [3/3] Starting Frontend Server...
start "CodeEcho Frontend" cmd /k "cd CodeEcho-app\frontend && npm run dev"

echo.
echo ✅ CodeEcho is starting up!
echo.
echo Backend: http://127.0.0.1:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this window...
pause >nul
