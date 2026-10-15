$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskOut = Join-Path $taskRoot 'workspace_cleanup_followup_2026-10-05'
$taskPlanPath = Join-Path $taskOut 'deletion_plan.json'
$taskResultPath = Join-Path $taskOut 'result.json'
if (Test-Path -LiteralPath $taskResultPath) { throw 'Completed cleanup cannot be overwritten' }
if ((Resolve-Path -LiteralPath $taskRoot).Path -ne $taskRoot) { throw 'Exact requested root required' }
$taskPlan = Get-Content -LiteralPath $taskPlanPath -Raw | ConvertFrom-Json
if ($taskPlan.root -ne $taskRoot -or -not $taskPlan.sourceCurrentBuildsROMsSettingsReleasePreserved) { throw 'Inspected scoped plan required' }
$taskSeen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($taskRow in $taskPlan.targets) {
    $taskTarget = (Resolve-Path -LiteralPath $taskRow.path).Path
    if ($taskTarget -ne $taskRow.path -or -not $taskTarget.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Exact descendant target required' }
    if (-not $taskSeen.Add($taskTarget)) { throw 'Duplicate removal target' }
    $taskRelative = $taskTarget.Substring($taskRoot.Length+1)
    if ($taskRow.kind -eq 'folder') {
        if ((Split-Path $taskTarget -Parent) -ne $taskRoot -or $taskRelative -notmatch '^(v\d+[a-z]?_[A-Za-z0-9_-]+|diagnostic_v(?:\d+[a-z]?|native)_[A-Za-z0-9_-]+|release_v1743_current_playtest)$') { throw 'Unexpected obsolete folder' }
        if ($taskRelative -in @('diagnostic_v1836_ball_register_boundary','diagnostic_v2753_native_friendship_palette','diagnostic_v3172_native_morph_shadow','release_v1863_current_playtest')) { throw 'Current build forbidden' }
    } elseif ($taskRow.kind -eq 'file') {
        $taskRecovery = $taskRelative -eq 'audit_v3262_obsolete_workspace_zstd_recovery\obsolete_470_folders_complete_recovery.tar.zst'
        $taskAudio = $taskRelative -match '^audit_v(\d+)_[A-Za-z0-9_]+(?:_campaign|_extended)\\native_mix\.wav$'
        if ($taskAudio) { $taskAudio = [int]$Matches[1] -ge 2110 -and [int]$Matches[1] -lt 2600 }
        if (-not $taskRecovery -and -not $taskAudio) { throw 'Unexpected obsolete file' }
    } else { throw 'Unknown target kind' }
    $taskAncestor = $taskTarget
    while ($taskAncestor -ne $taskRoot) {
        if ((Get-Item -LiteralPath $taskAncestor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked target or ancestor' }
        $taskAncestor = Split-Path $taskAncestor -Parent
    }
}
$taskLive = @(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -match '^(mkport_candidate|mkport|mkprobe|mame|gmake|make|gcc|g\+\+|cc1plus|ld|ar|compact)\.exe$' -and
    (($_.ExecutablePath -and $_.ExecutablePath.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)) -or
     ($_.CommandLine -and $_.CommandLine.Contains($taskRoot)))
})
if ($taskLive.Count) { throw 'Game/compiler/compression process still running' }
foreach ($taskPin in $taskPlan.preservedHashes.PSObject.Properties) {
    if ((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value) { throw ('Preserved input changed: '+$taskPin.Name) }
}
$taskBefore = (Get-PSDrive C).Free
$taskFiles = 0L
$taskFolders = 0L
$taskJournal = [IO.StreamWriter]::new((Join-Path $taskOut 'removed_targets.txt'), $false)
try {
    foreach ($taskRow in $taskPlan.targets) {
        $taskTarget = (Resolve-Path -LiteralPath $taskRow.path).Path
        if ($taskTarget -ne $taskRow.path -or -not $taskTarget.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Final absolute target validation failed' }
        $taskCount = 0L; $taskDirectories = 0L; $taskLogical = 0L
        if ($taskRow.kind -eq 'folder') {
            $taskDirectories = 1
            foreach ($taskItem in Get-ChildItem -LiteralPath $taskTarget -Recurse -Force) {
                if ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked entry in target' }
                if ($taskItem.PSIsContainer) { $taskDirectories++ }
                else { $taskCount++; $taskLogical += $taskItem.Length }
            }
        } else {
            $taskCount = 1; $taskLogical = (Get-Item -LiteralPath $taskTarget).Length
        }
        if ($taskCount -ne $taskRow.files -or $taskDirectories -ne $taskRow.directories -or $taskLogical -ne $taskRow.logicalBytes) { throw ('Target changed since inspection: '+$taskTarget) }
        if ($taskRow.kind -eq 'folder') {
            Remove-Item -LiteralPath $taskTarget -Recurse -Force
            $taskFolders++
        } else {
            Remove-Item -LiteralPath $taskTarget -Force
        }
        if (Test-Path -LiteralPath $taskTarget) { throw 'Target was not removed' }
        $taskFiles += $taskCount
        $taskJournal.WriteLine($taskTarget); $taskJournal.Flush()
        if ($taskFolders % 100 -eq 0) { Write-Output "Removed obsolete folders: $taskFolders" }
    }
} finally { $taskJournal.Dispose() }
foreach ($taskPin in $taskPlan.preservedHashes.PSObject.Properties) {
    if ((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value) { throw ('Preserved input changed after cleanup: '+$taskPin.Name) }
}
$taskResult = [ordered]@{
    passed=$true; removedFolders=$taskFolders; removedFiles=$taskFiles;
    reclaimedAllocatedBytes=$taskPlan.reclaimableAllocatedBytes;
    diskFreeBefore=$taskBefore; diskFreeAfter=(Get-PSDrive C).Free;
    preservedPlayableAndSourceHashesUnchanged=$true;
    retiredHistoricalEvidencePins=$taskPlan.retiredHistoricalEvidencePins;
    planSHA256=(Get-FileHash -LiteralPath $taskPlanPath).Hash;
    permanentlyDiscarded=$true; newRecoveryArchiveCreated=$false;
    fullPortAcceptance=$false
}
$taskResult | ConvertTo-Json -Depth 5 | Out-File -LiteralPath $taskResultPath -Encoding utf8
$taskResult | Select-Object passed,removedFolders,removedFiles,reclaimedAllocatedBytes,diskFreeBefore,diskFreeAfter | ConvertTo-Json
