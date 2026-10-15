$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
$repo=Join-Path $portRoot 'mame-mkp'
$name='diagnostic_v3172_native_morph_shadow'
$out=Join-Path $portRoot $name
$prior=Join-Path $portRoot 'diagnostic_v2753_native_friendship_palette'
$asset=Join-Path $portRoot 'audit_v3169_native_morph_shadow_payload'
$assetReport=Get-Content -LiteralPath "$asset/report.json" -Raw | ConvertFrom-Json
if(Test-Path -LiteralPath $out){throw 'Never overwrite candidate or evidence'}
if(-not $assetReport.passed -or -not $assetReport.allOtherPayloadBytesUnchanged -or -not $assetReport.originalNativeCompressedRowsSelected){throw 'Independent narrow native asset preparation required'}
foreach($item in $assetReport.inputHashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Asset source changed: $($item.Name)"}}
$payload="$asset/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash -LiteralPath $payload).Hash -ne 'ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3'){throw 'Exact original-stream twelve-descriptor payload required'}
$priorInfo=Get-Content -LiteralPath "$prior/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $priorInfo.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Prior build source changed: $($item.Name)"}}
$installed="$repo/mkport.exe"
if((Get-FileHash -LiteralPath $installed).Hash -ne '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'){throw 'Historical installed executable changed'}
if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $installed}).Count){throw 'Installed emulator running; cannot stage compiler output'}
$current=@("$repo/src/mame/midway/midtunit.cpp","$repo/src/mame/midway/midtunit_m.cpp","$repo/src/mame/midway/midtunit.h",$installed)
$originalHashes=@{}
foreach($path in $current){$originalHashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$stagedDriver="$portRoot/audit_v3170_native_morph_shadow_source/midtunit.cpp"
$oldDriver=Get-Content -LiteralPath "$prior/input_sources/mame-mkp/src/mame/midway/midtunit.cpp" -Raw
$newDriver=Get-Content -LiteralPath $stagedDriver -Raw
$expected=$oldDriver.Replace('CRC(4a606b51) SHA1(36a54a06e295ea08f1ce9bda9bfbce6353731ca9)','CRC(a65205cf) SHA1(b8f9602b0c1a620df3f7e13bd7f659185cc40afa)').Replace("`r`n","`n").TrimEnd()
if($expected -cne $newDriver.Replace("`r`n","`n").TrimEnd()){throw 'Whole native driver must differ only in correct payload ROM metadata'}
$machine="$prior/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp"
$header="$prior/input_sources/mame-mkp/src/mame/midway/midtunit.h"
if((Get-FileHash -LiteralPath $machine).Hash -ne 'F509CC18D5C9CA4152508E52FEBA23B93A1B6C4085986E498F02C53E5BE7EABA'){throw 'Current isolated native machine implementation changed'}
New-Item -ItemType Directory -Path "$out/input_sources","$out/restoration_backups" | Out-Null
$resolvedOut=(Get-Item -LiteralPath $out).FullName
$resolvedRoot=(Get-Item -LiteralPath $portRoot).FullName
if(-not $resolvedOut.StartsWith($resolvedRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or (Get-Item -LiteralPath $out).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Unsafe candidate leaf'}
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
  Copy-Item -LiteralPath $stagedDriver -Destination $current[0] -Force
  Copy-Item -LiteralPath $machine -Destination $current[1] -Force
  Copy-Item -LiteralPath $header -Destination $current[2] -Force
  $tracked=@($payload,$stagedDriver,$machine,$header,"$asset/report.json","$prior/build-info.json",$PSCommandPath)
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
    & gmake.exe SUBTARGET=mkport PYTHON_EXECUTABLE=C:/Users/kando/AppData/Local/Programs/Python/Python314/python.exe MINGW64=C:/Strawberry/c PTR64=1 -j4 2>&1 |
      Out-File -LiteralPath "$out/build.log" -Encoding utf8
    $buildCode=$LASTEXITCODE;$ErrorActionPreference='Stop'
    if($buildCode -ne 0){throw "Native build failed: $buildCode"}
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $before[$path]){throw "Compiled input changed: $path"}}
    Copy-Item -LiteralPath $installed -Destination "$out/mkport_candidate.exe"
    New-Item -ItemType Directory -Path "$out/roms/mk2ks" | Out-Null
    Copy-Item -LiteralPath $payload -Destination "$out/roms/mk2ks/mk2ks.mdata"
    [ordered]@{name=$name;executable_sha256=(Get-FileHash -LiteralPath "$out/mkport_candidate.exe").Hash;
      payload_sha256=$before[$payload];input_hashes=$compiled;canonical_source_hashes_at_compile=$before;
      expected_guest_sha256='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7';
      prior_candidate='diagnostic_v2753_native_friendship_palette';game_data_changed=$true;metadata_only_source_rebuild=$true;
      assembly='Exactly twelve morph graphic/format descriptor fields select already-imported original compressed donor streams. Entire native machine code unchanged; no custom shadow, pixel/palette/pivot/floor/timer/ID/AI change.'} |
      ConvertTo-Json -Depth 5 | Out-File -LiteralPath "$out/build-info.json" -Encoding utf8
  }finally{Pop-Location}
}finally{
  $env:PATH=$savedPath
  foreach($path in $current){
    Copy-Item -LiteralPath $backups[$path] -Destination $path -Force
    if((Get-FileHash -LiteralPath $path).Hash -ne $originalHashes[$path]){throw "Exact actual user-file restoration failed: $path"}
  }
  [ordered]@{passed=$true;restored_actual_preexisting_files=$originalHashes;backup_files=$backups;public_build_promoted=$false} |
    ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/restoration.json" -Encoding utf8
}
Get-Content -LiteralPath "$out/build-info.json" -Raw | ConvertFrom-Json | Select-Object name,executable_sha256,payload_sha256,expected_guest_sha256 | ConvertTo-Json -Compress
