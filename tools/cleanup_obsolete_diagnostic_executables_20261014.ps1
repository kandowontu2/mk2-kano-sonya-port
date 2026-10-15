$ErrorActionPreference='Stop'
$taskRoot=(Get-Item -LiteralPath 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port').FullName
$taskOut=Join-Path $taskRoot 'audit_obsolete_diagnostic_executable_cleanup_20261014'
if(Test-Path -LiteralPath $taskOut){throw 'Never overwrite cleanup evidence'}
if(Get-Process -Name mkport_candidate -ErrorAction SilentlyContinue){throw 'An emulator candidate is running'}
$taskProtected=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach($taskReport in @('audit_native_selector_cpu_startup_ring_audio_checked/report.json','audit_native_selector_exit_stock_comparison_saved_checked/report.json')){
 $taskPins=(Get-Content -LiteralPath (Join-Path $taskRoot $taskReport) -Raw | ConvertFrom-Json).inputHashes
 foreach($taskPin in $taskPins.PSObject.Properties){[void]$taskProtected.Add([IO.Path]::GetFullPath($taskPin.Name))}
}
$taskManifest=Get-Content -LiteralPath (Join-Path $taskRoot 'diagnostic_native_selector_layers_long/build-info.json') -Raw | ConvertFrom-Json
foreach($taskPin in $taskManifest.canonical_source_hashes_at_compile.PSObject.Properties){[void]$taskProtected.Add([IO.Path]::GetFullPath($taskPin.Name))}
[void]$taskProtected.Add((Join-Path $taskRoot 'diagnostic_native_selector_layers_long/mkport_candidate.exe'))
$taskRecords=@()
foreach($taskFolder in @('diagnostic_native_cpu_finisher_spacing','diagnostic_v6508_native_projectile_identifiers')){
 $taskParent=(Get-Item -LiteralPath (Join-Path $taskRoot $taskFolder)).FullName
 $taskFile=Get-Item -LiteralPath (Join-Path $taskParent 'mkport_candidate.exe') -Force
 $taskFull=[IO.Path]::GetFullPath($taskFile.FullName)
 if(-not $taskFull.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetDirectoryName($taskFull) -ne $taskParent){throw 'Target escaped exact workspace/parent'}
 if($taskFile.PSIsContainer -or $taskFile.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Only explicit regular executables may be removed'}
 if($taskProtected.Contains($taskFull)){throw "Protected dependency: $taskFull"}
 $taskRecords += [PSCustomObject]@{path=$taskFull;bytes=$taskFile.Length;sha256=(Get-FileHash -LiteralPath $taskFull).Hash;removed=$false}
}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskRecords | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $taskOut 'before.json')
foreach($taskRecord in $taskRecords){
 if((Get-FileHash -LiteralPath $taskRecord.path).Hash -ne $taskRecord.sha256){throw 'Target changed after validation'}
 Remove-Item -LiteralPath $taskRecord.path -Force
 $taskRecord.removed=-not(Test-Path -LiteralPath $taskRecord.path)
 if(-not $taskRecord.removed){throw 'Removal failed'}
}
$taskResult=[ordered]@{removedFiles=$taskRecords;logicalBytesRemoved=($taskRecords | Measure-Object bytes -Sum).Sum;archived=$false;permanentRemoval=$true;currentBuildRemoved=$false;sourceRemoved=$false;currentReleaseRemoved=$false;historicalScriptsRetained=$true;legacyAliasRoutesCurrent=$true;scope='Two obsolete diagnostic executables only. Historical replays naming them require a rebuilt executable.'}
$taskResult | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $taskOut 'report.json')
$taskResult | ConvertTo-Json -Depth 6 -Compress
