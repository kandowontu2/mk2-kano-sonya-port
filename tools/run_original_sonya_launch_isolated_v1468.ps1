param([string]$Command='baseline')
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($Command -notmatch '^(baseline|021[2-6]|02d[0-4]|089[8-9a-c])$'){throw 'Original Sonya square/bicycle launch sound only'}
$out=Join-Path $root "audit_v1468_original_sonya_launch_isolated_$Command"
if(Test-Path -LiteralPath $out){throw 'Do not overwrite isolated audio'}
$exe=(Resolve-Path -LiteralPath "$root/../hbmame/hbmame.exe").Path
$harness="$root/mk3_friendship_isolated_time_v772.lua"
$tracked=@($exe,$harness,"$root/mk3_isolated_sound_probe.lua",$PSCommandPath)
$tracked+=Get-ChildItem -LiteralPath "$root/mk3" -File | ForEach-Object {$_.FullName}
$hashes=@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path $out | Out-Null
$hashes | ConvertTo-Json | Out-File -LiteralPath "$out/inputs_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -like 'MK3_PROBE_*'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object {$_.Name -like 'MK3_PROBE_*'} | Remove-Item
 if($Command -ne 'baseline'){$env:MK3_PROBE_SOUND_CMD=$Command}
 $env:MK3_PROBE_SOUND_U8='1';$env:MK3_PROBE_SOUND_GAP_US='25';$env:MK3_PROBE_TRACE_PORT='1'
 & $exe mk3 -rompath "$root;$root/../mame0289/roms" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -samplerate 48000 -wavwrite "$out/native_mix.wav" -nothrottle -str 30 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Executed input changed: $path"}}
 [ordered]@{exit_code=$code;command=$Command;assistance='DCS_sound_port_only';guest_ram_writes=0;scope='isolated original audio/channel/timing oracle, not gameplay';input_hashes=$hashes;mix_sha256=(Get-FileHash -LiteralPath "$out/native_mix.wav").Hash} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
 "$Command terminal exit=$code"
}finally{
 Pop-Location;Get-ChildItem Env: | Where-Object {$_.Name -like 'MK3_PROBE_*'} | Remove-Item
 foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
