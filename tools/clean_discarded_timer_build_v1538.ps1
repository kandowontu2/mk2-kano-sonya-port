$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$out=Join-Path $root 'audit_v1538_discarded_timer_build_cleanup'
$target=(Resolve-Path -LiteralPath (Join-Path $root 'diagnostic_v1514_active_launch_timer')).Path
$expected=Join-Path $root 'diagnostic_v1514_active_launch_timer'
if(-not [string]::Equals($target,$expected,[StringComparison]::OrdinalIgnoreCase) -or
   -not $target.StartsWith($root+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){
    throw 'Discarded target outside exact checked workspace directory.'
}
if(Test-Path -LiteralPath $out){throw 'Preserve existing cleanup evidence'}
if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq (Join-Path $target 'mkport_candidate.exe')}).Count){throw 'Discarded candidate is running'}
if(@(Get-ChildItem -LiteralPath $target -Recurse | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'Unexpected link in discarded build'}
$files=@(Get-ChildItem -LiteralPath $target -Recurse -File)
if($files.Count -ne 17){throw 'Unexpected user files in discarded build; preserve it'}
if((Get-FileHash -LiteralPath "$target\mkport_candidate.exe").Hash -ne 'CDDC3C0A2753F0D5C13F9EE943C0111231DCA78F1621DEB99BA9E7C0E127ED8F'){
    throw 'Discarded executable changed; preserve it'
}
$build=Get-Content -LiteralPath "$target\build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw 'Discarded input changed; preserve it'}
}
$kept=@("$root\diagnostic_v1517_active_launch_timer\mkport_candidate.exe","$root\diagnostic_v1473_sonya_launch_audio\mkport_candidate.exe","$root\diagnostic_v1411_native_grab_audio\mkport_candidate.exe","$root\PLAY_CURRENT_V1517_TEST_BUILD.cmd","$root\PLAY_CURRENT_V1411_TEST_BUILD.cmd","$root\tools\build_active_launch_timer_v1513.ps1","$root\audit_v1512_active_launch_timer_source\midtunit_m.cpp")
$keptHashes=@{};foreach($p in $kept){$keptHashes[$p]=(Get-FileHash -LiteralPath $p).Hash}
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2CleanupAllocation1538 { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path,out uint high); }'
function Get-AllocatedBytes([string]$p){
    [uint32]$high=0;[uint32]$low=[MK2CleanupAllocation1538]::GetCompressedFileSizeW($p,[ref]$high)
    if($low -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Allocated size unavailable'}
    return (([uint64]$high -shl 32)+[uint64]$low)
}
New-Item -ItemType Directory -Path "$out\preserved" | Out-Null
$inventory=@();$retainedHashes=@{};$logical=0L;$allocated=0L
foreach($file in $files){
    $relative=[IO.Path]::GetRelativePath($target,$file.FullName)
    $hash=(Get-FileHash -LiteralPath $file.FullName).Hash
    $bytes=Get-AllocatedBytes $file.FullName
    $inventory+=[ordered]@{relativePath=$relative;bytes=$file.Length;allocatedBytes=$bytes;sha256=$hash}
    $logical+=$file.Length;$allocated+=$bytes
    if($file.Extension -notin '.exe','.mdata'){
        $dest=Join-Path "$out\preserved" $relative
        New-Item -ItemType Directory -Path (Split-Path $dest -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $dest
        if((Get-FileHash -LiteralPath $dest).Hash -ne $hash){throw 'Preserved source/metadata mismatch'}
        $retainedHashes[$dest]=$hash
    }
}
[ordered]@{target=$target;inventory=$inventory;keptHashes=$keptHashes;retainedHashes=$retainedHashes} | ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$out\before.json" -Encoding utf8
# Exact obsolete build from this turn only. Full frozen source and build logs
# are preserved; its executable regenerates with the retained v1513 builder.
Remove-Item -LiteralPath $target -Recurse -Force
if(Test-Path -LiteralPath $target){throw 'Discarded target still exists'}
foreach($p in $kept){if((Get-FileHash -LiteralPath $p).Hash -ne $keptHashes[$p]){throw 'Preserved playable/source input changed'}}
foreach($p in $retainedHashes.Keys){if((Get-FileHash -LiteralPath $p).Hash -ne $retainedHashes[$p]){throw 'Archived source changed'}}
[ordered]@{passed=$true;removedDirectory=$target;removedLogicalBytes=$logical;removedAllocatedBytes=$allocated;
    inventory=$inventory;keptHashes=$keptHashes;retainedHashes=$retainedHashes;
    recovery='Rebuild discarded v1514 with tools/build_active_launch_timer_v1513.ps1 and retained stage v1512; frozen compiled source and logs also preserved here.';
    reason='Superseded interim candidate used the wrong enabled() timer guard; it was never accepted or promoted.';
    allOldBuildFoldersDeleted=$false;fullPortAccepted=$false} | ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$out\report.json" -Encoding utf8
[ordered]@{removedLogicalBytes=$logical;removedAllocatedBytes=$allocated;allOldBuildFoldersDeleted=$false} | ConvertTo-Json
