$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
$repo=Join-Path $portRoot 'mame-mkp'
$name='diagnostic_v4850_native_subzero_victim_offset'
$out=Join-Path $portRoot $name
$prior=Join-Path $portRoot 'diagnostic_v3836_native_mileena_rom_identity'
$priorInfo=Get-Content -LiteralPath "$prior/build-info.json" -Raw | ConvertFrom-Json
$guardPath="$portRoot/audit_v4846_native_subzero_offset_staged_source_checked/report.json"
$guard=Get-Content -LiteralPath $guardPath -Raw | ConvertFrom-Json
if(Test-Path -LiteralPath $out){throw 'Never overwrite an executed build leaf'}
if(-not $guard.passed -or $guard.compiledFixAccepted -or $guard.actualSourceFaultsRejected.Count -ne 6){throw 'Qualified source-only native table repair required'}
foreach($entry in $guard.inputHashes.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Guard input changed: $($entry.Name)"}
}
foreach($entry in $priorInfo.input_hashes.PSObject.Properties){
  if((Get-FileHash -LiteralPath $entry.Name).Hash -ne $entry.Value){throw "Actual3836 frozen input changed: $($entry.Name)"}
}
$payload="$prior/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash -LiteralPath $payload).Hash -ne '91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24'){throw 'Exact unchanged owned-art payload required'}
$installed="$repo/mkport.exe"
if((Get-FileHash -LiteralPath $installed).Hash -ne '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'){throw 'Historical installed executable changed'}
if(@(Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $installed -or $_.Name -eq 'gmake.exe'}).Count){throw 'Compiler/installed emulator in use'}
$staged=@{
  "$repo/src/mame/midway/midtunit.cpp"="$prior/input_sources/mame-mkp/src/mame/midway/midtunit.cpp"
  "$repo/src/mame/midway/midtunit.h"="$prior/input_sources/mame-mkp/src/mame/midway/midtunit.h"
  "$repo/src/mame/midway/midtunit_m.cpp"=$guard.stagedSource
}
$expected=@{
  'src/mame/midway/midtunit.cpp'='0094EAE7DC9D3AF85474F720A16054BCFA5DF654751E8DA9C3D105588E674363'
  'src/mame/midway/midtunit.h'='FC81021BA7CA0535C9BBCC94A87138DF5AA5FFD18D126827D2A5059A7E8CEE20'
  'src/mame/midway/midtunit_m.cpp'='BAF102148E740A1CC96A44320E51051938E3AE4EADE5B716CD6B6D2534B252A6'
  'src/devices/cpu/tms34010/tms34010.cpp'='87B5F2953B374D890CC97F041AA450D8E89DAC735C8299BF40F3E491E7E94AEF'
  'src/devices/cpu/tms34010/tms34010.h'='EDDC108BA2A50993FE118BCA8B9AF4A7F9DB9B8AF748B1B13577EBFFCCE7493A'
  'src/devices/cpu/tms34010/34010gfx.hxx'='060BEDA20F292AF57AB0048E62BC7D4A87788B01353BA6B36EFC2BAC4A80EC73'
  'src/devices/cpu/tms34010/34010ops.hxx'='772F372A89CBDA2D7F8E59E51540350F17EFF175B0006EEA1C69BB033D2EDB12'
  'src/frontend/mame/mame.cpp'='93E5793C85D17F7DCDCB15EC108A5884E478032373694BD644F2EDCA18B536D1'
  'src/mame/midway/midtunit_v.cpp'='8912181C8D7560BFD4974CECFEADD0532A9588A60D8D3FC399D58433EDB37611'
  'src/mame/midway/midtunit_v.h'='2DCF4BCC521F821888684BC7FA4608DFA8693D660498D0FAB7315B839F6B22EE'
  'src/mame/midway/mk2ks_native_picture.h'='762E5426027395A2ADBD51EEB152B778A06365F47CDFED2EBCC2669B7E5946CA'
  'src/frontend/mame/ui/slider.h'='C480D82DB8B2297D2C337A9FA97F078BF09FA5B48BFBBBFDA9092382192A2341'
  'src/mame/mame.lst'='30192916B3B63C9A98A5EA40D58F4760FC0B11CB4588C411CA1FCC3C020D3C40'
  'src/osd/modules/lib/osdlib.h'='E896B1839BC3750A7E8A1B4DA76B35618C196F9591F3361FEA9AB771D21B1CDF'
  'src/osd/modules/monitor/monitor_module.h'='94F95B46AB1FEC792C10722162D0DC4C8225C7908256665A1EA6B5A15A5E9D88'
}
foreach($relative in $expected.Keys){
  $path="$repo/$relative"
  $source=if($staged.ContainsKey($path)){$staged[$path]}else{$path}
  if((Get-FileHash -LiteralPath $source).Hash -ne $expected[$relative]){throw "Explicit reviewed native/platform source changed: $relative"}
}
$current=@($staged.Keys)+@($installed)
$originalHashes=@{};foreach($path in $current){$originalHashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path "$out/input_sources","$out/restoration_backups" | Out-Null
$resolvedOut=(Get-Item -LiteralPath $out).FullName
$resolvedRoot=(Get-Item -LiteralPath $portRoot).FullName
if(-not $resolvedOut.StartsWith($resolvedRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or ((Get-Item -LiteralPath $out).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Unsafe candidate leaf'}
& compact.exe /C /I /Q "/S:$resolvedOut" | Out-Null
if($LASTEXITCODE -ne 0){throw 'Evidence compression required'}
$backups=@{}
foreach($path in $current){
  $dest=Join-Path "$out/restoration_backups" ([IO.Path]::GetFileName($path))
  Copy-Item -LiteralPath $path -Destination $dest
  if((Get-FileHash -LiteralPath $dest).Hash -ne $originalHashes[$path]){throw 'Exact preexisting-file backup required'}
  $backups[$path]=$dest
}
$savedPath=$env:PATH
try{
  foreach($path in $staged.Keys){Copy-Item -LiteralPath $staged[$path] -Destination $path -Force}
  $compiled=@{};$canonical=@{}
  foreach($relative in $expected.Keys){
    $path="$repo/$relative";$actual=(Get-FileHash -LiteralPath $path).Hash
    if($actual -ne $expected[$relative]){throw "Staged native source changed: $relative"}
    $frozen=Join-Path "$out/input_sources/mame-mkp" $relative
    New-Item -ItemType Directory -Path (Split-Path $frozen -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $path -Destination $frozen
    $compiled[$frozen]=$actual;$canonical[$path]=$actual
  }
  foreach($entry in $priorInfo.input_hashes.PSObject.Properties){$compiled[$entry.Name]=$entry.Value}
  foreach($path in @($payload,$guardPath,"$prior/build-info.json",$PSCommandPath)){$compiled[$path]=(Get-FileHash -LiteralPath $path).Hash}
  Copy-Item -LiteralPath $PSCommandPath -Destination "$out/input_sources"
  Push-Location $repo
  try{
    $env:PATH='C:\Program Files\Git\usr\bin;C:\Users\kando\AppData\Local\Programs\Python\Python314;C:\Strawberry\c\bin;'+$savedPath
    Write-Output 'Building guarded native Sub-Zero offset table; public build unchanged.'
    $ErrorActionPreference='Continue'
    & gmake.exe SUBTARGET=mkport SOURCES=src/mame/midway/midtunit.cpp NOWERROR=1 REGENIE=1 PYTHON_EXECUTABLE=C:/Users/kando/AppData/Local/Programs/Python/Python314/python.exe MINGW64=C:/Strawberry/c PTR64=1 -j4 2>&1 |
      Out-File -LiteralPath "$out/build.log" -Encoding utf8
    $buildCode=$LASTEXITCODE;$ErrorActionPreference='Stop'
    if($buildCode -ne 0){throw "Native build failed: $buildCode"}
    foreach($path in $canonical.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $canonical[$path]){throw "Compiled canonical source changed: $path"}}
    foreach($path in $compiled.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $compiled[$path]){throw "Frozen native input changed: $path"}}
    Copy-Item -LiteralPath $installed -Destination "$out/mkport_candidate.exe"
    New-Item -ItemType Directory -Path "$out/roms/mk2ks" | Out-Null
    New-Item -ItemType HardLink -Path "$out/roms/mk2ks/mk2ks.mdata" -Target $payload | Out-Null
    [ordered]@{name=$name;executable_sha256=(Get-FileHash -LiteralPath "$out/mkport_candidate.exe").Hash;
      payload_sha256=(Get-FileHash -LiteralPath $payload).Hash;input_hashes=$compiled;canonical_source_hashes_at_compile=$canonical;
      expected_guest_sha256=$guard.expectedGuestSHA256;prior_candidate='diagnostic_v3836_native_mileena_rom_identity';
      game_data_changed=$false;initialized_native_table_changed=$true;initialized_guest_byte_delta=39;
      payload_hardlink_to_immutable_prior=$payload;public_build_promoted=$false;native_runtime_accepted=$false;full_port_accepted=$false;
      current_platform_compatibility_sources_reviewed=$true;source_selected_target='src/mame/midway/midtunit.cpp';
      assembly='Extend native0616 victim word-offset data for true17/18; retain all17 original ID-indexed words. No instruction/task/cache/identity runtime repair. Separate own shatter-body art remains incomplete.'} |
      ConvertTo-Json -Depth 6 | Out-File -LiteralPath "$out/build-info.json" -Encoding utf8
  }finally{Pop-Location}
}finally{
  $env:PATH=$savedPath
  foreach($path in $current){
    Copy-Item -LiteralPath $backups[$path] -Destination $path -Force
    if((Get-FileHash -LiteralPath $path).Hash -ne $originalHashes[$path]){throw "Exact preexisting-file restoration failed: $path"}
  }
  [ordered]@{passed=$true;restored_actual_preexisting_files=$originalHashes;backup_files=$backups;public_build_promoted=$false} |
    ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/restoration.json" -Encoding utf8
  $temporaryExe=(Get-Item -LiteralPath $backups[$installed]).FullName
  $expectedBackup=[IO.Path]::GetFullPath((Join-Path $resolvedOut 'restoration_backups/mkport.exe'))
  if($temporaryExe -cne $expectedBackup -or -not $temporaryExe.StartsWith($resolvedOut+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Unsafe transient backup cleanup target'}
  if((Get-FileHash -LiteralPath $installed).Hash -ne $originalHashes[$installed]){throw 'Installed file must be restored before cleanup'}
  Remove-Item -LiteralPath $temporaryExe
}
Get-Content -LiteralPath "$out/build-info.json" -Raw | ConvertFrom-Json |
  Select-Object name,executable_sha256,payload_sha256,expected_guest_sha256 | ConvertTo-Json -Compress
