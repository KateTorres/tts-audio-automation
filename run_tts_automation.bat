@echo off
REM Navigate to the script directory
cd /d "%~dp0"

REM Display Python version for confirmation
python --version

REM Run the main Python script
echo Running TTS Audio Automation...
python main.py

REM Pause to review the output (optional)
pause