$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskReview = Join-Path $taskRoot 'audit_obsolete_capture_target_review_20261015'
$taskReceipt = Join-Path $taskReview 'deletion_receipt.json'
if (Test-Path -LiteralPath $taskReceipt) { throw 'Already executed; never overwrite receipt' }
$taskPlan = Get-Content -LiteralPath (Join-Path $taskReview 'deletion_plan.json') -Raw | ConvertFrom-Json
$taskAllowed = @('obj_dump2\snap','native_kano_knife_clean_fast2\snap','native_kano_knife_clean_fast\snap','native_kano_knife_scan_late_fast\snap','native_kano_knife_scan\snap')
if ($taskPlan.targets.Count -ne 5 -or $taskPlan.totalFiles -ne 2592) { throw 'Unexpected plan' }
$taskFiles = @()
foreach ($taskRelative in $taskAllowed) {
    $taskExact = Join-Path $taskRoot $taskRelative
    $taskRows = @($taskPlan.targets | Where-Object { $_.path -eq $taskExact })
    if ($taskRows.Count -ne 1) { throw 'Exact allowlist mismatch' }
    $taskResolved = (Resolve-Path -LiteralPath $taskExact).Path
    if ($taskResolved -ne $taskExact -or -not $taskResolved.StartsWith($taskRoot + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Containment failure' }
    $taskChildren = @(Get-ChildItem -LiteralPath $taskResolved -Recurse -Force)
    foreach ($taskNode in @((Get-Item -LiteralPath $taskResolved)) + $taskChildren) {
        if ($taskNode.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse point forbidden' }
    }
    $taskActualFiles = @($taskChildren | Where-Object { -not $_.PSIsContainer })
    if ($taskActualFiles.Count -ne $taskRows[0].files.Count) { throw 'File set changed' }
    foreach ($taskFile in $taskRows[0].files) {
        $taskPath = (Resolve-Path -LiteralPath $taskFile.path).Path
        if (-not $taskPath.StartsWith($taskResolved + '\',[StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetExtension($taskPath) -ne '.png') { throw 'Unexpected file' }
        $taskItem = Get-Item -LiteralPath $taskPath
        if ($taskItem.Length -ne $taskFile.bytes -or (Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash -ne $taskFile.SHA256) { throw 'File bytes changed' }
        $taskFiles += $taskPath
    }
}
if ($taskFiles.Count -ne 2592 -or @($taskFiles | Select-Object -Unique).Count -ne 2592) { throw 'Nonunique file set' }
foreach ($taskPath in $taskFiles) { Remove-Item -LiteralPath $taskPath -ErrorAction Stop }
foreach ($taskRelative in $taskAllowed) {
    $taskExact = Join-Path $taskRoot $taskRelative
    $taskDirs = @(Get-ChildItem -LiteralPath $taskExact -Recurse -Directory -Force | Sort-Object { $_.FullName.Length } -Descending)
    foreach ($taskDir in $taskDirs) {
        if (@(Get-ChildItem -LiteralPath $taskDir.FullName -Force).Count -ne 0) { throw 'Directory no longer empty' }
        Remove-Item -LiteralPath $taskDir.FullName -ErrorAction Stop
    }
    if (@(Get-ChildItem -LiteralPath $taskExact -Force).Count -ne 0) { throw 'Target not empty' }
    Remove-Item -LiteralPath $taskExact -ErrorAction Stop
    if (Test-Path -LiteralPath $taskExact) { throw 'Target survived deletion' }
}
[ordered]@{deletedFiles=$taskFiles.Count;allocatedBytesFromCensus=$taskPlan.allocatedCandidateBytes;targets=$taskAllowed;archiveCreated=$false;retained='Parent cfg/NVRAM/Lua, original ROM/GFX, accepted evidence, generated assets and current build';permanentDeletion=$true;planSHA256=(Get-FileHash -LiteralPath (Join-Path $taskReview 'deletion_plan.json')).Hash} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $taskReceipt
Get-Content -LiteralPath $taskReceipt
