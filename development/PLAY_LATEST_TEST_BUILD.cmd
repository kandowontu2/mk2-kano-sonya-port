@echo off
setlocal
rem Current checked playtest, NOT a finished release.
rem Explicitly versioned launchers and their saved settings remain unchanged.
if not exist "%~dp0PLAY_MK2_KANO_SONYA.cmd" (
    echo ERROR: The current Kano/Sonya playtest launcher is missing.
    pause
    exit /b 1
)
call "%~dp0PLAY_MK2_KANO_SONYA.cmd" %*
exit /b %errorlevel%
