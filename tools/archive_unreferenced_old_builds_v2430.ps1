$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskOut=Join-Path $taskRoot 'audit_v2430_unreferenced_old_build_recovery'
if(Test-Path -LiteralPath $taskOut){throw 'Never overwrite cleanup evidence'}
$taskCheckpointPath=Join-Path $taskRoot 'audit_v2407_current_shao_opening_guard_checkpoint/checkpoint.json'
$taskCheckpoint=Get-Content -LiteralPath $taskCheckpointPath -Raw | ConvertFrom-Json
if($taskCheckpoint.currentCandidate -ne 'diagnostic_v1836_ball_register_boundary' -or $taskCheckpoint.goalStatus -ne 'active'){throw 'Wrong current checkpoint'}
$taskPlans=@(
 @{name='diagnostic_v277_native_battle_photos';count=9;exe='6D3AC6FD03A34735EF16AD6AACA5170C93F2824FF35A4A1ADC0D1AC9CC6ABE33';build='E1A3A00ED93D3A74345E6B3CC5049EADC4072BE58B51C229B2CBBABF69944512'},
 @{name='diagnostic_v1329_native_ring_startup_core';count=14;exe='E813AF8662128D0F932937C44925039F633CCA958AE584D43BB263B76A320478';build='7DF8DDF90A343CD801CD17B15A8B395D4C85DAC6698BCA79966DD145CA474507'},
 @{name='diagnostic_v1340_native_ring_lookup';count=18;exe='A050762309CADA040B85214CCA435F10A37DD3AAA98173F2E17D12D70F034159';build='7B756D1418B6CD3E44ED11CFF1B6013EBEDA4AFF89E86DF7F14CBF23B889440A'},
 @{name='diagnostic_v1411_native_grab_audio';count=20;exe='01EF3950691A890BAA41723D99935E44A28B09A7431EA78EC5DBF8E0E90630C3';build='17CF707FF8DF03CB46FD84B33F16F656C66AFC64900B8B02D8F9A02D3E5EC85F'},
 @{name='diagnostic_v1473_sonya_launch_audio';count=17;exe='42151DB8134D8D68A2DD68DB5E1B81EA5B3CB0298DCDB5DAA8748421C6CA0209';build='6583CF94EF4BD91BDC829C778E536AEBF49C3169B955CF7DCB2B1AD062ED25CB'},
 @{name='diagnostic_v1517_active_launch_timer';count=21;exe='B0142C979C56C3906E8645D47CBE5CBE37D7AB33931A3447E3A6911DEC4911E8';build='B6E7AC14813D7796BAF11DF9C9A2B278BF1DA96591659B279B9E3C642376AA1F'})
$taskKeep=@($taskCheckpointPath,"$taskRoot/PLAY_MK2_KANO_SONYA.cmd","$taskRoot/PLAY_CURRENT_V1836_CHECKED.cmd",
 "$taskRoot/diagnostic_v1836_ball_register_boundary/mkport_candidate.exe","$taskRoot/diagnostic_v1836_ball_register_boundary/build-info.json",
 "$taskRoot/diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata",
 "$taskRoot/release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip",$PSCommandPath)
