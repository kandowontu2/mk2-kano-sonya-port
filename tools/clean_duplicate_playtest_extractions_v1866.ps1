$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskOut=Join-Path $taskRoot 'audit_v1866_duplicate_package_cleanup'
if(Test-Path -LiteralPath $taskOut){throw 'Never overwrite cleanup evidence'}
$taskCheckpointPath=Join-Path $taskRoot 'audit_v1853_ball_register_frontier_checkpoint/checkpoint.json'
$taskCheckpoint=Get-Content -LiteralPath $taskCheckpointPath -Raw | ConvertFrom-Json
if($taskCheckpoint.currentCandidate -ne 'diagnostic_v1836_ball_register_boundary'){throw 'Wrong current checkpoint'}
$taskPlans=@(
 @{audit='audit_v1744_portable_playtest_zip_checked';package='release_v1743_current_playtest';prefix='MK2_Kano_Sonya_v1597_CURRENT_PLAYTEST'},
 @{audit='audit_v1864_portable_playtest_zip_checked';package='release_v1863_current_playtest';prefix='MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST'})
$taskKeep=@("$taskRoot/diagnostic_v1836_ball_register_boundary/mkport_candidate.exe",
 "$taskRoot/diagnostic_v1836_ball_register_boundary/build-info.json","$taskRoot/diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata",
 "$taskRoot/diagnostic_v1836_ball_register_boundary/play/cfg/default.cfg","$taskRoot/diagnostic_v1836_ball_register_boundary/play/cfg/mk2ks.cfg",
 "$taskRoot/PLAY_CURRENT_V1836_CHECKED.cmd",$taskCheckpointPath)
