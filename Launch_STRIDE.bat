@echo off
title STRIDE - Tactical Decision Support System
cd /d "%~dp0"
echo =====================================================================
echo  Launching STRIDE Tactical Decision Engine v2.0...
echo  Air-Gapped Indian Defense UGV Evaluation Platform
echo =====================================================================
python src\main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Encountered an error launching STRIDE.
    pause
)
