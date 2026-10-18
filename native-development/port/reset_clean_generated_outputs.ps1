$ErrorActionPreference = 'Stop'
$expectedRoot = [IO.Path]::GetFullPath('C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\romhack\baseline\clean_program')
$plan = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'CLEAN_PROGRAM_REFRESH_PLAN.json') | ConvertFrom-Json
if ([IO.Path]::GetFullPath($plan.root) -ne $expectedRoot) { throw 'Unexpected clean-build target root.' }
foreach ($directory in @($expectedRoot, (Join-Path $expectedRoot 'srcp'), (Join-Path $expectedRoot 'srcp\rom'))) {
    $item = Get-Item -Force -LiteralPath $directory
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Refusing a redirected clean-build directory.' }
}
$verifiedTargets = @()
$totalBytes = 0L
foreach ($entry in $plan.targets) {
    $absolute = [IO.Path]::GetFullPath($entry.path)
    if (!$absolute.StartsWith($expectedRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Target escaped clean-build directory.' }
    $relative = $absolute.Substring($expectedRoot.Length + 1)
    if ($relative -notmatch '^srcp\\(?:[A-Za-z0-9_]+\.OBJ|MK2P\.OUT|rom\\P12(?:F8|FC)\.[01])$') {
        throw ('Not an authorized generated compiler output: ' + $relative)
    }
    $item = Get-Item -Force -LiteralPath $absolute
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Refusing a directory or reparse target.' }
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $absolute).Hash -ne $entry.SHA256) { throw ('Changed output: ' + $relative) }
    $verifiedTargets += $absolute
    $totalBytes += $item.Length
}
if (($verifiedTargets | Sort-Object -Unique).Count -ne $verifiedTargets.Count) { throw 'Duplicate output target.' }
# Every exact path is resolved and verified before any flat file is removed.
foreach ($absolute in $verifiedTargets) { Remove-Item -Force -LiteralPath $absolute }
[pscustomobject]@{RemovedGeneratedFiles=$verifiedTargets.Count;RemovedBytes=$totalBytes;SourcesRemoved=$false;RebuildInputsRemoved=$false} | ConvertTo-Json
