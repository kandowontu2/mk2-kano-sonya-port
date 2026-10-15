$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$taskCache=$taskRoot
if($taskCache -ne 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'){throw 'Unexpected root'}
$taskReportPath=Join-Path $taskRoot 'WORKSPACE_LZX_COMPACTION_2026-10-01.json'
if(Test-Path -LiteralPath $taskReportPath){throw 'Refusing overwrite'}
if(@(Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -like '*mk2port*' -and $_.Name -match 'gmake|g\+\+|cc1|ar.exe'}).Count){throw 'Compiler still active'}
Add-Type -TypeDefinition @'
using System; using System.Runtime.InteropServices;
public static class Mk2CacheAllocation {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)]
 static extern uint GetCompressedFileSizeW(string p,out uint h);
 public static ulong Bytes(string p) {uint h; uint l=GetCompressedFileSizeW(p,out h);
 if(l==UInt32.MaxValue && Marshal.GetLastWin32Error()!=0) throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
 return ((ulong)h<<32)|l;}
}
'@
$taskRows=@(@(269,272,275,276,292,300,324,330) | ForEach-Object {Get-ChildItem -LiteralPath $taskRoot -Directory -Filter "diagnostic_v$($_)_*" | ForEach-Object {Get-ChildItem -LiteralPath $_.FullName -File -Filter 'mkport_candidate.exe'}} | ForEach-Object {
 $taskPath=(Resolve-Path -LiteralPath $_.FullName).Path
 if(-not $taskPath.StartsWith($taskCache+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Target outside cache'}
 [pscustomobject]@{path=$taskPath;before=[Mk2CacheAllocation]::Bytes($taskPath);sha256=(Get-FileHash -LiteralPath $taskPath).Hash;after=$null;verified=$false;exitCode=$null}
})
try {
 foreach($taskRow in $taskRows){
  & compact.exe /C /F /EXE:LZX /Q $taskRow.path | Out-Null
  $taskRow.exitCode=$LASTEXITCODE
  $taskRow.after=[Mk2CacheAllocation]::Bytes($taskRow.path)
  $taskRow.verified=(Get-FileHash -LiteralPath $taskRow.path).Hash -eq $taskRow.sha256
  if(-not $taskRow.verified){throw 'Cache file content changed'}
 }
} finally {
 [ordered]@{method='Reversible Windows LZX executable compression; no deletion';files=$taskRows} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $taskReportPath -Encoding UTF8
}
[pscustomobject]@{files=$taskRows.Count;verified=@($taskRows | Where-Object verified).Count;reclaimedBytes=[long](($taskRows | Measure-Object before -Sum).Sum)-[long](($taskRows | Measure-Object after -Sum).Sum);compressionFailures=@($taskRows | Where-Object {$_.exitCode -ne 0}).Count} | Format-List
