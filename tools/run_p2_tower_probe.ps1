param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [ValidateSet('kano','sonya')][string]$Fighter='kano',
    [string]$CandidateName='diagnostic_v272_blue_palette_trial',
    [ValidateRange(150,2600)][int]$Seconds=2200,
    [switch]$NoAssistance
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence name'}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned candidate'}
$candidate=Join-Path $root $CandidateName
$exe=Join-Path $candidate 'mkport_candidate.exe'
$rompath=Join-Path $candidate 'roms'
$harness=Join-Path $root 'mk2ks_p2_tower_probe.lua'
$verifier=Join-Path $PSScriptRoot 'verify_p2_tower.py'
$tracked=@($exe,(Join-Path $rompath 'mk2ks/mk2ks.mdata'),$harness,$PSCommandPath,
    (Join-Path $root 'mk2ks_finish_range_test.lua'),(Join-Path $root 'mk2ks_finish_state_trace.lua'),
    (Join-Path $root 'mk2ks_selector_exit_test.lua'),(Join-Path $root 'mk2ks_native_shang_morph.lua'),
    (Join-Path $root 'mk2/mk2-maincpu.bin'),$verifier,(Join-Path $PSScriptRoot 'verify_p2_campaign.py'))
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=if($Fighter -eq 'kano'){'sonya'}else{'kano'}
    $env:MK2KS_P2_FIGHTER=$Fighter
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='1'
    $env:MK2KS_TEST_ROUND_LOSS='1';$env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    $env:MK2_TRACE_NATIVE_FINISH=$Fighter;$env:MK2_TRACE_NATIVE_FINISH_SIDE='2'
    $env:MK2_TRACE_INPUT_ONLY_APPROACH='1';$env:MK2_TRACE_FINISH_ACTORS='1'
    $env:MK2_RANGE_EXPECT='activate';$env:MK2_RANGE_MULTIPLE_FINISHES='1'
    if(-not $NoAssistance){$env:MK2_P2_TOWER_HEALTH_ASSIST='1'}
    & $exe mk2ks -rompath "$rompath;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat `
        -inipath "$out" -video none -sound none -nothrottle -str $Seconds -snapsize 400x300 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $tower=$log.Contains('MK2_P2_TOWER_RESULT pass=true ')
    $base=$log.Contains('MK2KS_EXIT_RESULT pass=true ')
    & python $verifier "$out/run.log" --fighter $Fighter |
        Out-File -LiteralPath "$out/tower_verification.json" -Encoding utf8
    $independent=$LASTEXITCODE -eq 0
    $required=@(0..12)+@(14,15,16)
    $missingSnapshots=@($required | Where-Object {-not (Test-Path -LiteralPath (Join-Path $out ('snap/p2_tower_stage_{0:d2}.png' -f $_)))})
    $passed=$exitCode -eq 0 -and $tower -and $base -and $independent -and $missingSnapshots.Count -eq 0 -and $log.Contains('MK2_RANGE_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    [ordered]@{passed=$passed;tower_observer_passed=$tower;base_acceptance_passed=$base;independent_verification=$independent;
        missing_stage_snapshots=$missingSnapshots;fighter=$Fighter;
        exit_code=$exitCode;seconds=$Seconds;assistance=if($NoAssistance){'none'}else{'health_only'};
        cheats_enabled=$false;unassisted_clear_proven=$false;
        scope='full_p2_tower_structure_not_unassisted_clear';input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed tower=$tower base=$base"
    if(-not $passed){throw 'P2 full tower acceptance failed; preserve evidence'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
