$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
$taskResolvedRoot = (Resolve-Path -LiteralPath $taskRoot).Path
if ($taskResolvedRoot -ne $taskRoot) { throw 'Exact requested workspace required' }
$taskOut = Join-Path $taskRoot 'workspace_cleanup_requested_2026-10-05'
$taskPlanPath = Join-Path $taskOut 'deletion_plan.json'
$taskResultPath = Join-Path $taskOut 'result.json'
if (Test-Path -LiteralPath $taskResultPath) { throw 'Never overwrite a completed cleanup' }
$taskPlan = Get-Content -LiteralPath $taskPlanPath -Raw | ConvertFrom-Json
if ($taskPlan.root -ne $taskRoot -or $taskPlan.sourceAndPlayableArtifactsRemoved) { throw 'Inspected scoped deletion plan required' }
$taskPlanHash = (Get-FileHash -LiteralPath $taskPlanPath).Hash
$taskProtectedNames = @('diagnostic_v1836_ball_register_boundary', 'diagnostic_v2753_native_friendship_palette', 'diagnostic_v3172_native_morph_shadow')
$taskSeen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($taskRow in $taskPlan.targets) {
    $taskTarget = (Resolve-Path -LiteralPath $taskRow.path).Path
    if ($taskTarget -ne $taskRow.path -or -not $taskTarget.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or $taskTarget -eq $taskRoot) { throw 'Target outside exact workspace' }
    $taskRelative = $taskTarget.Substring($taskRoot.Length+1)
    $taskAllowedSpecial = $taskRelative -in @('_archive\legacy_evidence_v284', 'mame-mkp\build\mingw-gcc')
    if (-not $taskAllowedSpecial) {
        if ((Split-Path $taskTarget -Parent) -ne $taskRoot -or $taskRelative -notmatch '^(audit|diagnostic|regression|control|trace|pilot|reference)_v(\d+)_[a-zA-Z0-9_]+$' -or [int]$Matches[2] -ge 3200 -or $taskRelative -in $taskProtectedNames) { throw 'Unexpected/current deletion target' }
    }
    if (-not $taskSeen.Add($taskTarget)) { throw 'Duplicate target' }
    $taskAncestor = $taskTarget
    while ($taskAncestor -ne $taskRoot) {
        if ((Get-Item -LiteralPath $taskAncestor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked removal target/ancestor' }
        $taskAncestor = Split-Path $taskAncestor -Parent
    }
}
$taskLive = @(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -match '^(mkport_candidate|mkport|mkprobe|mame|gmake|make|gcc|g\+\+|cc1plus|ld|ar|compact)\.exe$' -and
    (($_.ExecutablePath -and $_.ExecutablePath.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)) -or
     ($_.CommandLine -and $_.CommandLine.Contains($taskRoot)))
})
if ($taskLive.Count) { throw 'Relevant game/compiler/compression process still running' }
foreach ($taskPin in $taskPlan.preservedHashes.PSObject.Properties) {
    if ((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value) { throw ('Preserved input changed: '+$taskPin.Name) }
    foreach ($taskTarget in $taskSeen) {
        if ($taskPin.Name.StartsWith($taskTarget+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Current dependency inside obsolete target' }
    }
}
# Keep the lightweight historical archive inventory, not its discarded data blobs.
Copy-Item -LiteralPath (Join-Path $taskRoot '_archive\legacy_evidence_v284\result.json') -Destination (Join-Path $taskOut 'discarded_legacy_archive_inventory.json')
$taskFreeBefore = (Get-PSDrive C).Free
$taskRemoved = [Collections.Generic.List[string]]::new()
$taskRemovedFiles = 0L
$taskJournalPath = Join-Path $taskOut 'removed_folders.txt'
$taskJournal = [IO.StreamWriter]::new($taskJournalPath, $false)
try {
    foreach ($taskRow in $taskPlan.targets) {
        $taskTarget = (Resolve-Path -LiteralPath $taskRow.path).Path
        if ($taskTarget -ne $taskRow.path -or -not $taskTarget.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Final absolute target validation failed' }
        $taskFiles = 0L; $taskDirectories = 1L; $taskLogical = 0L
        foreach ($taskItem in Get-ChildItem -LiteralPath $taskTarget -Recurse -Force) {
            if ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse entry in removal tree' }
            if ($taskItem.PSIsContainer) { $taskDirectories++ }
            else { $taskFiles++; $taskLogical += $taskItem.Length }
        }
        if ($taskFiles -ne $taskRow.files -or $taskDirectories -ne $taskRow.directories -or $taskLogical -ne $taskRow.logicalBytes) { throw ('Tree changed since inspection: '+$taskTarget) }
        Remove-Item -LiteralPath $taskTarget -Recurse -Force
        if (Test-Path -LiteralPath $taskTarget) { throw 'Exact obsolete target was not removed' }
        $taskRemoved.Add($taskTarget)
        $taskRemovedFiles += $taskFiles
        $taskJournal.WriteLine($taskTarget); $taskJournal.Flush()
        if ($taskRemoved.Count % 250 -eq 0) { Write-Output "Removed obsolete folders: $($taskRemoved.Count)/$($taskPlan.targets.Count)" }
    }
} finally { $taskJournal.Dispose() }
foreach ($taskPin in $taskPlan.preservedHashes.PSObject.Properties) {
    if ((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value) { throw ('Preserved input changed after cleanup: '+$taskPin.Name) }
}
$taskResult = [ordered]@{
    passed = $true
    removedFolderCount = $taskRemoved.Count
    removedFiles = $taskRemovedFiles
    reclaimedAllocatedBytes = $taskPlan.reclaimableAllocatedBytes
    diskFreeBefore = $taskFreeBefore
    diskFreeAfter = (Get-PSDrive C).Free
    preservedHashesUnchanged = $true
    planSHA256 = $taskPlanHash
    obsoleteHistoryPermanentlyDiscarded = $true
    compilerCacheRegenerable = $true
    sourceCurrentBuildsROMsSettingsLaunchersReleasePreserved = $true
    recovery = $taskPlan.recovery
    fullPortAcceptance = $false
}
$taskResult | ConvertTo-Json -Depth 4 | Out-File -LiteralPath $taskResultPath -Encoding utf8
$taskResult | ConvertTo-Json -Depth 4