$taskKeep+=@(Get-ChildItem -LiteralPath "$taskRoot/diagnostic_v1836_ball_register_boundary/play" -Recurse -File | ForEach-Object {$_.FullName})
$taskKeptHashes=@{};foreach($taskFile in $taskKeep){$taskKeptHashes[$taskFile]=(Get-FileHash -LiteralPath $taskFile).Hash}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2CleanupAllocation2430 { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path,out uint high); }'
function Get-TaskAllocated([string]$taskPath){
 [uint32]$taskHigh=0;[uint32]$taskLow=[MK2CleanupAllocation2430]::GetCompressedFileSizeW($taskPath,[ref]$taskHigh)
 if($taskLow -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Allocation unavailable'}
 return (([uint64]$taskHigh -shl 32)+[uint64]$taskLow)
}
$taskTargets=@();$taskInventory=@();$taskDirectories=@();$taskLogical=0L;$taskAllocated=0L
# Resolve every explicitly named target and validate the complete dependency
# frontier before creating an archive or deleting anything. No broad glob.
foreach($taskPlan in $taskPlans){
 $taskExpected=Join-Path $taskRoot $taskPlan.name
 $taskTarget=(Resolve-Path -LiteralPath $taskExpected).Path
 if(-not [string]::Equals($taskTarget,$taskExpected,[StringComparison]::OrdinalIgnoreCase) -or
  -not $taskTarget.StartsWith($taskRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or
  (Get-Item -LiteralPath $taskTarget).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe exact cleanup target'}
 $taskTargets+=$taskTarget
 $taskEntries=@(Get-ChildItem -LiteralPath $taskTarget -Recurse -Force)
 if(@($taskEntries | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'Unexpected link; preserve build'}
 $taskFiles=@($taskEntries | Where-Object {-not $_.PSIsContainer})
 if($taskFiles.Count -ne $taskPlan.count){throw 'Inventory changed; preserve build'}
 if((Get-FileHash -LiteralPath "$taskTarget/mkport_candidate.exe").Hash -ne $taskPlan.exe -or
  (Get-FileHash -LiteralPath "$taskTarget/build-info.json").Hash -ne $taskPlan.build){throw 'Observed superseded build changed'}
 $taskDirectories+=($taskPlan.name+'/')
 $taskDirectories+=@($taskEntries | Where-Object {$_.PSIsContainer} | ForEach-Object {[IO.Path]::GetRelativePath($taskRoot,$_.FullName).Replace('\','/')+'/'})
 foreach($taskFile in $taskFiles){
  $taskRelative=[IO.Path]::GetRelativePath($taskRoot,$taskFile.FullName).Replace('\','/')
  if($taskRelative -match '(^[\\/]|:|(^|[\\/])\.\.([\\/]|$))'){throw 'Unsafe relative recovery path'}
  $taskBytes=Get-TaskAllocated $taskFile.FullName
  $taskInventory+=[ordered]@{path=$taskRelative;bytes=$taskFile.Length;allocatedBytes=$taskBytes;sha256=(Get-FileHash -LiteralPath $taskFile.FullName).Hash}
  $taskLogical+=$taskFile.Length;$taskAllocated+=$taskBytes
 }
}
$taskPrefixes=@($taskTargets | ForEach-Object {$_+[IO.Path]::DirectorySeparatorChar})
foreach($taskPin in $taskCheckpoint.inputHashes.PSObject.Properties.Name){
 $taskFull=[IO.Path]::GetFullPath($taskPin)
 foreach($taskPrefix in $taskPrefixes){if($taskFull.StartsWith($taskPrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Current evidence requires old build; preserve it'}}
}
function Assert-TaskNotRunning {
 foreach($taskProcess in @(Get-CimInstance Win32_Process)){
  if($taskProcess.ExecutablePath){foreach($taskPrefix in $taskPrefixes){if($taskProcess.ExecutablePath.StartsWith($taskPrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Old build is running'}}}
 }
}
Assert-TaskNotRunning
if(-not (Get-Content -LiteralPath "$taskRoot/PLAY_MK2_KANO_SONYA.cmd" -Raw).Contains('PLAY_CURRENT_V1836_CHECKED.cmd')){throw 'Current public entry point must not use old277'}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskInventory | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$taskOut/inventory-before.json" -Encoding utf8
Add-Type -AssemblyName System.IO.Compression.FileSystem
$taskZip=Join-Path $taskOut 'six_unreferenced_builds_complete_recovery.zip'
$taskArchive=[IO.Compression.ZipFile]::Open($taskZip,[IO.Compression.ZipArchiveMode]::Create)
try{
 foreach($taskDirectory in $taskDirectories){$taskArchive.CreateEntry($taskDirectory) | Out-Null}
 foreach($taskRecord in $taskInventory){
  [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($taskArchive,(Join-Path $taskRoot $taskRecord.path),$taskRecord.path,[IO.Compression.CompressionLevel]::Optimal) | Out-Null
 }
}finally{$taskArchive.Dispose()}
$taskArchive=[IO.Compression.ZipFile]::OpenRead($taskZip)
try{
 if($taskArchive.Entries.Count -ne $taskInventory.Count+$taskDirectories.Count){throw 'Incomplete recovery archive'}
 foreach($taskDirectory in $taskDirectories){if($null -eq $taskArchive.GetEntry($taskDirectory)){throw 'Missing original directory'}}
 foreach($taskRecord in $taskInventory){
  $taskEntry=$taskArchive.GetEntry($taskRecord.path)
  if($null -eq $taskEntry -or $taskEntry.Length -ne $taskRecord.bytes){throw 'Recovery inventory mismatch'}
  $taskStream=$taskEntry.Open();$taskSHA=[Security.Cryptography.SHA256]::Create()
  try{$taskHash=[BitConverter]::ToString($taskSHA.ComputeHash($taskStream)).Replace('-','')}
  finally{$taskStream.Dispose();$taskSHA.Dispose()}
  if($taskHash -ne $taskRecord.sha256 -or (Get-FileHash -LiteralPath (Join-Path $taskRoot $taskRecord.path)).Hash -ne $taskRecord.sha256){throw 'Recovery/source mismatch'}
 }
}finally{$taskArchive.Dispose()}
$taskZipHash=(Get-FileHash -LiteralPath $taskZip).Hash
$taskRecoveryAllocated=Get-TaskAllocated $taskZip
if($taskRecoveryAllocated -ge $taskAllocated){throw 'Archive does not save allocated space; preserve builds'}
Assert-TaskNotRunning
foreach($taskTarget in $taskTargets){
 if((Resolve-Path -LiteralPath $taskTarget).Path -ne $taskTarget -or (Get-Item -LiteralPath $taskTarget).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Target changed before removal'}
 $taskPrefix=$taskTarget+[IO.Path]::DirectorySeparatorChar
 $taskNow=@(Get-ChildItem -LiteralPath $taskTarget -Recurse -File -Force)
 $taskRecords=@($taskInventory | Where-Object {(Join-Path $taskRoot $_.path).StartsWith($taskPrefix,[StringComparison]::OrdinalIgnoreCase)})
 if($taskNow.Count -ne $taskRecords.Count){throw 'New files before removal; preserve build'}
 foreach($taskRecord in $taskRecords){if((Get-FileHash -LiteralPath (Join-Path $taskRoot $taskRecord.path)).Hash -ne $taskRecord.sha256){throw 'Build changed before removal'}}
 # Only the six exact validated, unreferenced, non-running targets. All files
 # and original directory names are already verified in the retained ZIP.
 Remove-Item -LiteralPath $taskTarget -Recurse -Force
 if(Test-Path -LiteralPath $taskTarget){throw 'Superseded build still present'}
}
foreach($taskFile in $taskKeep){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskKeptHashes[$taskFile]){throw 'Current build/settings/evidence changed'}}
if((Get-FileHash -LiteralPath $taskZip).Hash -ne $taskZipHash){throw 'Recovery archive changed'}
$taskReport=[ordered]@{passed=$true;removedDirectories=$taskTargets;archivedFiles=$taskInventory.Count;preservedDirectoryEntries=$taskDirectories.Count;
 removedLogicalBytes=$taskLogical;removedAllocatedBytes=$taskAllocated;recoveryZIP=$taskZip;recoveryZipSHA256=$taskZipHash;
 recoveryArchiveAllocatedBytes=$taskRecoveryAllocated;netBuildStorageReductionBytes=$taskAllocated-$taskRecoveryAllocated;
 archiveEveryEntryAndSourceHashVerified=$true;currentCheckpointTargetReferences=0;currentBuildSettingsAndPlaytestZIPUnchanged=$true;
 reason='Six superseded build folders absent from the entire current dependency frontier; usual launcher now points to checked1836, not277.';
 recovery='Extract six_unreferenced_builds_complete_recovery.zip into the mk2port root to restore all six folders, including source/build metadata, ROM, settings and snapshots.';
 keptHashes=$taskKeptHashes;inventory=$taskInventory;allOldBuildFoldersRemoved=$false;fullPortAcceptance=$false}
$taskReport | ConvertTo-Json -Depth 7 | Out-File -LiteralPath "$taskOut/report.json" -Encoding utf8
$taskReport | Select-Object passed,archivedFiles,removedLogicalBytes,removedAllocatedBytes,recoveryArchiveAllocatedBytes,netBuildStorageReductionBytes,allOldBuildFoldersRemoved | ConvertTo-Json
