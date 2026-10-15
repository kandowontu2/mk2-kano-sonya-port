$ErrorActionPreference='Stop'
$taskRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskOutput=Join-Path $taskRoot 'audit_v2487_next_old_build_solid_recovery_final'
$taskProofPath=Join-Path $taskRoot 'audit_v2489_next_old_build_solid_recovery_predelete\report.json'
$taskZip=Join-Path $taskRoot 'audit_v2483_next_unreferenced_old_build_recovery\ten_unreferenced_builds_complete_recovery.zip'
$taskArchive=Join-Path $taskRoot 'audit_v2486_next_old_build_solid_recovery\ten_unreferenced_builds_complete_recovery.tar.xz'
if(Test-Path -LiteralPath $taskOutput){throw 'Immutable cleanup finalization output already exists'}
$taskProof=Get-Content -LiteralPath $taskProofPath -Raw | ConvertFrom-Json
if(-not $taskProof.passed -or $taskProof.phase -ne 'pre-delete' -or $taskProof.oldZIPDeleted -or $taskProof.verifiedFiles -ne 61 -or $taskProof.verifiedDirectories -ne 37){throw 'Independent full recovery proof required before deletion'}
$taskRootResolved=(Resolve-Path -LiteralPath $taskRoot).ProviderPath.TrimEnd('\')
$taskZipResolved=(Resolve-Path -LiteralPath $taskZip).ProviderPath
$taskArchiveResolved=(Resolve-Path -LiteralPath $taskArchive).ProviderPath
if($taskZipResolved -ne [IO.Path]::GetFullPath($taskZip) -or -not $taskZipResolved.StartsWith($taskRootResolved+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Deletion target must be exact ZIP inside intended workspace'}
foreach($taskPath in @($taskZipResolved,$taskArchiveResolved,(Split-Path -Parent $taskZipResolved),(Split-Path -Parent $taskArchiveResolved))){if((Get-Item -LiteralPath $taskPath).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'No reparse points allowed in exact recovery paths'}}
if($taskProof.oldZIP -ne $taskZipResolved -or $taskProof.recoveryArchive -ne $taskArchiveResolved){throw 'Exact independently verified containers required'}
$taskPins=[ordered]@{}
foreach($taskEntry in $taskProof.inputHashes.PSObject.Properties){
 if([IO.Path]::GetFullPath($taskEntry.Name) -eq $taskZipResolved){throw 'Removed ZIP cannot be a live dependency'}
 if((Get-FileHash -LiteralPath $taskEntry.Name -Algorithm SHA256).Hash -ne $taskEntry.Value){throw ('Changed kept file '+$taskEntry.Name)}
 $taskPins[$taskEntry.Name]=$taskEntry.Value
}
if((Get-FileHash -LiteralPath $taskZipResolved -Algorithm SHA256).Hash -ne $taskProof.oldZipSHA256){throw 'Old ZIP changed after complete recovery proof'}
if((Get-FileHash -LiteralPath $taskArchiveResolved -Algorithm SHA256).Hash -ne $taskProof.recoveryArchiveSHA256){throw 'New recovery changed after complete recovery proof'}
$taskPins[$taskProofPath]=(Get-FileHash -LiteralPath $taskProofPath -Algorithm SHA256).Hash
$taskPins[$PSCommandPath]=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash
# All 61 original file bytes and 37 directories are already proven present in TAR.XZ.
# Remove only the exact redundant ZIP, never a folder or computed wildcard.
Remove-Item -LiteralPath $taskZipResolved -Force
if(Test-Path -LiteralPath $taskZipResolved){throw 'Exact redundant ZIP was not removed'}
foreach($taskEntry in $taskPins.GetEnumerator()){if((Get-FileHash -LiteralPath $taskEntry.Key -Algorithm SHA256).Hash -ne $taskEntry.Value){throw ('Kept dependency changed after retirement '+$taskEntry.Key)}}
New-Item -ItemType Directory -Path $taskOutput | Out-Null
$taskReport=[ordered]@{passed=$true;oldZIPDeleted=$true;removedRedundantZIP=$taskZipResolved;newRecoveryArchive=$taskArchiveResolved;
 recoveryArchiveSHA256=$taskProof.recoveryArchiveSHA256;verifiedFiles=61;verifiedDirectories=37;verifiedLogicalBytes=$taskProof.verifiedLogicalBytes;
 removedDirectories=$taskProof.removedDirectories;netOriginalBuildAllocationSavings=$taskProof.netOriginalBuildAllocationSavings;
 oldZIPContainerNotRetained=$true;allOriginalFileBytesAndDirectoriesRecoverable=$true;allCurrentPlayableAndSettingsUnchanged=$true;
 allOldBuildFoldersRemoved=$false;inputHashes=$taskPins;fullPortAcceptance=$false;
 scope='Retire only exact redundant ZIP after independent full solid-recovery verification; original files/directories remain recoverable, original ZIP-container bytes not retained.'}
$taskReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskOutput 'report.json') -Encoding UTF8
$taskReport | Select-Object passed,oldZIPDeleted,verifiedFiles,verifiedDirectories,netOriginalBuildAllocationSavings | ConvertTo-Json
