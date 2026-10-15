@echo off
setlocal
title Mortal Kombat II - Kano and Sonya (v1250 playtest)
cd /d "%~dp0"
rem Development playtest, not the final release. Keep older settings intact.
rem Clear diagnostic-only flags before normal play; no scripted inputs.
for /f "tokens=1 delims==" %%V in ('set MK2KS_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_TRACE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_RANGE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_P2_ 2^>nul') do set "%%V="
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\check_current_playtest_v1261.ps1"
if errorlevel 1 goto mismatch
"diagnostic_v1250_native_correct_rom_metadata\mkport_candidate.exe" mk2ks -rompath "diagnostic_v1250_native_correct_rom_metadata\roms;roms" -samplepath "samples" -artpath "artwork" -inipath "diagnostic_v1250_native_correct_rom_metadata\play" -cfg_directory "diagnostic_v1250_native_correct_rom_metadata\play\cfg" -nvram_directory "diagnostic_v1250_native_correct_rom_metadata\play\nvram" -snapshot_directory "diagnostic_v1250_native_correct_rom_metadata\play\snap" -nocheat %*
set "MK2_PLAY_EXIT=%errorlevel%"
if not "%MK2_PLAY_EXIT%"=="0" pause
exit /b %MK2_PLAY_EXIT%
:mismatch
echo ERROR: The current test executable and ROM payload are not a matched pair.
pause
exit /b 1
