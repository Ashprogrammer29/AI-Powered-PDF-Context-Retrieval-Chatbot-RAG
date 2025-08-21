@echo off
echo Starting AI-Powered Loan Risk Scoring API...
echo ==========================================

REM Check if virtual environment exists
if not exist venv\ (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Start the API server
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo ==========================================
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause