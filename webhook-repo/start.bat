@echo off
REM GitHub Webhook Monitor - Quick Start Script for Windows

echo 🚀 Starting GitHub Webhook Monitor...
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found. Please create .env file with DATABASE_URL
    echo    Example: DATABASE_URL=postgresql://user:password@localhost:5432/webhook_db
    pause
    exit /b 1
)

REM Check if DATABASE_URL is set
findstr /C:"DATABASE_URL" .env >nul 2>&1
if errorlevel 1 (
    echo ❌ DATABASE_URL not found in .env file
    echo    Please add: DATABASE_URL=postgresql://user:password@localhost:5432/webhook_db
    pause
    exit /b 1
)

REM Start the Flask application
echo 🌟 Starting Flask application...
echo    Dashboard: http://localhost:5000
echo    Webhook endpoint: http://localhost:5000/webhook
echo    Health check: http://localhost:5000/health
echo.
echo 💡 To test webhooks locally, use ngrok:
echo    ngrok http 5000
echo.
echo 🧪 To run tests:
echo    python test_webhook.py
echo.
echo Press Ctrl+C to stop the server
echo ==================================

python app_postgres.py

pause
