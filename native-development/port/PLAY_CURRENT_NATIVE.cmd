@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0check_native_launcher.ps1"
if errorlevel 1 exit /b 1
if /I "%~1"=="--check" exit /b 0
set "MK2KS_MAME=%~dp0..\..\..\mame0289\mame.exe"
set "MK2KS_ROMS=%~dp0development_patches\roundtrip\roms"
if not exist "%MK2KS_MAME%" (echo Stock MAME executable is missing.& pause& exit /b 1)
if not exist "%MK2KS_ROMS%\mk3.zip" (echo Patched development ROM set is missing.& pause& exit /b 1)
echo Native ROM development candidate - not a final release.
"%MK2KS_MAME%" mk3 -rompath "%MK2KS_ROMS%" -cfg_directory "%~dp0development_patches\play_config\cfg" -nvram_directory "%~dp0development_patches\play_config\nvram" -snapshot_directory "%~dp0development_patches\play_config\snap" -nocheat %*
endlocal
