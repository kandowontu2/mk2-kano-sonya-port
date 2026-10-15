param([string]$OutputName='audit_v304_projectile_render_final_inputs')
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
$previous=Get-Content "$root/audit_v301_choreography_fields_final_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $previous.passed -or $previous.reference_tests_passed -ne 506){throw 'Previous choreography checkpoint missing'}
$productionPrevious=Get-Content "$root/audit_v290_mobility_contact_final_inputs/result.json" -Raw | ConvertFrom-Json
foreach($suffix in 'PLAY_MK2_KANO_SONYA.cmd','diagnostic_v277_native_battle_photos/mkport_candidate.exe','diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata'){
    $item=$productionPrevious.current_inputs.PSObject.Properties | Where-Object {$_.Name.EndsWith($suffix)}
    if(@($item).Count -ne 1 -or (Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Production changed: $suffix"}
}
$caseFolders=@()
foreach($target in 'kano','sonya'){foreach($side in 1,2){foreach($scenario in 'hit','block','miss'){
    $name="audit_v303_render_shadow_${target}_${scenario}_p${side}"
    if(-not (Test-Path "$root/$name/result.json")){$name="audit_v302_render_${target}_${scenario}_p${side}"}
    if(-not (Test-Path "$root/$name/result.json")){throw "Terminal render evidence missing: $name"}
    $caseFolders+=[ordered]@{name=$name;target=$target;side=$side;scenario=$scenario}
}}}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$tracked=@($PSCommandPath,"$root/tools/run_join_projectile_probe.ps1","$root/mk2ks_projectile_render_probe.lua",
    "$root/mk2ks_projectile_choreography_probe.lua","$root/mk2ks_projectile_impact_probe.lua",
    "$root/mk2ks_join_projectile_probe.lua","$root/mk2ks_projectile_contact.lua","$root/mk2ks_restart_lifecycle.lua",
    "$root/mk2ks_selector_exit_test.lua","$root/mame-mkp/src/mame/midway/midtunit_m.cpp",
    "$root/mame-mkp/src/mame/midway/midtunit.cpp","$root/mame-mkp/src/mame/midway/midtunit_v.cpp",
    "$candidateRoot/mkport_candidate.exe","$candidateRoot/roms/mk2ks/mk2ks.mdata","$root/PLAY_MK2_KANO_SONYA.cmd",
    "$root/roms/mk2ks/mk2ks.ui","$root/mk2/mk2-maincpu.bin","$root/mk3/mk3-maincpu.bin",
    "$root/diagnostic_v298_projectile_choreography_payload/roms/mk2ks/mk2ks.choreography.json",
    "$root/diagnostic_v292_projectile_impact_payload/roms/mk2ks/mk2ks.impact.json")
$tracked+=Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.py' -File | Select-Object -ExpandProperty FullName
$tracked+=Get-ChildItem -LiteralPath "$root/mk2" -File | Where-Object {$_.Name -match '^l1_mortal_kombat_ii_game_rom_(ug|uj)(14|16|17|19|20|22)\.'} | Select-Object -ExpandProperty FullName
$tracked+=Get-ChildItem -LiteralPath "$root/mk3" -File | Where-Object {$_.Name -match '^l1_mortal_kombat_3_u(11[4-9]|12[0-9]|13[0-3])_game_rom\.'} | Select-Object -ExpandProperty FullName
$before=[ordered]@{};$evidence=[ordered]@{}
foreach($path in $tracked){
    $before[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.lua','.py','.ps1','.cpp','.json'){
        Copy-Item -LiteralPath $path -Destination "$out/input_sources"
    }
}
foreach($case in $caseFolders){
    Get-ChildItem -LiteralPath "$root/$($case.name)" -Recurse -File | Where-Object {$_.Extension -in '.json','.log','.png','.lua','.ps1'} |
        ForEach-Object {$evidence[$_.FullName]=(Get-FileHash -LiteralPath $_.FullName).Hash}
}
$before | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$evidence | ConvertTo-Json | Out-File "$out/evidence_hashes_before.json" -Encoding utf8
$cases=@()
foreach($case in $caseFolders){
    $name=$case.name;$folder=Join-Path $root $name
    python "$PSScriptRoot/verify_projectile_render.py" $folder --target $case.target --side $case.side |
        Out-File "$out/$name.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Independent current render failed: $name"}
    $proof=Get-Content "$out/$name.json" -Raw | ConvertFrom-Json
    $visible=@($proof.visual | Where-Object {$_.visible -gt 0})
    $cases+=[ordered]@{name=$name;target=$case.target;side=$case.side;scenario=$case.scenario;independent_pass=$proof.passed;
        fields=$proof.choreography.joined_fields;native_component_draws=$proof.native_component_draws;proved_culls=$proof.proved_culls;
        pixel_samples=$visible.Count;minimum_visible_component_pixel_match=($visible | Measure-Object -Property score -Minimum).Minimum;
        scope=$proof.scope;log_sha256=(Get-FileHash "$folder/run.log").Hash}
    "$name native components, palettes and actual bitmaps verified"
}
$modules=@($previous.reference_modules)+@('test_projectile_render')
$expected=506+(Select-String "$PSScriptRoot/test_projectile_render.py" -Pattern '^    def test_').Count
Push-Location $PSScriptRoot
try {
    $ErrorActionPreference='Continue'
    python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8
    $testExit=$LASTEXITCODE;$ErrorActionPreference='Stop'
    if($testExit -ne 0){throw 'Reference/render tests failed'}
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
foreach($path in $evidence.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $evidence[$path]){throw "Runtime evidence changed: $path"}}
$after | ConvertTo-Json | Out-File "$out/input_hashes_after.json" -Encoding utf8
[ordered]@{passed=$true;candidate=$build.name;candidate_executable_sha256=$build.executable_sha256;
    payload_sha256=$build.payload_sha256;production_launcher_and_v277_build_unchanged=$true;
    cold_native_render_cases=$cases;reference_modules=$modules;reference_tests_passed=$expected;
    all_release_startup_full_flight_impact_component_DMA_palette_fields_proven=$true;
    first_held_pose_component_pixels_each_cycle_proven=$true;every_bitmap_field_compared=$false;
    post_ending_current_candidate_proven=$false;full_character_integration_complete=$false;
    scope='12_cold_real_join_native_component_DMA_palette_inventory_and_original_pose_pixel_samples_not_whole_game';
    remaining='Post-ending/current stock/other-move/CPU regressions; finisher and whole-game audio/visual/play QA; launcher and release ZIP';
    input_hashes=$before;evidence_file_count=$evidence.Count;evidence_hashes_file='evidence_hashes_before.json'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Current original-art render checkpoint: 12 real cold cases and $expected reference tests. Production remains v277."
