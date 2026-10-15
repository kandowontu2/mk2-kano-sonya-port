@echo off
setlocal
title Mortal Kombat II - Kano and Sonya (v5219 checked playtest)
cd /d "%~dp0"
rem Current tested candidate, not the final release. No scripted inputs.
rem Keep the older launcher, ZIP and user settings unchanged.
for /f "tokens=1 delims==" %%V in ('set MK2KS_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_TRACE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_RANGE_ 2^>nul') do set "%%V="
for /f "tokens=1 delims==" %%V in ('set MK2_P2_ 2^>nul') do set "%%V="
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\check_current_playtest_v5975.ps1"
if errorlevel 1 goto mismatch
"diagnostic_v5219_current_payload_rom_metadata\mkport_candidate.exe" mk2ks -rompath "diagnostic_v5219_current_payload_rom_metadata\roms;roms" -samplepath "samples" -artpath "artwork" -samples -samplerate 48000 -inipath "play_v5219_checked" -cfg_directory "play_v5219_checked\cfg" -nvram_directory "play_v5219_checked\nvram" -snapshot_directory "play_v5219_checked\snap" -nocheat %*
set "MK2_PLAY_EXIT=%errorlevel%"
if not "%MK2_PLAY_EXIT%"=="0" pause
exit /b %MK2_PLAY_EXIT%
:mismatch
echo ERROR: The tested executable, ROM payload or voice assets are missing or changed.
pause
exit /b 1
