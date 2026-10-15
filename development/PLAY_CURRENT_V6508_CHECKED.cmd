@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Compatibility entry point: the obsolete v6508 executable was retired.
call "%~dp0PLAY_CURRENT_NATIVE_CHECKED.cmd" %*
exit /b %errorlevel%
