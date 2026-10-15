# Lossless compression of explicit retained non-running old builds; no deletions.
$ErrorActionPreference='Stop'
$mk2SpaceRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$mk2SpaceOut=Join-Path $mk2SpaceRoot 'audit_v5256_recent_retained_executable_compression'
if(Test-Path -LiteralPath $mk2SpaceOut){throw 'Fresh immutable evidence required'}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class Mk2AllocatedSpace5255 { [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path, out uint high); }'
function Get-Mk2Allocated([string]$mk2SpacePath){
 [uint32]$mk2SpaceHigh=0
 $mk2SpaceLow=[Mk2AllocatedSpace5255]::GetCompressedFileSizeW($mk2SpacePath,[ref]$mk2SpaceHigh)
 if($mk2SpaceLow -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Allocation API error'}
 return ([uint64]$mk2SpaceHigh -shl 32)+$mk2SpaceLow
}
$mk2SpaceLeaves=@('diagnostic_v4850_native_subzero_victim_offset','diagnostic_v4926_native_subzero_bodies','diagnostic_v4992_native_subzero_legs')
$mk2SpacePins=@{}
foreach($mk2SpaceRelative in @('PLAY_CURRENT_V1836_CHECKED.cmd','diagnostic_v1836_ball_register_boundary\mkport_candidate.exe','mame-mkp\mkport.exe','diagnostic_v5219_current_payload_rom_metadata\mkport_candidate.exe')){
 $mk2SpacePinnedPath=Join-Path $mk2SpaceRoot $mk2SpaceRelative
 $mk2SpacePins[$mk2SpacePinnedPath]=(Get-FileHash -LiteralPath $mk2SpacePinnedPath -Algorithm SHA256).Hash
}
$mk2SpaceProcesses=@(Get-CimInstance Win32_Process -Filter "Name='mkport_candidate.exe'" | Select-Object ProcessId,ExecutablePath,CommandLine)
$mk2SpaceTargets=@()
foreach($mk2SpaceLeaf in $mk2SpaceLeaves){
 $mk2SpaceExe=[IO.Path]::GetFullPath((Join-Path $mk2SpaceRoot "$mk2SpaceLeaf\mkport_candidate.exe"))
 if(-not $mk2SpaceExe.StartsWith($mk2SpaceRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Target escapes explicit project'}
 $mk2SpaceFile=Get-Item -LiteralPath $mk2SpaceExe
 if($mk2SpaceFile.PSIsContainer -or ($mk2SpaceFile.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Explicit normal file required'}
 foreach($mk2SpaceProc in $mk2SpaceProcesses){
  if($mk2SpaceProc.ExecutablePath -eq $mk2SpaceExe -or $mk2SpaceProc.CommandLine.Contains($mk2SpaceExe)){throw 'Never compress an actual running target'}
 }
 $mk2SpaceBuildPath=Join-Path $mk2SpaceRoot "$mk2SpaceLeaf\build-info.json"
 $mk2SpaceBuild=Get-Content -Raw -LiteralPath $mk2SpaceBuildPath | ConvertFrom-Json
 $mk2SpaceHash=(Get-FileHash -LiteralPath $mk2SpaceExe -Algorithm SHA256).Hash
 if($mk2SpaceHash -ne $mk2SpaceBuild.executable_sha256){throw 'Exact old compiled executable required'}
 $mk2SpacePins[$mk2SpaceBuildPath]=(Get-FileHash -LiteralPath $mk2SpaceBuildPath -Algorithm SHA256).Hash
 $mk2SpaceTargets+=[pscustomobject]@{Path=$mk2SpaceExe;SHA256=$mk2SpaceHash;LogicalBytes=$mk2SpaceFile.Length;AllocatedBefore=(Get-Mk2Allocated $mk2SpaceExe);LastWriteUtc=$mk2SpaceFile.LastWriteTimeUtc.ToString('o')}
}
$mk2SpaceResults=@()
foreach($mk2SpaceTarget in $mk2SpaceTargets){
 $mk2SpaceOutput=& compact.exe /C /F /EXE:LZX /I /Q $mk2SpaceTarget.Path 2>&1
 if($LASTEXITCODE -ne 0){throw "Native lossless compression failed: $mk2SpaceOutput"}
 $mk2SpaceAfter=Get-Item -LiteralPath $mk2SpaceTarget.Path
 $mk2SpaceAllocated=Get-Mk2Allocated $mk2SpaceTarget.Path
 $mk2SpaceAfterHash=(Get-FileHash -LiteralPath $mk2SpaceTarget.Path -Algorithm SHA256).Hash
 if($mk2SpaceAfterHash -ne $mk2SpaceTarget.SHA256 -or $mk2SpaceAfter.Length -ne $mk2SpaceTarget.LogicalBytes -or $mk2SpaceAfter.LastWriteTimeUtc.ToString('o') -ne $mk2SpaceTarget.LastWriteUtc -or $mk2SpaceAllocated -gt $mk2SpaceTarget.AllocatedBefore){throw 'Unchanged byte/time/allocation boundary failed'}
 $mk2SpaceResults+=[pscustomobject]@{Path=$mk2SpaceTarget.Path;SHA256=$mk2SpaceAfterHash;LogicalBytes=$mk2SpaceAfter.Length;AllocatedBefore=$mk2SpaceTarget.AllocatedBefore;AllocatedAfter=$mk2SpaceAllocated;AdditionalAllocatedBytesReclaimed=($mk2SpaceTarget.AllocatedBefore-$mk2SpaceAllocated);CompressionOutput=($mk2SpaceOutput -join [Environment]::NewLine)}
}
foreach($mk2SpacePinned in $mk2SpacePins.Keys){
 if((Get-FileHash -LiteralPath $mk2SpacePinned -Algorithm SHA256).Hash -ne $mk2SpacePins[$mk2SpacePinned]){throw 'Public/current/installed/source metadata bytes changed'}
}
$mk2SpaceScript=[IO.Path]::GetFullPath($PSCommandPath)
$mk2SpacePins[$mk2SpaceScript]=(Get-FileHash -LiteralPath $mk2SpaceScript -Algorithm SHA256).Hash
$mk2SpaceTotal=($mk2SpaceResults | Measure-Object -Property AdditionalAllocatedBytesReclaimed -Sum).Sum
$mk2SpaceReport=[ordered]@{passed=$true;files=$mk2SpaceResults;actualNativeProcessCensus=$mk2SpaceProcesses;inputHashes=$mk2SpacePins;additionalAllocatedBytesReclaimed=$mk2SpaceTotal;oldFilesDeleted=0;publicPlayableChanged=$false;newBuilds=0;rawMediaWritten=0;fullPortAcceptance=$false;scope='Lossless LZX only on three exact named retained non-running old executables. All full bytes/length/timestamps and public/current/installed bytes unchanged; prior savings not recounted.'}
New-Item -ItemType Directory -Path $mk2SpaceOut | Out-Null
$mk2SpaceReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $mk2SpaceOut 'report.json') -Encoding UTF8
[pscustomobject]@{passed=$true;files=3;additionalAllocatedBytesReclaimed=$mk2SpaceTotal;reclaimedMiB=[Math]::Round($mk2SpaceTotal/1MB,2);filesDeleted=0;publicPlayableChanged=$false} | ConvertTo-Json
