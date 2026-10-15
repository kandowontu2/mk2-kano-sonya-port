param([ValidateSet(1,2)][int]$Side=1,[string]$CaseName='audit_v744_original_friendship_kano')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned name required'}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Do not overwrite reference'}
$exe=(Resolve-Path -LiteralPath "$root/../hbmame/hbmame.exe").Path
$harness="$root/mk3_friendship_scene_reference_v744.lua"
$hashes=@{}
foreach($path in @($exe,$harness,$PSCommandPath,"$root/mk3_finish_input_selection.lua","$root/mk3/mk3-maincpu.bin")){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
New-Item -ItemType Directory -Path $out | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/inputs_before.json" -Encoding utf8
Copy-Item -LiteralPath $harness,$PSCommandPath,"$root/mk3_finish_input_selection.lua" -Destination $out
$previous=$env:MK3_FRIEND_SIDE
Push-Location $root
try{
 $env:MK3_FRIEND_SIDE="$Side"
 & $exe mk3 -rompath "$root;$root/../mame0289/roms" -skip_gameinfo -nocheat -video none -sound none -nothrottle -str 180 -snapsize 400x300 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $harness 2>&1 | Out-File "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($path in $hashes.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Executed input changed: $path"}}
 [ordered]@{exit_code=$code;winner_side=$Side;assistance='opponent_health_only';scope='original command/scene observation not port acceptance';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code"
}finally{Pop-Location;$env:MK3_FRIEND_SIDE=$previous}
