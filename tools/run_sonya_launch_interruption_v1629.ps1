param([Parameter(Mandatory=$true)][string]$CaseName)
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned case name required'}
$candidate=Join-Path $root 'diagnostic_v1597_native_ground_throw';$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$build=Get-Content -LiteralPath "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build source changed: $($item.Name)"}}
$exe="$candidate/mkport_candidate.exe";$payload="$candidate/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash -LiteralPath $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash -LiteralPath $payload).Hash -ne $build.payload_sha256){throw 'Matched build required'}
$tracked=@($exe,$payload,"$candidate/build-info.json",$PSCommandPath,"$root/mk2ks_human_special_matrix_v3.lua","$root/mk2ks_human_special_audio_v1397.lua","$root/mk2ks_native_grab_audio_v1412.lua","$root/mk2ks_launch_channels_v1483.lua","$root/mk2ks_launch_interruption_v1629.lua")
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
foreach($dir in @('artwork','roms/mk2ks','samples/mk2ks')){$tracked+=@(Get-ChildItem -LiteralPath (Join-Path $root $dir) -File | ForEach-Object {$_.FullName})}
$tracked=@($tracked | Select-Object -Unique)
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File -LiteralPath "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 $env:MK2KS_HUMAN_SPECIAL_MOVE='square';$env:MK2KS_HUMAN_SPECIAL_SIDE='2';$env:MK2KS_HUMAN_SPECIAL_AIR='0';$env:MK2KS_HUMAN_SPECIAL_VICTIM='sub_zero';$env:MK2KS_AUDIO_OUTPUT=$out
 & $exe mk2ks -rompath "$candidate/roms;$root/roms" -samplepath "$root/samples" -artpath "$root/artwork" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -samplerate 48000 -wavwrite "$out/game_mix.wav" -noautoframeskip -frameskip 0 -nothrottle -str 65 -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_launch_interruption_v1629.lua" 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}}
 [ordered]@{exit_code=$code;candidate=$build.name;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;move='square';side=2;air=$false;victim='sub_zero';cheats_enabled=$false;assistance='none';passed=$false;scope='P2_native_launch_interruption_diagnostic_pending';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code (independent verification pending)"
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
 foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
