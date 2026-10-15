$ErrorActionPreference='Stop'
$mk2Root=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$mk2Candidate=Join-Path $mk2Root 'diagnostic_v6508_native_projectile_identifiers'
$mk2Cache=(Resolve-Path -LiteralPath (Join-Path $mk2Root 'mame-mkp/build/mingw-gcc')).Path
$mk2Exact='C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\mame-mkp\build\mingw-gcc'
$mk2Out=Join-Path $mk2Root 'audit_v6517_generated_compiler_cache_retired'
if($mk2Cache -cne $mk2Exact -or -not $mk2Cache.StartsWith($mk2Root+'\',[StringComparison]::OrdinalIgnoreCase) -or
   ((Get-Item -LiteralPath $mk2Cache).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Unexpected cache target'}
if(Test-Path -LiteralPath $mk2Out){throw 'Never overwrite executed cleanup evidence'}
$mk2Jobs=@(Get-CimInstance Win32_Process | Where-Object {$_.Name -match '^(gmake|cc1plus|gcc|g\+\+|ar)\.exe$'})
if($mk2Jobs.Count){throw 'Same compiler tree must be confirmed terminal before cache retirement'}
$mk2Build=Get-Content -LiteralPath "$mk2Candidate/build-info.json" -Raw | ConvertFrom-Json
$mk2Restore=Get-Content -LiteralPath "$mk2Candidate/restoration.json" -Raw | ConvertFrom-Json
if(-not $mk2Restore.passed -or $mk2Build.name -ne 'diagnostic_v6508_native_projectile_identifiers' -or
   $mk2Build.initialized_guest_byte_delta -ne 158 -or $mk2Build.public_build_promoted){throw 'Completed isolated candidate/restoration required'}
$mk2Pins=@{}
foreach($mk2Entry in $mk2Build.input_hashes.PSObject.Properties){
 $mk2Path=[IO.Path]::GetFullPath($mk2Entry.Name)
 if($mk2Path.StartsWith($mk2Cache+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'A required compiled input is inside the cache'}
 if((Get-FileHash -LiteralPath $mk2Path).Hash -ne $mk2Entry.Value){throw "Compiled input changed: $mk2Path"}
 $mk2Pins[$mk2Path]=$mk2Entry.Value
}
foreach($mk2Entry in $mk2Restore.restored_actual_preexisting_files.PSObject.Properties){
 if((Get-FileHash -LiteralPath $mk2Entry.Name).Hash -ne $mk2Entry.Value){throw 'Preexisting dirty file not restored exactly'}
 $mk2Pins[$mk2Entry.Name]=$mk2Entry.Value
}
foreach($mk2Path in @("$mk2Candidate/mkport_candidate.exe","$mk2Candidate/roms/mk2ks/mk2ks.mdata","$mk2Candidate/build-info.json","$mk2Candidate/restoration.json",$PSCommandPath)){
 $mk2Pins[$mk2Path]=(Get-FileHash -LiteralPath $mk2Path).Hash
}
if($mk2Pins["$mk2Candidate/mkport_candidate.exe"] -ne $mk2Build.executable_sha256 -or
   $mk2Pins["$mk2Candidate/roms/mk2ks/mk2ks.mdata"] -ne $mk2Build.payload_sha256){throw 'Actual retained candidate pair changed'}
Add-Type -TypeDefinition @'
using System; using System.Runtime.InteropServices;
public static class Mk2GeneratedCacheSize {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)]
 static extern uint GetCompressedFileSizeW(string p,out uint h);
 public static ulong Bytes(string p) {uint h;uint l=GetCompressedFileSizeW(p,out h);
  if(l==UInt32.MaxValue&&Marshal.GetLastWin32Error()!=0)throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
  return ((ulong)h<<32)|l;}
}
'@
$mk2Items=@(Get-ChildItem -LiteralPath $mk2Cache -Recurse -Force)
$mk2Rows=@()
foreach($mk2Item in $mk2Items){
 $mk2Path=[IO.Path]::GetFullPath($mk2Item.FullName)
 if(-not $mk2Path.StartsWith($mk2Cache+'\',[StringComparison]::OrdinalIgnoreCase) -or
    ($mk2Item.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Cache child escaped resolved exact target'}
 if(-not $mk2Item.PSIsContainer){
  if($mk2Item.Extension -notin '.o','.a','.d','.gch','.res'){throw "Unexpected non-generated cache file: $mk2Path"}
  $mk2Rows+= [ordered]@{path=$mk2Path;logicalBytes=$mk2Item.Length;allocatedBytes=[Mk2GeneratedCacheSize]::Bytes($mk2Path)}
 }
}
if(-not $mk2Rows.Count){throw 'Expected actual generated compiler cache'}
New-Item -ItemType Directory -Path $mk2Out | Out-Null
& compact.exe /C /I /Q "/S:$mk2Out" | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cleanup report compression required'}
# This exact newly regenerated object/archive cache is reproducible by the
# retained build script. No source, executable, payload, settings or evidence
# folder is targeted. Resolve/check above precedes this one-shell deletion.
Remove-Item -LiteralPath $mk2Cache -Recurse -Force
if(Test-Path -LiteralPath $mk2Cache){throw 'Generated cache removal incomplete'}
foreach($mk2Path in $mk2Pins.Keys){if((Get-FileHash -LiteralPath $mk2Path).Hash -ne $mk2Pins[$mk2Path]){throw 'Retained candidate/source changed during cleanup'}}
[ordered]@{passed=$true;observedUTC=[DateTime]::UtcNow.ToString('o');exactTarget=$mk2Cache;
 removedFiles=$mk2Rows.Count;removedDirectories=@($mk2Items | Where-Object PSIsContainer).Count+1;
 reclaimedLogicalBytes=[long](($mk2Rows | Measure-Object logicalBytes -Sum).Sum);
 reclaimedAllocatedBytes=[long](($mk2Rows | Measure-Object allocatedBytes -Sum).Sum);
 files=$mk2Rows;inputHashes=$mk2Pins;compilerJobsTerminal=$true;
 retainedAllExecutablePayloadSourcesSettingsAndPriorEvidence=$true;
 recovery='Regenerate object/archive cache with retained isolated build recipe; not a backup of user data.';
 publicPlayableChanged=$false;fullPortAcceptance=$false} | ConvertTo-Json -Depth 5 |
 Out-File -LiteralPath "$mk2Out/report.json" -Encoding utf8
Get-Content -LiteralPath "$mk2Out/report.json" -Raw | ConvertFrom-Json |
 Select-Object passed,removedFiles,reclaimedAllocatedBytes | ConvertTo-Json -Compress
