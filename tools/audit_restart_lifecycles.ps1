param([string]$OutputName='audit_v289_restart_lifecycle_final_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned audit evidence'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite audit evidence'}
$build=Get-Content "$root/diagnostic_v277_native_battle_photos/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Production input changed: $($item.Name)"}}
$exe="$root/diagnostic_v277_native_battle_photos/mkport_candidate.exe"
$payload="$root/diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Playable build changed'}
New-Item -ItemType Directory -Path $out | Out-Null
$accepted=@()
foreach($target in 'kano','sonya'){foreach($side in 1,2){
    $move=if($target -eq 'kano'){'blade'}else{'bicycle'}
    $source=if($target -eq 'kano'){'sonya'}else{'kano'}
    $prefix=if($side -eq 1){'ending'}else{'slot_reset'}
    $name="audit_v289_${prefix}_join_${move}_p$side"
    $folder=Join-Path $root $name
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if(-not $original.passed -or $original.special_mode -ne 'lifecycle' -or $original.cheats_enabled -or $original.source_side -ne 1){throw "Original full ending lifecycle case not accepted: $name"}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
    $archived=0
    foreach($item in $inputs.PSObject.Properties){
        if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1','.py'){
            $path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))
            if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Original launch script changed: $path"}
            $archived++
        }
    }
    python "$PSScriptRoot/verify_post_ending_restart.py" "$folder/run.log" --fighter $source --target $target --source-side 1 --new-side $side --special-mode lifecycle |
        Out-File "$out/${name}_restart.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Latest full restart checker rejected: $name"}
    python "$PSScriptRoot/verify_restart_lifecycle.py" "$folder/run.log" --target $target --side $side |
        Out-File "$out/${name}_lifecycle.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Latest full native join/move checker rejected: $name"}
    python "$PSScriptRoot/check_post_restart_assistance.py" "$folder/run.log" --fighter $source --source-side 1 |
        Out-File "$out/${name}_assistance.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Source tower assistance persisted: $name"}
    foreach($snap in 'css','highlight','match','complete'){
        if(-not (Test-Path -LiteralPath "$folder/snap/join_life_$snap.png")){throw "Missing actual joined snapshot: $snap"}
    }
    $accepted+=[ordered]@{name=$name;source=$source;source_side=1;target=$target;side=$side;move=$move;
        original_result_passed=$true;latest_independent_checks_pass=$true;archived_launch_scripts_verified=$archived;
        log_sha256=(Get-FileHash "$folder/run.log").Hash;original_result_sha256=(Get-FileHash "$folder/result.json").Hash}
}}
$cold=@()
foreach($item in @(@('blade',2,'sonya'),@('bicycle',1,'kano'))){
    $move=$item[0];$side=$item[1];$victim=$item[2]
    $name="audit_v289_cold_regression_${move}_p${side}_${victim}"
    $folder=Join-Path $root $name
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if(-not $original.observer_passed -or $original.exit_code -ne 0){throw "Original cold default-mode regression failed: $name"}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
    $archived=0
    foreach($entry in $inputs.PSObject.Properties){
        if([IO.Path]::GetExtension($entry.Name) -in '.lua','.ps1'){
            $path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($entry.Name))
            if((Get-FileHash -LiteralPath $path).Hash -ne $entry.Value){throw "Original cold launch script changed: $path"}
            $archived++
        }
    }
    python "$PSScriptRoot/verify_current_lifecycle.py" "$folder/run.log" --move $move --side $side --victim $victim |
        Out-File "$out/${name}_independent.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Actual default-mode trace rejected: $name"}
    $cold+=[ordered]@{name=$name;latest_independent_pass=$true;archived_launch_scripts_verified=$archived;
        scope='cold_default_lifecycle_mode_regression_not_post_ending';log_sha256=(Get-FileHash "$folder/run.log").Hash}
}
$prior=Get-Content "$root/audit_v288_lifecycle_final_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $prior.passed -or $prior.reference_tests_passed -ne 345){throw 'Previous authoritative checkpoint missing'}
$modules=@($prior.reference_modules)+@('test_restart_lifecycle')
$added=(Select-String -LiteralPath "$PSScriptRoot/test_restart_lifecycle.py" -Pattern '^    def test_').Count
$expected=345+$added
Push-Location $PSScriptRoot
try {
    python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Reference suite failed'}
} finally {Pop-Location}
$log=Get-Content "$out/reference_tests.log" -Raw
if($log -notmatch "Ran $expected tests" -or $log -notmatch '(?m)^OK\s*$'){throw 'Incomplete reference suite'}
& "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File "$out/launcher_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Actual root CMD ROM check failed'}
$current=[ordered]@{}
foreach($path in @($PSCommandPath,"$PSScriptRoot/run_post_ending_restart.ps1","$PSScriptRoot/verify_post_ending_restart.py",
    "$PSScriptRoot/verify_restart_lifecycle.py","$PSScriptRoot/verify_current_lifecycle.py","$PSScriptRoot/test_restart_lifecycle.py",
    "$root/mk2ks_post_ending_restart.lua","$root/mk2ks_restart_lifecycle.lua","$root/mk2ks_lifecycle_trace.lua",
    "$root/mk2ks_blade_lifecycle_test.lua","$root/mk2ks_bicycle_lifecycle_test.lua",$exe,$payload,"$root/PLAY_MK2_KANO_SONYA.cmd")){$current[$path]=(Get-FileHash -LiteralPath $path).Hash}
[ordered]@{passed=$true;accepted_cases=$accepted;cold_default_mode_regressions=$cold;production_inputs_match_v277=$true;production_game_changed=$false;
    reference_tests_passed=$expected;reference_modules=$modules;current_inputs=$current;
    scope='full_health_assisted_P1_source_ending_pages_attract_fresh_601_field_P1_P2_CPU_match_native_challenger_join_full_blade_bicycle_KO_next_round_both_target_slots';
    unassisted_full_CPU_tower_proven=$false;full_character_integration_complete=$false;
    retained_diagnostics='Original cold round-construction and P2 slot-reset-assumption failures unchanged; corrected cold probes are not post-ending proof';
    remaining='P2 source ending special contexts; additional victims/CPU and other full move parity; broader unassisted CPU/continue/join; whole-game audio/visual QA; release ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Four full ending/restart/join/move cases, archived inputs, v277, $expected tests and root CMD verified"
