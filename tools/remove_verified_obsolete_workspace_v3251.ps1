$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
if($taskRoot -ne 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'){throw 'Exact explicitly requested workspace required'}
$taskSource=Join-Path $taskRoot 'audit_v3256_obsolete_workspace_parallel_removal_checked\report.json'
$taskOut=Join-Path $taskRoot 'audit_v3252_obsolete_workspace_removed'
if(Test-Path -LiteralPath $taskOut){throw 'Never overwrite deletion evidence'}
$taskReport=Get-Content -LiteralPath $taskSource -Raw | ConvertFrom-Json
if(-not $taskReport.passed -or $taskReport.filesDeleted -ne 0 -or $taskReport.netAllocatedSavings -le 0){throw 'Completed byte-verified recovery and exact positive savings required'}
if((Get-FileHash -LiteralPath $taskReport.recoveryReport).Hash -ne $taskReport.recoveryReportSHA256 -or
   (Get-FileHash -LiteralPath $taskReport.inventoryPath).Hash -ne $taskReport.inventorySHA256){throw 'Verified recovery metadata changed'}
if((Get-FileHash -LiteralPath $taskReport.sourceManifestPath).Hash -ne $taskReport.sourceManifestSHA256){throw 'Exact final source manifest changed'}
$taskExpectedFiles=@{}
$taskExpectedDirs=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach($taskLine in [IO.File]::ReadLines($taskReport.sourceManifestPath)){
    $taskParts=$taskLine.Split([char]9)
    if($taskParts[0] -eq 'd' -and $taskParts.Count -eq 2){$null=$taskExpectedDirs.Add($taskParts[1])}
    elseif($taskParts[0] -eq 'f' -and $taskParts.Count -eq 3){$taskExpectedFiles[$taskParts[2]]=[long]$taskParts[1]}
    else{throw 'Unexpected source manifest row'}
}
$taskTargets=@($taskReport.targetDirectories)
if($taskTargets.Count -ne 470 -or @($taskTargets | Select-Object -Unique).Count -ne 470){throw 'Exact 470 inspected targets required'}
$taskNames=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$taskLive=@(Get-CimInstance Win32_Process | Where-Object {$_.Name -match '^(mkport|mkprobe|mkwport|hbmame|gmake|gcc|g\+\+|cc1plus|compact)\.exe$' -and $_.CommandLine -and $_.CommandLine.Contains($taskRoot)})
if($taskLive.Count){throw 'Relevant game, build or compaction process still active'}
foreach($taskTarget in $taskTargets){
    $taskResolved=(Resolve-Path -LiteralPath $taskTarget).Path
    if($taskResolved -ne $taskTarget -or (Split-Path $taskResolved -Parent) -ne $taskRoot -or
       -not $taskResolved.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Removal target outside exact workspace'}
    $taskName=Split-Path $taskResolved -Leaf
    if($taskName -notmatch '^(audit|diagnostic|regression|control|trace|pilot|reference)_v(\d+)_' -or
       [int]$Matches[2] -ge 3200 -or $taskName -in @('diagnostic_v1836_ball_register_boundary','diagnostic_v2753_native_friendship_palette','diagnostic_v3172_native_morph_shadow')){throw 'Unexpected/current target'}
    if((Get-Item -LiteralPath $taskResolved -Force).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'No directory links'}
    $null=$taskNames.Add($taskName)
}
foreach($taskPin in $taskReport.preservedHashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value){throw 'Kept launcher/build/checkpoint changed'}
}
$taskObserved=@{}
$taskObservedDirs=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach($taskTarget in $taskTargets){
    $null=$taskObservedDirs.Add($taskTarget.Substring($taskRoot.Length+1).Replace('\','/'))
    foreach($taskEntry in Get-ChildItem -LiteralPath $taskTarget -Recurse -Force){
        if($taskEntry.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'No reparse points anywhere in targets'}
        if(-not $taskEntry.PSIsContainer){$taskObserved[$taskEntry.FullName.Substring($taskRoot.Length+1).Replace('\','/')]=[long]$taskEntry.Length}
        else{$null=$taskObservedDirs.Add($taskEntry.FullName.Substring($taskRoot.Length+1).Replace('\','/'))}
    }
}
if($taskObserved.Count -ne $taskReport.verifiedFiles -or $taskExpectedFiles.Count -ne $taskReport.verifiedFiles -or
   -not $taskObservedDirs.SetEquals($taskExpectedDirs)){throw 'Original tree topology changed after verification'}
foreach($taskName in $taskExpectedFiles.Keys){
    if(-not $taskObserved.ContainsKey($taskName) -or $taskObserved[$taskName] -ne $taskExpectedFiles[$taskName]){throw 'Exact original file paths/lengths changed'}
}
if((Get-FileHash -LiteralPath $taskReport.recoveryArchive).Hash -ne $taskReport.recoveryArchiveSHA256){throw 'Verified complete recovery archive changed before removal'}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskRemoved=[Collections.Generic.List[string]]::new()
$taskFreeBefore=(Get-PSDrive C).Free
try {
    foreach($taskTarget in $taskTargets){
        $taskResolved=(Resolve-Path -LiteralPath $taskTarget).Path
        if($taskResolved -ne $taskTarget -or (Split-Path $taskResolved -Parent) -ne $taskRoot){throw 'Final target validation failed'}
        Remove-Item -LiteralPath $taskResolved -Recurse -Force
        $taskRemoved.Add($taskResolved)
        if($taskRemoved.Count % 25 -eq 0){Write-Output "Removed verified obsolete folders: $($taskRemoved.Count)/470"}
    }
} finally {
    [ordered]@{removedDirectories=@($taskRemoved);recoveryArchive=$taskReport.recoveryArchive;sourceVerification=$taskSource} |
        ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$taskOut\removed.json" -Encoding utf8
}
foreach($taskPin in $taskReport.preservedHashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value){throw 'Kept launcher/build/checkpoint changed through removal'}
}
$taskResult=[ordered]@{passed=$true;removedFolderCount=$taskRemoved.Count;removedDirectories=@($taskRemoved);
    removedFiles=$taskReport.verifiedFiles;removedAllocatedBytes=$taskReport.reclaimableAllocatedBytes;
    recoveryAllocatedBytes=$taskReport.recoveryArchiveAllocatedBytes;netAllocatedSavings=$taskReport.netAllocatedSavings;
    diskFreeBefore=$taskFreeBefore;diskFreeAfter=(Get-PSDrive C).Free;
    recoveryArchive=$taskReport.recoveryArchive;recoveryArchiveSHA256=$taskReport.recoveryArchiveSHA256;
    sourceVerification=$taskSource;keptPlayableAndCheckpointHashesUnchanged=$true;
    allOldBuildFoldersRemoved=$false;fullPortAcceptance=$false;
    recovery='Extract the verified self-contained tar.zst into mk2port to restore the exact old folder/file names. Current builds, source, settings and ROMs were not removed.'}
$taskResult | ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$taskOut\report.json" -Encoding utf8
[ordered]@{passed=$true;removedFolderCount=$taskRemoved.Count;removedFiles=$taskReport.verifiedFiles;netAllocatedSavings=$taskReport.netAllocatedSavings;recoveryArchive=$taskReport.recoveryArchive} | ConvertTo-Json
