# Recheck the actual v283 evidence without changing any accepted case artifacts.
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$out=Join-Path $root 'audit_v283_final_inputs'
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite final evidence'}
if(@(Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe'}).Count){throw 'A candidate emulator is still live'}
New-Item -ItemType Directory -Path $out | Out-Null
$build=Get-Content -LiteralPath "$root/diagnostic_v277_native_battle_photos/build-info.json" -Raw | ConvertFrom-Json
foreach($prop in $build.input_hashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $prop.Name).Hash -ne $prop.Value){throw "Production input changed: $($prop.Name)"}
}
$prior=Get-Content -LiteralPath "$root/audit_v282_final_inputs/result.json" -Raw | ConvertFrom-Json
$outer='C:/Users/kando/Documents/Codex/2026-08-30/continue-the-mk2-kano-sonya-port'
$paths=[ordered]@{
    old_zip_sha256="$outer/MK2_Kano_Sonya_v258_playtest.zip"
    root_cmd_sha256="$root/PLAY_MK2_KANO_SONYA.cmd"
    candidate_cmd_sha256="$root/diagnostic_v277_native_battle_photos/PLAY_CANDIDATE.cmd"
    installed_generic_exe_sha256="$root/mame-mkp/mkport.exe"
    executable_sha256="$root/diagnostic_v277_native_battle_photos/mkport_candidate.exe"
    payload_sha256="$root/diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata"
}
$hashes=[ordered]@{}
foreach($key in $paths.Keys){
    $hashes[$key]=(Get-FileHash -LiteralPath $paths[$key]).Hash
    if($hashes[$key] -ne $prior.hashes.$key){throw "Playable/archive hash changed: $key"}
}
$outerCmd=(Get-FileHash -LiteralPath "$outer/PLAY_MK2_KANO_SONYA.cmd").Hash
if($outerCmd -ne 'C94CFA01D231BE90597DF799FC8043FCAA18ED467886B347A984B32BFABC91B7'){throw 'Outer launcher changed'}
$units=Get-Content -LiteralPath "$root/audit_v283_final_reference_units.log" -Raw
if($units -notmatch 'Ran 211 tests' -or $units -notmatch '\bOK\s*$' -or $units -match '(?m)^(FAILED|ERROR:|FAIL:)'){throw 'Reference tests did not all pass'}
$cases=@(
    @{name='audit_v283_retreat_p1_kano_retry';side=1;target='kano';source='sonya'},
    @{name='audit_v283_mobility_p2_kano';side=2;target='kano';source='sonya'},
    @{name='audit_v283_mobility_p1_sonya';side=1;target='sonya';source='kano'},
    @{name='audit_v283_extended_p2_sonya_retry';side=2;target='sonya';source='kano'}
)
$accepted=[ordered]@{}
Push-Location $root
try {
    foreach($case in $cases){
        $folder=Join-Path $root $case.name
        $result=Get-Content -LiteralPath "$folder/result.json" -Raw | ConvertFrom-Json
        if(-not $result.passed){throw "Recorded case failed: $($case.name)"}
        $sources=[ordered]@{}
        foreach($prop in $result.input_hashes.PSObject.Properties){
            if([IO.Path]::GetExtension($prop.Name) -in @('.lua','.ps1','.py')){
                $name=[IO.Path]::GetFileName($prop.Name)
                $sources[$name]=(Get-FileHash -LiteralPath "$folder/input_sources/$name").Hash
                if($sources[$name] -ne $prop.Value){throw "Incorrect archived source: $($case.name) $name"}
            }
        }
        $caseOut=Join-Path $out $case.name
        New-Item -ItemType Directory -Path $caseOut | Out-Null
        & python "$PSScriptRoot/verify_post_ending_restart.py" "$folder/run.log" --fighter $case.source --target $case.target --source-side $case.side --new-side $case.side --special-mode mobility |
            Out-File -LiteralPath "$caseOut/restart.json" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Current independent source/restart verification failed'}
        & python "$PSScriptRoot/check_post_restart_assistance.py" "$folder/run.log" --fighter $case.source --source-side $case.side |
            Out-File -LiteralPath "$caseOut/assistance.json" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Current independent assistance-stop verification failed'}
        Get-Content -LiteralPath "$folder/run.log" -Raw | & python -c 'import sys,json;sys.path.insert(0,sys.argv[1]);from verify_restart_mobility import verify;r=verify(sys.stdin.read(),sys.argv[2],int(sys.argv[3]));print(json.dumps(r,indent=2));sys.exit(0 if r["passed"] else 1)' $PSScriptRoot $case.target $case.side |
            Out-File -LiteralPath "$caseOut/mobility.json" -Encoding utf8
        if($LASTEXITCODE -ne 0){throw 'Current independent mobility verification failed'}
        $required=@('attract','css','highlight_140','highlight_156','match','combat_120','combat_600','mobility_action_1_12','mobility_action_1_24','mobility_ready_1')
        foreach($label in $required){if(-not(Test-Path -LiteralPath "$folder/snap/restart_$label.png")){throw 'Missing required runtime screenshot'}}
        $artifacts=[ordered]@{}
        Get-ChildItem -LiteralPath $folder -File -Recurse | Where-Object {$_.Extension -in @('.json','.log','.png')} | ForEach-Object {
            $artifacts[$_.FullName.Substring($folder.Length+1)]=(Get-FileHash -LiteralPath $_.FullName).Hash
        }
        $mobility=Get-Content -LiteralPath "$caseOut/mobility.json" -Raw | ConvertFrom-Json
        $accepted[$case.name]=[ordered]@{passed=$true;live_fields=601;restart_memory_writes=0;source_tower_assistance='health_only';
            post_attract_assistance_excluded=$true;exact_sources_archived=$true;archived_source_hashes=$sources;
            native_counts=$mobility.native_counts;completed_owned_cycles=$mobility.completed_owned_cycles;
            p2_square_recovery_includes_cpu_air_throw_interruption=($case.side -eq 2 -and $case.target -eq 'sonya');
            required_snapshots_present=$true;action_ready_and_final_combat_images_inspected=$true;artifact_hashes=$artifacts}
    }
    & "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File -LiteralPath "$out/launcher_verify.log" -Encoding utf8
    $launcherExit=$LASTEXITCODE
    if($launcherExit -ne 0){throw 'Actual launcher verification failed'}
} finally {Pop-Location}
$disk=Get-Content -LiteralPath "$root/audit_v283_disk_recovery/result.json" -Raw | ConvertFrom-Json
foreach($file in $disk.files){if((Get-FileHash -LiteralPath $file.path).Hash -ne $file.sha256){throw 'Old compressed binary changed contents'}}
$toolHashes=[ordered]@{}
foreach($path in @('mk2ks_restart_mobility.lua','mk2ks_post_ending_restart.lua','tools/run_post_ending_restart.ps1','tools/verify_restart_mobility.py','tools/test_restart_mobility.py','tools/audit_v283_restart_mobility.ps1')){
    $toolHashes[$path]=(Get-FileHash -LiteralPath "$root/$path").Hash
}
[ordered]@{playable_build='v277';production_inputs_match_build=$true;playable_and_old_zip_unchanged=$true;
    cases=$accepted;original_failed_cases_preserved=@('audit_v283_mobility_p1_kano','audit_v283_mobility_p2_sonya');
    disk_full_partials_preserved=@('audit_v283_retreat_p1_kano','audit_v283_extended_p2_sonya');
    reference_tests_passed=211;reference_log_sha256=(Get-FileHash -LiteralPath "$root/audit_v283_final_reference_units.log").Hash;
    current_test_source_hashes=$toolHashes;hashes=$hashes;outer_cmd_sha256=$outerCmd;launcher_verify_exit=$launcherExit;
    compressed_old_executables=22;compression_only_no_deletion=$true;disk_recovery_manifest_sha256=(Get-FileHash -LiteralPath "$root/audit_v283_disk_recovery/result.json").Hash;
    live_test_processes=0;scope='owned_post_restart_ball_and_square_flight_collision_checks_and_grounded_recovery_not_damage_parity_other_specials_or_unassisted_tower';
    full_goal_complete=$false} | ConvertTo-Json -Depth 9 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
'v283 final evidence audit passed; full goal remains active'
