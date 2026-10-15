$ErrorActionPreference='Stop'
$taskRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskReview=Join-Path $taskRoot 'audit_old_rom_tree_duplicate_review_20261015'
$taskReceipt=Join-Path $taskReview 'deletion_receipt.json'
if(Test-Path -LiteralPath $taskReceipt){throw 'Already executed'}
$taskPlan=Get-Content -LiteralPath (Join-Path $taskReview 'deletion_plan.json') -Raw | ConvertFrom-Json
$taskAllowed=@('roms_v19_clean','roms_v20_clean','roms_v21_clean','release_rom_stage') | ForEach-Object {Join-Path $taskRoot $_}
if($taskPlan.targets.Count -ne 130 -or $taskPlan.candidateFiles -ne 130 -or $taskPlan.allocatedCandidateBytes -ne 103828212){throw 'Unexpected plan'}
$taskSet=@{}
foreach($taskFile in $taskPlan.targets){
 $taskPath=(Resolve-Path -LiteralPath $taskFile.path).Path
 if($taskSet.ContainsKey($taskPath)){throw 'Duplicate target'}
 $taskSet[$taskPath]=$true
 if(-not @($taskAllowed | Where-Object {$taskPath.StartsWith($_+'\',[StringComparison]::OrdinalIgnoreCase)}).Count){throw 'Outside exact old folders'}
 if(-not $taskPath.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Outside workspace'}
}
foreach($taskFile in $taskPlan.targets){
 $taskPath=(Resolve-Path -LiteralPath $taskFile.path).Path
 $taskRetained=(Resolve-Path -LiteralPath $taskFile.retainedIdenticalFile).Path
 if($taskSet.ContainsKey($taskRetained)){throw 'Retained copy also targeted'}
 foreach($taskCheck in @($taskPath,$taskRetained)){
  if(-not $taskCheck.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Retained path outside workspace'}
  $taskNode=Get-Item -LiteralPath $taskCheck
  if($taskNode.PSIsContainer -or ($taskNode.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $taskNode.Length -ne $taskFile.bytes){throw 'Changed file type or size'}
  if((Get-FileHash -LiteralPath $taskCheck).Hash -ne $taskFile.SHA256){throw 'Target or retained bytes changed'}
  $taskParent=$taskNode.Directory
  while($taskParent.FullName -ne $taskRoot){
   if($taskParent.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked ancestor'}
   $taskParent=$taskParent.Parent
   if(-not $taskParent){throw 'Invalid ancestry'}
  }
 }
}
foreach($taskFile in $taskPlan.targets){Remove-Item -LiteralPath $taskFile.path -ErrorAction Stop}
foreach($taskFile in $taskPlan.targets){
 if(Test-Path -LiteralPath $taskFile.path){throw 'Target survived'}
 if((Get-FileHash -LiteralPath $taskFile.retainedIdenticalFile).Hash -ne $taskFile.SHA256){throw 'Retained copy changed'}
}
[ordered]@{deletedFiles=130;allocatedBytesFromCensus=103828212;permanentDeletion=$true;archiveCreated=$false;wholeFoldersDeleted=$false;retainedIdenticalCopiesRechecked=$true;unmatchedOriginalsPreserved=$true;planSHA256=(Get-FileHash -LiteralPath (Join-Path $taskReview 'deletion_plan.json')).Hash}|ConvertTo-Json|Set-Content -LiteralPath $taskReceipt
Get-Content -LiteralPath $taskReceipt
