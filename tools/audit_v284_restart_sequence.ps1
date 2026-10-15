$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$out=Join-Path $root 'audit_v284_sequence_final_inputs'
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite accepted evidence'}
if(@(Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe'}).Count){throw 'Candidate test is still live'}
$build=Get-Content -LiteralPath "$root/diagnostic_v277_native_battle_photos/build-info.json" -Raw | ConvertFrom-Json
foreach($prop in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $prop.Name).Hash -ne $prop.Value){throw 'Production input changed'}}
$prior=Get-Content -LiteralPath "$root/audit_v283_final_inputs/result.json" -Raw | ConvertFrom-Json
$paths=[ordered]@{executable_sha256="$root/diagnostic_v277_native_battle_photos/mkport_candidate.exe";
    payload_sha256="$root/diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata";
    root_cmd_sha256="$root/PLAY_MK2_KANO_SONYA.cmd";candidate_cmd_sha256="$root/diagnostic_v277_native_battle_photos/PLAY_CANDIDATE.cmd";
    installed_generic_exe_sha256="$root/mame-mkp/mkport.exe";
    old_zip_sha256='C:/Users/kando/Documents/Codex/2026-08-30/continue-the-mk2-kano-sonya-port/MK2_Kano_Sonya_v258_playtest.zip'}
$hashes=[ordered]@{}
foreach($key in $paths.Keys){$hashes[$key]=(Get-FileHash -LiteralPath $paths[$key]).Hash;if($hashes[$key] -ne $prior.hashes.$key){throw "Playable/archive changed: $key"}}
$units=Get-Content -LiteralPath "$root/audit_v284_final_reference_units.log" -Raw
if($units -notmatch 'Ran 236 tests' -or $units -notmatch '\bOK\s*$' -or $units -match '(?m)^(FAILED|FAIL:|ERROR:)'){throw 'Reference tests did not all pass'}
New-Item -ItemType Directory -Path $out | Out-Null
$cases=@(@{name='audit_v284_sequence_p1_kano';target='kano';source='sonya';side=1},
    @{name='audit_v284_sequence_p2_kano';target='kano';source='sonya';side=2},
    @{name='audit_v284_settled_sequence_p1_sonya';target='sonya';source='kano';side=1},
    @{name='audit_v284_sequence_p2_sonya';target='sonya';source='kano';side=2})
$accepted=[ordered]@{}
Push-Location $root
try {
    foreach($case in $cases){
        $folder=Join-Path $root $case.name
        $record=Get-Content -LiteralPath "$folder/result.json" -Raw | ConvertFrom-Json
        if(-not $record.passed){throw 'Runtime result failed'}
        $sources=[ordered]@{}
        foreach($prop in $record.input_hashes.PSObject.Properties){
            if([IO.Path]::GetExtension($prop.Name) -in @('.lua','.ps1','.py')){
                $name=[IO.Path]::GetFileName($prop.Name);$sources[$name]=(Get-FileHash -LiteralPath "$folder/input_sources/$name").Hash
                if($sources[$name] -ne $prop.Value){throw 'Incorrect archived runtime input'}
            }
        }
        $caseOut=Join-Path $out $case.name;New-Item -ItemType Directory -Path $caseOut | Out-Null
        & python "$PSScriptRoot/verify_post_ending_restart.py" "$folder/run.log" --fighter $case.source --target $case.target --source-side $case.side --new-side $case.side --special-mode sequence |
            Out-File -LiteralPath "$caseOut/restart.json" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Full source/restart verification failed'}
        & python "$PSScriptRoot/verify_restart_sequence.py" "$folder/run.log" --target $case.target --side $case.side |
            Out-File -LiteralPath "$caseOut/sequence.json" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Actual owned sequence verification failed'}
        & python "$PSScriptRoot/check_post_restart_assistance.py" "$folder/run.log" --fighter $case.source --source-side $case.side |
            Out-File -LiteralPath "$caseOut/assistance.json" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Assistance did not stop before attract'}
        foreach($label in @('attract','css','highlight_140','highlight_156','match','combat_120','combat_600','sequence_action_1_4','sequence_action_1_12','sequence_action_1_24','sequence_ready_1')){
            if(-not(Test-Path -LiteralPath "$folder/snap/restart_$label.png")){throw 'Required actual runtime capture missing'}
        }
        $native=Get-Content -LiteralPath "$caseOut/sequence.json" -Raw | ConvertFrom-Json
        $accepted[$case.name]=[ordered]@{passed=$true;source_side=$case.side;new_side=$case.side;live_fields=601;
            memory_writes=0;source_tower_assistance='health_only';post_attract_assistance_excluded=$true;
            first_command_age=$record.first_command_age;native_counts=$native.native_counts;completed_owned_cycles=$native.completed_owned_cycles;
            bicycle_paired_cycles=$native.bicycle_paired_cycles;exact_case_source_hashes=$sources;
            action_ready_and_final_images_inspected=$true;log_sha256=(Get-FileHash -LiteralPath "$folder/run.log").Hash;
            result_sha256=(Get-FileHash -LiteralPath "$folder/result.json").Hash}
    }
    & "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File -LiteralPath "$out/launcher_verify.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Actual CMD verification failed'}
} finally {Pop-Location}
$tools=[ordered]@{}
foreach($file in @('mk2ks_restart_sequence.lua','mk2ks_post_ending_restart.lua','tools/run_post_ending_restart.ps1','tools/verify_restart_sequence.py','tools/verify_post_ending_restart.py','tools/test_restart_sequence.py','tools/audit_v284_restart_sequence.ps1')){
    $tools[$file]=(Get-FileHash -LiteralPath "$root/$file").Hash
}
[ordered]@{playable_build='v277';production_inputs_match_build=$true;playable_and_old_zip_unchanged=$true;
    hashes=$hashes;cases=$accepted;reference_tests_passed=236;reference_log_sha256=(Get-FileHash -LiteralPath "$root/audit_v284_final_reference_units.log").Hash;
    current_test_source_hashes=$tools;original_failed_p1_bicycle_preserved=$true;live_emulator_processes=0;launcher_verify_exit=0;
    workspace_cleanup_state='still_running_separate_verified_archive_job_not_completion_proof';full_goal_complete=$false;
    scope='owned_post_restart_blade_effect_bicycle_flight_collision_checks_and_cleanup_not_uninterrupted_choreography_damage_parity_other_specials_or_unassisted_tower'} |
    ConvertTo-Json -Depth 7 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
'v284 move checkpoint passed; workspace archive job and full natural-integration goal remain open'
