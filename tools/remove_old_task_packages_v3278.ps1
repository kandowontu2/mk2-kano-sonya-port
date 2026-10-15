$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port'
if ((Resolve-Path -LiteralPath $taskRoot).Path -ne $taskRoot) { throw 'Exact attached working folder required' }
$taskPortRoot = 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskOut = Join-Path $taskPortRoot 'workspace_cleanup_requested_2026-10-05\old_task_packages.json'
if (Test-Path -LiteralPath $taskOut) { throw 'Never overwrite package removal evidence' }
$taskCheckpoint = Get-Content -LiteralPath (Join-Path $taskPortRoot 'audit_v3260_cleanup_and_adversity_full_scope_checkpoint\checkpoint.json') -Raw | ConvertFrom-Json
$taskNames = @('MK2_Kano_Sonya_v244_playtest.zip', 'MK2_Kano_Sonya_v249_playtest.zip',
    'MK2_Kano_Sonya_v250_playtest.zip', 'MK2_Kano_Sonya_v251_playtest.zip',
    'MK2_Kano_Sonya_v252_playtest.zip', 'MK2_Kano_Sonya_v253_playtest.zip',
    'MK2_Kano_Sonya_v255_playtest.zip', 'MK2_Kano_Sonya_v257_playtest.zip',
    'MK2_Kano_Sonya_v258_playtest.zip', '__verify_v244_package_20260927',
    'audit_v249_outer_cmd_sonya_vs_kano', 'audit_v250_outer_cmd_sonya_vs_kano')
$taskGuard = @{}
foreach ($taskPath in @((Join-Path $taskRoot 'PLAY_MK2_KANO_SONYA.cmd'), (Join-Path $taskPortRoot 'release_v1863_current_playtest\MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip'))) {
    $taskGuard[$taskPath] = (Get-FileHash -LiteralPath $taskPath).Hash
}
$taskRecords = [Collections.Generic.List[object]]::new()
foreach ($taskName in $taskNames) {
    $taskPath = (Resolve-Path -LiteralPath (Join-Path $taskRoot $taskName)).Path
    if ((Split-Path $taskPath -Parent) -ne $taskRoot -or (Split-Path $taskPath -Leaf) -ne $taskName) { throw 'Exact immediate-child obsolete package target required' }
    $taskItem = Get-Item -LiteralPath $taskPath -Force
    if ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'No linked package target' }
    foreach ($taskPin in $taskCheckpoint.inputHashes.PSObject.Properties) {
        if ($taskPin.Name -eq $taskPath -or $taskPin.Name.StartsWith($taskPath+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Current dependency inside old package target' }
    }
    $taskFiles = 0L; $taskBytes = 0L
    if ($taskItem.PSIsContainer) {
        foreach ($taskChild in Get-ChildItem -LiteralPath $taskPath -Recurse -Force) {
            if ($taskChild.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'No reparse entries anywhere in old package tree' }
            if (-not $taskChild.PSIsContainer) { $taskFiles++; $taskBytes += $taskChild.Length }
        }
    } else { $taskFiles=1; $taskBytes=$taskItem.Length }
    $taskRecords.Add([ordered]@{path=$taskPath;files=$taskFiles;logicalBytes=$taskBytes})
}
# Validation of every absolute target and all contents completed before removal.
foreach ($taskRow in $taskRecords) {
    $taskResolved = (Resolve-Path -LiteralPath $taskRow.path).Path
    if ((Split-Path $taskResolved -Parent) -ne $taskRoot -or $taskResolved -ne $taskRow.path) { throw 'Final target validation failed' }
    Remove-Item -LiteralPath $taskResolved -Recurse -Force
    if (Test-Path -LiteralPath $taskResolved) { throw 'Obsolete package not removed' }
}
foreach ($taskPath in $taskGuard.Keys) { if ((Get-FileHash -LiteralPath $taskPath).Hash -ne $taskGuard[$taskPath]) { throw 'Current launcher/release changed' } }
$taskResult = [ordered]@{passed=$true;removedTargets=@($taskRecords);removedTargetCount=$taskRecords.Count;removedLogicalBytes=($taskRecords | Measure-Object logicalBytes -Sum).Sum;currentLauncherAndReleaseUnchanged=$true;recovery='Old v244-v258 package copies and temporary verification outputs were intentionally discarded; the current v1836 release ZIP is retained.'}
$taskResult | ConvertTo-Json -Depth 5 | Out-File -LiteralPath $taskOut -Encoding utf8
$taskResult | Select-Object passed,removedTargetCount,removedLogicalBytes | ConvertTo-Json
