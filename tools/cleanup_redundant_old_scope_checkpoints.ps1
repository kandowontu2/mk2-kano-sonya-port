$ErrorActionPreference='Stop'
$taskRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskReceipt=Join-Path $taskRoot 'CLEANUP_REDUNDANT_SCOPE_CHECKPOINTS_2026-10-13.json'
if(Test-Path -LiteralPath $taskReceipt){throw 'Already executed'}
$taskExpected=[ordered]@{
'audit_v3208_corrected_morph_shadow_full_scope_checkpoint\checkpoint.json'=33422768
'audit_v3260_cleanup_and_adversity_full_scope_checkpoint\checkpoint.json'=33798842
'audit_v3288_current_cpu_square_full_scope_checkpoint\checkpoint.json'=33840383
'audit_v3334_current_bicycle_full_scope_checkpoint\checkpoint.json'=34073440
'audit_v3344_current_bicycle_push_full_scope_checkpoint\checkpoint.json'=34076851
'audit_v3355_current_bicycle_block_full_scope_checkpoint\checkpoint.json'=34089697
'audit_v3369_current_bicycle_block_render_full_scope_checkpoint\checkpoint.json'=34222955
'audit_v3385_current_bicycle_block_push_full_scope_checkpoint\checkpoint.json'=34237906
'audit_v3394_current_bicycle_block_audio_full_scope_checkpoint\checkpoint.json'=34264169
}
$taskTargets=@()
foreach($taskName in $taskExpected.Keys){
 $taskPath=[IO.Path]::GetFullPath((Join-Path $taskRoot $taskName))
 if(-not $taskPath.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Outside explicit root'}
 $taskItem=Get-Item -LiteralPath $taskPath
 if($taskItem.PSIsContainer -or $taskItem.Length -ne $taskExpected[$taskName]){throw 'Unexpected exact target size'}
 if(($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -or ((Get-Item -LiteralPath $taskItem.DirectoryName).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Reparse path'}
 $taskStream=[IO.File]::OpenRead($taskPath)
 try{$taskBuffer=New-Object byte[] 4096;$taskCount=$taskStream.Read($taskBuffer,0,4096);$taskHeader=[Text.Encoding]::UTF8.GetString($taskBuffer,0,$taskCount)}finally{$taskStream.Dispose()}
 if(-not $taskHeader.Contains('diagnostic_v1836_ball_register_boundary') -or -not $taskHeader.Contains('previousCheckpoint')){throw 'Not known superseded copied scope checkpoint'}
 $taskTargets+=[pscustomobject]@{Path=$taskPath;Length=$taskItem.Length;SHA256=(Get-FileHash -LiteralPath $taskPath).Hash}
}
$taskBefore=([IO.DriveInfo]::new('C')).AvailableFreeSpace
foreach($taskTarget in $taskTargets){
 if((Get-Item -LiteralPath $taskTarget.Path).Length -ne $taskTarget.Length){throw 'Target changed'}
 Remove-Item -LiteralPath $taskTarget.Path -Force
 if(Test-Path -LiteralPath $taskTarget.Path){throw 'Deletion not confirmed'}
}
$taskAfter=([IO.DriveInfo]::new('C')).AvailableFreeSpace
$taskReport=[ordered]@{Timestamp=(Get-Date).ToString('o');DeletedFiles=$taskTargets.Count;LogicalBytesRemoved=($taskTargets|Measure-Object Length -Sum).Sum;DriveFreeBytesBefore=$taskBefore;DriveFreeBytesAfter=$taskAfter;ObservedFreeSpaceDelta=$taskAfter-$taskBefore;Targets=$taskTargets;Archived=$false;RecoverableByThisTool=$false;CurrentBuildRemoved=$false;HistoricalCheckpointChainsRerunnable=$false;Scope='Nine exact superseded v3208..3394 copied scope checkpoint JSON files only; current full-scope frontier, source/build/assets/tests and independent reports retained'}
$taskReport|ConvertTo-Json -Depth 5|Set-Content -LiteralPath $taskReceipt
[pscustomobject]@{DeletedFiles=$taskTargets.Count;LogicalBytesRemoved=$taskReport.LogicalBytesRemoved;ObservedFreeSpaceDelta=$taskReport.ObservedFreeSpaceDelta}|ConvertTo-Json
