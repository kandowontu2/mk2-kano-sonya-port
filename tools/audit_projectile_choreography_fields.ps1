param([string]$OutputName='audit_v301_choreography_fields_final_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned evidence name'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$candidateRoot=Join-Path $root 'diagnostic_v300_native_projectile_choreography'
$build=Get-Content "$candidateRoot/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){
    if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build input changed: $($item.Name)"}
}
if((Get-FileHash "$candidateRoot/mkport_candidate.exe").Hash -ne $build.executable_sha256 -or
   (Get-FileHash "$candidateRoot/roms/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Candidate identity mismatch'}
$previous=Get-Content "$root/audit_v295_projectile_impacts_final_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $previous.passed -or $previous.reference_tests_passed -ne 475){throw 'Previous impact checkpoint missing'}
$productionPrevious=Get-Content "$root/audit_v290_mobility_contact_final_inputs/result.json" -Raw | ConvertFrom-Json
foreach($suffix in 'PLAY_MK2_KANO_SONYA.cmd','diagnostic_v277_native_battle_photos/mkport_candidate.exe','diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata'){
    $item=$productionPrevious.current_inputs.PSObject.Properties | Where-Object {$_.Name.EndsWith($suffix)}
    if(@($item).Count -ne 1 -or (Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Production changed: $suffix"}
}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$tracked=@($PSCommandPath,"$root/tools/run_join_projectile_probe.ps1","$root/mk2ks_projectile_choreography_probe.lua",
    "$root/mk2ks_projectile_impact_probe.lua","$root/mk2ks_join_projectile_probe.lua","$root/mk2ks_projectile_contact.lua",
    "$root/mk2ks_restart_lifecycle.lua","$root/mk2ks_selector_exit_test.lua","$root/mame-mkp/src/mame/midway/midtunit_m.cpp",
    "$root/mame-mkp/src/mame/midway/midtunit.cpp","$candidateRoot/mkport_candidate.exe","$candidateRoot/roms/mk2ks/mk2ks.mdata",
    "$root/PLAY_MK2_KANO_SONYA.cmd","$root/diagnostic_v298_projectile_choreography_payload/roms/mk2ks/mk2ks.choreography.json")
$tracked+=Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.py' -File | Select-Object -ExpandProperty FullName
$before=[ordered]@{}
foreach($path in $tracked){
    $before[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.lua','.py','.ps1','.cpp','.json'){
        Copy-Item -LiteralPath $path -Destination "$out/input_sources"
    }
}
$before | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$cases=@()
foreach($target in 'kano','sonya'){foreach($side in 1,2){foreach($scenario in 'hit','block','miss'){
    $name="audit_v300_choreo_${target}_${scenario}_p${side}";$folder=Join-Path $root $name
    python "$PSScriptRoot/verify_projectile_choreography.py" $folder --target $target --side $side |
        Out-File "$out/$name.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Independent current choreography failed: $name"}
    $proof=Get-Content "$out/$name.json" -Raw | ConvertFrom-Json
    $cases+=[ordered]@{name=$name;target=$target;side=$side;scenario=$scenario;independent_pass=$proof.passed;
        fields=$proof.joined_fields;scope=$proof.scope;log_sha256=(Get-FileHash "$folder/run.log").Hash}
    "$name native fields verified"
}}}
$modules=@($previous.reference_modules)+@('test_native_projectile_choreography','test_projectile_choreography')
$expected=475+(Select-String "$PSScriptRoot/test_native_projectile_choreography.py" -Pattern '^    def test_').Count+
    (Select-String "$PSScriptRoot/test_projectile_choreography.py" -Pattern '^    def test_').Count
Push-Location $PSScriptRoot
try {
    $ErrorActionPreference='Continue'
    python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8
    $testExit=$LASTEXITCODE;$ErrorActionPreference='Stop'
    if($testExit -ne 0){throw 'Reference tests failed'}
} finally {Pop-Location}
$log=Get-Content "$out/reference_tests.log" -Raw
if($log -notmatch "Ran $expected tests" -or $log -notmatch '(?m)^OK\s*$'){throw 'Incomplete reference test run'}
& "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File "$out/production_cmd_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Production CMD ROM check failed'}
& "$candidateRoot/mkport_candidate.exe" mk2ks -rompath "$candidateRoot/roms;$root/roms" -verifyroms |
    Out-File "$out/candidate_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Candidate ROM check failed'}
$after=[ordered]@{}
foreach($path in $tracked){
    $after[$path]=(Get-FileHash -LiteralPath $path).Hash
    if($before[$path] -ne $after[$path]){throw "Audit input changed: $path"}
}
$after | ConvertTo-Json | Out-File "$out/input_hashes_after.json" -Encoding utf8
[ordered]@{passed=$true;candidate=$build.name;candidate_executable_sha256=$build.executable_sha256;
    payload_sha256=$build.payload_sha256;production_launcher_and_v277_build_unchanged=$true;
    cold_native_field_cases=$cases;reference_modules=$modules;reference_tests_passed=$expected;
    original_release_intro_full_flight_field_timing_proven=$true;
    full_current_component_DMA_screenshot_proven=$false;post_ending_current_candidate_proven=$false;
    full_character_integration_complete=$false;scope='12_cold_real_join_release_intro_full_travel_cycles_contact_damage_recovery_fields_not_render_CPU_endings_or_audio';
    remaining='Full current component/DMA/pixel render proof; post-ending/current stock/other-move/CPU regressions; finisher and whole-game audio/visual/play QA; launcher and release ZIP';
    input_hashes=$before} | ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Current native choreography checkpoint: 12 real cold cases and $expected reference tests. Production remains v277."
