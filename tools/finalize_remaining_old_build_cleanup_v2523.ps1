$ErrorActionPreference='Stop'
$taskRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskPrepPath=Join-Path $taskRoot 'audit_v2518_remaining_old_build_recovery/report.json'
$taskProofPath=Join-Path $taskRoot 'audit_v2524_remaining_old_build_recovery_predelete/report.json'
$taskOutput=Join-Path $taskRoot 'audit_v2523_remaining_old_build_cleanup'
if(Test-Path -LiteralPath $taskOutput){throw 'Immutable final cleanup output already exists'}
$taskPrep=Get-Content -LiteralPath $taskPrepPath -Raw | ConvertFrom-Json
$taskProof=Get-Content -LiteralPath $taskProofPath -Raw | ConvertFrom-Json
if(-not $taskPrep.passed -or -not $taskProof.passed -or $taskProof.phase -ne 'pre-delete' -or $taskProof.filesDeleted -or $taskProof.verifiedFiles -ne 465 -or $taskProof.verifiedDirectories -ne 352){throw 'Independent complete recovery proof required'}
if(@($taskPrep.targetDirectories).Count -ne 68 -or (@($taskPrep.targetDirectories | Select-Object -Unique).Count -ne 68)){throw 'Exactly68 unique original targets required'}
if((Compare-Object $taskPrep.targetDirectories $taskProof.targetDirectories)){throw 'Exact proof targets differ'}
$taskResolvedRoot=(Resolve-Path -LiteralPath $taskRoot).ProviderPath.TrimEnd('\')
$taskProtected=@('diagnostic_v1836_ball_register_boundary','diagnostic_v1597_native_ground_throw','diagnostic_v1250_native_correct_rom_metadata')
$taskTargets=@()
foreach($taskPath in $taskPrep.targetDirectories){
 $taskResolved=(Resolve-Path -LiteralPath $taskPath).ProviderPath
 $taskName=[IO.Path]::GetFileName($taskResolved)
 if([IO.Path]::GetDirectoryName($taskResolved) -ne $taskResolvedRoot -or $taskResolved -ne [IO.Path]::GetFullPath($taskPath) -or $taskName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$' -or $taskName -in $taskProtected){throw ('Unsafe exact old-build target '+$taskPath)}
 if((Get-Item -LiteralPath $taskResolved).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'No target reparse point'}
 $taskTargets+=$taskResolved
}
$taskPins=[ordered]@{}
foreach($taskEntry in $taskProof.inputHashes.PSObject.Properties){
 if((Get-FileHash -LiteralPath $taskEntry.Name -Algorithm SHA256).Hash -ne $taskEntry.Value){throw ('Changed retained dependency '+$taskEntry.Name)}
 foreach($taskTarget in $taskTargets){if([IO.Path]::GetFullPath($taskEntry.Name).StartsWith($taskTarget+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Retained dependency inside target'}}
 $taskPins[$taskEntry.Name]=$taskEntry.Value
}
$taskRecovery=(Resolve-Path -LiteralPath $taskProof.recoveryArchive).ProviderPath
if(-not $taskRecovery.StartsWith($taskResolvedRoot+'\audit_v2518_remaining_old_build_recovery\',[StringComparison]::OrdinalIgnoreCase) -or (Get-Item -LiteralPath $taskRecovery).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Exact regular recovery archive required'}
if((Get-FileHash -LiteralPath $taskRecovery -Algorithm SHA256).Hash -ne $taskProof.recoveryArchiveSHA256){throw 'Complete recovery archive changed'}
$taskFiles=@{};foreach($taskRecord in $taskPrep.inventory){$taskFiles[[IO.Path]::GetFullPath((Join-Path $taskRoot $taskRecord.path))]=$taskRecord}
$taskDirectorySet=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach($taskDirectory in $taskPrep.preservedDirectories){[void]$taskDirectorySet.Add([IO.Path]::GetFullPath((Join-Path $taskRoot $taskDirectory)))}
$taskSeenFiles=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$taskSeenDirectories=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach($taskTarget in $taskTargets){
 [void]$taskSeenDirectories.Add($taskTarget)
 foreach($taskItem in Get-ChildItem -LiteralPath $taskTarget -Recurse -Force){
  if($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'No reparse anywhere in original tree'}
  if($taskItem.PSIsContainer){if(-not $taskDirectorySet.Contains($taskItem.FullName)){throw 'Unexpected original directory'};[void]$taskSeenDirectories.Add($taskItem.FullName)}
  else{if(-not $taskFiles.ContainsKey($taskItem.FullName)){throw 'Unexpected original file'};$taskRecord=$taskFiles[$taskItem.FullName]
   if($taskItem.Length -ne $taskRecord.bytes -or (Get-FileHash -LiteralPath $taskItem.FullName -Algorithm SHA256).Hash -ne $taskRecord.sha256){throw ('Original file changed '+$taskItem.FullName)}
   [void]$taskSeenFiles.Add($taskItem.FullName)
  }
 }
}
if($taskSeenFiles.Count -ne 465 -or $taskSeenDirectories.Count -ne 352 -or -not $taskSeenDirectories.SetEquals($taskDirectorySet)){throw 'Entire exact original tree required before deletion'}
foreach($taskProcess in Get-CimInstance Win32_Process | Where-Object {$_.Name -like '*mkport*' -or $_.Name -like '*mame*'}){
 if(-not $taskProcess.ExecutablePath -and -not $taskProcess.CommandLine){throw 'Cannot resolve active emulator path safely'}
 foreach($taskTarget in $taskTargets){if(($taskProcess.ExecutablePath -and $taskProcess.ExecutablePath.StartsWith($taskTarget+'\',[StringComparison]::OrdinalIgnoreCase)) -or ($taskProcess.CommandLine -and $taskProcess.CommandLine.IndexOf($taskTarget+'\',[StringComparison]::OrdinalIgnoreCase) -ge 0)){throw 'Old target executable is still running'}}
}
$taskPins[$taskProofPath]=(Get-FileHash -LiteralPath $taskProofPath -Algorithm SHA256).Hash
$taskPins[$taskPrepPath]=(Get-FileHash -LiteralPath $taskPrepPath -Algorithm SHA256).Hash
$taskPins[$PSCommandPath]=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash
# Exact resolved immediate-child targets only; every original byte already recovered.
foreach($taskTarget in $taskTargets){Remove-Item -LiteralPath $taskTarget -Recurse -Force;if(Test-Path -LiteralPath $taskTarget){throw ('Exact target not removed '+$taskTarget)}}
foreach($taskEntry in $taskPins.GetEnumerator()){if((Get-FileHash -LiteralPath $taskEntry.Key -Algorithm SHA256).Hash -ne $taskEntry.Value){throw ('Retained artifact changed after cleanup '+$taskEntry.Key)}}
New-Item -ItemType Directory -Path $taskOutput | Out-Null
$taskReport=[ordered]@{passed=$true;filesDeleted=$true;removedDirectories=$taskTargets;verifiedFiles=465;verifiedDirectories=352;
 verifiedLogicalBytes=$taskProof.verifiedLogicalBytes;recoveryArchive=$taskRecovery;recoveryArchiveSHA256=$taskProof.recoveryArchiveSHA256;
 netAllocatedSavings=$taskProof.netAllocatedSavings;allOriginalBytesAndDirectoriesRecoverable=$true;
 all68PreviouslyUnreferencedBuildFoldersRemoved=$true;allOldBuildFoldersRemoved=$false;currentAndRequiredNativeDependencyBuildsRetained=$true;
 inputHashes=$taskPins;fullPortAcceptance=$false;scope='Remove only68 exact resolved obsolete build folders after complete independent recovery; current executable, play settings and required native dependency builds retained.'}
$taskReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskOutput 'report.json') -Encoding UTF8
[pscustomobject]$taskReport | Select-Object passed,filesDeleted,verifiedFiles,verifiedDirectories,netAllocatedSavings | ConvertTo-Json
