param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$taskRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$expectedRoot = 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
if ($taskRoot -ne $expectedRoot) { throw 'Unexpected workspace; refusing cleanup.' }
$taskReportPath = Join-Path $taskRoot 'WORKSPACE_COMPACTION_2026-10-01.json'
if ($Apply -and (Test-Path -LiteralPath $taskReportPath)) {
    throw 'Existing report; refusing to repeat this one-time cleanup.'
}
if (-not ('Mk2CleanupAllocation' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class Mk2CleanupAllocation {
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    private static extern uint GetCompressedFileSizeW(string path, out uint high);
    public static ulong Bytes(string path) {
        uint high;
        uint low = GetCompressedFileSizeW(path, out high);
        if (low == UInt32.MaxValue && Marshal.GetLastWin32Error() != 0)
            throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
        return ((ulong)high << 32) | low;
    }
}
'@
}
$taskTargets = @(Get-ChildItem -LiteralPath $taskRoot -Directory | Where-Object {
    $_.Name -match '^diagnostic_v(\d+)_' -and
    [int]$Matches[1] -lt 400 -and [int]$Matches[1] -ne 277 -and
    -not ($_.Attributes -band [IO.FileAttributes]::ReparsePoint)
} | ForEach-Object {
    Get-ChildItem -LiteralPath $_.FullName -File -Filter '*.exe' | Where-Object {
        -not ($_.Attributes -band [IO.FileAttributes]::Compressed) -and
        -not ($_.Attributes -band [IO.FileAttributes]::ReparsePoint)
    }
})
$taskProcesses = @(Get-CimInstance Win32_Process | Where-Object {
    $_.ExecutablePath -and $taskTargets.FullName -contains $_.ExecutablePath
})
if ($taskProcesses.Count) { throw 'A historical target is running; refusing cleanup.' }
$taskProtected = @(
    'diagnostic_v400_native_kano_air_height\mkport_candidate.exe',
    'diagnostic_v277_native_battle_photos\mkport_candidate.exe',
    'mame-mkp\mkport.exe',
    'mame-mkp\src\mame\midway\midtunit_m.cpp',
    'mame-mkp\src\mame\midway\midtunit_v.cpp'
)
$taskProtectedBefore = @($taskProtected | ForEach-Object {
    $taskPath = Join-Path $taskRoot $_
    if (-not (Test-Path -LiteralPath $taskPath -PathType Leaf)) { throw "Missing protected file: $_" }
    [pscustomobject]@{path=$_;sha256=(Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash}
})
$taskRows = @($taskTargets | ForEach-Object {
    $taskPath = (Resolve-Path -LiteralPath $_.FullName).Path
    if (-not $taskPath.StartsWith($taskRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Target outside workspace.'
    }
    [pscustomobject]@{
        path=$taskPath.Substring($taskRoot.Length+1)
        bytes=$_.Length
        allocatedBefore=[Mk2CleanupAllocation]::Bytes($taskPath)
        sha256=(Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash
        allocatedAfter=$null
        verified=$false
    }
})
if (-not $Apply) {
    $taskRows | Select-Object path,bytes,allocatedBefore | Format-Table -AutoSize
    Write-Output ('Planned historical executables: ' + $taskRows.Count)
    return
}
foreach ($taskRow in $taskRows) {
    $taskPath = Join-Path $taskRoot $taskRow.path
    & compact.exe /C /Q $taskPath
    if ($LASTEXITCODE -ne 0) { throw "Compression failed: $($taskRow.path)" }
    $taskRow.allocatedAfter = [Mk2CleanupAllocation]::Bytes($taskPath)
    $taskRow.verified = (Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash -eq $taskRow.sha256
    if (-not $taskRow.verified) { throw "Content changed: $($taskRow.path)" }
}
foreach ($taskFile in $taskProtectedBefore) {
    if ((Get-FileHash -LiteralPath (Join-Path $taskRoot $taskFile.path) -Algorithm SHA256).Hash -ne $taskFile.sha256) {
        throw "Protected content changed: $($taskFile.path)"
    }
}
$taskReclaimed = [long](($taskRows | Measure-Object allocatedBefore -Sum).Sum) -
    [long](($taskRows | Measure-Object allocatedAfter -Sum).Sum)
$taskReport = [ordered]@{
    method='Reversible NTFS compression; no files deleted or relocated'
    timestampUtc=[DateTime]::UtcNow.ToString('o')
    root=$taskRoot
    reclaimedBytes=$taskReclaimed
    verifiedFiles=$taskRows.Count
    protectedFiles=$taskProtectedBefore
    files=$taskRows
    undo='Run compact.exe /U with each exact executable path listed here.'
}
if (Test-Path -LiteralPath $taskReportPath) { throw 'Existing report; refusing overwrite.' }
$taskReport | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $taskReportPath -Encoding UTF8
Write-Output ('Verified files: ' + $taskRows.Count)
Write-Output ('Reclaimed bytes: ' + $taskReclaimed)
Write-Output ('Report: ' + $taskReportPath)
