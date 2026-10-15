param([string]$OutputName='audit_v287_followup_final_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned evidence directory'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite audit evidence'}
$build=Get-Content "$root/diagnostic_v277_native_battle_photos/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Production input changed: $($item.Name)"}
}
$exe="$root/diagnostic_v277_native_battle_photos/mkport_candidate.exe"
$payload="$root/diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Playable build differs from v277'}
New-Item -ItemType Directory -Path $out | Out-Null
$accepted=@()
foreach($side in 1,2){
    $case="audit_v287_fractional_followup_p${side}_kano_sonya"
    $source=if($side -eq 1){'sonya'}else{'kano'}
    $folder=Join-Path $root $case
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if(-not $original.passed -or -not $original.air_followup){throw "Original follow-up case not accepted: $case"}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
    $archived=0
    foreach($item in $inputs.PSObject.Properties){
        if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1','.py'){
            $saved=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))
            if((Get-FileHash -LiteralPath $saved).Hash -ne $item.Value){throw "Archived launch input changed: $saved"}
            $archived++
        }
    }
    & python "$PSScriptRoot/verify_post_ending_restart.py" "$folder/run.log" --fighter $source --target kano --source-side 1 --new-side $side --special-mode airthrow --air-followup |
        Out-File "$out/${case}_restart.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Latest full restart/follow-up checker rejected $case"}
    & python "$PSScriptRoot/verify_restart_airthrow.py" "$folder/run.log" --side $side --followup |
        Out-File "$out/${case}_followup.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Latest joined follow-up checker rejected $case"}
    & python "$PSScriptRoot/check_post_restart_assistance.py" "$folder/run.log" --fighter $source --source-side 1 |
        Out-File "$out/${case}_assistance.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Tower assistance persisted in $case"}
    foreach($age in 8,64,120,144,160){
        if(-not (Test-Path -LiteralPath "$folder/snap/air_join_follow_$age.png")){throw "Missing actual follow-up snapshot $age"}
    }
    $accepted+=[ordered]@{case=$case;source=$source;source_side=1;target='kano';side=$side;victim='sonya';
        log_sha256=(Get-FileHash "$folder/run.log").Hash;original_result_sha256=(Get-FileHash "$folder/result.json").Hash;
        before_launch_archived_scripts_verified=$archived;latest_independent_checks_pass=$true}
}
$modules=@(Select-String -LiteralPath "$root/audit_v286_clean_airthrow_inputs/reference_tests.log" -Pattern '\((test_[A-Za-z0-9_]+)\.' -AllMatches |
    ForEach-Object {$_.Matches} | ForEach-Object {$_.Groups[1].Value} | Sort-Object -Unique)
$modules+='test_restart_airthrow_followup'
$newTests=(Select-String -LiteralPath "$PSScriptRoot/test_restart_airthrow_followup.py" -Pattern '^    def test_').Count
$expected=297+$newTests
Push-Location $PSScriptRoot
try {
    python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Full reference suite failed'}
} finally {Pop-Location}
$unitLog=Get-Content "$out/reference_tests.log" -Raw
if($unitLog -notmatch "Ran $expected tests" -or $unitLog -notmatch '(?m)^OK\s*$'){throw "Expected complete $expected-test suite"}
& "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File "$out/launcher_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Actual root CMD ROM verification failed'}
$hashes=[ordered]@{}
foreach($path in @($PSCommandPath,"$root/mk2ks_restart_airthrow.lua","$root/mk2ks_post_ending_restart.lua",
    "$PSScriptRoot/run_post_ending_restart.ps1","$PSScriptRoot/verify_restart_airthrow.py","$PSScriptRoot/verify_post_ending_restart.py",
    "$PSScriptRoot/test_restart_airthrow_followup.py","$root/mk2ks_join_airthrow_probe.lua","$PSScriptRoot/run_join_airthrow_probe.ps1",
    $exe,$payload,"$root/PLAY_MK2_KANO_SONYA.cmd")){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
[ordered]@{passed=$true;accepted_cases=$accepted;production_inputs_match_v277=$true;production_game_changed=$false;
    reference_tests_passed=$expected;reference_modules=$modules;reference_log_sha256=(Get-FileHash "$out/reference_tests.log").Hash;
    current_inputs=$hashes;unassisted_full_cpu_tower_proven=$false;full_character_integration_complete=$false;
    scope='full_health_assisted_source_endings_fresh_CPU_match_native_join_airthrow_then_both_Kano_Sonya_controllers_walk_exact_fixed_point_jump_high_punch_native_11_damage_block_and_clean_recovery_both_slots';
    retained_failures='Initial full pilots remain failed: reporting argument handling and integer-only jump assumptions were corrected, not retroactively accepted';
    remaining='naturally jumping CPU and edge airthrow; remaining full move choreography/damage parity; broader unassisted CPU and continue/join; whole-game audio/visual QA; updated release ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Both normal-input follow-up cases, archived inputs, v277, $expected tests and root CMD verified"
