$ErrorActionPreference='Stop'
$taskRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskReview=Join-Path $taskRoot 'audit_obsolete_combat_snapshot_review_20261015'
$taskReceipt=Join-Path $taskReview 'deletion_receipt.json'
if(Test-Path -LiteralPath $taskReceipt){throw 'Already executed'}
$taskPlan=Get-Content -LiteralPath (Join-Path $taskReview 'deletion_plan.json') -Raw | ConvertFrom-Json
$taskAllowed=@('snap\special_join_kano','snap\special2p_kano','snap\special2p_sonya','snap\special_health_kano')
if($taskPlan.targets.Count -ne 4 -or $taskPlan.totalFiles -ne 603){throw 'Unexpected plan'}
$taskDelete=@()
foreach($taskRelative in $taskAllowed){
 $taskExact=Join-Path $taskRoot $taskRelative
 $taskTarget=@($taskPlan.targets | Where-Object {$_.path -eq $taskExact})
 if($taskTarget.Count -ne 1){throw 'Exact allowlist mismatch'}
 $taskResolved=(Resolve-Path -LiteralPath $taskExact).Path
 if($taskResolved -ne $taskExact -or -not $taskResolved.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Containment failure'}
 $taskChildren=@(Get-ChildItem -LiteralPath $taskResolved -Recurse -Force)
 foreach($taskItem in @((Get-Item -LiteralPath $taskResolved))+$taskChildren){if($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked node'}}
 if(@($taskChildren | Where-Object {-not $_.PSIsContainer}).Count -ne $taskTarget[0].files.Count){throw 'File set changed'}
 foreach($taskFile in $taskTarget[0].files){
  $taskPath=(Resolve-Path -LiteralPath $taskFile.path).Path
  if(-not $taskPath.StartsWith($taskResolved+'\',[StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetExtension($taskPath) -ne '.png'){throw 'Unexpected target'}
  if((Get-Item -LiteralPath $taskPath).Length -ne $taskFile.bytes -or (Get-FileHash -LiteralPath $taskPath).Hash -ne $taskFile.SHA256){throw 'Changed bytes'}
  $taskDelete+=$taskPath
 }
}
if($taskDelete.Count -ne 603 -or @($taskDelete | Select-Object -Unique).Count -ne 603){throw 'Nonunique target set'}
foreach($taskPath in $taskDelete){Remove-Item -LiteralPath $taskPath -ErrorAction Stop}
foreach($taskRelative in $taskAllowed){
 $taskExact=Join-Path $taskRoot $taskRelative
 $taskDirs=@(Get-ChildItem -LiteralPath $taskExact -Directory -Recurse -Force | Sort-Object {$_.FullName.Length} -Descending)
 foreach($taskDir in $taskDirs){if(@(Get-ChildItem -LiteralPath $taskDir.FullName -Force).Count){throw 'Not empty'};Remove-Item -LiteralPath $taskDir.FullName}
 if(@(Get-ChildItem -LiteralPath $taskExact -Force).Count){throw 'Target not empty'}
 Remove-Item -LiteralPath $taskExact
 if(Test-Path -LiteralPath $taskExact){throw 'Target survived'}
}
[ordered]@{deletedFiles=603;allocatedBytesFromCensus=30784765;targets=$taskAllowed;archiveCreated=$false;permanentDeletion=$true;retained='Original UI screenshots, accepted captures, cfg/NVRAM/Lua and source assets';planSHA256=(Get-FileHash -LiteralPath (Join-Path $taskReview 'deletion_plan.json')).Hash}|ConvertTo-Json -Depth 4|Set-Content -LiteralPath $taskReceipt
Get-Content -LiteralPath $taskReceipt
