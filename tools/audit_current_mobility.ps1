param([string]$OutputName='audit_v314_current_mobility_checked_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use versioned evidence names'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$candidate=Join-Path $root 'diagnostic_v300_native_projectile_choreography'
$build=Get-Content "$candidate/build-info.json" -Raw | ConvertFrom-Json
$prior=Get-Content "$root/audit_v311_current_post_ending_checked_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $prior.passed -or $prior.reference_tests_passed -ne 549 -or $prior.candidate_executable_sha256 -ne $build.executable_sha256 -or $prior.payload_sha256 -ne $build.payload_sha256){throw 'Previous matched checkpoint missing'}
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Build input changed: $($item.Name)"}}
if((Get-FileHash "$candidate/mkport_candidate.exe").Hash -ne $build.executable_sha256 -or (Get-FileHash "$candidate/roms/mk2ks/mk2ks.mdata").Hash -ne $build.payload_sha256){throw 'Build identity mismatch'}
New-Item -ItemType Directory -Path "$out/input_sources" | Out-Null
$hashes=[ordered]@{}
$tracked=@($PSCommandPath,"$PSScriptRoot/run_join_mobility_probe.ps1","$root/mk2ks_join_mobility_probe.lua",
    "$root/mk2ks_mobility_contact.lua","$root/mk2ks_restart_lifecycle.lua","$root/mk2ks_selector_exit_test.lua",
    "$root/PLAY_MK2_KANO_SONYA.cmd","$candidate/mkport_candidate.exe","$candidate/roms/mk2ks/mk2ks.mdata",
    "$candidate/build-info.json","$root/audit_v311_current_post_ending_checked_inputs/result.json")
$tracked+=@(Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.py' | ForEach-Object {$_.FullName})
$tracked+=@($build.input_hashes.PSObject.Properties | ForEach-Object {$_.Name})
foreach($path in $tracked){
    $hashes[$path]=(Get-FileHash -LiteralPath $path).Hash
    if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.cpp','.h'){Copy-Item -LiteralPath $path -Destination "$out/input_sources"}
}
$cases=@()
foreach($target in 'kano','sonya'){foreach($side in 1,2){foreach($scenario in 'hit','block','miss'){
    $move=if($target -eq 'kano'){'ball'}else{'square'}
    $name="audit_v312_current_${move}_${scenario}_p$side";$folder=Join-Path $root $name
    $metadata=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    foreach($item in $metadata.input_hashes.PSObject.Properties){
        $path=$item.Name
        if([IO.Path]::GetExtension($path) -in '.lua','.ps1','.py','.json'){$path=Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($path))}
        if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Frozen case input changed: $path"};$hashes[$path]=$item.Value
    }
    foreach($path in @("$folder/run.log","$folder/result.json","$folder/input_hashes_before.json","$folder/independent_verification.json")+@(Get-ChildItem "$folder/snap" -Recurse -File | ForEach-Object {$_.FullName})){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
    python "$PSScriptRoot/verify_current_mobility.py" $folder --target $target --side $side --scenario $scenario | Out-File "$out/$name.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Current native contact failed: $name"}
    $proof=Get-Content "$out/$name.json" -Raw | ConvertFrom-Json
    $cases+=[ordered]@{name=$name;target=$target;side=$side;scenario=$scenario;passed=$proof.passed;fields=$proof.contact.fields;damage=$proof.contact.damage;flight_fields=$proof.contact.flight_fields;scope=$proof.scope}
}}
}
$hashes | ConvertTo-Json | Out-File "$out/input_hashes_before.json" -Encoding utf8
$modules=@($prior.reference_modules)+@('test_current_mobility')
$expected=549+(Select-String "$PSScriptRoot/test_current_mobility.py" -Pattern '^    def test_').Count
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
    current_mobility_cases=$cases;reference_tests_passed=$expected;reference_modules=$modules;checked_evidence_files=$hashes.Count;
    production_unchanged=$true;memory_assistance='none';whole_character_integration_complete=$false;
    scope='twelve_current_input_only_cold_native_CPU_starts_real_joins_full_mobility_hit_block_miss_and_followup_not_post_ending_CPU_variety_or_audio';
    remaining='Current remaining close/air throws, natural full CPU move variety, stock projectile regressions, finisher/victim/artwork/audio QA, wider unassisted play and final matched launcher/ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Current twelve mobility paths and $expected tests verified; launcher unchanged"
