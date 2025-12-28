@echo off
echo ===================================================
echo      Image Crawler - Installer
echo ===================================================
echo.
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/
    echo and make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

echo Python found. Launching install script...
python install.py
pause
