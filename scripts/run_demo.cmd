@echo off
setlocal
cd /d "%~dp0\.."
set PIP_DISABLE_PIP_VERSION_CHECK=1
if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
)
".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt
".venv\Scripts\python.exe" -m pip install --quiet -e .
".venv\Scripts\python.exe" -m factory_production_notice.cli run-demo --output output
echo.
echo Demo generated in output\
