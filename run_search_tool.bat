@echo off
echo Checking Python installation...

python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/Updating required packages...
python -m pip install --upgrade pip
python -m pip install tkinterdnd2

echo Starting Search Tool...
python "src\Search Tool\search-tool.py"
if errorlevel 1 (
    echo An error occurred while running the application
    pause
)

deactivate
pause