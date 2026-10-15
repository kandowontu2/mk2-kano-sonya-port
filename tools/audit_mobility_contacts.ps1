param([string]$OutputName='audit_v290_mobility_contact_final_inputs')
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
    $move=if($target -eq 'kano'){'ball'}else{'square'}
    $source=if($target -eq 'kano'){'sonya'}else{'kano'}
    $name="audit_v290_p2_ending_join_${move}_p$side"
    if($target -eq 'sonya' -and $side -eq 1){$name='audit_v290_observer_guard_join_square_p1'}
    $folder=Join-Path $root $name
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if(-not $original.passed -or $original.special_mode -ne 'mobility_contact' -or $original.contact_scenario -ne 'hit' -or $original.cheats_enabled -or $original.source_side -ne 2){throw "Original full case not accepted: $name"}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
    $archived=0
    foreach($item in $inputs.PSObject.Properties){
        if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1','.py'){
            $path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))
            if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Original launch script changed: $path"};$archived++
        }
    }
    python "$PSScriptRoot/verify_post_ending_restart.py" "$folder/run.log" --fighter $source --target $target --source-side 2 --new-side $side --special-mode mobility_contact |
        Out-File "$out/${name}_restart.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Latest full restart checker rejected: $name"}
    python "$PSScriptRoot/verify_mobility_contact.py" "$folder/run.log" --target $target --side $side |
        Out-File "$out/${name}_contact.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Latest native contact checker rejected: $name"}
    python "$PSScriptRoot/check_post_restart_assistance.py" "$folder/run.log" --fighter $source --source-side 2 |
        Out-File "$out/${name}_assistance.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Source assistance persisted: $name"}
    foreach($snap in 'css','highlight','match','complete'){
        if(-not (Test-Path -LiteralPath "$folder/snap/join_life_$snap.png")){throw "Missing joined snapshot: $snap"}
    }
    foreach($snap in '8','18','40','ready'){
        if(-not (Test-Path -LiteralPath "$folder/snap/mob_contact_$snap.png")){throw "Missing actual contact snapshot: $snap"}
    }
    $accepted+=[ordered]@{name=$name;source=$source;source_side=2;target=$target;side=$side;move=$move;
        original_result_passed=$true;latest_independent_checks_pass=$true;archived_launch_scripts_verified=$archived;
        log_sha256=(Get-FileHash "$folder/run.log").Hash;original_result_sha256=(Get-FileHash "$folder/result.json").Hash}
}}
$cold=@()
foreach($name in 'separation_ball_hit','root_square_hit','ball_block','ball_duck_miss','square_ground_block','square_far_miss'){
    $folder=Join-Path $root "audit_v290_$name"
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if(-not $original.observer_pass -or $original.exit_code -ne 0){throw "Original cold contact observer failed: $name"}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
    $archived=0
    foreach($item in $inputs.PSObject.Properties){
        if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1'){
            $path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))
            if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Original cold script changed: $path"};$archived++
        }
    }
    $target=if($name -match 'ball'){'kano'}else{'sonya'}
    python "$PSScriptRoot/verify_mobility_contact.py" "$folder/run.log" --target $target --side 1 |
        Out-File "$out/${name}_cold_contact.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Latest cold contact checker rejected: $name"}
    $cold+=[ordered]@{name="audit_v290_$name";scope='cold_joined_contact_not_post_ending';latest_independent_pass=$true;
        archived_launch_scripts_verified=$archived;log_sha256=(Get-FileHash "$folder/run.log").Hash}
}
$prior=Get-Content "$root/audit_v289_restart_lifecycle_final_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $prior.passed -or $prior.reference_tests_passed -ne 378){throw 'Previous authoritative checkpoint missing'}
$modules=@($prior.reference_modules)+@('test_mobility_contact')
$expected=378+(Select-String -LiteralPath "$PSScriptRoot/test_mobility_contact.py" -Pattern '^    def test_').Count
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
    "$PSScriptRoot/verify_restart_lifecycle.py","$PSScriptRoot/verify_mobility_contact.py","$PSScriptRoot/test_mobility_contact.py",
    "$root/mk2ks_post_ending_restart.lua","$root/mk2ks_restart_lifecycle.lua","$root/mk2ks_mobility_contact.lua",$exe,$payload,"$root/PLAY_MK2_KANO_SONYA.cmd")){$current[$path]=(Get-FileHash -LiteralPath $path).Hash}
[ordered]@{passed=$true;accepted_cases=$accepted;cold_contact_diagnoses=$cold;production_inputs_match_v277=$true;production_game_changed=$false;
    reference_tests_passed=$expected;reference_modules=$modules;current_inputs=$current;
    scope='full_health_assisted_P2_source_ending_pages_attract_fresh_601_field_P1_P2_CPU_match_native_challenger_join_601_contact_fields_full_ball_square_damage_poses_physics_recovery_and_subsequent_native_projectile';
    unassisted_full_CPU_tower_proven=$false;full_character_integration_complete=$false;
    retained_diagnostics='Cold cases are not ending proof; original traces without required pose/separation observations remain insufficient';
    remaining='Additional victim/CPU and projectile contact parity; P2-source blade/bicycle/other special contexts; broader unassisted CPU/continue/join; remaining finisher/victim fidelity and whole-game audio/visual QA; release ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Four P2 full ending/restart/join/contact cases, archived inputs, v277, $expected tests and root CMD verified"
