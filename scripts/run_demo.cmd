@echo off
setlocal
cd /d "%~dp0\.."
if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
".venv\Scripts\python.exe" -m pip install -e .
".venv\Scripts\python.exe" -m factory_production_notice.cli run-demo --output output
echo.
echo Demo generated in output\
