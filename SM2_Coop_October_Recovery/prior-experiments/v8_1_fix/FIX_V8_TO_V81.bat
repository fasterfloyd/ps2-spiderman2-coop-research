@echo off
cd /d "%~dp0"
py -3 FIX_V8_TO_V81.py
if errorlevel 1 python FIX_V8_TO_V81.py
pause
