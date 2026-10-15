@echo off
setlocal EnableExtensions DisableDelayedExpansion
title Mortal Kombat II - Kano and Sonya (current native playtest)
cd /d "%~dp0"
if errorlevel 1 exit /b 1
if /I "%~1"=="--check" goto check_only
rem Ordinary play only; clear inherited diagnostic switches.
for /f "tokens=1 delims==" %%V in ('set MK2KS_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_TRACE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_RANGE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_P2_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2PORT_ 2^>nul') do set "%%V="
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\check_current_native_playtest.ps1"
if errorlevel 1 goto mismatch
"diagnostic_native_selector_layers_long\mkport_candidate.exe" mk2ks -rompath "diagnostic_native_selector_layers_long\roms;roms" -samplepath "diagnostic_native_selector_layers_long\samples;samples" -artpath "artwork" -samples -samplerate 48000 -inipath "play_v5219_checked" -cfg_directory "play_v5219_checked\cfg" -nvram_directory "play_v5219_checked\nvram" -snapshot_directory "play_v5219_checked\snap" -nocheat %*
set "MK2_CURRENT_EXIT=%errorlevel%"
if not "%MK2_CURRENT_EXIT%"=="0" pause
exit /b %MK2_CURRENT_EXIT%
:check_only
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\check_current_native_playtest.ps1"
exit /b %errorlevel%
:mismatch
echo ERROR: Current game files are missing or changed. This is a work-in-progress.
pause
exit /b 1
