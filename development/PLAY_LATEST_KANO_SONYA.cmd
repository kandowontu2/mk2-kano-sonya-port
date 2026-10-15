@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Route the unversioned alias through the current native checked build.
call "%~dp0PLAY_CURRENT_NATIVE_CHECKED.cmd" %*
exit /b %errorlevel%

