param([string]$CaseName='audit_v684_pit_guest_rom_integrity')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Never overwrite evidence'}
$old='diagnostic_v635_native_shadow_rows';$new='diagnostic_v680_native_pit_initial_cache'
$oldExe='4CC606CFF6FC5747139948424DC38C9D9C932D6F41D45C372CCDB52B5C5C1F90'
$newExe='AD98FE42383F776BBD49BA4298EFD1F9F021FD2988C6B0A3956EE64316B44E82'
$payloadSha='1367D5A0D42C661CF555F42231A20A650C28E107AB9C80BD821C0BEA7EB4D5EF'
$hashes=@{};$resolutions=@{}
foreach($name in @($old,$new)){
 $build=Get-Content "$root/$name/build-info.json" -Raw | ConvertFrom-Json
 if($build.name -ne $name -or $build.executable_sha256 -ne $(if($name -eq $old){$oldExe}else{$newExe}) -or $build.payload_sha256 -ne $payloadSha){throw 'Exact known build required'}
 foreach($item in $build.input_hashes.PSObject.Properties){
  $actual=$item.Name
  if($name -eq $old -and [IO.Path]::GetFileName($actual) -eq 'midtunit_m.cpp'){
   if($item.Value -ne '2133D3D46E3DAFA3F44D0741962997595ADF4EB141A2EAB887EB7675A369707E'){throw 'Unknown old driver'}
   $actual="$root/audit_v680_pre_pit_initial_cache/sources/midtunit_m.cpp"
   $resolutions[$item.Name]=$actual
  }
  if((Get-FileHash -LiteralPath $actual).Hash -ne $item.Value){throw "Input changed: $actual"}
  $hashes[$actual]=$item.Value
 }
 foreach($file in @("$root/$name/mkport_candidate.exe","$root/$name/roms/mk2ks/mk2ks.mdata","$root/$name/build-info.json")){
  $hashes[$file]=(Get-FileHash -LiteralPath $file).Hash
 }
 if($hashes["$root/$name/mkport_candidate.exe"] -ne $build.executable_sha256 -or $hashes["$root/$name/roms/mk2ks/mk2ks.mdata"] -ne $payloadSha){throw 'Actual matched binaries required'}
}
foreach($file in @($PSCommandPath,"$root/mk2ks_pit_rom_integrity_v680.lua")+@(Get-ChildItem "$root/roms/mk2ks" -File | Select-Object -ExpandProperty FullName)){
 $hashes[$file]=(Get-FileHash -LiteralPath $file).Hash
}
New-Item -ItemType Directory -Path $out | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($name in @($old,$new)){
  $caseOut="$out/$name";New-Item -ItemType Directory -Path $caseOut | Out-Null
  $env:MK2KS_ROM_COMPARE_OUT=$caseOut
  & "$root/$name/mkport_candidate.exe" mk2ks -rompath "$root/$name/roms;$root/roms" -nocheat -skip_gameinfo -inipath "$caseOut" -video none -sound none -nothrottle -str 2 -cfg_directory "$caseOut/cfg" -nvram_directory "$caseOut/nvram" -autoboot_script "$root/mk2ks_pit_rom_integrity_v680.lua" 2>&1 | Out-File "$caseOut/run.log" -Encoding utf8
  if($LASTEXITCODE -ne 0){throw "Native ROM capture failed: $name"}
 }
 foreach($item in $hashes.GetEnumerator()){if((Get-FileHash -LiteralPath $item.Key).Hash -ne $item.Value){throw "Input changed during capture: $($item.Key)"}}
 [ordered]@{exit_code=0;assistance='none';old=$old;current=$new;source_resolutions=$resolutions;input_hashes=$hashes;scope='actual_complete_native_guest_ROM_delta_capture_not_gameplay_acceptance'} | ConvertTo-Json -Depth 5 | Out-File "$out/result.json" -Encoding utf8
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($name in $saved.Keys){Set-Item "Env:$name" -Value $saved[$name]}
}
