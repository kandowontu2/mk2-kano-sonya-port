param([ValidateSet(1,2)][int]$Side=1,[Parameter(Mandatory=$true)][string]$CaseName)
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned case name required'}
$out=Join-Path $root $CaseName;if(Test-Path -LiteralPath $out){throw 'Do not overwrite reference'}
$exe=(Resolve-Path -LiteralPath "$root/../hbmame/hbmame.exe").Path
$harness="$root/mk3_friendship_audio_reference_v770.lua"
$tracked=@($exe,$harness,$PSCommandPath,"$root/mk3_friendship_scene_reference_v758.lua","$root/mk3_finish_input_selection.lua")
$tracked+=Get-ChildItem -LiteralPath "$root/mk3" -File | ForEach-Object {$_.FullName}
$hashes=@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path $out | Out-Null
$hashes | ConvertTo-Json | Out-File -LiteralPath "$out/inputs_before.json" -Encoding utf8
$previous=$env:MK3_FRIEND_SIDE;Push-Location $root
try{
 $env:MK3_FRIEND_SIDE="$Side"
 & $exe mk3 -rompath "$root;$root/../mame0289/roms" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -samplerate 48000 -wavwrite "$out/original_mix.wav" -nothrottle -str 180 -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Executed input changed: $path"}}
 [ordered]@{exit_code=$code;side=$Side;assistance='opponent_health_only';scope='original Friendship command/sound oracle, not unassisted port gameplay';input_hashes=$hashes;mix_sha256=(Get-FileHash -LiteralPath "$out/original_mix.wav").Hash} | ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code"
}finally{Pop-Location;$env:MK3_FRIEND_SIDE=$previous}
