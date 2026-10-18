@echo off
cd /d "%~dp0"
set "MK2KS_MAME=%~1"
if not defined MK2KS_MAME set "MK2KS_MAME=%~dp0mame.exe"
if not exist "%MK2KS_MAME%" (echo Supply a stock MAME executable path.& pause& exit /b 1)
if not exist "%~dp0roms\mk3.zip" (echo Run PATCH.cmd first.& pause& exit /b 1)
"%MK2KS_MAME%" mk3 -rompath "%~dp0roms" -cfg_directory "%~dp0config\cfg" -nvram_directory "%~dp0config\nvram" -snapshot_directory "%~dp0config\snap"
