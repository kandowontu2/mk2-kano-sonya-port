param([Parameter(Mandatory=$true)][string]$CaseName,[ValidateSet('kano','sonya','liu_kang','kitana')][string]$Player='sonya',
    [ValidateSet(1,2)][int]$Side=1,[ValidateRange(30,180)][int]$Seconds=95,
    [string]$CandidateName='diagnostic_v1071_native_detached_arm_costume',
    [ValidateSet('cage','baraka','kitana','kung_lao','jax')][string]$Killer='baraka',
    [ValidateSet('ddff_lp','bbbb_hp','bbdb_hk','ffff_hp','ffdf_hk','ffdf_lk_release','bbdb_lk_release','fff_lk','fff_lp_release','bf_lp_release','bbbb_lp')][string]$Command='bbbb_hp',
    [ValidateRange(20,320)][int]$Gap=64)
$ErrorActionPreference='Stop';$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$' -or $CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Versioned evidence names required'}
$out=Join-Path $root $CaseName;$candidate=Join-Path $root $CandidateName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build input changed: $($item.Name)"}}
$exe="$candidate/mkport_candidate.exe";$payload="$candidate/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Matched build required'}
$tracked=@($exe,$payload,"$candidate/build-info.json",$PSCommandPath,"$root/mk2ks_stock_fatality_v1021.lua","$root/mk2ks_stock_fatality_display_v1021.lua","$root/mk2ks_native_split_trace_v1095.lua","$root/mk2/mk2-maincpu.bin","$root/tools/build_native_death_art_v900.py","$root/audit_v900_native_death_grounding_encoding/report.json","$root/tools/build_rolling_head_order_v1001.py","$root/audit_v1001_owned_rolling_head_encoding/report.json")
$tracked+=@(Get-ChildItem -LiteralPath "$root/art_native_rolling_heads_v998" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/art_native_torso_blood_v976" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/art_native_death_v893" -File | ForEach-Object {$_.FullName})
$tracked+=@($build.input_hashes.PSObject.Properties.Name)
$tracked+=@(Get-ChildItem -LiteralPath "$root/roms/mk2ks" -File | ForEach-Object {$_.FullName})
$tracked+=@(Get-ChildItem -LiteralPath "$root/artwork" -File | ForEach-Object {$_.FullName})
$tracked=@($tracked | Select-Object -Unique)
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes=@{};foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash;if([IO.Path]::GetExtension($file) -in '.lua','.ps1','.json'){Copy-Item -LiteralPath $file -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$saved=@{};Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try{
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$Player;$env:MK2KS_CAMPAIGN_SIDE="$Side"
    $env:MK2KS_STOCK_KILLER=$Killer;$env:MK2KS_STOCK_COMMAND=$Command;$env:MK2KS_STOCK_GAP="$Gap"
    $env:MK2KS_REPTILE_AUDIT_DIR=$out

    & $exe mk2ks -rompath "$candidate/roms;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat -inipath "$out" -video none -sound none -noautoframeskip -frameskip 0 -nothrottle -str $Seconds -snapsize 400x254 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script "$root/mk2ks_native_split_trace_v1095.lua","$root/mk2ks_native_split_trace_v1095.lua" 2>&1 | Out-File "$out/run.log" -Encoding utf8
    $code=$LASTEXITCODE
    foreach($file in $tracked){if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}}
    [ordered]@{exit_code=$code;candidate=$CandidateName;executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;player=$Player;victim_slot=$Side;winner_slot=(3-$Side);killer=$Killer;command=$Command;target_gap=$Gap;seconds=$Seconds;assistance='none';cheats_enabled=$false;passed=$false;scope='physical_input_stock_head_victim_diagnostic_independent_verification_pending';input_hashes=$hashes} | ConvertTo-Json -Depth 4 | Out-File "$out/result.json" -Encoding utf8
    "$CaseName terminal exit=$code (independent verification pending)"
}finally{
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($name in $saved.Keys){Set-Item -LiteralPath "Env:$name" -Value $saved[$name]}
}
