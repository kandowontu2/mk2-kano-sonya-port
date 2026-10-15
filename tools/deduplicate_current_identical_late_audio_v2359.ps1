# Lossless storage cleanup: exact accepted immutable replay audio only.
$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$taskOutput=Join-Path $taskRoot 'audit_v2360_current_identical_late_audio_storage'
if(Test-Path -LiteralPath $taskOutput){throw 'Immutable cleanup proof exists'}
if((Get-Item -LiteralPath $taskRoot).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse root'}
if(Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe' -and $_.CommandLine -like "*$taskRoot*"}){throw 'Emulator still recording'}
# Parent must close all proof/test handles too before running this script.
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class MK2PortLateAudioAllocation { [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)] public static extern uint GetCompressedFileSizeW(string path, out uint high); }'
function Task-FileId([string]$TaskPath){
 $taskRaw=& fsutil.exe file queryfileid $TaskPath
 if($LASTEXITCODE -ne 0){throw 'Cannot check actual NTFS file identity'}
 $taskMatch=[regex]::Match(($taskRaw -join ' '),'0x[0-9a-fA-F]+')
 if(-not $taskMatch.Success){throw 'Missing NTFS file identity'}
 return $taskMatch.Value.ToUpperInvariant()
}
function Task-Path([string]$TaskLeaf){
 $taskFull=[IO.Path]::GetFullPath((Join-Path $taskRoot $TaskLeaf))
 $taskParent=Get-Item -LiteralPath (Split-Path $taskFull -Parent)
 if(-not $taskFull.StartsWith($taskRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or (Split-Path $taskParent.FullName -Parent) -ne $taskRoot -or $taskParent.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe exact capture leaf'}
 if((Test-Path -LiteralPath $taskFull) -and (Get-Item -LiteralPath $taskFull).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse file target'}
 return $taskFull
}
$taskPairs=@();$taskPins=@{}
foreach($taskFighter in @('kano','sonya')){foreach($taskPolicy in @('late_apex','late_descend')){
 $taskCase='{0}_{1}' -f $taskFighter,$taskPolicy
 foreach($taskLeaf in @(('audit_v2350_current_{0}_boss_ledger_checked/report.json' -f $taskCase),('audit_v2352_current_{0}_input_counterexamples/report.json' -f $taskCase))){
  $taskReportPath=Join-Path $taskRoot $taskLeaf;$taskReport=Get-Content -Raw -LiteralPath $taskReportPath | ConvertFrom-Json
  if(-not $taskReport.passed -or $taskReport.fullPortAcceptance){throw 'Complete accepted bounded proof required before cleanup'}
  $taskPins[$taskReportPath]=(Get-FileHash -LiteralPath $taskReportPath).Hash
 }
 $taskOld=Task-Path ('audit_v2335_current_{0}_p1_{1}_campaign/native_mix.wav' -f $taskFighter,$taskPolicy)
 $taskNew=Task-Path ('audit_v2347_current_{0}_p1_{1}_campaign/native_mix.wav' -f $taskFighter,$taskPolicy)
 $taskBackup=Task-Path ('audit_v2347_current_{0}_p1_{1}_campaign/native_mix.wav.dedup-v2359-backup' -f $taskFighter,$taskPolicy)
 if(Test-Path -LiteralPath $taskBackup){throw 'Recoverable duplicate already exists'}
 $taskWanted=@()
 foreach($taskVersion in @(2336,2348)){
  $taskPositivePath=Join-Path $taskRoot ('audit_v{0}_current_{1}_p1_{2}_checked/report.json' -f $taskVersion,$taskFighter,$taskPolicy)
  $taskPositive=Get-Content -Raw -LiteralPath $taskPositivePath | ConvertFrom-Json
  if(-not $taskPositive.passed){throw 'Original and replay positive proofs required'}
  $taskWave=if($taskVersion -eq 2336){$taskOld}else{$taskNew}
  $taskPin=$taskPositive.inputHashes.PSObject.Properties | Where-Object {$_.Name -eq $taskWave}
  if(-not $taskPin){throw 'Missing accepted audio hash'}
  $taskWanted+=$taskPin.Value;$taskPins[$taskPositivePath]=(Get-FileHash -LiteralPath $taskPositivePath).Hash
 }
 if($taskWanted[0] -ne $taskWanted[1] -or (Get-FileHash -LiteralPath $taskOld).Hash -ne $taskWanted[0] -or (Get-FileHash -LiteralPath $taskNew).Hash -ne $taskWanted[0]){throw 'Only exact accepted identical audio may share storage'}
 $taskOldId=Task-FileId $taskOld;$taskNewId=Task-FileId $taskNew
 if($taskOldId -eq $taskNewId){throw 'Already shared: do not count reclaimed space'}
 [uint32]$taskHigh=0;[uint32]$taskLow=[MK2PortLateAudioAllocation]::GetCompressedFileSizeW($taskNew,[ref]$taskHigh)
 if($taskLow -eq [uint32]::MaxValue -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 0){throw 'Cannot measure real allocation'}
 $taskPairs+=[pscustomobject]@{fighter=$taskFighter;policy=$taskPolicy;original=$taskOld;replay=$taskNew;backup=$taskBackup;sha256=$taskWanted[0];originalFileId=$taskOldId;duplicateFileId=$taskNewId;allocatedDuplicateBytes=([uint64]$taskHigh*4294967296+[uint64]$taskLow);logicalBytes=(Get-Item -LiteralPath $taskNew).Length}
}}
$taskDone=@()
foreach($taskPair in $taskPairs){
 $taskLinked=$false
 Move-Item -LiteralPath $taskPair.replay -Destination $taskPair.backup
 try{
  New-Item -ItemType HardLink -Path $taskPair.replay -Value $taskPair.original | Out-Null;$taskLinked=$true
  if((Task-FileId $taskPair.replay) -ne $taskPair.originalFileId -or (Task-FileId $taskPair.original) -ne $taskPair.originalFileId -or (Task-FileId $taskPair.backup) -ne $taskPair.duplicateFileId){throw 'File identities changed'}
  foreach($taskWave in @($taskPair.original,$taskPair.replay,$taskPair.backup)){if((Get-FileHash -LiteralPath $taskWave).Hash -ne $taskPair.sha256){throw 'Audio bytes changed'}}
  # Exact validated duplicate only. All named capture files remain readable.
  Remove-Item -LiteralPath $taskPair.backup
  $taskPins[$taskPair.original]=$taskPair.sha256;$taskPins[$taskPair.replay]=$taskPair.sha256;$taskDone+=$taskPair
 }catch{
  if(Test-Path -LiteralPath $taskPair.backup){
   if($taskLinked){Remove-Item -LiteralPath $taskPair.replay}
   Move-Item -LiteralPath $taskPair.backup -Destination $taskPair.replay
  }
  throw
 }
}
$taskPins[$PSCommandPath]=(Get-FileHash -LiteralPath $PSCommandPath).Hash
New-Item -ItemType Directory -Path $taskOutput | Out-Null
$taskResult=[ordered]@{passed=$true;duplicatesRemoved=$taskDone.Count;allocatedDuplicateBytesReclaimed=($taskDone | Measure-Object allocatedDuplicateBytes -Sum).Sum;logicalDuplicateBytesRemoved=($taskDone | Measure-Object logicalBytes -Sum).Sum;allOriginalAndReplayPathsPreserved=$true;allEvidenceBytesAndHashesUnchanged=$true;uniqueDataDeleted=$false;independentCopyRecoverableFromEitherPath=$true;foldersDeleted=@();pairs=$taskDone;inputHashes=$taskPins;fullPortAcceptance=$false;scope='Exact accepted immutable replay audio shares NTFS storage. No game, source, report or capture bytes changed. Not all-old-build-folder cleanup.'}
$taskResult | ConvertTo-Json -Depth 5 | Out-File -LiteralPath (Join-Path $taskOutput 'report.json') -Encoding utf8
$taskResult | Select-Object passed,duplicatesRemoved,allocatedDuplicateBytesReclaimed,allEvidenceBytesAndHashesUnchanged,uniqueDataDeleted | ConvertTo-Json -Compress
