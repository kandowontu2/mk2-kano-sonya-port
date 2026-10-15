@echo off
setlocal
title Mortal Kombat II - Kano and Sonya (v1411 playtest)
cd /d "%~dp0"
rem Current checked development build, not a finished release.
rem Keep older builds and settings intact; use no scripted inputs.
for /f "tokens=1 delims==" %%V in ('set MK2KS_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_TRACE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_RANGE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_P2_ 2^>nul') do set "%%V="
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\check_current_playtest_v1436.ps1"
if errorlevel 1 goto mismatch
"diagnostic_v1411_native_grab_audio\mkport_candidate.exe" mk2ks -rompath "diagnostic_v1411_native_grab_audio\roms;roms" -samplepath "samples" -artpath "artwork" -inipath "diagnostic_v1411_native_grab_audio\play" -cfg_directory "diagnostic_v1411_native_grab_audio\play\cfg" -nvram_directory "diagnostic_v1411_native_grab_audio\play\nvram" -snapshot_directory "diagnostic_v1411_native_grab_audio\play\snap" -nocheat %*
set "MK2_PLAY_EXIT=%errorlevel%"
if not "%MK2_PLAY_EXIT%"=="0" pause
exit /b %MK2_PLAY_EXIT%
:mismatch
echo ERROR: The current test executable and ROM payload are not a matched pair.
pause
exit /b 1
