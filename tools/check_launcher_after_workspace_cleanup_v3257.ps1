$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskOut=Join-Path $taskRoot 'audit_v3258_current_launcher_after_workspace_cleanup'
if(Test-Path -LiteralPath $taskOut){throw 'Immutable launcher check'}
$taskOuter='C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\PLAY_MK2_KANO_SONYA.cmd'
$taskFiles=@($taskOuter,(Join-Path $taskRoot 'PLAY_MK2_KANO_SONYA.cmd'),(Join-Path $taskRoot 'PLAY_CURRENT_V1836_CHECKED.cmd'),
    (Join-Path $taskRoot 'tools\check_ball_register_playtest_v1849.ps1'),
    (Join-Path $taskRoot 'diagnostic_v1836_ball_register_boundary\mkport_candidate.exe'),
    (Join-Path $taskRoot 'diagnostic_v1836_ball_register_boundary\roms\mk2ks\mk2ks.mdata'),
    (Join-Path $taskRoot 'diagnostic_v3172_native_morph_shadow\mkport_candidate.exe'),
    (Join-Path $taskRoot 'release_v1863_current_playtest\MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip'))
$taskHashes=@{};foreach($taskFile in $taskFiles){$taskHashes[$taskFile]=(Get-FileHash -LiteralPath $taskFile).Hash}
$taskPlay=Join-Path $taskRoot 'diagnostic_v1836_ball_register_boundary\play'
$taskSettings=@{};foreach($taskFile in Get-ChildItem -LiteralPath $taskPlay -Recurse -File -Force){$taskSettings[$taskFile.FullName]=(Get-FileHash -LiteralPath $taskFile.FullName).Hash}
New-Item -ItemType Directory -Path $taskOut | Out-Null
foreach($taskName in @('ini','cfg','nvram','snap')){New-Item -ItemType Directory -Path (Join-Path $taskOut $taskName) | Out-Null}
$taskArgs='/d /s /c ""{0}" -video none -sound none -str 12 -nothrottle -inipath "{1}\ini" -cfg_directory "{1}\cfg" -nvram_directory "{1}\nvram" -snapshot_directory "{1}\snap""' -f $taskOuter,$taskOut
$taskProcess=Start-Process -FilePath $env:ComSpec -ArgumentList $taskArgs -WorkingDirectory (Split-Path $taskOuter -Parent) -WindowStyle Hidden -RedirectStandardOutput "$taskOut\run.log" -RedirectStandardError "$taskOut\run-error.log" -PassThru
$taskTimer=[Diagnostics.Stopwatch]::StartNew()
while(-not $taskProcess.HasExited -and $taskTimer.Elapsed.TotalSeconds -lt 90){Start-Sleep -Milliseconds 200;$taskProcess.Refresh()}
if(-not $taskProcess.HasExited){throw 'Launcher smoke is still running; preserve and inspect, never restart blindly'}
$taskProcess.WaitForExit()
$taskLog=(Get-Content -LiteralPath "$taskOut\run.log" -Raw)+(Get-Content -LiteralPath "$taskOut\run-error.log" -Raw)
$taskPassed=$taskProcess.ExitCode -eq 0 -and $taskLog -match 'Average speed:.*\(11 seconds\)' -and $taskLog -notmatch 'WRONG CHECKSUMS|might not run correctly|\[LUA ERROR\]|fatal error|access violation'
foreach($taskFile in $taskHashes.Keys){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskHashes[$taskFile]){throw 'Playable or launcher input changed'}}
foreach($taskFile in $taskSettings.Keys){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskSettings[$taskFile]){throw 'User setting changed'}}
if(@(Get-ChildItem -LiteralPath $taskPlay -Recurse -File -Force).Count -ne $taskSettings.Count){throw 'User settings file set changed'}
$taskReport=[ordered]@{passed=$taskPassed;exitCode=$taskProcess.ExitCode;defaultBuild='diagnostic_v1836_ball_register_boundary';
    outerCMD=$taskOuter;seconds=12;headlessBootOnly=$true;userSettingsFilesUnchanged=$taskSettings.Count;
    currentPlayableLatestCandidateAndZIPHashesUnchanged=$true;preservedHashes=$taskHashes;fullPortAcceptance=$false}
$taskReport | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$taskOut\report.json" -Encoding utf8
if(-not $taskPassed){throw 'Outer CMD boot check failed; inspect retained logs'}
[ordered]@{passed=$true;defaultBuild='v1836';userSettingsUnchanged=$true;headlessBootOnly=$true} | ConvertTo-Json
