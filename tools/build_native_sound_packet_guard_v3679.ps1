$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
$repo=Join-Path $portRoot 'mame-mkp'
$name='diagnostic_v3680_native_sound_packet_guard'
$out=Join-Path $portRoot $name
$prior=Join-Path $portRoot 'diagnostic_v3172_native_morph_shadow'
$priorInfo=Get-Content -LiteralPath "$prior/build-info.json" -Raw | ConvertFrom-Json
$guardReportPath="$portRoot/audit_v3670_native_sound_packet_guard_checked/report.json"
$guard=Get-Content -LiteralPath $guardReportPath -Raw | ConvertFrom-Json
if(Test-Path -LiteralPath $out){throw 'Never overwrite a candidate or evidence'}
if(-not $guard.passed -or -not $guard.stagedFixRequiresCompilationAndRuntimeRegression){throw 'Independent whole-source native packet guard proof required'}
foreach($item in $guard.inputHashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Guard input changed: $($item.Name)"}}
foreach($item in $priorInfo.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Actual current compiled source changed: $($item.Name)"}}
$payload="$prior/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash -LiteralPath $payload).Hash -ne 'ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3'){throw 'Exact unchanged current payload required'}
$installed="$repo/mkport.exe"
if((Get-FileHash -LiteralPath $installed).Hash -ne '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'){throw 'Historical installed executable changed'}
if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $installed}).Count){throw 'Installed emulator running; cannot stage compiler output'}
$current=@("$repo/src/mame/midway/midtunit.cpp","$repo/src/mame/midway/midtunit_m.cpp","$repo/src/mame/midway/midtunit.h",$installed)
$originalHashes=@{}
foreach($path in $current){$originalHashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$driver="$prior/input_sources/mame-mkp/src/mame/midway/midtunit.cpp"
$machine=$guard.stagedSource
$header="$prior/input_sources/mame-mkp/src/mame/midway/midtunit.h"
if((Get-FileHash -LiteralPath $machine).Hash -ne 'A3D4B37E644B845D83ADD746E1705F33F90BA8BB5E8A4D86F85938A2767F7F40'){throw 'Exact independently checked source fix required'}
New-Item -ItemType Directory -Path "$out/input_sources","$out/restoration_backups" | Out-Null
$resolvedOut=(Get-Item -LiteralPath $out).FullName
$resolvedRoot=(Get-Item -LiteralPath $portRoot).FullName
if(-not $resolvedOut.StartsWith($resolvedRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or (Get-Item -LiteralPath $out).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe new candidate leaf'}
& compact.exe /C /I /Q "/S:$resolvedOut" | Out-Null
if($LASTEXITCODE -ne 0){throw 'Cannot enable lossless evidence compression'}
$backups=@{}
foreach($path in $current){
  $destination=Join-Path "$out/restoration_backups" ([IO.Path]::GetFileName($path))
  Copy-Item -LiteralPath $path -Destination $destination
  if((Get-FileHash -LiteralPath $destination).Hash -ne $originalHashes[$path]){throw 'Exact actual preexisting file backup required'}
  $backups[$path]=$destination
}
$savedPath=$env:PATH
try{
  Copy-Item -LiteralPath $driver -Destination $current[0] -Force
  Copy-Item -LiteralPath $machine -Destination $current[1] -Force
  Copy-Item -LiteralPath $header -Destination $current[2] -Force
  $tracked=@($payload,$driver,$machine,$header,$guardReportPath,"$prior/build-info.json",$PSCommandPath)
  $tracked+=@($priorInfo.input_hashes.PSObject.Properties.Name)
  $tracked+=@("$repo/src/mame/midway/midtunit.cpp","$repo/src/mame/midway/midtunit_m.cpp","$repo/src/mame/midway/midtunit.h",
    "$repo/src/devices/cpu/tms34010/34010gfx.hxx","$repo/src/devices/cpu/tms34010/34010ops.hxx")
  $tracked=@($tracked | Select-Object -Unique)
  $before=@{};$compiled=@{}
  foreach($path in $tracked){
    $before[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.cpp','.h','.hxx'){
      $relative=[IO.Path]::GetRelativePath($portRoot,$path)
      $frozen=Join-Path "$out/input_sources" $relative
      New-Item -ItemType Directory -Path (Split-Path $frozen -Parent) -Force | Out-Null
      Copy-Item -LiteralPath $path -Destination $frozen
      $compiled[$frozen]=$before[$path]
    }else{$compiled[$path]=$before[$path]}
  }
  Copy-Item -LiteralPath $PSCommandPath -Destination "$out/input_sources"
  Push-Location $repo
  try{
    $env:PATH='C:\Program Files\Git\usr\bin;C:\Users\kando\AppData\Local\Programs\Python\Python314;C:\Strawberry\c\bin;'+$savedPath
    $ErrorActionPreference='Continue'
    # New GCC diagnoses unchanged bundled LZMA/NanoVG code. Preserve the
    # vendor sources; warnings remain visible, only their error promotion ends.
    & gmake.exe SUBTARGET=mkport SOURCES=src/mame/midway/midtunit.cpp NOWERROR=1 REGENIE=1 PYTHON_EXECUTABLE=C:/Users/kando/AppData/Local/Programs/Python/Python314/python.exe MINGW64=C:/Strawberry/c PTR64=1 -j4 2>&1 |
      Out-File -LiteralPath "$out/build.log" -Encoding utf8
    $buildCode=$LASTEXITCODE;$ErrorActionPreference='Stop'
    if($buildCode -ne 0){throw "Native build failed: $buildCode"}
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $before[$path]){throw "Compiled input changed: $path"}}
    Copy-Item -LiteralPath $installed -Destination "$out/mkport_candidate.exe"
    New-Item -ItemType Directory -Path "$out/roms/mk2ks" | Out-Null
    # Payload is immutable and identical; no additional 3.1MB data allocation.
    New-Item -ItemType HardLink -Path "$out/roms/mk2ks/mk2ks.mdata" -Target $payload | Out-Null
    if((Get-FileHash -LiteralPath "$out/roms/mk2ks/mk2ks.mdata").Hash -ne $before[$payload]){throw 'Unchanged current payload link required'}
    [ordered]@{name=$name;executable_sha256=(Get-FileHash -LiteralPath "$out/mkport_candidate.exe").Hash;
      payload_sha256=$before[$payload];input_hashes=$compiled;canonical_source_hashes_at_compile=$before;
      expected_guest_sha256='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7';
      prior_candidate='diagnostic_v3172_native_morph_shadow';game_data_changed=$false;metadata_only_source_rebuild=$false;
      payload_hardlink_to_immutable_prior=$payload;public_build_promoted=$false;compiler_warnings_as_errors=$false;
      source_selected_target='src/mame/midway/midtunit.cpp';project_makefiles_regenerated=$true;
      assembly='Only native sound packet store PCs bypass imported FFF7..FFFE markers. Entire guest/payload and all other host implementation unchanged.'} |
      ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$out/build-info.json" -Encoding utf8
  }finally{Pop-Location}
}finally{
  $env:PATH=$savedPath
  foreach($path in $current){
    Copy-Item -LiteralPath $backups[$path] -Destination $path -Force
    if((Get-FileHash -LiteralPath $path).Hash -ne $originalHashes[$path]){throw "Exact actual user-file restoration failed: $path"}
  }
  [ordered]@{passed=$true;restored_actual_preexisting_files=$originalHashes;backup_files=$backups;public_build_promoted=$false} |
    ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/restoration.json" -Encoding utf8
  # Remove only our new transient executable backup after exact restoration.
  # The restored installed executable and untouched public/current builds remain.
  $temporaryExe=(Get-Item -LiteralPath $backups[$installed]).FullName
  $expectedBackup=Join-Path $resolvedOut 'restoration_backups/mkport.exe'
  if($temporaryExe -cne $expectedBackup -or -not $temporaryExe.StartsWith($resolvedOut+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Unsafe transient backup cleanup target'}
  if((Get-FileHash -LiteralPath $installed).Hash -ne $originalHashes[$installed]){throw 'Cannot remove backup before exact installed restoration'}
  Remove-Item -LiteralPath $temporaryExe
}
Get-Content -LiteralPath "$out/build-info.json" -Raw | ConvertFrom-Json | Select-Object name,executable_sha256,payload_sha256,expected_guest_sha256 | ConvertTo-Json -Compress
