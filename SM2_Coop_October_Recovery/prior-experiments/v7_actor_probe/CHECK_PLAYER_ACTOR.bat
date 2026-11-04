@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 probe_spidermanx.py
) else (
  python probe_spidermanx.py
)
pause
