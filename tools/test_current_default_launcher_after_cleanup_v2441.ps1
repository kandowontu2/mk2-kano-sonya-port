$ErrorActionPreference='Stop'
$taskRoot=(Get-Item -LiteralPath (Split-Path $PSScriptRoot -Parent)).FullName
$taskOut=Join-Path $taskRoot 'audit_v2442_current_default_launcher_after_cleanup_checked'
if(Test-Path -LiteralPath $taskOut){throw 'Immutable default launcher proof'}
$taskOuter='C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\PLAY_MK2_KANO_SONYA.cmd'
$taskDefault=Join-Path $taskRoot 'PLAY_MK2_KANO_SONYA.cmd'
$taskInner=Join-Path $taskRoot 'PLAY_CURRENT_V1836_CHECKED.cmd'
$taskChecker=Join-Path $taskRoot 'tools\check_ball_register_playtest_v1849.ps1'
$taskCandidate=Join-Path $taskRoot 'diagnostic_v1836_ball_register_boundary'
$taskExe=Join-Path $taskCandidate 'mkport_candidate.exe'
$taskBackup=Join-Path $taskRoot 'audit_v2414_current_default_launcher_before\PLAY_MK2_KANO_SONYA_v277.cmd'
$taskExpected=@{
 $taskBackup='9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7'
 $taskDefault='631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7'
 $taskOuter='C94CFA01D231BE90597DF799FC8043FCAA18ED467886B347A984B32BFABC91B7'
 $taskInner='ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E'
 $taskExe='34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E'
 (Join-Path $taskCandidate 'roms\mk2ks\mk2ks.mdata')='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D'
}
$taskHashes=@{}
foreach($taskFile in $taskExpected.Keys){
 $taskActual=(Get-FileHash -LiteralPath $taskFile).Hash
 if($taskActual -ne $taskExpected[$taskFile]){throw "Wrong current/legacy launcher or playable pair: $taskFile"}
 $taskHashes[$taskFile]=$taskActual
}
foreach($taskFile in @($PSCommandPath,$taskChecker,(Join-Path $taskCandidate 'build-info.json'))){$taskHashes[$taskFile]=(Get-FileHash -LiteralPath $taskFile).Hash}
$taskDefaultText=Get-Content -LiteralPath $taskDefault -Raw
if($taskDefaultText -notmatch 'set "MK2_CANDIDATE_CMD=%~dp0PLAY_CURRENT_V1836_CHECKED\.cmd"' -or $taskDefaultText -notmatch 'call "%MK2_CANDIDATE_CMD%" %\*'){throw 'Default launcher does not forward all user options to checked current build'}
$taskOuterText=Get-Content -LiteralPath $taskOuter -Raw
if($taskOuterText -notmatch [regex]::Escape($taskRoot) -or $taskOuterText -notmatch 'call "%MK2_PORT%\\PLAY_MK2_KANO_SONYA\.cmd" %\*'){throw 'Outer launcher does not enter this workspace'}
$taskSettings=@{}
$taskPlay=Join-Path $taskCandidate 'play'
if(Test-Path -LiteralPath $taskPlay){
 foreach($taskFile in @(Get-ChildItem -LiteralPath $taskPlay -Recurse -File)){ $taskSettings[$taskFile.FullName]=(Get-FileHash -LiteralPath $taskFile.FullName).Hash }
}
New-Item -ItemType Directory -Path $taskOut | Out-Null
foreach($taskName in @('ini','cfg','nvram','snap')){New-Item -ItemType Directory -Path (Join-Path $taskOut $taskName) | Out-Null}
$taskArgs='/d /s /c ""{0}" -video none -sound none -str 12 -nothrottle -inipath "{1}\ini" -cfg_directory "{1}\cfg" -nvram_directory "{1}\nvram" -snapshot_directory "{1}\snap""' -f $taskOuter,$taskOut
$taskProcess=Start-Process -FilePath $env:ComSpec -ArgumentList $taskArgs -WorkingDirectory (Split-Path $taskOuter -Parent) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $taskOut 'run.log') -RedirectStandardError (Join-Path $taskOut 'run-error.log') -PassThru
$taskObserved=@();$taskWatch=[Diagnostics.Stopwatch]::StartNew()
while(-not $taskProcess.HasExited -and $taskWatch.Elapsed.TotalSeconds -lt 90){
 foreach($taskChild in @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($taskProcess.Id)" | Where-Object Name -eq 'mkport_candidate.exe')){
  $taskObserved+=@([ordered]@{processId=$taskChild.ProcessId;parentProcessId=$taskChild.ParentProcessId;executablePath=$taskChild.ExecutablePath;commandLine=$taskChild.CommandLine})
 }
 Start-Sleep -Milliseconds 100;$taskProcess.Refresh()
}
if(-not $taskProcess.HasExited){throw 'Default launcher still live after bounded observation; preserve process/evidence and inspect it, do not restart'}
$taskProcess.WaitForExit();$taskCode=$taskProcess.ExitCode
foreach($taskFile in $taskHashes.Keys){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskHashes[$taskFile]){throw "Changed default launch input: $taskFile"}}
foreach($taskFile in $taskSettings.Keys){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskSettings[$taskFile]){throw "User current-build setting changed: $taskFile"}}
$taskSettingsAfter=if(Test-Path -LiteralPath $taskPlay){@(Get-ChildItem -LiteralPath $taskPlay -Recurse -File | ForEach-Object FullName)}else{@()}
if(@($taskSettingsAfter).Count -ne $taskSettings.Count){throw 'User current-build settings file set changed'}
$taskLog=(Get-Content -LiteralPath (Join-Path $taskOut 'run.log') -Raw)+(Get-Content -LiteralPath (Join-Path $taskOut 'run-error.log') -Raw)
$taskCompleteSnapshots=@($taskObserved | Where-Object { -not [string]::IsNullOrWhiteSpace($_.executablePath) })
$taskIncompleteSnapshots=@($taskObserved | Where-Object { [string]::IsNullOrWhiteSpace($_.executablePath) })
$taskPassed=$taskCode -eq 0 -and $taskCompleteSnapshots.Count -gt 0 -and $taskLog -match 'Average speed:.*\(11 seconds\)' -and $taskLog -notmatch 'WRONG CHECKSUMS|might not run correctly|\[LUA ERROR\]|fatal error|access violation|MK2_NAT_CAMPAIGN_'
foreach($taskChild in $taskObserved){
 if(-not [string]::IsNullOrWhiteSpace($taskChild.executablePath) -and -not [string]::Equals($taskChild.executablePath,$taskExe,[StringComparison]::OrdinalIgnoreCase)){ $taskPassed=$false }
 if($taskChild.commandLine -notmatch '-nocheat' -or $taskChild.commandLine -match '-autoboot_script|-debugscript'){ $taskPassed=$false }
 # A null early CIM path is unknown, not an accepted path. Every observed
 # PID must later have a complete expected executable-path observation.
 if(-not @($taskCompleteSnapshots | Where-Object { $_.processId -eq $taskChild.processId -and $_.parentProcessId -eq $taskChild.parentProcessId }).Count){ $taskPassed=$false }
}
foreach($taskFile in $taskSettings.Keys){$taskHashes[$taskFile]=$taskSettings[$taskFile]}
foreach($taskFile in @(Get-ChildItem -LiteralPath $taskOut -Recurse -File)){$taskHashes[$taskFile.FullName]=(Get-FileHash -LiteralPath $taskFile.FullName).Hash}
$taskReport=[ordered]@{afterVerifiedSixOldBuildRemoval=$true;passed=$taskPassed;exit_code=$taskCode;candidate='diagnostic_v1836_ball_register_boundary';defaultLauncher=$taskDefault;outerLauncher=$taskOuter;checkedVersionedLauncher=$taskInner;oldV277LauncherBackup=$taskBackup;observedActualProcesses=$taskObserved;completeExecutablePathSnapshots=$taskCompleteSnapshots.Count;unknownEarlyCIMPathSnapshots=$taskIncompleteSnapshots.Count;everyObservedPIDHasCompleteExpectedPath=$taskPassed;ordinaryBootFromOuterWorkingDirectory=$true;seconds=12;diagnosticAutobootUsed=$false;settingsIsolated=$true;userSettingsFilesPreserved=$taskSettings.Count;defaultTargetChangedFromV277ToV1836=$true;historicalV1852DefaultLauncherHashCheckSuperseded=$true;gameExecutableAndPayloadChanged=$false;inputHashes=$taskHashes;fullPortAcceptance=$false;scope='Actual outer CMD to public default CMD to guarded current1836 EXE/ROM boot; headless smoke, not full interactive video/audio/gameplay/release acceptance'}
$taskReport | ConvertTo-Json -Depth 7 | Out-File -LiteralPath (Join-Path $taskOut 'report.json') -Encoding utf8
if(-not $taskPassed){throw "Default launcher verification failed: exit=$taskCode; observed=$($taskObserved.Count)"}
[ordered]@{passed=$true;actualDefaultBuild='v1836';observedActualProcessSnapshots=$taskObserved.Count;userSettingsPreserved=$true;gameBytesChanged=$false;fullPortAcceptance=$false} | ConvertTo-Json
