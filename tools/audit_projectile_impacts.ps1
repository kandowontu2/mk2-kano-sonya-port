param([string]$OutputName='audit_v295_projectile_impacts_final_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned evidence name'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$candidateRoot=Join-Path $root 'diagnostic_v293_native_projectile_impacts'
$build=Get-Content "$candidateRoot/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Candidate build input changed: $($item.Name)"}}
if((Get-FileHash "$candidateRoot/mkport_candidate.exe").Hash -ne $build.executable_sha256 -or
   (Get-FileHash "$candidateRoot/roms/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Candidate build changed'}
$prior=Get-Content "$root/audit_v291_projectile_core_checked_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $prior.passed -or $prior.reference_tests_passed -ne 440){throw 'Previous geometry checkpoint missing'}
$productionPrior=Get-Content "$root/audit_v290_mobility_contact_final_inputs/result.json" -Raw | ConvertFrom-Json
foreach($suffix in 'PLAY_MK2_KANO_SONYA.cmd','diagnostic_v277_native_battle_photos/mkport_candidate.exe','diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata'){
    $item=$productionPrior.current_inputs.PSObject.Properties | Where-Object {$_.Name.EndsWith($suffix)}
    if(@($item).Count -ne 1 -or (Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Production build/launcher changed: $suffix"}
}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$tracked=@($PSCommandPath,"$root/mk2ks_projectile_impact_probe.lua","$root/mk2ks_join_projectile_probe.lua","$root/mk2ks_projectile_contact.lua",
    "$root/mk2ks_restart_lifecycle.lua","$root/mk3_projectile_impact_reference.lua","$root/mk3_knife_geometry_reference.lua",
    "$root/mame-mkp/src/mame/midway/midtunit_m.cpp","$root/mame-mkp/src/mame/midway/midtunit.cpp",
    "$candidateRoot/mkport_candidate.exe","$candidateRoot/roms/mk2ks/mk2ks.mdata","$root/PLAY_MK2_KANO_SONYA.cmd",
    "$root/diagnostic_v292_projectile_impact_payload/roms/mk2ks/mk2ks.impact.json")
$tracked+=Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.py' -File | Select-Object -ExpandProperty FullName
$hashes=[ordered]@{};foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.lua','.py','.ps1','.cpp','.json'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$accepted=@()
foreach($target in 'kano','sonya'){foreach($side in 1,2){foreach($scenario in 'hit','block','miss'){
    $name="audit_v295_impact_${target}_${scenario}_p${side}";$folder=Join-Path $root $name
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if($original.exit_code -ne 0 -or -not $original.observer_pass -or $original.candidate -ne 'diagnostic_v293_native_projectile_impacts'){throw "Original runtime failed: $name"}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json;$archived=0
    foreach($item in $inputs.PSObject.Properties){
        if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1'){
            $path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))
            if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Archived launch source changed: $path"};$archived++
        }elseif((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Launch build changed: $($item.Name)"}
    }
    python "$PSScriptRoot/verify_projectile_impacts.py" $folder --target $target --side $side | Out-File "$out/$name.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Independent native impact/render verification failed: $name"}
    $proof=Get-Content "$out/$name.json" -Raw | ConvertFrom-Json
    $rendered=@($proof.visual | Where-Object phase -ne 'startup_diagnostic')
    $accepted+=[ordered]@{name=$name;target=$target;side=$side;scenario=$scenario;original_observer_pass=$true;independent_impact_render_pass=$proof.passed;
        archived_launch_sources_verified=$archived;log_sha256=(Get-FileHash "$folder/run.log").Hash;rendered_pose_checks=$rendered.Count;
        min_render_pixel_agreement=($rendered.score | Measure-Object -Minimum).Minimum;startup_fidelity_proven=$false;scope=$proof.scope}
    "$name impact/render verified"
}}}
$references=@()
foreach($kind in 'knife','ring'){foreach($scenario in 'hit','block'){
    $version=if($scenario -eq 'hit'){292}else{295};$name="audit_v${version}_original_${kind}_impact_${scenario}"
    $folder=Join-Path $root $name;$result=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if($result.exit_code -ne 0 -or $result.scope -ne 'original_MK3_read_only_reference'){throw 'Original reference failed'}
    $inputs=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
    foreach($item in $inputs.PSObject.Properties){
        $path=if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1'){Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))}else{$item.Name}
        if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw 'Original reference frozen input changed'}
    }
    $references+=[ordered]@{name=$name;log_sha256=(Get-FileHash "$folder/run.log").Hash;scope='original_input_only_hit_or_block_pose_cadence_origin_drift'}
}}
$modules=@($prior.reference_modules)+@('test_native_projectile_impacts','test_projectile_impacts')
$expected=440+(Select-String "$PSScriptRoot/test_native_projectile_impacts.py" -Pattern '^    def test_').Count+
    (Select-String "$PSScriptRoot/test_projectile_impacts.py" -Pattern '^    def test_').Count
Push-Location $PSScriptRoot
try {python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Reference suite failed'}
}finally{Pop-Location}
$log=Get-Content "$out/reference_tests.log" -Raw
if($log -notmatch "Ran $expected tests" -or $log -notmatch '(?m)^OK\s*$'){throw 'Incomplete reference suite'}
& "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File "$out/production_cmd_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Production CMD ROM check failed'}
& "$candidateRoot/mkport_candidate.exe" mk2ks -rompath "$candidateRoot/roms;$root/roms" -verifyroms | Out-File "$out/candidate_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Candidate ROM check failed'}
foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Audit input changed: $path"}}
[ordered]@{passed=$true;candidate='diagnostic_v293_native_projectile_impacts';candidate_executable_sha256=$build.executable_sha256;
    payload_sha256=$build.payload_sha256;production_launcher_and_v277_build_unchanged=$true;cold_impact_render_cases=$accepted;
    original_game_references=$references;reference_tests_passed=$expected;reference_modules=$modules;
    impact_choreography_proven=$true;startup_and_full_flight_choreography_proven=$false;post_ending_current_candidate_proven=$false;
    full_character_integration_complete=$false;original_static_visual_crop_failures_retained=$prior.original_static_visual_crop_failures_retained;
    scope='12_cold_real_join_hit_block_duck_native_impact_original_composites_four_field_holds_origin_drift_components_DMA_render_damage_cleanup';
    remaining='Original release/startup and complete flight cadence; current-candidate post-ending/CPU/stock/other-move regressions; remaining finisher/fidelity and whole-game audio/visual/play QA; final launcher and release ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Native impact checkpoint: 12 actual cold cases, $expected reference tests; production remains v277"
