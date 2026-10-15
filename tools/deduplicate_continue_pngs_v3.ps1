param([Parameter(Mandatory=$true)][string]$CaseName)
$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if($taskRoot -ne 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port'){throw 'Unexpected workspace'}
if($CaseName -notmatch '^audit_v(469|470)_[a-z0-9_]+$'){throw 'Only new continue evidence is in scope'}
$taskCase=(Resolve-Path -LiteralPath (Join-Path $taskRoot $CaseName)).Path
if(-not $taskCase.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Outside workspace'}
$taskResult=Get-Content -LiteralPath (Join-Path $taskCase 'result.json') -Raw | ConvertFrom-Json
if($taskResult.exit_code -ne 0){throw 'Only a terminal successful diagnostic may be consolidated'}
$taskReport=Join-Path $taskCase 'png_storage.json'
$taskJournal=Join-Path $taskCase 'png_storage.jsonl'
if((Test-Path -LiteralPath $taskReport) -or (Test-Path -LiteralPath $taskJournal)){throw 'Refusing overwrite'}
Add-Type -TypeDefinition @'
using System; using System.IO; using System.Runtime.InteropServices;
public static class Mk2PngIdentity {
 [StructLayout(LayoutKind.Sequential)] struct Details {
  public uint attr,createdLow,createdHigh,accessLow,accessHigh,writeLow,writeHigh;
  public uint volume,sizeHigh,sizeLow,links,indexHigh,indexLow;
 }
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool GetFileInformationByHandle(IntPtr h,out Details info);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern uint GetCompressedFileSizeW(string p,out uint h);
 public static string Id(string p) {
  using(var f=File.Open(p,FileMode.Open,FileAccess.Read,FileShare.ReadWrite|FileShare.Delete)) {
   Details d; if(!GetFileInformationByHandle(f.SafeFileHandle.DangerousGetHandle(),out d))throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
   return d.volume.ToString("X8")+d.indexHigh.ToString("X8")+d.indexLow.ToString("X8");
  }
 }
 public static ulong Allocation(string p) {
  uint h;uint l=GetCompressedFileSizeW(p,out h);
  if(l==UInt32.MaxValue && Marshal.GetLastWin32Error()!=0)throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
  return ((ulong)h<<32)|l;
 }
}
'@
$taskFiles=@(foreach($taskFolder in (Get-Item -LiteralPath $taskCase)) {
  if($taskFolder.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse case folder'}
  $taskSnap=Join-Path $taskFolder.FullName 'snap'
  if(Test-Path -LiteralPath $taskSnap){
   if((Get-Item -LiteralPath $taskSnap).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse snapshot directory'}
   Get-ChildItem -LiteralPath $taskSnap -File -Filter '*.png'
  }
})
function Assert-Target([string]$taskPath) {
 $taskResolved=(Resolve-Path -LiteralPath $taskPath).Path
 if(-not $taskResolved.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or
    $taskResolved -notmatch '\\audit_v(469|470)_[a-z0-9_]+\\snap\\[a-zA-Z0-9_.-]+\.png$') {throw 'Target outside selected evidence'}
 if((Get-Item -LiteralPath $taskResolved).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse PNG'}
 return $taskResolved
}
$taskCanonical=@{};$taskRows=[Collections.Generic.List[object]]::new();$taskReleased=[Collections.Generic.HashSet[string]]::new();[long]$taskSaved=0
try {
 foreach($taskFile in $taskFiles){
  $taskPath=Assert-Target $taskFile.FullName
  $taskSha=(Get-FileHash -LiteralPath $taskPath).Hash
  $taskKey="$taskSha/$($taskFile.Length)"
  if(-not $taskCanonical.ContainsKey($taskKey)){$taskCanonical[$taskKey]=$taskPath;continue}
  $taskKeep=Assert-Target $taskCanonical[$taskKey]
  $taskId=[Mk2PngIdentity]::Id($taskPath);$taskKeepId=[Mk2PngIdentity]::Id($taskKeep)
  if($taskId -eq $taskKeepId){continue}
  if((Get-FileHash -LiteralPath $taskKeep).Hash -ne $taskSha){throw 'Canonical bytes changed'}
  $taskAllocated=[Mk2PngIdentity]::Allocation($taskPath)
  $taskRow=[pscustomobject]@{path=$taskPath;canonical=$taskKeep;sha256=$taskSha;oldFileId=$taskId;allocated=$taskAllocated;linked=$false;verified=$false}
  $taskRows.Add($taskRow)
  # Persist recovery information BEFORE replacing the redundant physical copy.
  $taskRow | ConvertTo-Json -Compress | Out-File -LiteralPath $taskJournal -Append -Encoding utf8
  Remove-Item -LiteralPath $taskPath
  try {New-Item -ItemType HardLink -Path $taskPath -Target $taskKeep | Out-Null}
  catch {Copy-Item -LiteralPath $taskKeep -Destination $taskPath;throw}
  $taskRow.linked=[Mk2PngIdentity]::Id($taskPath) -eq $taskKeepId
  $taskRow.verified=(Get-FileHash -LiteralPath $taskPath).Hash -eq $taskSha
  if(-not $taskRow.linked -or -not $taskRow.verified){throw 'Hard-link preservation failed'}
 }
 # Count only original allocations whose final file identity no longer occurs
 # among selected paths. Already-linked originals are never double-counted.
 $taskRemaining=[Collections.Generic.HashSet[string]]::new()
 foreach($taskFile in $taskFiles){[void]$taskRemaining.Add([Mk2PngIdentity]::Id($taskFile.FullName))}
 foreach($taskRow in $taskRows){if(-not $taskRemaining.Contains($taskRow.oldFileId) -and $taskReleased.Add($taskRow.oldFileId)){$taskSaved+=$taskRow.allocated}}
} finally {
 [ordered]@{method='SHA256-identical PNG physical copies replaced by NTFS hard links; every filename and byte preserved';selectedFiles=$taskFiles.Count;duplicateCopyBytesConsolidated=$taskSaved;rows=$taskRows} |
  ConvertTo-Json -Depth 5 | Out-File -LiteralPath $taskReport -Encoding utf8
}
[pscustomobject]@{files=$taskFiles.Count;linked=$taskRows.Count;verified=@($taskRows | Where-Object verified).Count;reportedDuplicateCopyBytes=$taskSaved} | Format-List
