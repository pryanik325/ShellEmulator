@echo off
cd /d "%~dp0\.."
echo Тест: параметр --script
py -m src.main --script "scripts/start_demo.txt"
pause