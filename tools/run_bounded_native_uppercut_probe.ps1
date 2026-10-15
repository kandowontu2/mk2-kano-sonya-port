$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskCase=Join-Path $taskRoot 'audit_bounded_native_uppercut_runtime'
$taskBuild=Join-Path $taskRoot 'diagnostic_native_selector_layers_long'
$taskExe=Join-Path $taskBuild 'mkport_candidate.exe'
$taskLua=Join-Path $taskRoot 'audit_bounded_native_uppercut_owners_bound_preparation/prepared_observer.lua'
if(Test-Path -LiteralPath $taskCase){throw 'Never overwrite an executed case'}
if((Get-FileHash -LiteralPath $taskLua -Algorithm SHA256).Hash -ne '92F2EBD73A57733ED7638FE90D78F57B10CD238742BB6F02C49BE0123323DE94'){throw 'Observer changed'}
if((Get-FileHash -LiteralPath $taskExe -Algorithm SHA256).Hash -ne 'EBDFEB6CCA3617308F1448A4A0F6778E3E787420CACF3D11E9B4F40358C87F6A'){throw 'Executable changed'}
foreach($taskName in @('MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES')){
 if([Environment]::GetEnvironmentVariable($taskName)){throw "Forbidden assistance: $taskName"}
}
New-Item -ItemType Directory -Path $taskCase | Out-Null
foreach($taskDir in @('cfg','nvram','snap')){New-Item -ItemType Directory -Path (Join-Path $taskCase $taskDir)|Out-Null}
$env:MK2KS_TEST_FIGHTER='kano'
$env:MK2KS_CPU_PAIR_APPROACH='original'
$env:MK2KS_CPU_CONTINUATION_POLICY='neutral_hold'
$taskArgs=@('mk2ks','-rompath',"`"$taskBuild/roms;$taskRoot/roms`"",'-samplepath',"`"$taskBuild/samples;$taskRoot/samples`"",'-artpath',"`"$taskRoot/artwork`"",'-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-inipath',"`"$taskCase`"",'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','100','-wavwrite','NUL','-cfg_directory',"`"$taskCase/cfg`"",'-nvram_directory',"`"$taskCase/nvram`"",'-snapshot_directory',"`"$taskCase/snap`"",'-autoboot_script',"`"$taskLua`"")
$taskLog=Join-Path $taskCase 'run.log'
$taskProcess=Start-Process -FilePath $taskExe -ArgumentList $taskArgs -WorkingDirectory $taskRoot -WindowStyle Hidden -RedirectStandardOutput $taskLog -RedirectStandardError (Join-Path $taskCase 'stderr.log') -PassThru
$taskBirth=$taskProcess.StartTime
$taskClock=[Diagnostics.Stopwatch]::StartNew()
$taskPeak=0L
$taskLimitReason=$null
while(-not $taskProcess.HasExited){
 $taskProcess.Refresh()
 $taskPeak=[Math]::Max($taskPeak,$taskProcess.WorkingSet64)
 if($taskPeak -gt 320MB){$taskLimitReason='memory_limit'}
 if($taskClock.Elapsed.TotalSeconds -gt 90){$taskLimitReason='wall_limit'}
 if((Get-Item -LiteralPath $taskLog).Length -gt 10MB){$taskLimitReason='log_limit'}
 if($taskLimitReason){
  $taskActual=Get-Process -Id $taskProcess.Id -ErrorAction SilentlyContinue
  if($taskActual -and $taskActual.StartTime -eq $taskBirth){Stop-Process -InputObject $taskActual -Force}
  break
 }
 Start-Sleep -Milliseconds 200
}
$taskProcess.WaitForExit()
$taskProcess.Refresh()
$taskReport=[ordered]@{pid=$taskProcess.Id;birth=$taskBirth.ToString('o');exitCode=$taskProcess.ExitCode;limitReason=$taskLimitReason;peakWorkingSetBytes=$taskPeak;elapsedSeconds=$taskClock.Elapsed.TotalSeconds;logBytes=(Get-Item -LiteralPath $taskLog).Length;rawMedia='none';acceptance=$false;observerSha256=(Get-FileHash -LiteralPath $taskLua).Hash}
$taskReport|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $taskCase 'terminal.json')
$taskReport|ConvertTo-Json -Compress
