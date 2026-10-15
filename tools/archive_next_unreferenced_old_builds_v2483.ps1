$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskOut=Join-Path $taskRoot 'audit_v2483_next_unreferenced_old_build_recovery'
if(Test-Path -LiteralPath $taskOut){throw 'Never overwrite cleanup evidence'}
$taskCheckpointPath=Join-Path $taskRoot 'audit_v2460_current_native_crouch_jump_checkpoint/checkpoint.json'
$taskCheckpoint=Get-Content -LiteralPath $taskCheckpointPath -Raw | ConvertFrom-Json
if($taskCheckpoint.currentCandidate -ne 'diagnostic_v1836_ball_register_boundary' -or $taskCheckpoint.goalStatus -ne 'active'){throw 'Wrong current checkpoint'}
$taskPlans=@(
 @{name='diagnostic_v249_battle_card_aligned_trial';count=11;exe='B55EDDD6D981EFBC4F812B7BDEC14CB8D7732634D0C9E3EAC447A7F33F123D6B';build='415DA7629FBB050988FC776F1623A5BFB8E28EDA784FBE88136E44EF07F34644'},
 @{name='diagnostic_v260_skeleton_winner_hold_trial';count=13;exe='97ACAAAD71F11002C03609885B0771EA91914478AF93604086DECF8FB0CEC5F5';build='D6B4C88F4A2F85BDA676FC1175E0FDC9A60C4326D229DC01960C780A2FAD008E'},
 @{name='diagnostic_v261_victim_pull_sync_trial';count=5;exe='73895FE16E169FCB7AB2D3459A1244118C66211E75146375768088094E8AEBE5';build='D262748EDA1CD500145341EF517E7A55C4548F37D6C56F5801BC26DACA673758'},
 @{name='diagnostic_v262_native_jax_body_trial';count=3;exe='D4F51BADAD7B12232CA3F655B0AA76BD62FF54B23173B30A95F2C8946136E49E';build='BA4AD14B1EF19E4748D02AFD61DEC299C199ECA5E1AE2D1E3CADB33338C0661C'},
 @{name='diagnostic_v263_native_stock_body_trial';count=3;exe='2A683E04CE0645B2A6C3525EAD29228A14B6E978BFE4DC79C0982CDFE1863981';build='959C6938DBD182F338A87D0981C7C67A64FEBDFEA433D1D44DA13B31F109AF8F'},
 @{name='diagnostic_v264_native_stock_body_trial';count=10;exe='7EEC7B75113C78F49D9188E45D2CBE16E8F45FCE4BCFC0A627E0112FF7316109';build='783D212D70E40186F61A8C7E9B1673ECE6273A0CED68160AE647BAB76F65A688'},
 @{name='diagnostic_v265_skeleton_facing_trial';count=5;exe='AA09F082838558D43D1CC71DD882C9555F990735C619915A9C04FD7571A37C91';build='74C01ACF65FE3B7AC1E514508480E87DE8FBB6CB3B8FF0C2F6EEACF13B66AEAA'},
 @{name='diagnostic_v267_sonya_native_arc_trial';count=3;exe='86C104816AB978B13EC43FE2AABE748A192B3C5F239CDC9411C325A82D4E6969';build='E4F399291E6FD62BA54363D835F06C085E0BE189E08A38D72D388EB3D80E32F6'},
 @{name='diagnostic_v268_sonya_arc_register_trial';count=3;exe='951F6EB256C0898CC4D3E81FC21FB7A371C4F120DB1F13FBA398326FE0DCDE92';build='E9FC4669C15BAEEC67D02EE286EE1ABF2A02CA015E59164C8FD215A8E3F8121C'},
 @{name='diagnostic_v269_sonya_arc_contact_trial';count=5;exe='B2A650266D8B047809D88B0B712ACF12B8E672F8D0D9F7499A38FEFF80AFFAA4';build='069429E5A14F8F3EE50C370412640FF323E4F9D4968650EF271A05FF7AE7ACA7'})
