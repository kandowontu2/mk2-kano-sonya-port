param(
 [Parameter(Mandatory=$true)][string]$LeanPackageReceipt,
 [Parameter(Mandatory=$true)][string]$LeanPortableReceipt
)
$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskPlanPath=Join-Path $taskRoot 'audit_requested_old_release_retirement_plan_20261015\deletion_plan.json'
$taskPlan=Get-Content -LiteralPath $taskPlanPath -Raw | ConvertFrom-Json
$taskLean=Get-Content -LiteralPath $LeanPackageReceipt -Raw | ConvertFrom-Json
$taskPortable=Get-Content -LiteralPath $LeanPortableReceipt -Raw | ConvertFrom-Json
if(-not $taskLean.passedArchiveIntegrity -or -not $taskPortable.passedPortableHashAndROMCheck -or
 $taskPortable.exitCode -ne 0 -or -not $taskPortable.temporaryExtractionRemoved -or
 $taskPortable.zipSHA256 -ne $taskLean.zipSHA256){throw 'Completed lean archive and extracted CMD proofs required'}
$taskLatest=(Resolve-Path -LiteralPath $taskLean.zip).Path
if(-not $taskLatest.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or
 (Get-FileHash -LiteralPath $taskLatest).Hash -ne $taskLean.zipSHA256){throw 'Lean archive changed/outside workspace'}
$taskOut=Join-Path $taskRoot 'audit_requested_old_release_retirement_20261015'
if(Test-Path -LiteralPath $taskOut){throw 'Never overwrite executed retirement'}
$taskTargets=@($taskPlan.targets)+@([PSCustomObject]@{
 path=(Join-Path $taskRoot 'release_mk2_kano_sonya_20261015\MK2_Kano_Sonya_20261015.zip')
 bytes=59961702;SHA256='4B8288D0CC1E94D476D60D87C0EF4DF5B5BB22A0BD123D4943330A2CD223B9B2'
})
$taskAllow=@(
 'release_current_native_playtest_20261013\MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013.zip',
 'release_current_native_playtest_20261013_complete_roms\MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip',
 'release_v1863_current_playtest\MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip',
 'release_v5986_current_playtest\MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip',
 'release_mk2_kano_sonya_20261015\MK2_Kano_Sonya_20261015.zip'
)
function Assert-TaskRebuildPreservation {
 foreach($taskPin in $taskPlan.preservedHashes.PSObject.Properties){
  if($taskPin.Name -eq $taskPlan.latestPreserved){continue}
  if((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value){throw 'Current rebuild input changed'}
 }
 if((Get-FileHash -LiteralPath $taskLatest).Hash -ne $taskLean.zipSHA256){throw 'Latest lean ZIP changed'}
}
Assert-TaskRebuildPreservation
foreach($taskRow in $taskTargets){
 $taskResolved=(Resolve-Path -LiteralPath $taskRow.path).Path
 if($taskResolved -eq $taskLatest -or -not $taskResolved.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Invalid obsolete target'}
 $taskRel=$taskResolved.Substring($taskRoot.Length+1)
 if($taskRel -notin $taskAllow){throw 'Target not allowlisted'}
 for($taskCheck=$taskResolved;$taskCheck -ne $taskRoot;$taskCheck=[IO.Path]::GetDirectoryName($taskCheck)){
  if(-not $taskCheck -or (Get-Item -LiteralPath $taskCheck).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked/escaping old ZIP target'}
 }
 $taskInfo=Get-Item -LiteralPath $taskResolved
 if($taskInfo.PSIsContainer -or $taskInfo.Length -ne $taskRow.bytes -or
  (Get-FileHash -LiteralPath $taskResolved).Hash -ne $taskRow.SHA256){throw 'Obsolete ZIP changed'}
}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskRecords=@()
foreach($taskRow in $taskTargets){
 # Native file-only removal; never retry a denial through another mechanism.
 $taskRemoved=$false;$taskFailure=$null
 try {Remove-Item -LiteralPath $taskRow.path -Force -ErrorAction Stop;$taskRemoved=-not (Test-Path -LiteralPath $taskRow.path)}
 catch {$taskFailure=$_.Exception.Message}
 $taskRecords+=[ordered]@{path=$taskRow.path;SHA256=$taskRow.SHA256;bytes=$taskRow.bytes;removed=$taskRemoved;failure=$taskFailure;reason='User explicitly requested old release ZIP removal; not a current rebuild input.'}
}
Assert-TaskRebuildPreservation
$taskReceipt=[ordered]@{
 userAuthorizedOldReleaseRemoval=$true;archiveCreated=$false;removedFiles=$taskRecords
 latestZIP=$taskLatest;latestSHA256=$taskLean.zipSHA256;currentRebuildPreserved=$true
 oldArchiveBytesStillVerifiableAfterDeletion=$false
 logicalBytesRemoved=($taskRecords | Where-Object removed | Measure-Object bytes -Sum).Sum
 allRequestedRemoved=(@($taskRecords | Where-Object {-not $_.removed}).Count -eq 0)
 noPolicyBypassAttempted=$true;planSHA256=(Get-FileHash -LiteralPath $taskPlanPath).Hash
 leanPackageReceiptSHA256=(Get-FileHash -LiteralPath $LeanPackageReceipt).Hash
 leanPortableReceiptSHA256=(Get-FileHash -LiteralPath $LeanPortableReceipt).Hash
}
$taskReceipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $taskOut 'deletion_receipt.json')
$taskReceipt | ConvertTo-Json -Depth 6
