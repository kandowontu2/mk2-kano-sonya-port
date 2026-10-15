$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskAudit=Join-Path $taskRoot 'audit_lean_player_actual_boot_20261015'
if(Test-Path -LiteralPath $taskAudit){throw 'Never overwrite boot case'}
$taskZip=Join-Path $taskRoot 'release_mk2_kano_sonya_20261015_player/MK2_Kano_Sonya_20261015_PLAYER.zip'
if((Get-FileHash -LiteralPath $taskZip).Hash -ne '3B6E59E9998EA2D3B03F0AFE8470DA4F98E417FFD2B6DFBE3D3C3DDC7C2ED342'){throw 'Player ZIP changed'}
$taskTemp=Join-Path $taskAudit 'temporary_extracted_package'
$taskExpected=[IO.Path]::GetFullPath($taskTemp)
if(-not $taskExpected.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Unsafe extraction'}
New-Item -ItemType Directory -Path $taskTemp -Force|Out-Null
Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::ExtractToDirectory($taskZip,$taskTemp)
$taskPlayer=Join-Path $taskTemp 'MK2_Kano_Sonya'
$taskExe=Join-Path $taskPlayer 'MK2_Kano_Sonya.exe'
if((Get-FileHash -LiteralPath $taskExe).Hash -ne 'EBDFEB6CCA3617308F1448A4A0F6778E3E787420CACF3D11E9B4F40358C87F6A'){throw 'Executable changed'}
$taskArgs=@('mk2ks','-rompath','roms','-samplepath','samples','-artpath','artwork','-samples','-samplerate','48000','-inipath','config','-cfg_directory','config/cfg','-nvram_directory','config/nvram','-snapshot_directory','config/snap','-nocheat','-skip_gameinfo','-video','none','-sound','none','-nothrottle','-str','3','-log')
$taskProcess=Start-Process -FilePath $taskExe -ArgumentList $taskArgs -WorkingDirectory $taskPlayer -WindowStyle Hidden -RedirectStandardOutput (Join-Path $taskAudit 'run.log') -RedirectStandardError (Join-Path $taskAudit 'stderr.log') -PassThru
$null=$taskProcess.Handle
$taskBirth=$taskProcess.StartTime
$taskClock=[Diagnostics.Stopwatch]::StartNew();$taskPeak=0L;$taskLimit=$null
while(-not $taskProcess.HasExited){
 $taskProcess.Refresh();$taskPeak=[Math]::Max($taskPeak,$taskProcess.WorkingSet64)
 if($taskPeak -gt 320MB){$taskLimit='memory320MiB'}
 if($taskClock.Elapsed.TotalSeconds -gt 30){$taskLimit='wall30sec'}
 if($taskLimit){if((Get-Process -Id $taskProcess.Id).StartTime -eq $taskBirth){Stop-Process -InputObject $taskProcess -Force};break}
 Start-Sleep -Milliseconds 100
}
$taskProcess.WaitForExit();$taskProcess.Refresh()
if($taskLimit -or $taskProcess.ExitCode -ne 0){throw 'Bounded actual boot failed; preserve extraction'}
$taskGameLog=Join-Path $taskPlayer 'error.log'
if(Test-Path -LiteralPath $taskGameLog){Copy-Item -LiteralPath $taskGameLog -Destination (Join-Path $taskAudit 'native.log')}
$taskStdout=Get-Content -LiteralPath (Join-Path $taskAudit 'run.log') -Raw
$taskErrors=Get-Content -LiteralPath (Join-Path $taskAudit 'stderr.log') -Raw
$taskNative=if(Test-Path -LiteralPath $taskGameLog){Get-Content -LiteralPath $taskGameLog -Raw}else{''}
if($taskErrors -or $taskStdout -notmatch 'Average speed:' -or ($taskStdout+$taskNative) -match 'Error opening sample|Error reading sample|Fatal error|NOT FOUND|incorrect length'){throw 'Actual native ROM/sample load error'}
$taskResolved=(Resolve-Path -LiteralPath $taskTemp).Path
if($taskResolved -ne $taskExpected -or (Get-Item -LiteralPath $taskResolved).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe temp cleanup'}
if(Get-ChildItem -LiteralPath $taskResolved -Recurse -Force|Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}){throw 'Linked temp descendant'}
if(Get-CimInstance Win32_Process|Where-Object {$_.ExecutablePath -and $_.ExecutablePath.StartsWith($taskResolved+'\',[StringComparison]::OrdinalIgnoreCase)}){throw 'Live temp executable'}
Remove-Item -LiteralPath $taskResolved -Recurse -Force
[ordered]@{actualNativeBootPassed=$true;romAndZippedSampleLoadingPassed=$true;guestSeconds=3;exitCode=$taskProcess.ExitCode;peakWorkingSetBytes=$taskPeak;elapsedSeconds=$taskClock.Elapsed.TotalSeconds;temporaryExtractionRemoved=(-not (Test-Path -LiteralPath $taskTemp));zipSHA256='3B6E59E9998EA2D3B03F0AFE8470DA4F98E417FFD2B6DFBE3D3C3DDC7C2ED342';scope='Actual cold boot with only packaged relative ROM/sample/art paths; no guest automation, recording or external asset fallback.'}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $taskAudit 'report.json')
Get-Content -LiteralPath (Join-Path $taskAudit 'report.json')
