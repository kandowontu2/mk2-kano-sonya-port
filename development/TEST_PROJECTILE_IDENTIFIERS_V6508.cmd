@echo off
setlocal
cd /d "%~dp0"
rem Isolated unpromoted candidate, never replaces the public play launcher.
"diagnostic_v6508_native_projectile_identifiers\mkport_candidate.exe" mk2ks -rompath "diagnostic_v6508_native_projectile_identifiers\roms;roms" -samplepath "samples" -artpath "artwork" -samples -samplerate 48000 -inipath "play_v5219_checked" -nocheat %*
exit /b %errorlevel%
