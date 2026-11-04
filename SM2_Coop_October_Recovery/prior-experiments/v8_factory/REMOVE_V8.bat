@echo off
cd /d "%~dp0"
py -3 install_v8.py --remove
if errorlevel 1 python install_v8.py --remove
pause
