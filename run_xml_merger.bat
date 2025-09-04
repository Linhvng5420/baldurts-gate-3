@echo off
echo Starting XML Merger App...
echo.

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "venv\Scripts\activate.bat"
)

REM Run the XML merger app
python xml_merger.py

echo.
echo XML Merger App closed.
pause
