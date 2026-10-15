$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
if($taskRoot -ne 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'){throw 'Explicit user cleanup workspace only'}
$taskOut=Join-Path $taskRoot 'audit_v1632_immutable_old_build_compression'
if(Test-Path -LiteralPath $taskOut){throw 'Preserve previous cleanup evidence'}
$taskPilot=Get-Content -LiteralPath "$taskRoot\audit_v1631_immutable_build_compression_pilot\report.json" -Raw | ConvertFrom-Json
if(-not $taskPilot.passed -or $taskPilot.shaBefore -ne $taskPilot.shaAfter){throw 'Pilot must prove lossless savings'}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2Allocation1632 { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path,out uint high); }'
function Get-TaskAllocated([string]$taskPath){
 [uint32]$taskHigh=0;[uint32]$taskLow=[MK2Allocation1632]::GetCompressedFileSizeW($taskPath,[ref]$taskHigh)
 if($taskLow -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Allocation measurement failed'}
 return (([uint64]$taskHigh -shl 32)+[uint64]$taskLow)
}
function Assert-TaskLeaf([string]$taskPath){
 $taskResolved=(Resolve-Path -LiteralPath $taskPath).Path
 if(-not [string]::Equals($taskResolved,$taskPath,[StringComparison]::OrdinalIgnoreCase) -or -not $taskResolved.StartsWith($taskRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Exact workspace leaf required'}
 $taskItem=Get-Item -LiteralPath $taskResolved
 while($taskItem.FullName -ne $taskRoot){
  if($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Do not traverse links'}
  $taskItem=if($taskItem -is [IO.DirectoryInfo]){$taskItem.Parent}else{$taskItem.Directory}
 }
}
$taskKeep=@("$taskRoot\diagnostic_v1597_native_ground_throw\mkport_candidate.exe","$taskRoot\diagnostic_v1517_active_launch_timer\mkport_candidate.exe","$taskRoot\mame-mkp\mkport.exe","$taskRoot\PLAY_CURRENT_V1597_TEST_BUILD.cmd","$taskRoot\PLAY_CURRENT_V1517_TEST_BUILD.cmd")
$taskKeptHashes=@{};foreach($taskPath in $taskKeep){$taskKeptHashes[$taskPath]=(Get-FileHash -LiteralPath $taskPath).Hash}
$taskRunning=@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath} | ForEach-Object {$_.ExecutablePath})
$taskTargets=@();$taskSkipped=@()
foreach($taskDir in Get-ChildItem -LiteralPath $taskRoot -Directory){
 if($taskDir.Name -notmatch '^diagnostic_v([0-9]+)_'){continue}
 $taskVersion=[int]$Matches[1]
 if($taskVersion -ge 1597 -or $taskVersion -in @(43,1411,1473,1517,1002)){continue}
 $taskExe=Join-Path $taskDir.FullName 'mkport_candidate.exe';$taskBuildPath=Join-Path $taskDir.FullName 'build-info.json'
 if(-not(Test-Path -LiteralPath $taskExe) -or -not(Test-Path -LiteralPath $taskBuildPath)){continue}
 Assert-TaskLeaf $taskExe;Assert-TaskLeaf $taskBuildPath
 if($taskRunning -contains $taskExe){throw 'Do not compress a running old candidate'}
 $taskBuild=Get-Content -LiteralPath $taskBuildPath -Raw | ConvertFrom-Json
 $taskHash=(Get-FileHash -LiteralPath $taskExe).Hash
 if(-not $taskBuild.executable_sha256 -or $taskHash -ne $taskBuild.executable_sha256){$taskSkipped+=$taskExe;continue}
 $taskTargets+=[ordered]@{path=$taskExe;sha256=$taskHash;buildInfoPath=$taskBuildPath;buildInfoSHA=(Get-FileHash -LiteralPath $taskBuildPath).Hash;logicalBytes=(Get-Item -LiteralPath $taskExe).Length;allocatedBefore=(Get-TaskAllocated $taskExe)}
}
if(-not $taskTargets.Count){throw 'No independently hash-matched obsolete build leaves'}
New-Item -ItemType Directory -Path $taskOut | Out-Null
[ordered]@{targets=$taskTargets;keptHashes=$taskKeptHashes;skippedUnmatched=$taskSkipped;algorithm='LZX';deletions=0} | ConvertTo-Json -Depth 7 | Out-File -LiteralPath "$taskOut\before.json" -Encoding utf8
$taskResults=@()
foreach($taskTarget in $taskTargets){
 Assert-TaskLeaf $taskTarget.path
 if((Get-FileHash -LiteralPath $taskTarget.path).Hash -ne $taskTarget.sha256){throw 'Target changed after inventory'}
 if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $taskTarget.path}).Count){throw 'Target started during cleanup'}
 & "$env:SystemRoot\System32\compact.exe" /C /EXE:LZX /F /Q $taskTarget.path 2>&1 | Out-File -LiteralPath "$taskOut\compact.log" -Encoding utf8 -Append
 $taskCode=$LASTEXITCODE
 $taskHash=(Get-FileHash -LiteralPath $taskTarget.path).Hash
 if($taskHash -ne $taskTarget.sha256 -or (Get-FileHash -LiteralPath $taskTarget.buildInfoPath).Hash -ne $taskTarget.buildInfoSHA){throw 'Byte content changed during compression'}
 $taskAfter=Get-TaskAllocated $taskTarget.path
 if($taskCode -ne 0 -or $taskAfter -gt $taskTarget.allocatedBefore){throw 'Compression failed or grew a target'}
 $taskRow=[ordered]@{path=$taskTarget.path;shaBefore=$taskTarget.sha256;shaAfter=$taskHash;allocatedBefore=$taskTarget.allocatedBefore;allocatedAfter=$taskAfter;reclaimedBytes=($taskTarget.allocatedBefore-$taskAfter);compactExit=$taskCode}
 $taskResults+=$taskRow
 $taskRow | ConvertTo-Json -Compress | Out-File -LiteralPath "$taskOut\completed.jsonl" -Encoding utf8 -Append
 Write-Output ("Compressed {0}/{1}: {2}" -f $taskResults.Count,$taskTargets.Count,[IO.Path]::GetFileName([IO.Path]::GetDirectoryName($taskTarget.path)))
}
foreach($taskPath in $taskKeep){if((Get-FileHash -LiteralPath $taskPath).Hash -ne $taskKeptHashes[$taskPath]){throw 'Protected current/recovery byte content changed'}}
$taskSaved=($taskResults | ForEach-Object {$_.reclaimedBytes} | Measure-Object -Sum).Sum
[ordered]@{passed=$true;filesCompressed=$taskResults.Count;reclaimedBytes=$taskSaved;pilotReclaimedBytes=$taskPilot.reclaimedBytes;totalReclaimedIncludingPilot=($taskSaved+$taskPilot.reclaimedBytes);files=$taskResults;keptHashes=$taskKeptHashes;skippedUnmatched=$taskSkipped;allContentHashesUnchanged=$true;deletedFiles=0;allOldBuildFoldersRemoved=$false;currentCandidate='diagnostic_v1597_native_ground_throw';recovery='Lossless Windows LZX filesystem compression. Use compact /U /EXE on exact leaves to restore uncompressed allocation. No build/source/evidence paths removed.';fullPortAcceptance=$false} | ConvertTo-Json -Depth 7 | Out-File -LiteralPath "$taskOut\report.json" -Encoding utf8
[ordered]@{passed=$true;filesCompressed=$taskResults.Count;reclaimedBytes=$taskSaved;totalIncludingPilot=($taskSaved+$taskPilot.reclaimedBytes);deletedFiles=0} | ConvertTo-Json
