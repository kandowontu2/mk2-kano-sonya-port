$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskRelease=Join-Path $taskRoot 'release_current_native_playtest_20261015_updated_docs'
$taskReceipt=Get-Content -LiteralPath (Join-Path $taskRelease 'package-report.json') -Raw | ConvertFrom-Json
$taskZip=Join-Path $taskRelease 'MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261015_updated_docs.zip'
if((Get-FileHash -LiteralPath $taskZip).Hash -ne $taskReceipt.zipSHA256){throw 'Package changed'}
$taskAudit=Join-Path $taskRoot 'audit_updated_private_playtest_portable_check_20261015'
if(Test-Path -LiteralPath $taskAudit){throw 'Never overwrite executed check'}
$taskTemp=Join-Path $taskAudit 'temporary_extracted_package'
$taskExpected=[IO.Path]::GetFullPath($taskTemp)
if(-not $taskExpected.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Invalid temp containment'}
Add-Type -AssemblyName System.IO.Compression.FileSystem
$taskArchive=[IO.Compression.ZipFile]::OpenRead($taskZip)
try {
 if($taskArchive.Entries.Count -ne 86){throw 'Unexpected member count'}
 $taskSize=0L
 foreach($taskEntry in $taskArchive.Entries){
  $taskSize+=$taskEntry.Length
  $taskMember=$taskEntry.FullName
  if($taskMember -notlike 'MK2_Kano_Sonya_Playtest/*' -or $taskMember -match '(^/|\\|:|(^|/)\.\.(/|$))'){throw 'Unsafe ZIP member'}
 }
 if($taskSize -gt 256MB){throw 'Extraction exceeds bound'}
} finally {$taskArchive.Dispose()}
New-Item -ItemType Directory -Path $taskTemp -Force | Out-Null
$taskTimedOut=$false
try {
 [IO.Compression.ZipFile]::ExtractToDirectory($taskZip,$taskTemp)
 $taskPlay=Join-Path $taskTemp 'MK2_Kano_Sonya_Playtest\PLAY.cmd'
 $taskArgs='/d /c ""'+$taskPlay+'" --check"'
 $taskProc=Start-Process -FilePath $env:ComSpec -ArgumentList $taskArgs -WindowStyle Hidden -RedirectStandardOutput (Join-Path $taskAudit 'check.log') -RedirectStandardError (Join-Path $taskAudit 'stderr.log') -PassThru
 $null=$taskProc.Handle
 if(-not $taskProc.WaitForExit(45000)){
  $taskTimedOut=$true
  throw 'Portable --check exceeded 45 seconds; preserve extraction until exact child identity reviewed'
 }
 $taskProc.Refresh()
 $taskText=Get-Content -LiteralPath (Join-Path $taskAudit 'check.log') -Raw
 if($taskProc.ExitCode -ne 0 -or $taskText -notmatch 'complete mk2ks ROM set is good'){throw 'Portable check failed'}
 if((Get-Item -LiteralPath (Join-Path $taskAudit 'stderr.log')).Length){throw 'Portable stderr not empty'}
 $taskCheckResult=[ordered]@{passedPortableHashAndROMCheck=$true;extractedCMDChecked=$true;exitCode=$taskProc.ExitCode;interactiveBootTested=$false;fullPortAccepted=$false;temporaryExtractionRemoved=$true;zipSHA256=$taskReceipt.zipSHA256}
} finally {
 if(-not $taskTimedOut){
  $taskActual=(Resolve-Path -LiteralPath $taskTemp).Path
  if($taskActual -ne $taskExpected){throw 'Temporary path changed'}
  if((Get-Item -LiteralPath $taskActual).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Refuse linked root cleanup'}
  if(Get-ChildItem -LiteralPath $taskActual -Recurse -Force | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}){throw 'Refuse linked cleanup'}
  if(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -and $_.ExecutablePath.StartsWith($taskActual+'\',[StringComparison]::OrdinalIgnoreCase)}){throw 'Extraction executable still running'}
  Remove-Item -LiteralPath $taskActual -Recurse -Force
 }
}
if(Test-Path -LiteralPath $taskTemp){throw 'Temporary extraction remains'}
$taskCheckResult|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $taskAudit 'report.json')
Get-Content -LiteralPath (Join-Path $taskAudit 'report.json')
