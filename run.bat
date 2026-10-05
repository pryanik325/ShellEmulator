@echo off
cd /d "%~dp0"
py -m src.main %*
if errorlevel 1 pause