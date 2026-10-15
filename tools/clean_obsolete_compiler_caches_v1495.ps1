$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$out=Join-Path $root 'audit_v1495_old_compiler_cache_cleanup'
if(Test-Path -LiteralPath $out){throw 'Never overwrite cleanup evidence'}
$cacheRoot=(Resolve-Path -LiteralPath "$root/mame-mkp/build/mingw-gcc/bin/x64/Release").Path
$targets=@("$cacheRoot/mame_mkprobe","$cacheRoot/mame_mkwport")
$activeNames=@('gmake.exe','gcc.exe','g++.exe','cc1plus.exe','ld.exe','mkport.exe','mkprobe.exe','mkwport.exe','hbmame.exe')
if(@(Get-CimInstance Win32_Process | Where-Object {$_.Name -in $activeNames -and ($_.CommandLine -match 'mk2port|mame-mkp|SUBTARGET=(mkport|mkprobe|mkwport)' -or ($_.ExecutablePath -and $_.ExecutablePath.StartsWith($root,[StringComparison]::OrdinalIgnoreCase)))}).Count){throw 'Relevant MK2 build/emulator process is active; do not clean'}
$inventory=@()
foreach($target in $targets){
 $resolved=(Resolve-Path -LiteralPath $target).Path
 if(-not $resolved.StartsWith($cacheRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Cache target outside checked compiler output directory'}
 if((Split-Path $resolved -Leaf) -notin @('mame_mkprobe','mame_mkwport')){throw 'Wrong obsolete subtarget'}
 if(@(Get-ChildItem -LiteralPath $resolved -Directory).Count){throw 'Unexpected nested cache data'}
 $files=@(Get-ChildItem -LiteralPath $resolved -File)
 if($files.Count -ne 4 -or @($files | Where-Object {$_.Extension -ne '.a'}).Count){throw 'Unexpected non-library data; preserve it'}
 $inventory+=@($files | ForEach-Object {[ordered]@{path=$_.FullName;bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash}})
}
$kept=@("$root/mame-mkp/mkport.exe","$root/mame-mkp/mkwport.exe","$root/diagnostic_v1411_native_grab_audio/mkport_candidate.exe","$root/diagnostic_v1473_sonya_launch_audio/mkport_candidate.exe","$root/PLAY_CURRENT_V1411_TEST_BUILD.cmd")
$keptHashes=@{};foreach($path in $kept){$keptHashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$logPaths=@('audit_v1478_host_launch_square_p1','audit_v1478_host_launch_square_p2','audit_v1478_host_launch_bicycle_p1','audit_v1478_host_launch_bicycle_p2','audit_v1478_baseline_square_air_p1','audit_v1478_baseline_square_air_p2') | ForEach-Object {(Resolve-Path -LiteralPath "$root/$_/run.log").Path}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2CleanupAllocation1495 { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path,out uint high); }'
function Get-TaskAllocatedBytes([string]$path){[uint32]$high=0;[uint32]$low=[MK2CleanupAllocation1495]::GetCompressedFileSizeW($path,[ref]$high);if($low -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Allocated size unavailable'};return (([uint64]$high -shl 32)+[uint64]$low)}
$logs=@();foreach($path in $logPaths){$logs+=[ordered]@{path=$path;sha256=(Get-FileHash -LiteralPath $path).Hash;logicalBytes=(Get-Item -LiteralPath $path).Length;allocatedBefore=(Get-TaskAllocatedBytes $path)}}
New-Item -ItemType Directory -Path $out | Out-Null
[ordered]@{cacheFiles=$inventory;keptHashes=$keptHashes;logs=$logs;toolSHA256=(Get-FileHash -LiteralPath $PSCommandPath).Hash} | ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$out/before.json" -Encoding utf8
# Exact, checked obsolete compiler-library directories only. These libraries
# regenerate from retained source; installed/frozen executables are not deleted.
foreach($target in $targets){$resolved=(Resolve-Path -LiteralPath $target).Path;Remove-Item -LiteralPath $resolved -Recurse -Force}
foreach($row in $logs){
 & compact.exe /C /I /EXE:LZX $row.path | Out-File -LiteralPath "$out/compaction.log" -Append -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'NTFS compaction failed'}
 if((Get-FileHash -LiteralPath $row.path).Hash -ne $row.sha256){throw 'Log contents changed'}
 $row['allocatedAfter']=Get-TaskAllocatedBytes $row.path
}
foreach($path in $kept){if((Get-FileHash -LiteralPath $path).Hash -ne $keptHashes[$path]){throw 'Preserved build or launcher changed'}}
$cacheBytes=($inventory | Measure-Object -Property bytes -Sum).Sum
$logSaved=0L;foreach($row in $logs){$logSaved+=($row.allocatedBefore-$row.allocatedAfter)}
$report=[ordered]@{passed=$true;removedDirectories=$targets;removedFiles=$inventory;removedLogicalCacheBytes=$cacheBytes;recovery='Deleted compiler libraries regenerate from retained source; playable EXEs and source preserved';logs=$logs;logAllocatedBytesReclaimed=$logSaved;keptHashes=$keptHashes;allObsoleteBuildFoldersCleaned=$false;fullPortAccepted=$false}
$report | ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$out/report.json" -Encoding utf8
[ordered]@{removedCompilerCacheBytes=$cacheBytes;logAllocatedBytesReclaimed=$logSaved;allObsoleteBuildFoldersCleaned=$false} | ConvertTo-Json
