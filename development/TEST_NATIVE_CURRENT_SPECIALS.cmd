@echo off
setlocal
cd /d "%~dp0"
"diagnostic_native_ai_response\mkport_candidate.exe" mk2ks -rompath "diagnostic_native_ai_response\roms;roms" -samplepath "diagnostic_native_ai_response\samples;samples" -artpath "artwork" -samples -samplerate 48000 -inipath "play_v5219_checked" -nocheat %*
exit /b %errorlevel%
