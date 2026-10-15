$ErrorActionPreference = 'Stop'
$root = 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$target = 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\__pycache__'
$out = Join-Path $root 'audit_v4530_regenerable_python_cache_removed'
if (Test-Path -LiteralPath $out) { throw 'Fresh immutable cleanup result required' }
$resolvedRoot = (Resolve-Path -LiteralPath $root).Path
$resolvedTarget = (Resolve-Path -LiteralPath $target).Path
if ($resolvedTarget -ne $target -or $resolvedTarget -ne (Join-Path $resolvedRoot 'tools\__pycache__')) {
    throw 'Exact cache path must remain inside the named working folder'
}
$dir = Get-Item -LiteralPath $target
if (($dir.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'No junction or symbolic-link cache target' }
$checkpointPath = Join-Path $root 'audit_v4517_native_ending_audio_full_scope_checkpoint\checkpoint.json'
$manifestPath = Join-Path $root 'audit_v4524_kano_p2_ending_display_ram\input_hashes_before.json'
$checkpoint = Get-Content -LiteralPath $checkpointPath -Raw | ConvertFrom-Json
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$protected = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($p in $checkpoint.inputHashes.PSObject.Properties) { [void]$protected.Add($p.Name) }
foreach ($p in $manifest.PSObject.Properties) { [void]$protected.Add($p.Name) }
$entries = @(Get-ChildItem -LiteralPath $target -Force)
if ($entries.Count -ne 711) { throw 'The actual cache inventory changed; do not delete new or unknown entries' }
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class CacheAllocation4529 {
 [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
 public static extern uint GetCompressedFileSizeW(string name, out uint high);
 public static ulong Bytes(string name) {
  uint high; uint low=GetCompressedFileSizeW(name,out high);
  if(low==0xffffffff && Marshal.GetLastWin32Error()!=0) throw new Exception("Allocated-size query failed");
  return ((ulong)high<<32)|low;
 }
}
'@
$records = @()
foreach ($entry in $entries) {
    if ($entry.PSIsContainer -or ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 -or
        $entry.DirectoryName -ne $target -or $protected.Contains($entry.FullName)) {
        throw 'Only unpinned regular bytecode files at the exact cache target may be removed'
    }
    if ($entry.Name -notmatch '^(.+)\.cpython-\d+(?:\.opt-\d+)?\.pyc$') { throw 'Non-bytecode file preserved' }
    $source = Join-Path (Join-Path $root 'tools') ($Matches[1] + '.py')
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw 'A cache lacking its source must be preserved' }
    $records += [pscustomobject]@{
        cache = $entry.FullName
        cacheSHA256 = (Get-FileHash -LiteralPath $entry.FullName -Algorithm SHA256).Hash
        logicalBytes = $entry.Length
        allocatedBytes = [CacheAllocation4529]::Bytes($entry.FullName)
        source = $source
        sourceSHA256 = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
    }
}
# Validate the complete inventory again before the first native-shell removal.
foreach ($record in $records) {
    if ((Get-FileHash -LiteralPath $record.cache -Algorithm SHA256).Hash -ne $record.cacheSHA256 -or
        (Get-FileHash -LiteralPath $record.source -Algorithm SHA256).Hash -ne $record.sourceSHA256) {
        throw 'Cache or preserved source changed during cleanup preflight'
    }
}
New-Item -ItemType Directory -Path $out | Out-Null
& compact.exe /C /I /Q $out | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Compress cleanup evidence before writes' }
$report = [ordered]@{
    passed = $false
    exactTarget = $target
    deletedFiles = 0
    newlyReclaimedAllocatedBytes = 0
    allOriginalSourceFilesPreserved = $false
    pinnedOrLiveInputFilesRemoved = 0
    publicPlayableReleaseROMAndBuildFilesRemoved = 0
    recoverability = 'Regenerable Python bytecode only; all original .py sources retained. No Recycle Bin copy.'
    records = $records
}
$reportPath = Join-Path $out 'report.json'
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $reportPath -Encoding utf8
foreach ($record in $records) {
    # One shell end-to-end, individual exact verified files; no recursive delete.
    Remove-Item -LiteralPath $record.cache -Force
    if (Test-Path -LiteralPath $record.cache) { throw 'Exact cache file was not removed' }
    $report.deletedFiles++
    $report.newlyReclaimedAllocatedBytes += $record.allocatedBytes
}
if (@(Get-ChildItem -LiteralPath $target -Force).Count -ne 0) { throw 'Unexpected remaining cache entry preserved' }
Remove-Item -LiteralPath $target -Force
foreach ($record in $records) {
    if ((Get-FileHash -LiteralPath $record.source -Algorithm SHA256).Hash -ne $record.sourceSHA256) {
        throw 'An original source changed; do not claim successful cleanup'
    }
}
$report.allOriginalSourceFilesPreserved = $true
$report.passed = $true
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $reportPath -Encoding utf8
[pscustomobject]@{
    passed = $report.passed
    deletedFiles = $report.deletedFiles
    newlyReclaimedAllocatedBytes = $report.newlyReclaimedAllocatedBytes
    allOriginalSourceFilesPreserved = $report.allOriginalSourceFilesPreserved
    report = $reportPath
} | ConvertTo-Json -Compress
