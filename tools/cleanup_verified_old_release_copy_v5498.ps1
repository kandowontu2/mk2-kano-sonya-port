param([switch]$DeleteMatchedCopies)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class MK2OldReleaseAllocation5498 {
 [StructLayout(LayoutKind.Sequential)] public struct Info {
  public long AllocationSize; public long EndOfFile; public uint NumberOfLinks;
  [MarshalAs(UnmanagedType.I1)] public bool DeletePending;
  [MarshalAs(UnmanagedType.I1)] public bool Directory;
 }
 [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
 static extern Microsoft.Win32.SafeHandles.SafeFileHandle CreateFileW(string path, uint access, uint share, IntPtr security, uint creation, uint flags, IntPtr template);
 [DllImport("kernel32.dll", SetLastError=true)]
 static extern bool GetFileInformationByHandleEx(Microsoft.Win32.SafeHandles.SafeFileHandle h, int infoClass, out Info info, uint size);
 public static Info Read(string path) {
  using(var h=CreateFileW(path,0,7,IntPtr.Zero,3,0,IntPtr.Zero)) {
   Info value;
   if(h.IsInvalid || !GetFileInformationByHandleEx(h,1,out value,(uint)Marshal.SizeOf(typeof(Info)))) throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
   return value;
  }
 }
}
'@
$taskOutputRoot = 'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port\outputs'
$taskTarget = [IO.Path]::GetFullPath((Join-Path $taskOutputRoot 'MK2-Kano-Sonya-v44-WIP-2026-09-05\MK2-Kano-Sonya-v44-WIP'))
$taskArchivePath = Join-Path $taskOutputRoot 'MK2-Kano-Sonya-v44-WIP-2026-09-05.zip'
$taskArchiveHash = (Get-FileHash -LiteralPath $taskArchivePath -Algorithm SHA256).Hash
if ($taskArchiveHash -ne 'C72E5B40A01CC566167D41FD221B4170D0417A496C132B1B4E044B099EAB5C7F') { throw 'Changed retained recovery ZIP' }
if ((Get-Item -LiteralPath $taskTarget).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse-point target' }
$taskPinPath = 'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\audit_v5496_current_reptile_overlap_ram\kano_p1\input_hashes_before.json'
$taskPins = Get-Content -LiteralPath $taskPinPath -Raw | ConvertFrom-Json
$taskPinnedCopies = @($taskPins.PSObject.Properties.Name | Where-Object { $_.StartsWith($taskTarget+'\',[StringComparison]::OrdinalIgnoreCase) })
if ($taskPinnedCopies.Count) { throw 'Active proof dependency inside obsolete extracted release' }
$taskLiveCopies = @(Get-CimInstance Win32_Process -Filter "Name='mkport.exe' OR Name='mkport_candidate.exe'" | Where-Object { $_.ExecutablePath -and $_.ExecutablePath.StartsWith($taskTarget+'\',[StringComparison]::OrdinalIgnoreCase) })
if ($taskLiveCopies.Count) { throw 'Old extracted release is running' }
$taskArchive = [IO.Compression.ZipFile]::OpenRead($taskArchivePath)
$taskMatched = [Collections.Generic.List[object]]::new()
try {
 foreach ($taskEntry in $taskArchive.Entries) {
  if ($taskEntry.FullName.EndsWith('/')) { continue }
  if (-not $taskEntry.FullName.StartsWith('MK2-Kano-Sonya-v44-WIP/')) { throw 'Unexpected archive root' }
  $taskRelative = $taskEntry.FullName.Substring('MK2-Kano-Sonya-v44-WIP/'.Length)
  $taskPath = [IO.Path]::GetFullPath((Join-Path $taskTarget ($taskRelative.Replace('/','\'))))
  if (-not $taskPath.StartsWith($taskTarget+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Archive path escapes exact extracted release' }
  $taskFile = Get-Item -LiteralPath $taskPath
  if ($taskFile.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse-point file' }
  if ($taskFile.Length -ne $taskEntry.Length) { throw "Modified old release file: $taskRelative" }
  $taskHasher = [Security.Cryptography.SHA256]::Create()
  $taskStream = $taskEntry.Open()
  try { $taskWanted = [BitConverter]::ToString($taskHasher.ComputeHash($taskStream)).Replace('-','') }
  finally { $taskStream.Dispose(); $taskHasher.Dispose() }
  if ((Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash -ne $taskWanted) { throw "Unique/modified file preserved: $taskRelative" }
  $taskInfo = [MK2OldReleaseAllocation5498]::Read($taskPath)
  if ($taskInfo.NumberOfLinks -ne 1) { throw 'Shared hard-linked release file must be preserved' }
  $taskMatched.Add([pscustomobject]@{Path=$taskPath;ArchiveEntry=$taskEntry.FullName;SHA256=$taskWanted;Bytes=$taskFile.Length;AllocatedBytes=$taskInfo.AllocationSize})
 }
} finally { $taskArchive.Dispose() }
$taskMatchedPaths = @($taskMatched | ForEach-Object Path)
$taskUniqueFiles = @(Get-ChildItem -LiteralPath $taskTarget -File -Recurse -Force | Where-Object { $_.FullName -notin $taskMatchedPaths } | ForEach-Object FullName)
if ($taskMatched.Count -lt 40) { throw 'Incomplete original release inventory' }
$taskReport = [ordered]@{
 Target=$taskTarget; RecoveryZIP=$taskArchivePath; RecoveryZIPSHA256=$taskArchiveHash
 MatchedArchiveFiles=$taskMatched.Count
 LogicalBytes=($taskMatched | Measure-Object -Property Bytes -Sum).Sum
 AllocatedBytes=($taskMatched | Measure-Object -Property AllocatedBytes -Sum).Sum
 PreservedUniqueFiles=$taskUniqueFiles; DeletedFiles=0; MatchedFiles=$taskMatched
 CurrentGameLauncherSourcesAndProofDependenciesChanged=$false
}
if ($DeleteMatchedCopies) {
 # Only individually source-identical archive copies; keep configs/NVRAM and
 # all parent folders. Never recursively delete the workspace or output root.
 if ((Get-FileHash -LiteralPath $taskArchivePath -Algorithm SHA256).Hash -ne $taskArchiveHash) { throw 'Recovery ZIP changed before cleanup' }
 foreach ($taskFile in $taskMatched) {
  $taskResolved = (Resolve-Path -LiteralPath $taskFile.Path).ProviderPath
  if (-not $taskResolved.StartsWith($taskTarget+'\',[StringComparison]::OrdinalIgnoreCase) -or
      (Get-FileHash -LiteralPath $taskResolved -Algorithm SHA256).Hash -ne $taskFile.SHA256) { throw 'Cleanup target changed' }
  Remove-Item -LiteralPath $taskResolved -Force
  $taskReport.DeletedFiles++
 }
 if (@($taskMatched | Where-Object { Test-Path -LiteralPath $_.Path }).Count) { throw 'Duplicate files still exist' }
 if (@($taskUniqueFiles | Where-Object { -not (Test-Path -LiteralPath $_) }).Count) { throw 'Unique configuration lost' }
}
$taskReport | ConvertTo-Json -Depth 5
