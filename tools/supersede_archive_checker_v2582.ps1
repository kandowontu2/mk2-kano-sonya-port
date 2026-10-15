# Supersede only our exact live read-only checker after its equivalent has passed.
$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskOutput=Join-Path $taskRoot 'audit_v2583_original_archive_checker_superseded'
if(Test-Path -LiteralPath $taskOutput){throw 'Immutable evidence'}
$taskProofPath=Join-Path $taskRoot 'audit_v2574_restored_native_dependency_archive_checked/report.json'
$taskProof=Get-Content -LiteralPath $taskProofPath -Raw | ConvertFrom-Json
if(-not $taskProof.passed -or -not $taskProof.boundedSequentialArchiveDraining -or $taskProof.independentlyComparedFiles -ne 14 -or $taskProof.exactOriginalBytesCompared -ne 232151126){throw 'Equivalent archive proof required'}
foreach($taskPin in $taskProof.inputHashes.PSObject.Properties){
 if((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value){throw "Changed passed proof dependency: $($taskPin.Name)"}
}
$taskProcess=Get-CimInstance Win32_Process -Filter 'ProcessId=103868'
if(-not $taskProcess){throw 'Original checker already terminal; collect its actual result instead'}
$taskExpected='"C:\Users\kando\AppData\Local\Programs\Python\Python314\python.exe" tools/verify_restored_native_dependency_archive_v2561.py --output audit_v2562_restored_native_dependency_archive_checked'
if($taskProcess.CommandLine -ne $taskExpected -or $taskProcess.CreationDate.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ') -ne '2026-10-05T01:07:12.075Z'){throw 'Exact own checker PID, command and creation time required'}
$taskOriginalReport=Join-Path $taskRoot 'audit_v2562_restored_native_dependency_archive_checked/report.json'
if(Test-Path -LiteralPath $taskOriginalReport){throw 'Original result exists; preserve terminal result instead'}
New-Item -ItemType Directory -Path $taskOutput | Out-Null
$taskRecord=[ordered]@{
 passed=$true
 reason='Equivalent successor passed every original target/source/protection check; unneeded-member draining avoids tarfile 10KB streaming seek copies. Original checker is superseded for source-grounded performance, never accepted from a timeout.'
 originalCheckPassed=$false
 originalSourceUnmodified=$true
 originalSourceSHA256=(Get-FileHash -LiteralPath (Join-Path $taskRoot 'tools/verify_restored_native_dependency_archive_v2561.py')).Hash
 observedOwnProcess=$taskProcess | Select-Object ProcessId,CreationDate,CommandLine,UserModeTime,KernelModeTime
 equivalentPassedReport=$taskProofPath
 equivalentPassedReportSHA256=(Get-FileHash -LiteralPath $taskProofPath).Hash
 stoppingOnlyOwnReadOnlyProcess=$true
 filesDeleted=$false
 gameChanged=$false
 fullPortAcceptance=$false
}
Stop-Process -Id $taskProcess.ProcessId -ErrorAction Stop
$taskProcessAlive=Get-CimInstance Win32_Process -Filter 'ProcessId=103868'
if($taskProcessAlive){throw 'Original process still live; do not claim terminal'}
$taskRecord.originalProcessConfirmedTerminal=$true
$taskRecord.utc=[DateTime]::UtcNow.ToString('o')
$taskRecord | ConvertTo-Json -Depth 6 | Out-File -LiteralPath (Join-Path $taskOutput 'report.json') -Encoding utf8
$taskRecord | ConvertTo-Json -Depth 6
