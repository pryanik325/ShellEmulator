@echo off
cd /d "%~dp0\.."
echo Тест: все параметры сразу
py -m src.main --vfs "vfs/from_cli" --script "scripts/start_demo.txt" --config "config/example.toml"
pause