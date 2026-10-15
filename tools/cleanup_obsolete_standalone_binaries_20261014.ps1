$ErrorActionPreference='Stop'
$taskRoot=(Get-Item -LiteralPath 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port').FullName
$taskRepo=(Get-Item -LiteralPath (Join-Path $taskRoot 'mame-mkp')).FullName
$taskOut=Join-Path $taskRoot 'audit_obsolete_standalone_binary_cleanup_20261014'
if(Test-Path -LiteralPath $taskOut){throw 'Do not overwrite cleanup record'}
$taskProtected=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach($taskReport in @('audit_native_selector_cpu_startup_ring_audio_checked/report.json','audit_native_selector_exit_stock_comparison_saved_checked/report.json')){
 $taskPins=(Get-Content -LiteralPath (Join-Path $taskRoot $taskReport) -Raw | ConvertFrom-Json).inputHashes
 foreach($taskPin in $taskPins.PSObject.Properties){[void]$taskProtected.Add([IO.Path]::GetFullPath($taskPin.Name))}
}
$taskManifest=Get-Content -LiteralPath (Join-Path $taskRoot 'diagnostic_native_selector_layers_long/build-info.json') -Raw | ConvertFrom-Json
foreach($taskPin in $taskManifest.canonical_source_hashes_at_compile.PSObject.Properties){[void]$taskProtected.Add([IO.Path]::GetFullPath($taskPin.Name))}
if(Get-Process -Name mkport,mkprobe,mkwport -ErrorAction SilentlyContinue){throw 'Old standalone executable is running'}
$taskRecords=@()
foreach($taskName in @('mkport.exe','mkprobe.exe','mkwport.exe','mkport.sym','mkwport.sym')){
 $taskFile=Get-Item -LiteralPath (Join-Path $taskRepo $taskName) -Force
 $taskFull=[IO.Path]::GetFullPath($taskFile.FullName)
 if($taskFile.PSIsContainer -or $taskFile.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Only regular explicit files may be removed'}
 if([IO.Path]::GetDirectoryName($taskFull) -ne $taskRepo -or $taskFile.Name -ne $taskName){throw 'Resolved cleanup target escaped exact repository directory'}
 if($taskProtected.Contains($taskFull)){throw "Protected dependency: $taskFull"}
 $taskRecords+= [PSCustomObject]@{path=$taskFull;bytes=$taskFile.Length;sha256=(Get-FileHash -LiteralPath $taskFull -Algorithm SHA256).Hash;removed=$false}
}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskRecords | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskOut 'before.json')
foreach($taskRecord in $taskRecords){
 if((Get-FileHash -LiteralPath $taskRecord.path -Algorithm SHA256).Hash -ne $taskRecord.sha256){throw 'Target changed after validation'}
 Remove-Item -LiteralPath $taskRecord.path -Force
 $taskRecord.removed=-not(Test-Path -LiteralPath $taskRecord.path)
 if(-not $taskRecord.removed){throw 'File removal did not complete'}
}
$taskResult=[ordered]@{removedFiles=$taskRecords;logicalBytesRemoved=($taskRecords | Measure-Object bytes -Sum).Sum;archived=$false;permanentRemoval=$true;currentBuildRemoved=$false;sourceRemoved=$false;currentReleaseRemoved=$false;historicalScriptsRetained=$true;scope='Five obsolete standalone root executables/symbol maps, not the active diagnostic build. Historical scripts naming them require a rebuilt binary before reuse.'}
$taskResult | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $taskOut 'report.json')
$taskResult | ConvertTo-Json -Depth 6 -Compress
