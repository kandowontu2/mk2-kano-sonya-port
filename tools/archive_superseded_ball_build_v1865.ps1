$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskName='diagnostic_v1816_ball_native_boundary'
$taskTarget=(Resolve-Path -LiteralPath (Join-Path $taskRoot $taskName)).Path
$taskExpected=Join-Path $taskRoot $taskName
$taskOut=Join-Path $taskRoot 'audit_v1865_superseded_ball_build_cleanup'
if(Test-Path -LiteralPath $taskOut){throw 'Never overwrite cleanup evidence'}
if(-not [string]::Equals($taskTarget,$taskExpected,[StringComparison]::OrdinalIgnoreCase) -or
 -not $taskTarget.StartsWith($taskRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Exact target outside explicit workspace'}
$taskCheckpointPath=Join-Path $taskRoot 'audit_v1853_ball_register_frontier_checkpoint/checkpoint.json'
$taskCheckpoint=Get-Content -LiteralPath $taskCheckpointPath -Raw | ConvertFrom-Json
if($taskCheckpoint.currentCandidate -ne 'diagnostic_v1836_ball_register_boundary' -or $taskCheckpoint.goalStatus -ne 'active'){throw 'Wrong current checkpoint'}
foreach($taskPinned in $taskCheckpoint.inputHashes.PSObject.Properties.Name){
 if([IO.Path]::GetFullPath($taskPinned).StartsWith($taskTarget+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Current evidence still needs this folder'}
}
if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq (Join-Path $taskTarget 'mkport_candidate.exe')}).Count){throw 'Target is running'}
$taskEntries=@(Get-ChildItem -LiteralPath $taskTarget -Recurse -Force)
if(@($taskEntries | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'Target contains links; preserve it'}
$taskFiles=@($taskEntries | Where-Object {-not $_.PSIsContainer})
if($taskFiles.Count -ne 19){throw 'Unexpected new user files in target; preserve it'}
if((Get-FileHash -LiteralPath "$taskTarget/mkport_candidate.exe").Hash -ne '31964536E5DC7C48763E593926688594B63ED64EDE25AE5CFCBD59279C337104' -or
 (Get-FileHash -LiteralPath "$taskTarget/build-info.json").Hash -ne '191FE108BA8D3CDA161F2FDD0CDF9DA8C407D53CEBCC82B4F6842E3958614963'){throw 'Superseded build changed; preserve it'}
$taskKeep=@("$taskRoot/diagnostic_v1836_ball_register_boundary/mkport_candidate.exe",
 "$taskRoot/diagnostic_v1836_ball_register_boundary/build-info.json","$taskRoot/diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata",
 "$taskRoot/diagnostic_v1836_ball_register_boundary/play/cfg/default.cfg","$taskRoot/diagnostic_v1836_ball_register_boundary/play/cfg/mk2ks.cfg",
 "$taskRoot/PLAY_CURRENT_V1836_CHECKED.cmd",$taskCheckpointPath,"$taskRoot/audit_v1856_current_native_ui_checked/report.json",
 "$taskRoot/audit_v1859_current_ground_shadow_checked/report.json",
 "$taskRoot/release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip")
$taskKeptHashes=@{};foreach($taskFile in $taskKeep){$taskKeptHashes[$taskFile]=(Get-FileHash -LiteralPath $taskFile).Hash}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2CleanupAllocation1865 { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path,out uint high); }'
function Get-TaskAllocated([string]$taskPath){
 [uint32]$taskHigh=0;[uint32]$taskLow=[MK2CleanupAllocation1865]::GetCompressedFileSizeW($taskPath,[ref]$taskHigh)
 if($taskLow -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Allocation unavailable'}
 return (([uint64]$taskHigh -shl 32)+[uint64]$taskLow)
}
$taskInventory=@();$taskLogical=0L;$taskAllocated=0L
foreach($taskFile in $taskFiles){
 $taskRelative=[IO.Path]::GetRelativePath($taskTarget,$taskFile.FullName).Replace('\','/')
 if($taskRelative -match '(^[\\/]|:|(^|[\\/])\.\.([\\/]|$))'){throw 'Unsafe recovery entry'}
 $taskHash=(Get-FileHash -LiteralPath $taskFile.FullName).Hash;$taskBytes=Get-TaskAllocated $taskFile.FullName
 $taskInventory+=[ordered]@{relativePath=$taskRelative;bytes=$taskFile.Length;allocatedBytes=$taskBytes;sha256=$taskHash}
 $taskLogical+=$taskFile.Length;$taskAllocated+=$taskBytes
}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskInventory | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$taskOut/inventory-before.json" -Encoding utf8
Add-Type -AssemblyName System.IO.Compression.FileSystem
$taskZip=Join-Path $taskOut 'diagnostic_v1816_complete_recovery.zip'
$taskArchive=[IO.Compression.ZipFile]::Open($taskZip,[IO.Compression.ZipArchiveMode]::Create)
try{
 foreach($taskFile in $taskFiles){
  $taskRelative=[IO.Path]::GetRelativePath($taskTarget,$taskFile.FullName).Replace('\','/')
  [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($taskArchive,$taskFile.FullName,$taskName+'/'+$taskRelative,[IO.Compression.CompressionLevel]::Optimal) | Out-Null
 }
}finally{$taskArchive.Dispose()}
$taskArchive=[IO.Compression.ZipFile]::OpenRead($taskZip)
try{
 if($taskArchive.Entries.Count -ne $taskInventory.Count){throw 'Incomplete recovery archive'}
 foreach($taskRecord in $taskInventory){
  $taskEntry=$taskArchive.GetEntry($taskName+'/'+$taskRecord.relativePath)
  if($null -eq $taskEntry -or $taskEntry.Length -ne $taskRecord.bytes){throw 'Recovery archive inventory mismatch'}
  $taskStream=$taskEntry.Open();$taskSHA=[Security.Cryptography.SHA256]::Create()
  try{$taskHash=[BitConverter]::ToString($taskSHA.ComputeHash($taskStream)).Replace('-','')}
  finally{$taskStream.Dispose();$taskSHA.Dispose()}
  if($taskHash -ne $taskRecord.sha256 -or (Get-FileHash -LiteralPath (Join-Path $taskTarget $taskRecord.relativePath)).Hash -ne $taskRecord.sha256){throw 'Recovery/source byte mismatch'}
 }
}finally{$taskArchive.Dispose()}
$taskZipHash=(Get-FileHash -LiteralPath $taskZip).Hash
# Exact resolved, non-running superseded build only; all 19 files archived and
# independently checked before removal, including source, settings, ROM and EXE.
Remove-Item -LiteralPath $taskTarget -Recurse -Force
if(Test-Path -LiteralPath $taskTarget){throw 'Old build directory still exists'}
foreach($taskFile in $taskKeep){if((Get-FileHash -LiteralPath $taskFile).Hash -ne $taskKeptHashes[$taskFile]){throw 'Current build/settings/evidence changed'}}
if((Get-FileHash -LiteralPath $taskZip).Hash -ne $taskZipHash){throw 'Recovery archive changed'}
$taskRecoveryAllocated=Get-TaskAllocated $taskZip
$taskReport=[ordered]@{passed=$true;removedDirectory=$taskTarget;archivedFiles=$taskInventory.Count;
 removedLogicalBytes=$taskLogical;removedAllocatedBytes=$taskAllocated;recoveryZIP=$taskZip;recoveryZipSHA256=$taskZipHash;
 recoveryArchiveAllocatedBytes=$taskRecoveryAllocated;netBuildStorageReductionBytes=$taskAllocated-$taskRecoveryAllocated;
 archiveEveryEntryAndSourceHashVerified=$true;currentCheckpointTargetReferences=0;currentBuildSettingsAndPlaytestZIPUnchanged=$true;
 reason='Superseded v1816 callback changed caller scratch registers; current v1836 fixes this and passes the complete bounded matrix.';
 recovery='Extract diagnostic_v1816_complete_recovery.zip into the mk2port root to restore the complete original versioned folder.';
 keptHashes=$taskKeptHashes;inventory=$taskInventory;allOldBuildFoldersRemoved=$false;fullPortAcceptance=$false}
$taskReport | ConvertTo-Json -Depth 7 | Out-File -LiteralPath "$taskOut/report.json" -Encoding utf8
$taskReport | Select-Object passed,archivedFiles,removedLogicalBytes,removedAllocatedBytes,recoveryArchiveAllocatedBytes,netBuildStorageReductionBytes,allOldBuildFoldersRemoved | ConvertTo-Json
