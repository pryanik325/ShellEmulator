@echo off
cd /d "%~dp0\.."
echo Тест: параметр --vfs
py -m src.main --vfs "vfs/minimal"
pause