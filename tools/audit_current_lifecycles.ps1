param([string]$OutputName='audit_v288_lifecycle_final_inputs')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($OutputName -notmatch '^audit_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned evidence directory'}
$out=Join-Path $root $OutputName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$build=Get-Content "$root/diagnostic_v277_native_battle_photos/build-info.json" -Raw | ConvertFrom-Json
foreach($item in $build.input_hashes.PSObject.Properties){if((Get-FileHash -LiteralPath $item.Name).Hash -ne $item.Value){throw "Production input changed: $($item.Name)"}}
$exe="$root/diagnostic_v277_native_battle_photos/mkport_candidate.exe"
$payload="$root/diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata"
if((Get-FileHash $exe).Hash -ne $build.executable_sha256 -or (Get-FileHash $payload).Hash -ne $build.payload_sha256){throw 'Playable build changed'}
New-Item -ItemType Directory -Path $out | Out-Null
$cases=@()
foreach($move in 'blade','bicycle'){foreach($side in 1,2){
    $victim=if($move -eq 'blade'){'sonya'}else{'kano'}
    $prefix=if($move -eq 'bicycle'){'boundary_'}else{''}
    $name="audit_v288_${prefix}${move}_p${side}_${victim}"
    $folder=Join-Path $root $name
    $original=Get-Content "$folder/result.json" -Raw | ConvertFrom-Json
    if(-not $original.observer_passed -or $original.exit_code -ne 0 -or $original.cheats -or $original.memory_assistance -ne 'none'){throw "Original lifecycle not accepted: $name"}
    $hashes=Get-Content "$folder/input_hashes_before.json" -Raw | ConvertFrom-Json
    $archived=0
    foreach($item in $hashes.PSObject.Properties){
        $path=if([IO.Path]::GetExtension($item.Name) -in '.lua','.ps1'){Join-Path "$folder/input_sources" ([IO.Path]::GetFileName($item.Name))}else{$item.Name}
        if((Get-FileHash -LiteralPath $path).Hash -ne $item.Value){throw "Original launch input changed: $path"}
        if($path -like '*input_sources*'){$archived++}
    }
    python "$PSScriptRoot/verify_current_lifecycle.py" "$folder/run.log" --move $move --side $side --victim $victim |
        Out-File "$out/${name}_independent.json" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw "Independent actual trace rejected: $name"}
    $cases+=[ordered]@{name=$name;move=$move;side=$side;victim=$victim;original_observer_pass=$true;latest_independent_pass=$true;
        archived_launch_scripts_verified=$archived;log_sha256=(Get-FileHash "$folder/run.log").Hash;
        original_result_sha256=(Get-FileHash "$folder/result.json").Hash}
}}
$prior=Get-Content "$root/audit_v287_followup_final_inputs/result.json" -Raw | ConvertFrom-Json
if(-not $prior.passed -or $prior.reference_tests_passed -ne 315){throw 'Previous checkpoint missing'}
$modules=@($prior.reference_modules)+@('test_current_lifecycle')
$newTests=(Select-String -LiteralPath "$PSScriptRoot/test_current_lifecycle.py" -Pattern '^    def test_').Count
$expected=315+$newTests
Push-Location $PSScriptRoot
try {
    python -m unittest @modules -v 2>&1 | Out-File "$out/reference_tests.log" -Encoding utf8
    if($LASTEXITCODE -ne 0){throw 'Reference suite failed'}
} finally {Pop-Location}
$log=Get-Content "$out/reference_tests.log" -Raw
if($log -notmatch "Ran $expected tests" -or $log -notmatch '(?m)^OK\s*$'){throw 'Incomplete reference suite'}
& "$root/PLAY_MK2_KANO_SONYA.cmd" -verifyroms mk2ks | Out-File "$out/launcher_verify.log" -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Actual launcher ROM check failed'}
$current=[ordered]@{}
foreach($path in @($PSCommandPath,"$PSScriptRoot/run_current_lifecycle.ps1","$PSScriptRoot/verify_current_lifecycle.py",
    "$PSScriptRoot/test_current_lifecycle.py","$root/mk2ks_lifecycle_trace.lua","$root/mk2ks_blade_lifecycle_test.lua",
    "$root/mk2ks_bicycle_lifecycle_test.lua",$exe,$payload,"$root/PLAY_MK2_KANO_SONYA.cmd")){$current[$path]=(Get-FileHash -LiteralPath $path).Hash}
[ordered]@{passed=$true;cases=$cases;production_inputs_match_v277=$true;production_game_changed=$false;
    reference_tests_passed=$expected;reference_modules=$modules;current_inputs=$current;
    scope='current_v277_unassisted_cold_two_human_blade_8_cycles_and_bicycle_9_cycles_both_slots_native_KO_full_health_next_round';
    full_integration_complete=$false;unassisted_CPU_tower_proven=$false;post_ending_full_choreography_proven=$false;
    preserved_diagnostics='Original bicycle traces without bound/velocity observations remain insufficient for strict acceptance';
    remaining='full post-ending and more-victim choreography; other moves full damage/effect parity; CPU and wider continue/join; whole-game audio/visual QA; release ZIP'} |
    ConvertTo-Json -Depth 6 | Out-File "$out/result.json" -Encoding utf8
"Four full current lifecycle cases, archived inputs, v277, $expected tests and root CMD verified"
