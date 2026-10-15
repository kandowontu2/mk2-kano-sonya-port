$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
if($taskRoot -ne 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'){throw 'Exact requested workspace only'}
$taskOut=Join-Path $taskRoot 'audit_v1729_completed_capture_log_compression'
if(Test-Path -LiteralPath $taskOut){throw 'Preserve prior evidence'}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2LogAllocation1728 { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path,out uint high); }'
function Get-TaskAllocated([string]$taskPath){
 [uint32]$taskHigh=0;[uint32]$taskLow=[MK2LogAllocation1728]::GetCompressedFileSizeW($taskPath,[ref]$taskHigh)
 if($taskLow -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Allocation measurement failed'}
 return (([uint64]$taskHigh -shl 32)+[uint64]$taskLow)
}
function Assert-TaskLeaf([string]$taskPath){
 $taskResolved=(Resolve-Path -LiteralPath $taskPath).Path
 if(-not [string]::Equals($taskResolved,$taskPath,[StringComparison]::OrdinalIgnoreCase) -or -not $taskResolved.StartsWith($taskRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Exact workspace leaf only'}
 $taskItem=Get-Item -LiteralPath $taskResolved
 while($taskItem.FullName -ne $taskRoot){
  if($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'No links'}
  $taskItem=if($taskItem -is [IO.DirectoryInfo]){$taskItem.Parent}else{$taskItem.Directory}
 }
}
$taskCases=@('audit_v1642_current_kano_p1_campaign','audit_v1664_current_kano_p1_native_counter','audit_v1700_current_kano_p1_early_native_counter')
$taskTargets=@()
foreach($taskCase in $taskCases){
 $taskPath=Join-Path (Join-Path $taskRoot $taskCase) 'run.log';Assert-TaskLeaf $taskPath
 $taskResult=Join-Path (Join-Path $taskRoot $taskCase) 'result.json';Assert-TaskLeaf $taskResult
 $taskMeta=Get-Content -LiteralPath $taskResult -Raw | ConvertFrom-Json
 if($taskMeta.exit_code -ne 0){throw 'Completed capture only'}
 if(@(Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -and $_.CommandLine.Contains($taskCase)}).Count){throw 'Capture or verifier still active'}
 $taskTargets+=[ordered]@{path=$taskPath;case=$taskCase;shaBefore=(Get-FileHash -LiteralPath $taskPath).Hash;logicalBytes=(Get-Item -LiteralPath $taskPath).Length;allocatedBefore=(Get-TaskAllocated $taskPath);resultSHA=(Get-FileHash -LiteralPath $taskResult).Hash}
}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskTargets | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$taskOut\before.json" -Encoding utf8
$taskResults=@()
foreach($taskTarget in $taskTargets){
 Assert-TaskLeaf $taskTarget.path
 if((Get-FileHash -LiteralPath $taskTarget.path).Hash -ne $taskTarget.shaBefore){throw 'Target changed after inventory'}
 & "$env:SystemRoot\System32\compact.exe" /C /EXE:LZX /F /Q $taskTarget.path 2>&1 | Out-File -LiteralPath "$taskOut\compact.log" -Encoding utf8 -Append
 $taskExit=$LASTEXITCODE;$taskHash=(Get-FileHash -LiteralPath $taskTarget.path).Hash;$taskAfter=Get-TaskAllocated $taskTarget.path
 if($taskExit -ne 0 -or $taskHash -ne $taskTarget.shaBefore -or $taskAfter -gt $taskTarget.allocatedBefore){throw 'Lossless compression check failed'}
 $taskResults+=[ordered]@{path=$taskTarget.path;shaBefore=$taskTarget.shaBefore;shaAfter=$taskHash;logicalBytes=$taskTarget.logicalBytes;allocatedBefore=$taskTarget.allocatedBefore;allocatedAfter=$taskAfter;reclaimedBytes=($taskTarget.allocatedBefore-$taskAfter)}
 Write-Output ("Losslessly compressed completed log: "+$taskTarget.case)
}
$taskSaved=($taskResults | ForEach-Object {$_.reclaimedBytes} | Measure-Object -Sum).Sum
[ordered]@{passed=$true;filesCompressed=$taskResults.Count;reclaimedBytes=$taskSaved;allContentHashesUnchanged=$true;files=$taskResults;deletedFiles=0;allOldBuildFoldersRemoved=$false;recovery='compact /U /EXE on these three exact leaves; files remain readable at their existing paths';fullPortAcceptance=$false} | ConvertTo-Json -Depth 7 | Out-File -LiteralPath "$taskOut\report.json" -Encoding utf8
[ordered]@{passed=$true;filesCompressed=$taskResults.Count;reclaimedBytes=$taskSaved;deletedFiles=0} | ConvertTo-Json
