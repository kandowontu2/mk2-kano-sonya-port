param([string]$OutputName='audit_v318_natural_cpu_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$candidate=Join-Path $root 'diagnostic_v300_native_projectile_choreography'
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
$prior=Get-Content "$root/audit_v314_current_mobility_checked_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $prior.passed -or $prior.reference_tests_passed -ne 561 -or $prior.candidate_executable_sha256 -ne $build.executable_sha256 -or $prior.payload_sha256 -ne $build.payload_sha256){throw 'Previous matched current checkpoint missing'}
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build input changed: $($item.Name)"}}
if((Get-FileHash "$candidate/mkport_candidate.exe").Hash -ne $build.executable_sha256 -or (Get-FileHash "$candidate/roms/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Build identity mismatch'}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes=[ordered]@{}
$tracked=@($PSCommandPath,"$PSScriptRoot/run_cpu_owned_special.ps1","$root/mk2ks_natural_cpu_moves_probe.lua",
    "$root/mk2ks_cpu_ladder_trace.lua","$root/mk2ks_selector_exit_test.lua","$root/PLAY_MK2_KANO_SONYA.cmd",
    "$candidate/mkport_candidate.exe","$candidate/roms/mk2ks/mk2ks.mdata","$candidate/build-info.json",
    "$root/mk2/mk2-maincpu.bin","$root/audit_v314_current_mobility_checked_inputs/result.json")
$tracked+=@(Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.py' | ForEach-Object {$_.FullName})
$tracked+=@($build.input_hashes.PSObject.Properties | ForEach-Object {$_.Name})
foreach($path in $tracked){
    $hashes[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.cpp','.h'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}
}
$cases=@();$union=@();$fields=0;$returns=0;$children=0
foreach($suffix in 'kano_boot605','kano_boot606','sonya_boot601','sonya_boot604'){
    $name="audit_v317_natural_cpu_$suffix";$folder=Join-Path $root $name
    $metadata=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    foreach($item in $metadata.input_hashes.PSObject.Properties){
        $path=$item.Name
        if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.json'){$path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($path))}
        if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Frozen case input changed: $path"};$hashes[$path]=$item.Value
    }
    foreach($path in @("$folder/run.log","$folder/result.json","$folder/input_hashes_before.json")+@(Get-ChildItem "$folder/snap" -Recurse -File | ForEach-Object {$_.FullName})){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
    python "$PSScriptRoot/verify_natural_cpu_moves.py" $folder | Out-File "$out/$name.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Current natural CPU proof failed: $name"}
    $proof=Get-Content "$out/$name.json" -Raw | ConvertFrom-Json
    $union+=@($proof.observed_moves);$fields+=$proof.paired_fields;$returns+=@($proof.native_returns).Count;$children+=$proof.projectile_children
    $cases+=[ordered]@{name=$name;passed=$proof.passed;opponent=$proof.opponent;paired_fields=$proof.paired_fields;
        observed_moves=$proof.observed_moves;native_returns=@($proof.native_returns).Count;projectile_children=$proof.projectile_children;scope=$proof.scope}
}
$union=@($union | Sort-Object -Unique)
if(($union -join ',') -ne 'ball,bicycle,blade,choke,knife,leg,ring,square'){throw 'All eight naturally owned CPU move routes not observed'}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$modules=@($prior.reference_modules)+@('test_natural_cpu_moves')
$expected=561+(Select-String "$PSScriptRoot/test_natural_cpu_moves.py" -Pattern '^    def test_').Count
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
    natural_CPU_cases=$cases;observed_owned_moves=$union;paired_fields=$fields;native_returns=$returns;projectile_children=$children;
    reference_tests_passed=$expected;reference_modules=$modules;checked_evidence_files=$hashes.Count;
    production_unchanged=$true;memory_assistance='none';whole_character_integration_complete=$false;
    scope='four_actual_natural_CPU_ladder_cases_canonical_ownership_eight_move_dispatches_finite_native_returns_full_projectile_release_child_cadence_not_every_CPU_contact_pose_component_audio_or_unassisted_tower';
    retained_insufficient='v313 scouting and v315 preliminary observer records are not promoted to full current CPU proof; new v317 actual entry-time roles prove mid-field fight activation';
    remaining='Successful CPU paired-contact/choreography and air throw coverage, current close/air human regressions, stock projectiles, finisher/victim/artwork/audio QA, wider unassisted play and final matched launcher/ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Four natural CPU cases, all eight owned dispatches, $returns finite returns and $expected tests verified"
