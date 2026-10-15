@echo off
setlocal
cd /d "%~dp0"
rem Isolated unpromoted Kano startup-cue candidate. Ordinary launcher unchanged.
"diagnostic_v6640_kano_ball_launch\mkport_candidate.exe" mk2ks -rompath "diagnostic_v6640_kano_ball_launch\roms;roms" -samplepath "diagnostic_v6640_kano_ball_launch\samples;samples" -artpath "artwork" -samples -samplerate 48000 -inipath "play_v5219_checked" -nocheat %*
exit /b %errorlevel%