$taskKeptHashes=@{};foreach($taskFile in $taskKeep){$taskKeptHashes[$taskFile]=(Get-FileHash -LiteralPath $taskFile).Hash}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2DuplicateAllocation1866 { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path,out uint high); }'
function Get-TaskAllocated([string]$taskPath){
 [uint32]$taskHigh=0;[uint32]$taskLow=[MK2DuplicateAllocation1866]::GetCompressedFileSizeW($taskPath,[ref]$taskHigh)
 if($taskLow -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Allocation unavailable'}
 return (([uint64]$taskHigh -shl 32)+[uint64]$taskLow)
}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskTotal=0L;$taskPreserved=0L;$taskRecords=@()
foreach($taskPlan in $taskPlans){
 $taskExpected=Join-Path $taskRoot ($taskPlan.audit+'/extracted')
 $taskTarget=(Resolve-Path -LiteralPath $taskExpected).Path
 if(-not [string]::Equals($taskTarget,$taskExpected,[StringComparison]::OrdinalIgnoreCase) -or
  -not $taskTarget.StartsWith($taskRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Exact extraction target outside workspace'}
 foreach($taskPinned in $taskCheckpoint.inputHashes.PSObject.Properties.Name){
  if([IO.Path]::GetFullPath($taskPinned).StartsWith($taskTarget+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Current evidence still needs extracted copy'}
 }
 if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -and $_.ExecutablePath.StartsWith($taskTarget+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)}).Count){throw 'Extracted game is running'}
 $taskResult=Get-Content -LiteralPath "$taskRoot/$($taskPlan.audit)/report.json" -Raw | ConvertFrom-Json
 if(-not $taskResult.passed -or (Get-FileHash -LiteralPath $taskResult.zip).Hash -ne $taskResult.zipSHA256){throw 'Complete retained ZIP required'}
 $taskKeptHashes[$taskResult.zip]=$taskResult.zipSHA256
 $taskPortable=Join-Path $taskTarget $taskPlan.prefix
 $taskManifest=Get-Content -LiteralPath "$taskPortable/RELEASE.json" -Raw | ConvertFrom-Json
 if((Get-FileHash -LiteralPath "$taskPortable/RELEASE.json").Hash -ne
  (Get-FileHash -LiteralPath "$taskRoot/$($taskPlan.package)/RELEASE.json").Hash){throw 'Package manifest changed'}
 $taskEntries=@(Get-ChildItem -LiteralPath $taskTarget -Recurse -Force)
 if(@($taskEntries | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'Unexpected link'}
 $taskFiles=@($taskEntries | Where-Object {-not $_.PSIsContainer})
 if($taskFiles.Count -ne 64 -or $taskManifest.files.PSObject.Properties.Count -ne 59){throw 'Unexpected extraction inventory'}
 $taskExpectedFiles=@('RELEASE.json')+@($taskManifest.files.PSObject.Properties.Name)
 $taskBoot=@('play/cfg/default.cfg','play/cfg/mk2ks.cfg','play/nvram/mk2ks/nvram','play/snap/mk2ks/0000.png')
 $taskActual=@($taskFiles | ForEach-Object {[IO.Path]::GetRelativePath($taskPortable,$_.FullName).Replace('\','/')})
 if(@(Compare-Object ($taskActual | Sort-Object) (($taskExpectedFiles+$taskBoot) | Sort-Object)).Count){throw 'New unexpected files; preserve extraction'}
 foreach($taskItem in $taskManifest.files.PSObject.Properties){
  if($taskItem.Name -match '(^[\\/]|:|(^|[\\/])\.\.([\\/]|$))'){throw 'Unsafe package-relative name'}
  if((Get-FileHash -LiteralPath (Join-Path $taskPortable $taskItem.Name)).Hash -ne $taskItem.Value){throw 'Extracted packaged file changed'}
 }
 $taskInventory=@();$taskBytes=0L;$taskSaved=@{}
 foreach($taskFile in $taskFiles){
  $taskRelative=[IO.Path]::GetRelativePath($taskPortable,$taskFile.FullName).Replace('\','/')
  $taskHash=(Get-FileHash -LiteralPath $taskFile.FullName).Hash;$taskAllocated=Get-TaskAllocated $taskFile.FullName
  $taskInventory+=[ordered]@{relativePath=$taskRelative;bytes=$taskFile.Length;allocatedBytes=$taskAllocated;sha256=$taskHash}
  $taskBytes+=$taskAllocated
  if($taskRelative -in $taskBoot){
   $taskDest=Join-Path $taskOut ('preserved_boot/'+$taskPlan.prefix+'/'+$taskRelative)
   New-Item -ItemType Directory -Path (Split-Path $taskDest -Parent) -Force | Out-Null
   Copy-Item -LiteralPath $taskFile.FullName -Destination $taskDest
   if((Get-FileHash -LiteralPath $taskDest).Hash -ne $taskHash){throw 'Preserved boot output mismatch'}
   $taskSaved[$taskDest]=$taskHash;$taskPreserved+=Get-TaskAllocated $taskDest
  }
 }
 $taskInventory | ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$taskOut/$($taskPlan.audit)-inventory.json" -Encoding utf8
 # Only disposable exact extraction copies, with no active/pinned inputs.
 # Packaged bytes restore from the retained verified ZIP; four unique boot
 # cfg/NVRAM/snapshot files are preserved above with exact hashes.
 Remove-Item -LiteralPath $taskTarget -Recurse -Force
 if(Test-Path -LiteralPath $taskTarget){throw 'Duplicate extraction still exists'}
 foreach($taskFile in $taskSaved.Keys){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskSaved[$taskFile]){throw 'Boot output preservation changed'}}
 $taskTotal+=$taskBytes
 $taskRecords+=[ordered]@{removedDirectory=$taskTarget;removedAllocatedBytes=$taskBytes;retainedZIP=$taskResult.zip;zipSHA256=$taskResult.zipSHA256;
   packagedFilesMatchRetainedManifest=59;uniqueBootFilesPreserved=4;preservedHashes=$taskSaved}
}
foreach($taskFile in $taskKeptHashes.Keys){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskKeptHashes[$taskFile]){throw 'Current build/settings or retained ZIP changed'}}
$taskReport=[ordered]@{passed=$true;removedDuplicateDirectories=2;removedAllocatedBytes=$taskTotal;
 uniqueBootFilesPreserved=8;preservedBootAllocatedBytes=$taskPreserved;netDuplicateFileStorageReductionBytes=$taskTotal-$taskPreserved;
 currentBuildSettingsAndBothReleaseZIPsUnchanged=$true;recovery='Re-extract the retained versioned playtest ZIPs; unique boot outputs are saved under preserved_boot.';
 removed=$taskRecords;keptHashes=$taskKeptHashes;allOldBuildFoldersRemoved=$false;fullPortAcceptance=$false}
$taskReport | ConvertTo-Json -Depth 8 | Out-File -LiteralPath "$taskOut/report.json" -Encoding utf8
[PSCustomObject]$taskReport | Select-Object passed,removedDuplicateDirectories,removedAllocatedBytes,preservedBootAllocatedBytes,netDuplicateFileStorageReductionBytes | ConvertTo-Json
