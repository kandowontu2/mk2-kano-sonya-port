@echo off
setlocal
title Mortal Kombat II - Kano and Sonya (current checked playtest)

rem Use the current native tested build; versioned launchers remain available.
rem The versioned launcher validates the matched EXE, ROM and voice assets.
rem This remains a playable work-in-progress, not the final release package.
set "MK2_CANDIDATE_CMD=%~dp0PLAY_CURRENT_NATIVE_CHECKED.cmd"
if not exist "%MK2_CANDIDATE_CMD%" (
    echo ERROR: The current checked Kano/Sonya launcher is missing.
    pause
    exit /b 1
)

call "%MK2_CANDIDATE_CMD%" %*
exit /b %ERRORLEVEL%
