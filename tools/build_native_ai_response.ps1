$ErrorActionPreference='Stop'
$portRoot=(Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
$repo=Join-Path $portRoot 'mame-mkp'
$name='diagnostic_native_ai_response'
$out=Join-Path $portRoot $name
$prior=Join-Path $portRoot 'diagnostic_native_attract_bios'
$guardPath=Join-Path $portRoot 'audit_native_ai_response_source/report.json'
$guard=Get-Content -LiteralPath $guardPath -Raw | ConvertFrom-Json
$old=Get-Content -LiteralPath "$prior/build-info.json" -Raw | ConvertFrom-Json
$cache=Join-Path $repo 'build/mingw-gcc'
if((Test-Path -LiteralPath $out) -or (Test-Path -LiteralPath $cache)){throw 'Fresh candidate and absent compiler cache required'}
if(-not $guard.passed -or -not $guard.sourceOnlyAccepted -or $guard.nativeFixAccepted -or $guard.expectedGuestChangedBytes -ne 448 -or $guard.actualRecordFaultsRejected.Count -ne 8 -or $guard.knownAdditionalLiveIDTables -ne 7 -or $guard.pointerConsumers -ne 8){throw 'Exact actual diagnosis and source-only conservation repair required'}
foreach($entry in @($guard.inputHashes.PSObject.Properties)+@($old.input_hashes.PSObject.Properties)){
 if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Reviewed input changed: $($entry.Name)"}
}
$installed=Join-Path $repo 'mkport.exe'
if((Get-FileHash -LiteralPath $installed).Hash -ne '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'){throw 'Preexisting installed executable changed'}
function Get-PortCompilerJobs {
 $processes=@(Get-CimInstance Win32_Process)
 $owned=[Collections.Generic.HashSet[uint32]]::new()
 foreach($process in $processes){
  if($process.Name -in @('gmake.exe','g++.exe','gcc.exe','ld.exe','cc1plus.exe') -and
     (($process.CommandLine -and $process.CommandLine.IndexOf($repo,[StringComparison]::OrdinalIgnoreCase) -ge 0) -or
      ($process.CommandLine -and $process.CommandLine.IndexOf('SUBTARGET=mkport',[StringComparison]::OrdinalIgnoreCase) -ge 0))){
   [void]$owned.Add([uint32]$process.ProcessId)
  }
 }
 do {
  $changed=$false
  foreach($process in $processes){
   if($owned.Contains([uint32]$process.ParentProcessId) -and -not $owned.Contains([uint32]$process.ProcessId)){
    [void]$owned.Add([uint32]$process.ProcessId);$changed=$true
   }
  }
 }while($changed)
 return @($processes | Where-Object {$owned.Contains([uint32]$_.ProcessId)})
}
if(@(Get-PortCompilerJobs).Count -or @(Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe' -or $_.ExecutablePath -eq $installed}).Count){throw 'Relevant compiler/emulator jobs must be terminal'}
if((Get-PSDrive -Name C).Free -lt 3GB){throw 'Insufficient transient compiler space'}
$payload=Join-Path $prior 'roms/mk2ks/mk2ks.mdata'
$asset=Join-Path $prior 'samples/mk2ks/kano_ball_launch.wav'
if((Get-FileHash -LiteralPath $payload).Hash -ne $old.payload_sha256 -or (Get-FileHash -LiteralPath $asset).Hash -ne '3D2FB8BD79C818AA2079B10E869D3F1CF444B914582DB560CA64D4408EE57BD7'){throw 'Unchanged shared payload and launch waveform required'}
$stage=Join-Path $portRoot 'source_native_ai_response'
$staged=@{};foreach($file in @('midtunit.cpp','midtunit.h','midtunit_m.cpp')){$staged[(Join-Path $repo "src/mame/midway/$file")]=Join-Path $stage $file}
$expected=@{};foreach($entry in $old.canonical_source_hashes_at_compile.PSObject.Properties){$expected[[IO.Path]::GetFullPath($entry.Name)]=$entry.Value}
foreach($entry in $guard.stagedSourceHashes.PSObject.Properties){$expected[(Join-Path $repo "src/mame/midway/$($entry.Name)")]=$entry.Value}
foreach($path in $expected.Keys){$source=if($staged.ContainsKey($path)){$staged[$path]}else{$path};if((Get-FileHash -LiteralPath $source).Hash -ne $expected[$path]){throw "Reviewed compile input changed: $source"}}
New-Item -ItemType Directory -Path "$out/input_sources","$out/restoration_backups",$cache | Out-Null
$resolvedOut=(Resolve-Path -LiteralPath $out).Path
foreach($leaf in @($resolvedOut,(Resolve-Path -LiteralPath $cache).Path)){
 if(-not $leaf.StartsWith($portRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or ((Get-Item -LiteralPath $leaf).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Unsafe generated build leaf'}
 & compact.exe /C /I /Q "/S:$leaf" | Out-Null
 if($LASTEXITCODE -ne 0){throw 'Compressed build directories required'}
}
$current=@($staged.Keys)+@($installed);$backups=@{};$originalHashes=@{}
foreach($path in $current){
 $originalHashes[$path]=(Get-FileHash -LiteralPath $path).Hash
 $copy=Join-Path "$out/restoration_backups" ([IO.Path]::GetFileName($path));Copy-Item -LiteralPath $path -Destination $copy
 if((Get-FileHash -LiteralPath $copy).Hash -ne $originalHashes[$path]){throw 'Exact preexisting-file backup required'}
 $backups[$path]=$copy
}
$savedPath=$env:PATH;$buildCode=$null
try{
 foreach($path in $staged.Keys){Copy-Item -LiteralPath $staged[$path] -Destination $path -Force}
 $compiled=@{};$canonical=@{}
 foreach($path in $expected.Keys){
  $actual=(Get-FileHash -LiteralPath $path).Hash;if($actual -ne $expected[$path]){throw "Staged compile input changed: $path"}
  $relative=[IO.Path]::GetRelativePath($repo,$path);$frozen=Join-Path "$out/input_sources/mame-mkp" $relative
  New-Item -ItemType Directory -Path (Split-Path $frozen -Parent) -Force | Out-Null
  Copy-Item -LiteralPath $path -Destination $frozen;$compiled[$frozen]=$actual;$canonical[$path]=$actual
 }
 foreach($entry in $old.input_hashes.PSObject.Properties){$compiled[$entry.Name]=$entry.Value}
 foreach($path in @($guardPath,$PSCommandPath,"$prior/build-info.json",$payload,$asset)){$compiled[$path]=(Get-FileHash -LiteralPath $path).Hash}
 Copy-Item -LiteralPath $PSCommandPath -Destination "$out/input_sources"
 Push-Location $repo
 try{
  $env:PATH='C:\Program Files\Git\usr\bin;C:\Users\kando\AppData\Local\Programs\Python\Python314;C:\Strawberry\c\bin;'+$savedPath
  Write-Output 'Compiling one seven-table native AI roster repair; original identities, special moves, bios and audio conserved. Public CMD unchanged; temporary compiler cache will be retired.'
  $ErrorActionPreference='Continue'
  & gmake.exe SUBTARGET=mkport SOURCES=src/mame/midway/midtunit.cpp NOWERROR=1 REGENIE=1 PYTHON_EXECUTABLE=C:/Users/kando/AppData/Local/Programs/Python/Python314/python.exe MINGW64=C:/Strawberry/c PTR64=1 -j4 2>&1 | Out-File -LiteralPath "$out/build.log" -Encoding utf8
  $buildCode=$LASTEXITCODE;$ErrorActionPreference='Stop';if($buildCode -ne 0){throw "Native build failed: $buildCode"}
  foreach($path in $canonical.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $canonical[$path]){throw 'Compiled canonical source changed'}}
  foreach($path in $compiled.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $compiled[$path]){throw 'Frozen compiled input changed'}}
  Copy-Item -LiteralPath $installed -Destination "$out/mkport_candidate.exe"
  New-Item -ItemType Directory -Path "$out/roms/mk2ks","$out/samples/mk2ks" | Out-Null
  New-Item -ItemType HardLink -Path "$out/roms/mk2ks/mk2ks.mdata" -Target $payload | Out-Null
  New-Item -ItemType HardLink -Path "$out/samples/mk2ks/kano_ball_launch.wav" -Target $asset | Out-Null
  & compact.exe /C /EXE:LZX /F /I /Q "$out/mkport_candidate.exe" | Out-Null
  if($LASTEXITCODE -ne 0){throw 'Compressed candidate executable required'}
  [ordered]@{name=$name;executable_sha256=(Get-FileHash -LiteralPath "$out/mkport_candidate.exe").Hash;
   payload_sha256=(Get-FileHash -LiteralPath $payload).Hash;input_hashes=$compiled;canonical_source_hashes_at_compile=$canonical;
   expected_guest_sha256=$guard.proposedGuestSHA256;prior_candidate=$old.name;initialized_guest_byte_delta=$guard.expectedGuestChangedBytes;
   payload_hardlink_to_immutable_prior=$payload;donor_asset_hardlink=$asset;samplepath="$out/samples;$portRoot/samples";
   public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;
   assembly='Seven live-ID AI tables extended to real Kano17/Sonya18. All existing effective rows, native attack/special grammar, identities, biographies, audio, images and RNG conserved. Runtime regression required.'} |
   ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$out/build-info.json" -Encoding utf8
 }finally{Pop-Location}
}finally{
 $env:PATH=$savedPath
 foreach($path in $current){Copy-Item -LiteralPath $backups[$path] -Destination $path -Force;if((Get-FileHash -LiteralPath $path).Hash -ne $originalHashes[$path]){throw "Preexisting file restoration failed: $path"}}
 [ordered]@{passed=$true;restored_actual_preexisting_files=$originalHashes;backup_files=$backups;public_build_promoted=$false;native_build_exit=$buildCode} |
  ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/restoration.json" -Encoding utf8
 $temporaryExe=(Resolve-Path -LiteralPath $backups[$installed]).Path
 if($temporaryExe -cne [IO.Path]::GetFullPath((Join-Path $resolvedOut 'restoration_backups/mkport.exe')) -or -not $temporaryExe.StartsWith($resolvedOut+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Unsafe transient executable backup cleanup'}
 Remove-Item -LiteralPath $temporaryExe
 if(@(Get-PortCompilerJobs).Count){throw 'Do not retire this project cache while its compiler job is live'}
 $checkedCache=(Resolve-Path -LiteralPath $cache).Path;$expectedCache=[IO.Path]::GetFullPath((Join-Path $repo 'build/mingw-gcc'))
 if($checkedCache -cne $expectedCache -or -not $checkedCache.StartsWith($portRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or ((Get-Item -LiteralPath $checkedCache).Attributes -band [IO.FileAttributes]::ReparsePoint) -or @(Get-ChildItem -LiteralPath $checkedCache -Recurse -Force -Attributes ReparsePoint).Count){throw 'Unsafe generated compiler cache cleanup'}
 Remove-Item -LiteralPath $checkedCache -Recurse -Force
 [ordered]@{passed=$true;removedGeneratedCache=$checkedCache;cacheAbsent=(-not(Test-Path -LiteralPath $checkedCache));nativeCompilerExit=$buildCode;preexistingFilesRestored=$true;reclaimedBytesNotMeasured=$true} |
  ConvertTo-Json | Out-File -LiteralPath "$out/cache_retirement.json" -Encoding utf8
}
Get-Content -LiteralPath "$out/build-info.json" -Raw | ConvertFrom-Json | Select-Object name,executable_sha256,payload_sha256,expected_guest_sha256 | ConvertTo-Json -Compress


