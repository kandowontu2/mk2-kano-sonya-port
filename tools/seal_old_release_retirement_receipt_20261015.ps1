# No deletion: verify completed removals after the first receipt formatter failed.
$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskOut=Join-Path $taskRoot 'audit_requested_old_release_retirement_20261015'
$taskReceipt=Join-Path $taskOut 'deletion_receipt.json'
if(Test-Path -LiteralPath $taskReceipt){throw 'Never overwrite receipt'}
$taskPlanPath=Join-Path $taskRoot 'audit_requested_old_release_retirement_plan_20261015/deletion_plan.json'
$taskPlan=Get-Content -LiteralPath $taskPlanPath -Raw|ConvertFrom-Json
$taskLatestReceipt=Join-Path $taskRoot 'release_mk2_kano_sonya_20261015_player/package-report.json'
$taskLatest=Get-Content -LiteralPath $taskLatestReceipt -Raw|ConvertFrom-Json
$taskPortablePath=Join-Path $taskRoot 'audit_lean_player_portable_check_20261015/report.json'
$taskPortable=Get-Content -LiteralPath $taskPortablePath -Raw|ConvertFrom-Json
if(-not $taskLatest.passedArchiveIntegrity -or -not $taskPortable.passedPortableHashAndROMCheck -or $taskPortable.exitCode -ne 0 -or $taskPortable.zipSHA256 -ne $taskLatest.zipSHA256){throw 'Latest package not verified'}
if((Get-FileHash -LiteralPath $taskLatest.zip).Hash -ne $taskLatest.zipSHA256){throw 'Latest changed'}
foreach($taskPin in $taskPlan.preservedHashes.PSObject.Properties){
 if($taskPin.Name -eq $taskPlan.latestPreserved){continue}
 if((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value){throw 'Rebuild input changed'}
}
$taskTargets=@($taskPlan.targets)+@([PSCustomObject]@{path=(Join-Path $taskRoot 'release_mk2_kano_sonya_20261015/MK2_Kano_Sonya_20261015.zip');bytes=59961702;SHA256='4B8288D0CC1E94D476D60D87C0EF4DF5B5BB22A0BD123D4943330A2CD223B9B2'})
$taskRecords=@();$taskTotal=0L
foreach($taskRow in $taskTargets){
 if(Test-Path -LiteralPath $taskRow.path){throw 'Target remains; do not claim deletion'}
 $taskRecords+=[PSCustomObject]@{path=$taskRow.path;SHA256=$taskRow.SHA256;bytes=$taskRow.bytes;removed=$true;reason='Explicit renewed user request; pre-deletion exact path/length/hash checks passed in original remover.'}
 $taskTotal+=[long]$taskRow.bytes
}
[ordered]@{userAuthorizedOldReleaseRemoval=$true;archiveCreated=$false;removedFiles=$taskRecords;latestZIP=$taskLatest.zip;latestSHA256=$taskLatest.zipSHA256;currentRebuildPreserved=$true;oldArchiveBytesStillVerifiableAfterDeletion=$false;logicalBytesRemoved=$taskTotal;allRequestedRemoved=$true;noPolicyBypassAttempted=$true;planSHA256=(Get-FileHash -LiteralPath $taskPlanPath).Hash;leanPackageReceiptSHA256=(Get-FileHash -LiteralPath $taskLatestReceipt).Hash;leanPortableReceiptSHA256=(Get-FileHash -LiteralPath $taskPortablePath).Hash;receiptRecovery='Original native remover completed deletions and rebuild preservation, then OrderedDictionary Measure-Object formatter failed. This read-only successor confirms all five absences and rehashes every retained rebuild input; no deletion retried.'}|ConvertTo-Json -Depth 6|Set-Content -LiteralPath $taskReceipt
Get-FileHash -LiteralPath $taskReceipt
Get-Content -LiteralPath $taskReceipt
