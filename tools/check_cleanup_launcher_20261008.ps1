$ErrorActionPreference = 'Stop'
$taskRoot = (Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskOut = Join-Path $taskRoot 'workspace_cleanup_2026-10-08\launcher_check'
if (Test-Path -LiteralPath $taskOut) { throw 'Never overwrite a launcher check' }
$taskCleanup = Get-Content -LiteralPath (Join-Path $taskRoot 'workspace_cleanup_2026-10-08\result.json') -Raw | ConvertFrom-Json
if (-not $taskCleanup.passed -or -not $taskCleanup.preservedPlayableAndSourceHashesUnchanged) { throw 'Completed verified cleanup required' }
$taskOuter = 'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\PLAY_MK2_KANO_SONYA.cmd'
$taskOuterHash = (Get-FileHash -LiteralPath $taskOuter).Hash
$taskPlay = Join-Path $taskRoot 'diagnostic_v1836_ball_register_boundary\play'
$taskSettings = @{}
foreach ($taskFile in Get-ChildItem -LiteralPath $taskPlay -Recurse -File -Force) { $taskSettings[$taskFile.FullName] = (Get-FileHash -LiteralPath $taskFile.FullName).Hash }
New-Item -ItemType Directory -Path $taskOut | Out-Null
foreach ($taskName in @('ini','cfg','nvram','snap')) { New-Item -ItemType Directory -Path (Join-Path $taskOut $taskName) | Out-Null }
$taskArgs = '/d /s /c ""{0}" -video none -sound none -str 12 -nothrottle -inipath "{1}\ini" -cfg_directory "{1}\cfg" -nvram_directory "{1}\nvram" -snapshot_directory "{1}\snap""' -f $taskOuter,$taskOut
$taskProcess = Start-Process -FilePath $env:ComSpec -ArgumentList $taskArgs -WorkingDirectory (Split-Path $taskOuter -Parent) -WindowStyle Hidden -RedirectStandardOutput "$taskOut\run.log" -RedirectStandardError "$taskOut\run-error.log" -PassThru
$taskTimer = [Diagnostics.Stopwatch]::StartNew()
while (-not $taskProcess.HasExited -and $taskTimer.Elapsed.TotalSeconds -lt 60) { Start-Sleep -Milliseconds 200; $taskProcess.Refresh() }
if (-not $taskProcess.HasExited) { throw 'Launcher remains running; inspect without starting another' }
$taskProcess.WaitForExit()
$taskLog = (Get-Content -LiteralPath "$taskOut\run.log" -Raw) + (Get-Content -LiteralPath "$taskOut\run-error.log" -Raw)
$taskPassed = $taskProcess.ExitCode -eq 0 -and $taskLog -match 'Average speed:.*\(11 seconds\)' -and $taskLog -notmatch 'WRONG CHECKSUMS|might not run correctly|\[LUA ERROR\]|fatal error|access violation'
if ((Get-FileHash -LiteralPath $taskOuter).Hash -ne $taskOuterHash) { throw 'Outer CMD changed' }
foreach ($taskFile in $taskSettings.Keys) { if ((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskSettings[$taskFile]) { throw 'User setting changed' } }
if (@(Get-ChildItem -LiteralPath $taskPlay -Recurse -File -Force).Count -ne $taskSettings.Count) { throw 'User settings file set changed' }
$taskResult = [ordered]@{ passed=$taskPassed; exitCode=$taskProcess.ExitCode; defaultBuild='diagnostic_v1836_ball_register_boundary'; seconds=12; headlessBootOnly=$true; userSettingsUnchanged=$true; outerCMDUnchanged=$true; fullPortAcceptance=$false }
$taskResult | ConvertTo-Json | Out-File -LiteralPath "$taskOut\report.json" -Encoding utf8
if (-not $taskPassed) { throw 'Launcher boot check failed; retained logs require inspection' }
$taskResult | ConvertTo-Json
