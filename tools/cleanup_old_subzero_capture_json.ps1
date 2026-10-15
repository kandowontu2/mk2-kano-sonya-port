$ErrorActionPreference='Stop'
$taskRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskReceipt=Join-Path $taskRoot 'CLEANUP_OLD_SUBZERO_CAPTURE_JSON_2026-10-13.json'
if(Test-Path -LiteralPath $taskReceipt){throw 'Already executed'}
$taskNames=@(
'audit_v6200_current_normal_subzero_kano_p1/result.json',
'audit_v6200_current_normal_subzero_kano_p2/result.json',
'audit_v6200_current_normal_subzero_kitana_p1/result.json',
'audit_v6200_current_normal_subzero_liu_kang_p2/result.json',
'audit_v6200_current_normal_subzero_sonya_p1/result.json',
'audit_v6200_current_normal_subzero_sonya_p2/result.json',
'audit_v6201_current_normal_subzero_kano_p1_observed/report.json',
'audit_v6201_current_normal_subzero_kano_p2_observed/report.json',
'audit_v6201_current_normal_subzero_kitana_p1_observed/report.json',
'audit_v6201_current_normal_subzero_liu_kang_p2_observed/report.json',
'audit_v6201_current_normal_subzero_sonya_p1_observed/report.json',
'audit_v6201_current_normal_subzero_sonya_p2_observed/report.json',
'audit_v6203_current_normal_subzero_sonya_p1/result.json',
'audit_v6204_current_normal_subzero_sonya_p1_observed/report.json')
$taskTargets=@()
foreach($taskName in $taskNames){
 $taskPath=[IO.Path]::GetFullPath((Join-Path $taskRoot $taskName))
 if(-not $taskPath.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Outside exact root'}
 $taskItem=Get-Item -LiteralPath $taskPath
 if($taskItem.PSIsContainer -or $taskItem.Length -lt 40MB -or $taskItem.Length -gt 60MB){throw 'Unexpected target'}
 if($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse target'}
 $taskStream=[IO.File]::OpenRead($taskPath)
 try{
  $taskBuffer=New-Object byte[] 512
  $taskCount=$taskStream.Read($taskBuffer,0,512)
  $taskHeader=[Text.Encoding]::UTF8.GetString($taskBuffer,0,$taskCount)
 }finally{$taskStream.Dispose()}
 if(-not $taskHeader.Contains('A6BC32F526C78A5BD72ED1960EAE56AB40701D7FE881D70A93E031AEB87AB944')){throw 'Not known old executable capture'}
 $taskTargets+= [pscustomobject]@{Path=$taskPath;Length=$taskItem.Length;SHA256=(Get-FileHash -LiteralPath $taskPath).Hash}
}
$taskBefore=([IO.DriveInfo]::new('C')).AvailableFreeSpace
foreach($taskTarget in $taskTargets){
 if((Get-Item -LiteralPath $taskTarget.Path).Length -ne $taskTarget.Length){throw 'Target changed'}
 Remove-Item -LiteralPath $taskTarget.Path -Force
 if(Test-Path -LiteralPath $taskTarget.Path){throw 'Deletion not confirmed'}
}
$taskAfter=([IO.DriveInfo]::new('C')).AvailableFreeSpace
$taskReport=[ordered]@{Timestamp=(Get-Date).ToString('o');DeletedFiles=$taskTargets.Count;LogicalBytesRemoved=($taskTargets|Measure-Object Length -Sum).Sum;DriveFreeBytesBefore=$taskBefore;DriveFreeBytesAfter=$taskAfter;ObservedFreeSpaceDelta=$taskAfter-$taskBefore;Targets=$taskTargets;Archived=$false;RecoverableByThisTool=$false;CurrentBuildRemoved=$false;HistoricalDenseChecksRerunnable=$false;Scope='Exact14oldSubZeroJSONcapturesandduplicatereports;smallmetadata/scriptsretained'}
$taskReport|ConvertTo-Json -Depth 5|Set-Content -LiteralPath $taskReceipt
$taskReport|Select-Object DeletedFiles,LogicalBytesRemoved,ObservedFreeSpaceDelta|ConvertTo-Json
