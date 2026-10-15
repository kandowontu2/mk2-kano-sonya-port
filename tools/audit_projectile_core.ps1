param([string]$OutputName='audit_v291_projectile_core_final_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned evidence name'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$candidate=Join-Path $root 'diagnostic_v291_native_projectile_core'
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Candidate source/asset changed: $($item.Name)"}}
if((Get-FileHash "$candidate/mkport_candidate.exe").Hash -ne $build.executable_sha256 -or
   (Get-FileHash "$candidate/roms/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Candidate build changed'}
$prior=Get-Content "$root/audit_v290_mobility_contact_final_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $prior.passed -or $prior.reference_tests_passed -ne 413){throw 'Previous checkpoint missing'}
foreach($suffix in 'PLAY_MK2_KANO_SONYA.cmd','diagnostic_v277_native_battle_photos/mkport_candidate.exe','diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata'){
    $item=$prior.current_inputs.PSObject.Properties | Where-Object {$_.Name.EndsWith($suffix)}
    if(@($item).Count -ne 1 -or (Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Production launcher/build changed: $suffix"}
}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$tracked=@($PSCommandPath,"$root/mk2ks_join_projectile_probe.lua","$root/mk2ks_projectile_contact.lua","$root/mk2ks_restart_lifecycle.lua",
    "$root/mk3_knife_geometry_reference.lua","$root/mame-mkp/src/mame/midway/midtunit_m.cpp",
    "$candidate/mkport_candidate.exe","$candidate/roms/mk2ks/mk2ks.mdata","$root/PLAY_MK2_KANO_SONYA.cmd")
$tracked+=Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.py' -File | Select-Object -ExpandProperty FullName
$hashes=[ordered]@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.lua','.py','.ps1','.cpp'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json -Depth 3 | Out-File "$out/input_hashes_before.json" -Encoding utf8
$accepted=@()
foreach($target in 'kano','sonya'){foreach($side in 1,2){foreach($scenario in 'hit','block','miss'){
    $name="audit_v291_native_core_${target}_${scenario}_p${side}";$folder=Join-Path $root $name
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if($original.exit_code -ne 0 -or -not $original.observer_pass -or
       [IO.Path]::GetFullPath($original.candidate) -ne [IO.Path]::GetFullPath($candidate)){throw "Original runtime failed: $name"}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json;$archived=0
    foreach($item in $inputs.PSObject.Properties){
        if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1'){
            $path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))
            if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Archived launch source changed: $path"};$archived++
        }elseif((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Launch build changed: $($item.Name)"}
    }
    python "$PSScriptRoot/verify_projectile_contact.py" "$folder/run.log" --target $target --side $side |
        Out-File "$out/${name}_contact.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Independent collision-core verification failed: $name"}
    foreach($age in 200,210,225,410,440,560){if(-not (Test-Path -LiteralPath "$folder/snap/proj_contact_$age.png")){throw 'Missing actual scene evidence'}}
    $accepted+=[ordered]@{name=$name;target=$target;side=$side;scenario=$scenario;original_observer_pass=$true;independent_geometry_pass=$true;
        archived_launch_sources_verified=$archived;log_sha256=(Get-FileHash "$folder/run.log").Hash;scope='cold_actual_challenger_join_not_post_ending_or_CPU'}
}}}
$commands=@()
foreach($target in 'kano','sonya'){foreach($command in 'native','legacy','chord','reversed','expired','wrong_button','airborne','with_block'){
    $folder=Join-Path $root "audit_v291_command_core_${target}_${command}"
    $result=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    $log=Get-Content "$folder/run.log" -Raw
    if($result.exit_code -ne 0 -or $log -notmatch 'MK2KS_PROJECTILES_RESULT pass=true ' -or $log -notmatch 'MK2KS_EXIT_RESULT pass=true ' -or
       $log -notmatch 'MK2KS_DISPLAY_RESULT pass=true ' -or $log -notmatch 'MK2KS_HUD_SHADOW_RESULT pass=true ' -or
       $log -notmatch 'MK2KS_STABILITY stalled_frames=0 trap_frames=0'){throw "Current command/scene gates failed: $folder"}
    if(-not $result.passed -and ($command -ne 'native' -or $result.visual_alignment_passed -ne $false)){throw 'Unexpected original command gate failure'}
    $commands+=[ordered]@{target=$target;command=$command;original_overall_passed=$result.passed;runtime_command_scene_gates_pass=$true;
        old_static_visual_crop_passed=$result.visual_alignment_passed;log_sha256=(Get-FileHash "$folder/run.log").Hash}
}}
$modules=@($prior.reference_modules)+@('test_projectile_contact')
$expected=413+(Select-String -LiteralPath "$PSScriptRoot/test_projectile_contact.py" -Pattern '^    def test_').Count
Push-Location $PSScriptRoot
try {python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Reference suite failed'}
}finally{Pop-Location}
$log=Get-Content "$out/reference_tests.log" -Raw
if($log -notmatch "Ran $expected tests" -or $log -notmatch '(?m)^OK\s*$'){throw 'Incomplete reference suite'}
& "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File "$out/production_cmd_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Production CMD ROM check failed'}
& "$candidate/mkport_candidate.exe" mk2ks -rompath "$candidate/roms;$root/roms" -verifyroms | Out-File "$out/candidate_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Candidate ROM check failed'}
foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Final audit input changed: $path"}}
[ordered]@{passed=$true;candidate='diagnostic_v291_native_projectile_core';candidate_executable_sha256=$build.executable_sha256;
    payload_sha256=$build.payload_sha256;candidate_source_changed=$true;production_launcher_and_v277_build_unchanged=$true;
    cold_geometry_cases=$accepted;command_runtime_diagnostics=$commands;reference_tests_passed=$expected;reference_modules=$modules;
    scope='candidate_only_12_cold_native_join_contact_core_origin_damage_chip_duck_cleanup_paths_unchanged_stock_attack_region';
    original_static_visual_crop_failures_retained=@('audit_v291_command_core_kano_native','audit_v291_command_core_sonya_native');
    post_ending_current_candidate_proven=$false;full_impact_choreography_proven=$false;full_character_integration_complete=$false;
    remaining='Frame-aware rendered projectile QA and impact choreography; current-candidate post-ending/CPU/other-move regressions; remaining integration and whole-game audio/visual/play QA; final launcher promotion/release ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Candidate geometry checkpoint: 12 actual cold paths, $expected reference tests; production remains v277"
