$ErrorActionPreference='Stop'
$taskRoot="C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port"
$taskCase=Join-Path $taskRoot 'audit_current_os_audio_admission_runtime'
$taskBuild=Join-Path $taskRoot 'diagnostic_native_selector_layers_long'
$taskExe=Join-Path $taskBuild 'mkport_candidate.exe'
$taskLua=Join-Path $taskRoot 'audit_current_os_audio_admission_preparation/campaign.lua'
if(Test-Path -LiteralPath $taskCase){throw 'Never overwrite an executed case'}
if((Get-FileHash -LiteralPath $taskLua -Algorithm SHA256).Hash -ne 'C7D3065956A776A9A9B8706E0E3357587D7A19CE46CA7CE21334DD52029A3709'){throw 'Observer changed'}
if((Get-FileHash -LiteralPath $taskExe -Algorithm SHA256).Hash -ne 'EBDFEB6CCA3617308F1448A4A0F6778E3E787420CACF3D11E9B4F40358C87F6A'){throw 'Executable changed'}
foreach($taskName in @('MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES')){
 if([Environment]::GetEnvironmentVariable($taskName)){throw "Forbidden assistance: $taskName"}
}
New-Item -ItemType Directory -Path $taskCase | Out-Null
foreach($taskDir in @('cfg','nvram','snap')){New-Item -ItemType Directory -Path (Join-Path $taskCase $taskDir)|Out-Null}
$env:MK2KS_TEST_FIGHTER='sonya'
$env:MK2KS_CAMPAIGN_SIDE='2'
$env:MK2KS_CAMPAIGN_STRATEGY='leg'
$env:MK2KS_TEST_BOOT_FRAME='600'
$taskArgs=@('mk2ks','-rompath',"`"$taskBuild/roms;$taskRoot/roms`"",'-samplepath',"`"$taskBuild/samples;$taskRoot/samples`"",'-artpath',"`"$taskRoot/artwork`"",'-verbose','-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-inipath',"`"$taskCase`"",'-video','none','-sound','auto','-noautoframeskip','-frameskip','0','-throttle','-str','40','-snapsize','400x254','-wavwrite','NUL','-cfg_directory',"`"$taskCase/cfg`"",'-nvram_directory',"`"$taskCase/nvram`"",'-snapshot_directory',"`"$taskCase/snap`"",'-autoboot_script',"`"$taskLua`"")
$taskCOMSource=Join-Path $taskRoot 'tools/ReadOnlyAudioSession.cs'
if((Get-FileHash -LiteralPath $taskCOMSource -Algorithm SHA256).Hash -ne 'E9B922C55BA9B850BF709BD415289E58B9A49420721559130E965C3A97012808'){throw 'Read-only COM observer changed'}
Add-Type -Path $taskCOMSource
$taskLog=Join-Path $taskCase 'run.log'
$taskProcess=Start-Process -FilePath $taskExe -ArgumentList $taskArgs -WorkingDirectory $taskRoot -WindowStyle Hidden -RedirectStandardOutput $taskLog -RedirectStandardError (Join-Path $taskCase 'stderr.log') -PassThru
$taskBirth=$taskProcess.StartTime
$taskClock=[Diagnostics.Stopwatch]::StartNew()
$taskPeak=0L
$taskHostPeak=0L
$taskHost=[Diagnostics.Process]::GetCurrentProcess()
$taskAudioWriter=[IO.StreamWriter]::new((Join-Path $taskCase 'audio_sessions.jsonl'),$false)
$taskAudioClock=-1.0
$taskLimitReason=$null
while(-not $taskProcess.HasExited){
 $taskProcess.Refresh()
 $taskPeak=[Math]::Max($taskPeak,$taskProcess.WorkingSet64)
 $taskHost.Refresh();$taskHostPeak=[Math]::Max($taskHostPeak,$taskHost.WorkingSet64)
 if($taskHostPeak -gt 320MB){$taskLimitReason='host_memory_limit'}
 if($taskClock.Elapsed.TotalSeconds-$taskAudioClock -ge 0.5){
  $taskActual=Get-Process -Id $taskProcess.Id -ErrorAction SilentlyContinue
  if($taskActual -and $taskActual.StartTime -eq $taskBirth){
   $taskReadings=@([MK2OutputProbe.ReadOnly]::Snapshot([uint32]$taskProcess.Id))
   $taskAudioRow=[ordered]@{elapsedSeconds=$taskClock.Elapsed.TotalSeconds;pid=$taskProcess.Id;birth=$taskBirth.ToString('o');readings=$taskReadings;hostWorkingSetBytes=$taskHost.WorkingSet64}
   $taskAudioWriter.WriteLine(($taskAudioRow|ConvertTo-Json -Compress -Depth 5));$taskAudioWriter.Flush()
  }
  $taskAudioClock=$taskClock.Elapsed.TotalSeconds
 }

 if($taskPeak -gt 320MB){$taskLimitReason='memory_limit'}
 if($taskClock.Elapsed.TotalSeconds -gt 45){$taskLimitReason='wall_limit'}
 if((Get-Item -LiteralPath $taskLog).Length -gt 10MB){$taskLimitReason='log_limit'}
 if($taskLimitReason){
  $taskActual=Get-Process -Id $taskProcess.Id -ErrorAction SilentlyContinue
  if($taskActual -and $taskActual.StartTime -eq $taskBirth){Stop-Process -InputObject $taskActual -Force}
  break
 }
 Start-Sleep -Milliseconds 200
}
$taskAudioWriter.Dispose()
$taskProcess.WaitForExit()
$taskProcess.Refresh()
$taskReport=[ordered]@{pid=$taskProcess.Id;birth=$taskBirth.ToString('o');exitCode=$taskProcess.ExitCode;limitReason=$taskLimitReason;peakWorkingSetBytes=$taskPeak;elapsedSeconds=$taskClock.Elapsed.TotalSeconds;logBytes=(Get-Item -LiteralPath $taskLog).Length;hostPeakWorkingSetBytes=$taskHostPeak;rawMedia='none';osAudioSettingsModified=$false;soundProvider='auto';throttled=$true;acceptance=$false;observerSha256=(Get-FileHash -LiteralPath $taskLua).Hash}
$taskReport|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $taskCase 'terminal.json')
$taskReport|ConvertTo-Json -Compress
