$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskOut=Join-Path $taskRoot 'audit_v1631_immutable_build_compression_pilot'
$taskExpected=Join-Path $taskRoot 'diagnostic_v1002_owned_rolling_head_order\mkport_candidate.exe'
$taskTarget=(Resolve-Path -LiteralPath $taskExpected).Path
if(-not [string]::Equals($taskTarget,$taskExpected,[StringComparison]::OrdinalIgnoreCase) -or -not $taskTarget.StartsWith($taskRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Exact workspace leaf required'}
if(Test-Path -LiteralPath $taskOut){throw 'Preserve previous evidence'}
if((Get-Item -LiteralPath $taskTarget).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'No links'}
if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $taskTarget}).Count){throw 'Do not compress live executable'}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2Allocation1631 { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path,out uint high); }'
function Get-TaskAllocated([string]$taskPath){
 [uint32]$taskHigh=0;[uint32]$taskLow=[MK2Allocation1631]::GetCompressedFileSizeW($taskPath,[ref]$taskHigh)
 if($taskLow -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Allocation measurement failed'}
 return (([uint64]$taskHigh -shl 32)+[uint64]$taskLow)
}
$taskBeforeHash=(Get-FileHash -LiteralPath $taskTarget).Hash
$taskBefore=Get-TaskAllocated $taskTarget
$taskLength=(Get-Item -LiteralPath $taskTarget).Length
New-Item -ItemType Directory -Path $taskOut | Out-Null
[ordered]@{path=$taskTarget;sha256=$taskBeforeHash;logicalBytes=$taskLength;allocatedBytes=$taskBefore} | ConvertTo-Json | Out-File -LiteralPath "$taskOut\before.json" -Encoding utf8
& "$env:SystemRoot\System32\compact.exe" /C /EXE:LZX /F /Q $taskTarget 2>&1 | Out-File -LiteralPath "$taskOut\compact.log" -Encoding utf8
$taskCode=$LASTEXITCODE
$taskAfterHash=(Get-FileHash -LiteralPath $taskTarget).Hash
$taskAfter=Get-TaskAllocated $taskTarget
$taskPassed=$taskCode -eq 0 -and $taskBeforeHash -eq $taskAfterHash -and $taskAfter -lt $taskBefore
[ordered]@{passed=$taskPassed;path=$taskTarget;compactExit=$taskCode;shaBefore=$taskBeforeHash;shaAfter=$taskAfterHash;logicalBytes=$taskLength;allocatedBefore=$taskBefore;allocatedAfter=$taskAfter;reclaimedBytes=($taskBefore-$taskAfter);deletedFiles=0;sourceAndEvidenceBytesUnchanged=($taskBeforeHash -eq $taskAfterHash);allOldBuildFoldersRemoved=$false;recovery='Lossless Windows compression; compact /U /EXE restores uncompressed storage without changing file contents.'} | ConvertTo-Json | Out-File -LiteralPath "$taskOut\report.json" -Encoding utf8
Get-Content -LiteralPath "$taskOut\report.json" -Raw
if(-not $taskPassed){exit 1}
