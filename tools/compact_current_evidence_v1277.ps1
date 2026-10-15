param([switch]$Apply)
$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$expectedRoot='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'
if($taskRoot -ne $expectedRoot){throw 'Unexpected workspace'}
$taskOut=Join-Path $taskRoot 'audit_v1277_current_evidence_compaction'
if($Apply -and (Test-Path -LiteralPath $taskOut)){throw 'Preserve previous compaction evidence'}
if(-not ('Mk2BuildAllocation1259' -as [type])){
 Add-Type -TypeDefinition @'
using System; using System.Runtime.InteropServices;
public static class Mk2BuildAllocation1259 {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)]
 static extern uint GetCompressedFileSizeW(string path,out uint high);
 public static ulong Bytes(string path) {
  uint high;uint low=GetCompressedFileSizeW(path,out high);
  if(low==UInt32.MaxValue && Marshal.GetLastWin32Error()!=0)
   throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
  return ((ulong)high<<32)|low;
 }
}
'@
}
$taskFolders=@('audit_v1268_ground_shadow_kano_p1','audit_v1268_ground_shadow_kano_p2',
 'audit_v1268_ground_shadow_sonya_p1','audit_v1268_ground_shadow_sonya_p2',
 'audit_v1270_ui_kano_p1','audit_v1270_ui_kano_p2','audit_v1270_ui_sonya_p1','audit_v1270_ui_sonya_p2')
$taskTargets=@($taskFolders | ForEach-Object {
 $taskFolder=(Resolve-Path -LiteralPath (Join-Path $taskRoot $_)).Path
 if(-not $taskFolder.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Unexpected capture folder'}
 if(@(Get-Item -LiteralPath $taskFolder; Get-ChildItem -LiteralPath $taskFolder -Recurse -Directory | Where-Object {
  $_.Attributes -band [IO.FileAttributes]::ReparsePoint
 }).Where({$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'Capture has reparse directory'}
 $taskResult=Get-Content -LiteralPath (Join-Path $taskFolder 'result.json') -Raw | ConvertFrom-Json
 if($taskResult.exit_code -ne 0 -or $taskResult.candidate -ne 'diagnostic_v1250_native_correct_rom_metadata'){throw 'Capture is not terminal/current'}
 Get-ChildItem -LiteralPath $taskFolder -Recurse -File | Where-Object {
  $_.Extension -in '.bin','.log' -and $_.Length -ge 256KB -and
  -not ($_.Attributes -band [IO.FileAttributes]::Compressed) -and
  -not ($_.Attributes -band [IO.FileAttributes]::ReparsePoint)
 }
})
$taskPaths=@($taskTargets.FullName)
if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -and $taskPaths -contains $_.ExecutablePath}).Count){throw 'An old target executable is running'}
$taskRows=@($taskTargets | ForEach-Object {
 $taskPath=(Resolve-Path -LiteralPath $_.FullName).Path
 if(-not $taskPath.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Target outside workspace'}
 [pscustomobject]@{path=$taskPath;logicalBytes=$_.Length;allocatedBefore=[Mk2BuildAllocation1259]::Bytes($taskPath);
  sha256=$null;allocatedAfter=$null;verified=$false;exitCode=$null}
})
if(-not $Apply){
 [pscustomobject]@{terminalCaptureFiles=$taskRows.Count;allocatedBytes=($taskRows | Measure-Object allocatedBefore -Sum).Sum;
  method='Reversible NTFS compression only; no deletion or relocation';current1219And1250Excluded=$true} | Format-List
 return
}
$taskProtected=@('diagnostic_v1219_owned_native_headed_reaction\mkport_candidate.exe',
 'diagnostic_v1250_native_correct_rom_metadata\mkport_candidate.exe','mame-mkp\mkport.exe',
 'mame-mkp\src\mame\midway\midtunit.cpp','mame-mkp\src\mame\midway\midtunit_m.cpp')
$taskProtectedHashes=@{};foreach($file in $taskProtected){$taskPath=Join-Path $taskRoot $file;$taskProtectedHashes[$taskPath]=(Get-FileHash -LiteralPath $taskPath).Hash}
New-Item -ItemType Directory -Path $taskOut | Out-Null
try{
 # Hash all exact validated files before changing storage attributes. Batch
 # the native compactor to avoid thousands of shell/process round trips.
 foreach($row in $taskRows){
  if(-not (Resolve-Path -LiteralPath $row.path).Path.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Resolved target outside workspace'}
  if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $row.path}).Count){throw 'Target became active'}
  $row.sha256=(Get-FileHash -LiteralPath $row.path).Hash
 }
 for($taskIndex=0;$taskIndex -lt $taskRows.Count;$taskIndex+=32){
  $taskBatch=@($taskRows[$taskIndex..([Math]::Min($taskIndex+31,$taskRows.Count-1))])
  & compact.exe /C /Q @($taskBatch.path) | Out-Null
  $taskCode=$LASTEXITCODE
  foreach($row in $taskBatch){
   $row.exitCode=$taskCode;$row.allocatedAfter=[Mk2BuildAllocation1259]::Bytes($row.path)
   $row.verified=(Get-FileHash -LiteralPath $row.path).Hash -eq $row.sha256
   if(-not $row.verified){throw 'Compaction changed file content'}
  }
  if(($taskIndex%320) -eq 0){"Verified $([Math]::Min($taskIndex+32,$taskRows.Count)) / $($taskRows.Count) terminal capture files"}
 }
 foreach($file in $taskProtectedHashes.Keys){if((Get-FileHash -LiteralPath $file).Hash -ne $taskProtectedHashes[$file]){throw 'Protected current/source file changed'}}
}finally{
 $completed=@($taskRows | Where-Object verified)
 $taskReport=[ordered]@{method='Reversible NTFS compression; no files deleted or moved';
  files=$taskRows;verifiedFiles=$completed.Count;plannedFiles=$taskRows.Count;
  reclaimedBytes=[long](($completed | Measure-Object allocatedBefore -Sum).Sum)-[long](($completed | Measure-Object allocatedAfter -Sum).Sum);
  protectedFileHashes=$taskProtectedHashes;undo='compact.exe /U with each exact path in this report';
  oldBuildFoldersDeleted=$false;currentBuildsExcluded=$true;fullPortAccepted=$false}
 $taskReport | ConvertTo-Json -Depth 5 | Out-File (Join-Path $taskOut 'report.json') -Encoding utf8
}
"Verified $($taskReport.verifiedFiles) terminal capture files; reclaimed $($taskReport.reclaimedBytes) bytes; no deletion."
