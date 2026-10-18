@echo off
cd /d "%~dp0"
if "%~2"=="" (echo Usage: PATCH.cmd "path\mk2.zip" "path\mk3.zip"& pause& exit /b 1)
py -3 patch_native_roms.py --mk2 "%~1" --mk3 "%~2" --output "%~dp0roms\mk3.zip"
if errorlevel 1 (echo PATCH FAILED& pause& exit /b 1)
echo DEVELOPMENT ROM SET CREATED
pause
