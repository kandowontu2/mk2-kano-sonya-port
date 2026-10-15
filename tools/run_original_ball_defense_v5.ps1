param([Parameter(Mandatory=$true)][string]$CaseName,
 [ValidateSet('ground','duck','block')][string]$Scenario,
 [ValidateSet('liu_kang','sub_zero')][string]$Victim,
 [ValidateRange(3960,4020)][int]$DuckStart=4000)
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence name required'}
$out=Join-Path $root $CaseName;if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$exe=(Resolve-Path -LiteralPath "$root/../mame0289/mame.exe").Path
$harness="$root/mk3_cannonball_defense_reference_v4.lua"
$tracked=@($exe,$harness,$PSCommandPath)+@(Get-ChildItem -LiteralPath "$root/mk3" -File | ForEach-Object {$_.FullName})
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
Copy-Item -LiteralPath $harness,$PSCommandPath -Destination "$out/input_sources"
$saved=@{};Get-ChildItem Env: | Where-Object Name -Match '^MK3_' | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
 Get-ChildItem Env: | Where-Object Name -Match '^MK3_' | Remove-Item
 $env:MK3_BALL_TARGET=$Scenario;$env:MK3_BALL_VICTIM=$Victim;$env:MK3_BALL_DUCK_START="$DuckStart"
 & $exe mk3 -rompath "$root;$root/../mame0289/roms" -verifyroms 2>&1 | Out-File "$out/verifyroms.log" -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Original ROM verification failed'}
 & $exe mk3 -rompath "$root;$root/../mame0289/roms" -nocheat -skip_gameinfo -video none -sound none -nothrottle -str 85 -inipath "$out" -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -snapsize 400x254 -autoboot_script $harness 2>&1 | Out-File "$out/run.log" -Encoding utf8
 $code=$LASTEXITCODE
 foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Reference changed: $file"}}
 [ordered]@{exit_code=$code;scenario=$Scenario;victim=$Victim;duck_start=$DuckStart;game='mk3';cheats=$false;assistance='none';passed=$false;scope='original_ball_defense_diagnostic_pending';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
 "$CaseName terminal exit=$code (independent verification pending)"
}finally{
 Pop-Location
 Get-ChildItem Env: | Where-Object Name -Match '^MK3_' | Remove-Item
 foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
