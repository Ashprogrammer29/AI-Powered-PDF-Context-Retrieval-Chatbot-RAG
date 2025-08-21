@echo off
echo Testing AI-Powered Loan Risk Scoring API...
echo ==========================================

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install test dependencies
pip install requests

REM Run the test script
python test_api.py

pause
