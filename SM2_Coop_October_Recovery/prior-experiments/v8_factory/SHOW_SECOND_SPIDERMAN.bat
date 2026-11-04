@echo off
cd /d "%~dp0"
py -3 second_spiderman_button.py
if errorlevel 1 python second_spiderman_button.py
pause
