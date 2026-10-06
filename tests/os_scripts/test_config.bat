@echo off
cd /d "%~dp0\.."
echo Тест: параметр --config
py -m src.main --config "config/example.toml"
pause