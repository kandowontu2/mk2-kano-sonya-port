param([string]$OutputName='audit_v322_current_specials_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$candidate=Join-Path $root 'diagnostic_v300_native_projectile_choreography'
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
$prior=Get-Content "$root/audit_v318_natural_cpu_checked_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $prior.passed -or $prior.reference_tests_passed -ne 580 -or $prior.candidate_executable_sha256 -ne $build.executable_sha256 -or $prior.payload_sha256 -ne $build.payload_sha256){throw 'Previous matched current checkpoint missing'}
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build input changed: $($item.Name)"}}
if((Get-FileHash "$candidate/mkport_candidate.exe").Hash -ne $build.executable_sha256 -or (Get-FileHash "$candidate/roms/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Build identity mismatch'}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes=[ordered]@{}
$tracked=@($PSCommandPath,"$PSScriptRoot/run_post_ending_restart.ps1","$PSScriptRoot/run_join_airthrow_probe.ps1",
    "$root/mk2ks_restart_pair.lua","$root/mk2ks_restart_airthrow.lua","$root/mk2ks_join_airthrow_probe.lua",
    "$root/mk2ks_post_ending_restart.lua","$root/mk2ks_cpu_ladder_trace.lua","$root/mk2ks_selector_exit_test.lua",
    "$root/PLAY_MK2_KANO_SONYA.cmd","$candidate/mkport_candidate.exe","$candidate/roms/mk2ks/mk2ks.mdata",
    "$candidate/build-info.json","$root/mk2/mk2-maincpu.bin","$root/audit_v318_natural_cpu_checked_inputs/result.json")
$tracked+=@(Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.py' | ForEach-Object {$_.FullName})
$tracked+=@($build.input_hashes.PSObject.Properties | ForEach-Object {$_.Name})
foreach($path in $tracked){
    $hashes[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.cpp','.h'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}
}
$specs=@(
    @('audit_v319_current_pair_p1_kano','sonya','kano',1,1,'pair','sonya',$false),
    @('audit_v319_current_pair_p1_sonya','kano','sonya',1,1,'pair','sonya',$false),
    @('audit_v319_current_pair_p2_kano','sonya','kano',2,2,'pair','sonya',$false),
    @('audit_v319_current_pair_p2_sonya','kano','sonya',2,2,'pair','sonya',$false),
    @('audit_v319_current_air_p1_sonya_followup','kano','kano',1,1,'airthrow','sonya',$true),
    @('audit_v321_current_air_p2_subzero_followup','sonya','kano',2,2,'airthrow','sub_zero',$true)
)
$cases=@()
foreach($spec in $specs){
    $name=$spec[0];$folder=Join-Path $root $name
    $metadata=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    foreach($item in $metadata.input_hashes.PSObject.Properties){
        $path=$item.Name
        if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.json','.cpp','.h'){$path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($path))}
        if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Frozen case input changed: $path"};$hashes[$path]=$item.Value
    }
    foreach($path in @("$folder/run.log","$folder/result.json","$folder/input_hashes_before.json")+@(Get-ChildItem "$folder/snap" -Recurse -File | ForEach-Object {$_.FullName})){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
    $extra=@();if($spec[7]){$extra+='--followup'}
    python "$PSScriptRoot/verify_current_post_ending_specials.py" $folder --source $spec[1] --target $spec[2] --source-side $spec[3] --new-side $spec[4] --mode $spec[5] --victim $spec[6] @extra | Out-File "$out/$name.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Current native special proof failed: $name"}
    $proof=Get-Content "$out/$name.json" -Raw | ConvertFrom-Json
    $cases+=[ordered]@{name=$name;passed=$proof.passed;source=$spec[1];target=$spec[2];source_side=$spec[3];new_side=$spec[4];mode=$spec[5];victim=$proof.victim;followup=$proof.followup;scope=$proof.scope}
}
# Keep the narrowly failed short-walk fixture and both pilots as actual history.
# The v320 pilot's gameplay log passes independently, but its wrapper failed
# argument splatting. Neither cold pilot is promoted to an ending proof.
foreach($name in 'audit_v319_current_air_p2_subzero_followup','audit_v320_subzero_follow_walk_pilot','audit_v321_subzero_follow_walk_pilot'){
    $folder=Join-Path $root $name
    foreach($path in @("$folder/run.log","$folder/result.json","$folder/input_hashes_before.json")+@(Get-ChildItem "$folder/input_sources" -File | ForEach-Object {$_.FullName})+@(Get-ChildItem "$folder/snap" -Recurse -File | ForEach-Object {$_.FullName})){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$modules=@($prior.reference_modules)+@('test_current_post_ending_specials')
$expected=580+(Select-String "$PSScriptRoot/test_current_post_ending_specials.py" -Pattern '^    def test_').Count
Push-Location $PSScriptRoot
try {python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8;if($LASTEXITCODE -ne 0){throw 'Reference suite failed'}} finally {Pop-Location}
$log=Get-Content "$out/reference_tests.log" -Raw
if($log -notmatch "Ran $expected tests" -or $log -notmatch '(?m)^OK\s*$'){throw 'Incomplete reference suite'}
& "$candidate/mkport_candidate.exe" -rompath "$candidate/roms;$root/roms" -verifyroms mk2ks | Out-File "$out/current_roms.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Current ROM verification failed'}
& "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File "$out/launcher_roms.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Existing launcher ROM verification failed'}
foreach($path in $hashes.Keys){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Inputs/evidence changed: $path"}}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_after.json" -Encoding utf8
[ordered]@{passed=$true;candidate=$build.name;candidate_executable_sha256=$build.executable_sha256;payload_sha256=$build.payload_sha256;
    current_ending_special_cases=$cases;reference_tests_passed=$expected;reference_modules=$modules;checked_evidence_files=$hashes.Count;
    production_unchanged=$true;source_campaign_assistance='health_only_all_events_before_attract';restart_assistance='none';
    whole_character_integration_complete=$false;
    scope='six_current_full_endings_fresh_CPU_games_pair_choreography_both_slots_airthrow_both_slots_and_actual_normal_control_followups_not_every_victim_CPU_action_finisher_or_full_goal';
    retained_failures='v319 P2 airthrow recovered but followup punch missed with eight walk fields; remains rejected. v320 cold pilot wrapper argument failure remains failed; v321 rerun uses 24 actual Subzero walk fields and full independent contact proof';
    remaining='Successful CPU paired-contact/choreography and air throw coverage, stock projectiles, finisher/victim/artwork/audio QA, wider unassisted play, roster-consumer audit and final matched launcher/ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Six current ending/native-special cases and $expected tests verified"
