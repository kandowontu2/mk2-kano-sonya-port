param([Parameter(Mandatory=$true)][string]$CaseName,
 [ValidateSet('choke','leg','bicycle','square')][string]$Family)
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned case name required'}
$out=Join-Path $root $CaseName;if(Test-Path -LiteralPath $out){throw 'Never overwrite evidence'}
$exe=Join-Path $root 'mame-mkp/mkwport.exe'
$harness=Join-Path $root 'mk3_special_audio_reference_v1470.lua'
$tracked=@($exe,$harness,$PSCommandPath,"$root/mk3_choke_reference_v1406.lua","$root/mk3_leggrab_reference_v1406.lua","$root/mk3_bicycle_reference_v1406.lua","$root/mk3_choke_reference.lua","$root/mk3_leggrab_reference.lua","$root/mk3_bicycle_reference.lua","$root/mk3.zip","$root/mk3_square_reference.lua")
$tracked+=Get-ChildItem -LiteralPath "$root/mk3" -File | ForEach-Object {$_.FullName}
$tracked+=Get-ChildItem -LiteralPath "$root/roms" -File | Where-Object {$_.Name -eq 'mk3.zip'} | ForEach-Object {$_.FullName}
$hashes=@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
foreach($path in $tracked){if([IO.Path]::GetExtension($path) -in '.lua','.ps1'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK3_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK3_)'} | Remove-Item
 $env:MK3_AUDIO_FAMILY=$Family
 $env:MK3_CHOKE_TARGET='near';$env:MK3_CHOKE_VICTIM='sonya';$env:MK3_CHOKE_SIDE='1'
 $env:MK3_LEG_TARGET='near';$env:MK3_LEG_VICTIM='kano'
 $env:MK3_BICYCLE_TARGET='near'
 & $exe mk3 -rompath "$root/roms;$root" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -samplerate 48000 -wavwrite "$out/original_mix.wav" -noautoframeskip -frameskip 0 -nothrottle -str 100 -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $harness 2>&1 | Out-File "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Executed input changed: $path"}}
 [ordered]@{exit_code=$code;family=$Family;assistance='none';writes=0;scope='original_MK3_real_input_sound_reference_not_port_acceptance';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code"
}finally {
 Pop-Location
 Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK3_)'} | Remove-Item
 foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
