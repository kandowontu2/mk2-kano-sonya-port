@echo off
rem Current v786 native-integration playtest, NOT the final release.
call "%~dp0diagnostic_v786_native_fighter_fade_exclusions\PLAY_TEST_BUILD.cmd" %*
exit /b %errorlevel%
