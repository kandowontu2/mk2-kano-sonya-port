$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskZip=Join-Path $taskRoot 'release_current_native_playtest_20261013_complete_roms\MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip'
if((Get-FileHash -LiteralPath $taskZip).Hash -ne 'EDAC17A71DC7353ABC35C32D914E8248DB7804DCA6F9AA3A24B9B25EDF2797B7'){throw 'Archive changed'}
$taskAudit=Join-Path $taskRoot 'audit_current_native_portable_boot_20261013'
if(Test-Path -LiteralPath $taskAudit){throw 'Never overwrite an executed test'}
New-Item -ItemType Directory -Path $taskAudit | Out-Null
$taskTemp=Join-Path $taskAudit 'temporary_extracted_package'
$taskResolved=[IO.Path]::GetFullPath($taskTemp)
if(-not $taskResolved.StartsWith([IO.Path]::GetFullPath($taskAudit)+[IO.Path]::DirectorySeparatorChar)){throw 'Unsafe temporary target'}
New-Item -ItemType Directory -Path $taskResolved | Out-Null
try {
 Add-Type -AssemblyName System.IO.Compression.FileSystem
 [IO.Compression.ZipFile]::ExtractToDirectory($taskZip,$taskResolved)
 $taskPackage=Join-Path $taskResolved 'MK2_Kano_Sonya_Playtest'
 foreach($taskName in [Environment]::GetEnvironmentVariables().Keys){
  if($taskName -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)'){[Environment]::SetEnvironmentVariable($taskName,$null)}
 }
 $taskBuild=Join-Path $taskPackage 'diagnostic_native_selector_layers_long'
 $taskArgs=@('mk2ks','-rompath','"diagnostic_native_selector_layers_long/roms;roms"','-samplepath','"diagnostic_native_selector_layers_long/samples;samples"','-artpath','artwork','-samples','-samplerate','48000','-inipath','play_v5219_checked','-cfg_directory','play_v5219_checked/cfg','-nvram_directory','play_v5219_checked/nvram','-snapshot_directory','play_v5219_checked/snap','-nocheat','-skip_gameinfo','-video','none','-sound','none','-nothrottle','-noautoframeskip','-frameskip','0','-str','30')
 $taskLog=Join-Path $taskAudit 'run.log'
 $taskErr=Join-Path $taskAudit 'stderr.log'
 $taskProcess=Start-Process -FilePath (Join-Path $taskBuild 'mkport_candidate.exe') -ArgumentList $taskArgs -WorkingDirectory $taskPackage -WindowStyle Hidden -RedirectStandardOutput $taskLog -RedirectStandardError $taskErr -PassThru
 $taskBirth=$taskProcess.StartTime
 $taskClock=[Diagnostics.Stopwatch]::StartNew()
 $taskPeak=0L;$taskLimit=$null
 while(-not $taskProcess.HasExited){
  $taskProcess.Refresh();$taskPeak=[Math]::Max($taskPeak,$taskProcess.WorkingSet64)
  if($taskPeak -gt 320MB){$taskLimit='memory_limit'}
  if($taskClock.Elapsed.TotalSeconds -gt 90){$taskLimit='wall_limit'}
  if((Get-Item -LiteralPath $taskLog).Length+(Get-Item -LiteralPath $taskErr).Length -gt 10MB){$taskLimit='log_limit'}
  if($taskLimit){
   $taskActual=Get-Process -Id $taskProcess.Id -ErrorAction SilentlyContinue
   if($taskActual -and $taskActual.StartTime -eq $taskBirth){Stop-Process -InputObject $taskActual -Force}
   break
  }
  Start-Sleep -Milliseconds 200
 }
 $taskProcess.WaitForExit();$taskProcess.Refresh()
 $taskOutput=Get-Content -LiteralPath $taskLog -Raw
 $taskErrorOutput=Get-Content -LiteralPath $taskErr -Raw
 $taskPassed=$taskProcess.ExitCode -eq 0 -and -not $taskLimit -and -not $taskErrorOutput -and $taskOutput -match 'Average speed:'
 $taskReport=[ordered]@{passedPortableHeadlessStartup=$taskPassed;exitCode=$taskProcess.ExitCode;limitReason=$taskLimit;peakWorkingSetBytes=$taskPeak;elapsedSeconds=$taskClock.Elapsed.TotalSeconds;emulatedSecondsRequested=30;externalWorkspaceROMFallback=$false;controllerScript='none';rawMedia='none';interactiveVideoAudioAcceptance=$false;fullPortAccepted=$false}
 $taskReport|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $taskAudit 'report.json')
 $taskReport|ConvertTo-Json
 if(-not $taskPassed){throw 'Portable startup did not pass'}
} finally {
 $taskActual=(Resolve-Path -LiteralPath $taskResolved).Path
 if($taskActual -ne $taskResolved){throw 'Temporary target resolution changed'}
 if(Get-ChildItem -LiteralPath $taskActual -Recurse -Force | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}){throw 'Refuse cleanup through reparse points'}
 Remove-Item -LiteralPath $taskActual -Recurse -Force
}
