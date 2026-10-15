param([string]$OutputName='audit_v311_current_post_ending_checked_inputs')
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
$prior=Get-Content "$root/audit_v304_projectile_render_final_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $prior.passed -or $prior.reference_tests_passed -ne 531){throw 'Prior current render checkpoint missing'}
$specs=@(@('kano','sonya',1,1,'hit'),@('sonya','kano',1,2,'miss'),@('kano','sonya',2,2,'block'),@('sonya','kano',2,1,'hit'))
$names=@()
foreach($spec in $specs){
    $name="audit_v310_current_end_p$($spec[2])_$($spec[0])_p$($spec[3])_$($spec[1])_$($spec[4])"
    $names+=$name
    if(-not (Test-Path "$root/$name/result.json")){throw "Terminal current ending case missing: $name"}
}
$finishNames=@('audit_v308_current_finish_kano_sonya','audit_v308_current_finish_sonya_sub_zero')
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$tracked=@($PSCommandPath,"$candidateRoot/mkport_candidate.exe","$candidateRoot/roms/mk2ks/mk2ks.mdata",
    "$candidateRoot/build-info.json","$root/PLAY_MK2_KANO_SONYA.cmd","$root/mk2ks_post_ending_restart.lua",
    "$root/mk2ks_projectile_choreography_probe.lua","$root/mk2ks_projectile_impact_probe.lua",
    "$root/mk2ks_projectile_observer_bridge_probe.lua","$root/mk2ks_cpu_ladder_trace.lua",
    "$root/mk2ks_p2_tower_probe.lua","$root/mk2ks_restart_lifecycle.lua","$root/mk2ks_projectile_contact.lua",
    "$PSScriptRoot/run_post_ending_restart.ps1","$PSScriptRoot/run_unassisted_finish_case.ps1")
$tracked+=Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.py' -File | Select-Object -ExpandProperty FullName
$tracked+=@($build.input_hashes.PSObject.Properties | Select-Object -ExpandProperty Name)
$hashes=[ordered]@{};$evidence=[ordered]@{}
foreach($path in $tracked){
    $hashes[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.lua','.py','.ps1','.cpp','.h','.json'){
        Copy-Item -LiteralPath $path -Destination "$out/input_sources"
    }
}
foreach($name in ($names+$finishNames+@('audit_v309_observer_bridge_kano_hit_p1','audit_v307_current_end_p2_kano_p2_sonya_block'))){
    Get-ChildItem -LiteralPath "$root/$name" -Recurse -File | Where-Object {$_.Extension -in '.json','.log','.png','.lua','.ps1','.py','.cpp','.h'} |
        ForEach-Object {$evidence[$_.FullName]=(Get-FileHash -LiteralPath $_.FullName).Hash}
}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$evidence | ConvertTo-Json | Out-File "$out/evidence_hashes_before.json" -Encoding utf8
$cases=@()
foreach($spec in $specs){
    $source=$spec[0];$target=$spec[1];$ss=$spec[2];$ns=$spec[3];$scenario=$spec[4]
    $name="audit_v310_current_end_p${ss}_${source}_p${ns}_${target}_${scenario}"
    python "$PSScriptRoot/verify_current_post_ending_choreography.py" "$root/$name" --source $source --target $target --source-side $ss --new-side $ns --scenario $scenario |
        Out-File "$out/$name.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Independent full current ending path failed: $name"}
    $proof=Get-Content "$out/$name.json" -Raw | ConvertFrom-Json
    $cases+=[ordered]@{name=$name;passed=$proof.passed;source=$source;target=$target;source_side=$ss;new_side=$ns;
        scenario=$scenario;scope=$proof.scope;assistance_scope=$proof.assistance.proof_scope}
    "$name matched current full ending / fresh game / real join / complete throws verified"
}
$finishes=@()
foreach($spec in @(@('kano','sonya'),@('sonya','sub_zero'))){
    $name="audit_v308_current_finish_$($spec[0])_$($spec[1])";$folder=Join-Path $root $name
    $metadata=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if(-not $metadata.passed -or $metadata.exit_code -ne 0 -or $metadata.assistance -ne 'none' -or
       $metadata.candidate_executable_sha256 -ne $build.executable_sha256 -or $metadata.payload_sha256 -ne $build.payload_sha256){throw "Current finisher case identity failed: $name"}
    foreach($item in $metadata.input_hashes.PSObject.Properties){
        $path=$item.Name
        if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.json'){$path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($path))}
        if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Frozen current finisher input failed: $path"}
    }
    python "$PSScriptRoot/verify_unassisted_finish.py" "$folder/run.log" --fighter $spec[0] --victim $spec[1] |
        Out-File "$out/$name.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Independent unassisted current finisher failed: $name"}
    $proof=Get-Content "$out/$name.json" -Raw | ConvertFrom-Json
    $finishes+=[ordered]@{name=$name;passed=$proof.passed;native_damage=$proof.total_native_damage;native_rounds=$proof.complete_native_rounds;scope=$proof.scope}
}
$modules=@($prior.reference_modules)+@('test_current_post_ending_choreography')
$expected=531+(Select-String "$PSScriptRoot/test_current_post_ending_choreography.py" -Pattern '^    def test_').Count
Push-Location $PSScriptRoot
try{
    $ErrorActionPreference='Continue'
    python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8
    $code=$LASTEXITCODE;$ErrorActionPreference='Stop'
    if($code -ne 0){throw 'Reference/current ending tests failed'}
}finally{Pop-Location}
$log=Get-Content "$out/reference_tests.log" -Raw
if($log -notmatch "Ran $expected tests" -or $log -notmatch '(?m)^OK\s*$'){throw 'Incomplete reference test run'}
& "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File "$out/production_cmd_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Production CMD ROM check failed'}
& "$candidateRoot/mkport_candidate.exe" mk2ks -rompath "$candidateRoot/roms;$root/roms" -verifyroms |
    Out-File "$out/candidate_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Current candidate ROM check failed'}
foreach($path in $hashes.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Audit input changed: $path"}}
foreach($path in $evidence.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $evidence[$path]){throw "Case evidence changed: $path"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_after.json" -Encoding utf8
[ordered]@{passed=$true;candidate=$build.name;candidate_executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;
    current_post_ending_cases=$cases;current_unassisted_finisher_input_cases=$finishes;reference_tests_passed=$expected;reference_modules=$modules;
    tower_health_assistance='health_only';restart_assistance='none';unassisted_tower_clear_proven=$false;
    full_CPU_action_coverage_proven=$false;full_post_ending_component_DMA_pixel_proof=$false;full_finisher_art_audio_coverage=$false;
    production_unchanged=$true;full_character_integration_complete=$false;
    retained_failed_observer_cases='audit_v307_*';observer_bridge_pilot='audit_v309_observer_bridge_kano_hit_p1';
    scope='four_current_full_ending_to_fresh_CPU_game_and_real_join_projectile_field_paths_plus_two_unassisted_P1_finisher_inputs_not_all_characters_modes_or_audio';
    remaining='Current stock projectile/remaining move/CPU and all-victim regressions; whole-game finisher/audio/visual/play-feel QA; launcher/release ZIP';
    input_hashes=$hashes;evidence_file_count=$evidence.Count;evidence_hashes_file='evidence_hashes_before.json'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Current full ending-to-fresh-game checkpoint: 4 paths, 2 unassisted finisher inputs and $expected tests."