$taskAdditionalGraphs=@('audit_v2465_current_kano_p1_shao_crouch_exit_checked/report.json','audit_v2465_current_sonya_p1_shao_crouch_exit_checked/report.json','audit_v2479_current_sonya_p1_shao_crouch_exit_checked/report.json','audit_v2467_current_kano_shao_crouch_exit_escape_boss_ledger_checked/report.json','audit_v2467_current_sonya_shao_crouch_exit_escape_boss_ledger_checked/report.json','audit_v2469_current_kano_shao_crouch_exit_escape_input_counterexamples/report.json','audit_v2481_current_sonya_crouch_exit_extended_boundary/report.json')
$taskAllPins=@($taskCheckpoint.inputHashes.PSObject.Properties.Name)
foreach($taskGraph in $taskAdditionalGraphs){
 $taskGraphPath=Join-Path $taskRoot $taskGraph
 $taskGraphReport=Get-Content -LiteralPath $taskGraphPath -Raw | ConvertFrom-Json
 if(-not @($taskGraphReport.inputHashes.PSObject.Properties.Name).Count){throw 'Missing current accepted/rejected dependency frontier'}
 $taskAllPins+=@($taskGraphReport.inputHashes.PSObject.Properties.Name)
}
$taskKeep=@($taskCheckpointPath,"$taskRoot/PLAY_MK2_KANO_SONYA.cmd","$taskRoot/PLAY_CURRENT_V1836_CHECKED.cmd",
 "$taskRoot/diagnostic_v1836_ball_register_boundary/mkport_candidate.exe","$taskRoot/diagnostic_v1836_ball_register_boundary/build-info.json",
 "$taskRoot/diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata",
 "$taskRoot/release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip",$PSCommandPath)
$taskKeep+=@($taskAdditionalGraphs | ForEach-Object {Join-Path $taskRoot $_})
$taskKeep+=@(Get-ChildItem -LiteralPath "$taskRoot/diagnostic_v1836_ball_register_boundary/play" -Recurse -File | ForEach-Object {$_.FullName})
$taskKeptHashes=@{};foreach($taskFile in $taskKeep){$taskKeptHashes[$taskFile]=(Get-FileHash -LiteralPath $taskFile).Hash}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2CleanupAllocation2483 { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path,out uint high); }'
function Get-TaskAllocated([string]$taskPath){
 [uint32]$taskHigh=0;[uint32]$taskLow=[MK2CleanupAllocation2483]::GetCompressedFileSizeW($taskPath,[ref]$taskHigh)
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
foreach($taskPin in $taskAllPins){
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
$taskZip=Join-Path $taskOut 'ten_unreferenced_builds_complete_recovery.zip'
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
 # Only the ten exact validated, unreferenced, non-running targets. All files
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
 reason='Ten superseded trial-build folders absent from the entire2460checkpoint and all current accepted/rejected boss/selection-boundary dependency frontiers; current1836launcher, build, settings and playtest ZIP preserved.';
 recovery='Extract ten_unreferenced_builds_complete_recovery.zip into the mk2port root to restore all ten folders, including source/build metadata, ROM, settings and snapshots.';
 dependencyFrontierGraphs=@($taskCheckpointPath)+@($taskAdditionalGraphs | ForEach-Object {Join-Path $taskRoot $_});keptHashes=$taskKeptHashes;inventory=$taskInventory;allOldBuildFoldersRemoved=$false;fullPortAcceptance=$false}
$taskReport | ConvertTo-Json -Depth 7 | Out-File -LiteralPath "$taskOut/report.json" -Encoding utf8
[pscustomobject]$taskReport | Select-Object passed,archivedFiles,removedLogicalBytes,removedAllocatedBytes,recoveryArchiveAllocatedBytes,netBuildStorageReductionBytes,allOldBuildFoldersRemoved | ConvertTo-Json
