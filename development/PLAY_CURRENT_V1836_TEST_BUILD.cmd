@echo off
setlocal
title Mortal Kombat II - Kano and Sonya (v1836 playtest)
cd /d "%~dp0"
rem Current checked development build, not a finished release.
rem Older builds and settings stay intact; no scripted inputs are used.
for /f "tokens=1 delims==" %%V in ('set MK2KS_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_TRACE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_RANGE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_P2_ 2^>nul') do set "%%V="
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\check_ball_register_playtest_v1849.ps1"
if errorlevel 1 goto mismatch
"diagnostic_v1836_native_ground_throw\mkport_candidate.exe" mk2ks -rompath "diagnostic_v1836_native_ground_throw\roms;roms" -samplepath "samples" -artpath "artwork" -inipath "diagnostic_v1836_native_ground_throw\play" -cfg_directory "diagnostic_v1836_native_ground_throw\play\cfg" -nvram_directory "diagnostic_v1836_native_ground_throw\play\nvram" -snapshot_directory "diagnostic_v1836_native_ground_throw\play\snap" -nocheat %*
set "MK2_PLAY_EXIT=%errorlevel%"
if not "%MK2_PLAY_EXIT%"=="0" pause
exit /b %MK2_PLAY_EXIT%
:mismatch
echo ERROR: The current executable, ROM payload or voice assets are missing or changed.
pause
exit /b 1
