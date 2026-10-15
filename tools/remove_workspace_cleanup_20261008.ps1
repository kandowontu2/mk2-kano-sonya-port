$ErrorActionPreference = 'Stop'
$taskRoot = (Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).ProviderPath
$taskOut = Join-Path $taskRoot 'workspace_cleanup_2026-10-08'
$taskPlanPath = Join-Path $taskOut 'deletion_plan.json'
$taskResultPath = Join-Path $taskOut 'result.json'
if (Test-Path -LiteralPath $taskResultPath) { throw 'Never overwrite executed cleanup results' }
$taskPlanHash = (Get-FileHash -LiteralPath $taskPlanPath -Algorithm SHA256).Hash
$taskPlan = Get-Content -LiteralPath $taskPlanPath -Raw | ConvertFrom-Json
if ([IO.Path]::GetFullPath($taskPlan.root) -ne $taskRoot) { throw 'Unexpected cleanup root' }
$taskLive = @(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -match '^(make|mingw32-make|gcc|g\+\+|cc1|cc1plus|ld|ar|mkport|mkport_candidate)\.exe$'
})
if ($taskLive.Count) { throw 'Build/game processes still active; preserve outputs' }
function Assert-TaskHashes {
    foreach ($taskGuard in $taskPlan.preservedHashes.PSObject.Properties) {
        if ((Get-FileHash -LiteralPath $taskGuard.Name -Algorithm SHA256).Hash -ne $taskGuard.Value) {
            throw "Protected source/playable/evidence changed: $($taskGuard.Name)"
        }
    }
}
Assert-TaskHashes
$taskFolders = [Collections.Generic.List[string]]::new()
$taskFiles = [Collections.Generic.List[object]]::new()
foreach ($taskTarget in $taskPlan.targets) {
    $taskResolved = (Resolve-Path -LiteralPath $taskTarget.path).ProviderPath
    if (-not $taskResolved.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)) {
        throw 'Exact descendant required; never delete workspace root'
    }
    $taskRelative = $taskResolved.Substring($taskRoot.Length+1)
    if ($taskTarget.kind -eq 'folder') {
        if ($taskRelative -ne 'mame-mkp\build\mingw-gcc') { throw 'Unexpected folder target' }
        $taskItems = @(Get-ChildItem -LiteralPath $taskResolved -Recurse -Force)
        if (@($taskItems | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
            throw 'Linked entry in exact cache target'
        }
        $taskExpected = @($taskTarget.files | ForEach-Object path | Sort-Object)
        $taskActual = @($taskItems | Where-Object { -not $_.PSIsContainer } | ForEach-Object FullName | Sort-Object)
        if (@(Compare-Object $taskExpected $taskActual).Count) { throw 'Compiler output file set changed' }
        foreach ($taskDir in $taskItems | Where-Object PSIsContainer) { $taskFolders.Add($taskDir.FullName) }
        $taskFolders.Add($taskResolved)
    } elseif ($taskTarget.kind -eq 'file') {
        if ($taskRelative -notmatch '^audit_v(2347|2611|2633)_[^\\]+campaign\\native_mix\.wav$' -and
            $taskRelative -notin @(
                'audit_v2430_unreferenced_old_build_recovery\six_unreferenced_builds_complete_recovery.zip',
                'audit_v2486_next_old_build_solid_recovery\ten_unreferenced_builds_complete_recovery.tar.xz',
                'audit_v2518_remaining_old_build_recovery\remaining_68_builds_complete_recovery.tar.xz',
                'audit_v3254_obsolete_workspace_parallel_recovery\obsolete_470_folders_complete_recovery.tar.xz')) {
            throw 'Unexpected individual old-output target'
        }
    } else { throw 'Unknown cleanup kind' }
    foreach ($taskFile in $taskTarget.files) {
        $taskPath = (Resolve-Path -LiteralPath $taskFile.path).ProviderPath
        if ($taskTarget.kind -eq 'folder' -and -not $taskPath.StartsWith($taskResolved+'\',[StringComparison]::OrdinalIgnoreCase)) {
            throw 'Manifest escapes exact cache target'
        }
        if ($taskTarget.kind -eq 'file' -and $taskPath -ne $taskResolved) { throw 'Unexpected leaf' }
        for ($taskParent = [IO.Path]::GetDirectoryName($taskPath); $taskParent -ne $taskRoot; $taskParent = [IO.Path]::GetDirectoryName($taskParent)) {
            if (-not $taskParent -or (Get-Item -LiteralPath $taskParent).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked/escaping ancestor' }
        }
        $taskInfo = Get-Item -LiteralPath $taskPath
        if ($taskInfo.Attributes -band [IO.FileAttributes]::ReparsePoint -or $taskInfo.Length -ne $taskFile.bytes -or
            (Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash -ne $taskFile.SHA256) { throw 'Removal leaf changed' }
        $taskFiles.Add($taskFile)
    }
}
if ((Get-FileHash -LiteralPath $taskPlanPath -Algorithm SHA256).Hash -ne $taskPlanHash) { throw 'Cleanup plan changed' }
$taskFreeBefore = (Get-PSDrive -Name C).Free
foreach ($taskFile in $taskFiles) { Remove-Item -LiteralPath $taskFile.path -Force }
foreach ($taskFolder in $taskFolders | Sort-Object Length -Descending) {
    if (@(Get-ChildItem -LiteralPath $taskFolder -Force).Count) { throw 'Unexpected remaining/new compiler output; do not recurse' }
    Remove-Item -LiteralPath $taskFolder -Force
}
foreach ($taskFile in $taskFiles) { if (Test-Path -LiteralPath $taskFile.path) { throw 'Target remains' } }
Assert-TaskHashes
$taskResult = [ordered]@{
    passed=$true; planSHA256=$taskPlanHash; removedFiles=$taskFiles.Count; removedCacheDirectories=$taskFolders.Count
    reclaimedAllocatedBytes=$taskPlan.reclaimableAllocatedBytes
    diskFreeBefore=$taskFreeBefore; diskFreeAfter=(Get-PSDrive -Name C).Free
    preservedPlayableAndSourceHashesUnchanged=$true; protectedHashCount=@($taskPlan.preservedHashes.PSObject.Properties).Count
    retiredHistoricalEvidencePins=$taskPlan.retiredHistoricalEvidencePins
    recovery='Obsolete data permanently discarded; compiler cache can be regenerated from retained source. No recovery archive created.'
    fullPortAcceptance=$false
}
$taskResult | ConvertTo-Json -Depth 5 | Out-File -LiteralPath $taskResultPath -Encoding utf8
$taskResult | Select-Object passed,removedFiles,removedCacheDirectories,reclaimedAllocatedBytes,protectedHashCount | ConvertTo-Json
