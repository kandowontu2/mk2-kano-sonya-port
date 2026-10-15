param([string]$OutputName='audit_v285_pair_final_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned evidence directory'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite audit evidence'}
$cases=@(
    @{folder='audit_v285_cross_slot_pair_p1_kano';source='sonya';target='kano';source_side=2;side=1},
    @{folder='audit_v285_walking_recovery_p1_sonya';source='kano';target='sonya';source_side=1;side=1},
    @{folder='audit_v285_native_pair_p2_kano';source='sonya';target='kano';source_side=2;side=2},
    @{folder='audit_v285_native_pair_p2_sonya';source='kano';target='sonya';source_side=2;side=2})
$build=Get-Content "$root/diagnostic_v277_native_battle_photos/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Production input changed: $($item.Name)"}
}
$exe="$root/diagnostic_v277_native_battle_photos/mkport_candidate.exe"
$payload="$root/diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Playable build differs from v277'}
New-Item -ItemType Directory -Path $out | Out-Null
$accepted=@()
foreach($case in $cases){
    $folder=Join-Path $root $case.folder
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if(-not $original.passed){throw "Original case was not accepted: $($case.folder)"}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
    $archiveCount=0
    foreach($item in $inputs.PSObject.Properties){
        if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1','.py'){
            $saved=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))
            if((Get-FileHash -LiteralPath $saved).Hash -ne $item.Value){throw "Archived input changed: $saved"}
            $archiveCount++
        }
    }
    & python "$PSScriptRoot/verify_post_ending_restart.py" "$folder/run.log" --fighter $case.source --target $case.target `
        --source-side $case.source_side --new-side $case.side --special-mode pair |
        Out-File "$out/$($case.folder)_restart.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Latest source/restart verifier rejected $($case.folder)"}
    & python "$PSScriptRoot/verify_restart_pair.py" "$folder/run.log" --target $case.target --side $case.side |
        Out-File "$out/$($case.folder)_pair.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Latest complete-pair verifier rejected $($case.folder)"}
    & python "$PSScriptRoot/check_post_restart_assistance.py" "$folder/run.log" --fighter $case.source --source-side $case.source_side |
        Out-File "$out/$($case.folder)_assistance.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Health assistance persisted in $($case.folder)"}
    $accepted += [ordered]@{case=$case.folder;source=$case.source;source_side=$case.source_side;target=$case.target;side=$case.side;
        log_sha256=(Get-FileHash "$folder/run.log").Hash;original_result_sha256=(Get-FileHash "$folder/result.json").Hash;
        before_launch_archived_scripts_verified=$archiveCount;latest_independent_checks_pass=$true}
}
$modules=@(Select-String -LiteralPath "$root/audit_v284_cleanup_confirmed_inputs/reference_tests.log" -Pattern '\((test_[A-Za-z0-9_]+)\.' -AllMatches |
    ForEach-Object {$_.Matches} | ForEach-Object {$_.Groups[1].Value} | Sort-Object -Unique)
$modules+='test_restart_pair'
Push-Location $PSScriptRoot
try {
    python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Full reference suite failed'}
} finally {Pop-Location}
$unitLog=Get-Content "$out/reference_tests.log" -Raw
if($unitLog -notmatch 'Ran 271 tests' -or $unitLog -notmatch '(?m)^OK\s*$'){throw 'Expected complete 271-test suite'}
& "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File "$out/launcher_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Actual root launcher ROM verification failed'}
$hashes=[ordered]@{}
foreach($path in @($PSCommandPath,"$root/mk2ks_restart_pair.lua","$root/mk2ks_post_ending_restart.lua",
    "$PSScriptRoot/run_post_ending_restart.ps1","$PSScriptRoot/verify_restart_pair.py","$PSScriptRoot/verify_post_ending_restart.py",
    "$PSScriptRoot/test_restart_pair.py","$root/mk2ks_close_pair_probe.lua","$PSScriptRoot/run_close_pair_probe.ps1",
    $exe,$payload,"$root/PLAY_MK2_KANO_SONYA.cmd")){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
[ordered]@{passed=$true;accepted_cases=$accepted;production_inputs_match_v277=$true;production_game_changed=$false;
    reference_tests_passed=271;reference_modules=$modules;reference_log_sha256=(Get-FileHash "$out/reference_tests.log").Hash;
    current_inputs=$hashes;unassisted_full_cpu_tower_proven=$false;full_character_integration_complete=$false;
    scope='complete_native_close_pair_poses_exact_damage_release_and_both_recoveries_on_both_slots_after_full_health_assisted_source_endings_then_601_input_only_fields';
    retained_failures='Original approach/continuous/P1 cases remain red; P1 Kano versus Baraka is a real CPU interruption/defeat, not accepted as a complete grab';
    remaining='air throws after restart; broader unassisted CPU gameplay and continue/join; remaining full move choreography/damage parity; whole-game audio/visual QA; updated release ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
'Four full close-pair restart cases, archived inputs, current v277, 271 tests and root CMD verified'
