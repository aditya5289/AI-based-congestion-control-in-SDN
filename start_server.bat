@echo off
title AI-Based Congestion Control in SDN - Project Launcher
color 0A
echo ============================================================
echo     AI-Based Congestion Control in SDN (MMMUT Gorakhpur)
echo ============================================================
echo.

:: 1️⃣ Start virtual environment & Flask backend
echo [1/4] Starting Flask Backend Server...
cd backend
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt >nul
start cmd /k "title Flask Backend & python server.py"
cd ..

:: 2️⃣ Start Ryu Controller
echo [2/4] Launching Ryu Controller...
start cmd /k "title Ryu Controller & ryu-manager ryu_app\controller_ai.py"

:: 3️⃣ Start Mininet Topology (Linux users only)
echo [3/4] Starting Mininet topology (requires Linux subsystem or VM)...
echo NOTE: Mininet cannot run natively on Windows.
echo If you have WSL/Ubuntu installed, run this command there:
echo     sudo python3 mininet/topology.py
echo.

:: 4️⃣ Start React Frontend
echo [4/4] Starting React Frontend...
cd frontend
if not exist node_modules (
    echo Installing frontend dependencies...
    npm install >nul
)
start cmd /k "title React Frontend & npm start"
cd ..

echo ============================================================
echo All services launched! Open your browser at:
echo    http://127.0.0.1:3000
echo ============================================================

pause
exit
