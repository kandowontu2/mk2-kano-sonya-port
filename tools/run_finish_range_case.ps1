param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [ValidateSet('kano','sonya')][string]$Fighter='kano',
    [ValidateSet(1,2)][int]$Side=1,
    [ValidateRange(60,180)][int]$ApproachGap=65,
    [ValidateRange(0,180)][int]$RetreatGap=0,
    [ValidateSet('activate','reject')][string]$Expected='activate',
    [switch]$ObserveContact,
    [switch]$AssertNativeArc,
    [string]$CandidateName='diagnostic_v272_blue_palette_trial',
    [string]$PayloadRomDirectory='',
    [ValidateRange(75,150)][int]$Seconds=95
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence prefix'}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned candidate directory'}
$candidate=Join-Path $root $CandidateName
$exe=Join-Path $candidate 'mkport_candidate.exe'
$rompath=Join-Path $candidate 'roms'
if($PayloadRomDirectory){$rompath=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path}
$harness=Join-Path $root $(if($ObserveContact){'mk2ks_sonya_projectile_contact.lua'}else{'mk2ks_finish_range_test.lua'})
if($ObserveContact -and $Fighter -ne 'sonya'){throw 'Continuous projectile capture is for Sonya'}
if($AssertNativeArc -and (-not $ObserveContact -or $Expected -ne 'activate')){throw 'Native arc assertion requires a positive continuous Sonya capture'}
$out=Join-Path $root "${CasePrefix}_${Fighter}_side${Side}_gap${ApproachGap}"
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite range evidence'}
$tracked=@($exe,$harness,$PSCommandPath,(Join-Path $rompath 'mk2ks/mk2ks.mdata'),
    (Join-Path $root 'mk2ks_finish_state_trace.lua'),(Join-Path $root 'mk2ks_selector_exit_test.lua'),
    (Join-Path $root 'mk2ks_finish_range_test.lua'))
$arcVerifier=Join-Path $PSScriptRoot 'verify_sonya_native_arc.py'
if($AssertNativeArc){$tracked+=@($arcVerifier,(Join-Path $PSScriptRoot 'verify_sonya_contact_reference.py'),(Join-Path $root 'mk3/mk3-maincpu.bin'))}
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*' -or $_.Name -like 'MK2_RANGE_*'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*' -or $_.Name -like 'MK2_RANGE_*'} | Remove-Item
    $victim=if($Fighter -eq 'kano'){'sonya'}else{'kano'}
    $env:MK2KS_TEST_FIGHTER=if($Side -eq 1){$Fighter}else{$victim}
    $env:MK2KS_P2_FIGHTER=if($Side -eq 1){$victim}else{$Fighter}
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='1'
    if($Side -eq 1){$env:MK2KS_TEST_ROUND_WIN='1'}else{$env:MK2KS_TEST_ROUND_LOSS='1'}
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    $env:MK2_TRACE_NATIVE_FINISH=$Fighter;$env:MK2_TRACE_NATIVE_FINISH_SIDE="$Side"
    $env:MK2_TRACE_INPUT_ONLY_APPROACH='1';$env:MK2_TRACE_APPROACH_GAP="$ApproachGap"
    if($RetreatGap){
        if($RetreatGap -lt 60 -or $RetreatGap -gt $ApproachGap){throw 'Retreat gap must be 60..ApproachGap'}
        $env:MK2_TRACE_INITIAL_RETREAT_GAP="$RetreatGap"
    }
    $env:MK2_TRACE_FINISH_ACTORS='1';$env:MK2_TRACE_FINISH_SNAPSHOTS='1'
    $env:MK2_RANGE_EXPECT=$Expected
    if($Fighter -eq 'kano'){$env:MK2_TRACE_SKELETON_OBJECT='1'}
    & $exe mk2ks -rompath "$rompath;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat -video none -sound none -nothrottle -str $Seconds -snapsize 400x300 -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $passed=$exitCode -eq 0 -and $log.Contains('MK2_RANGE_RESULT pass=true ') -and
        $log.Contains('MK2_FINISH_INPUT_APPROACH ') -and $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    if($Expected -eq 'activate'){
        $effect=if($Fighter -eq 'kano'){'MK2_FINISH_SKELETON '}else{'MK2_FINISH_FIRE_PALETTE '}
        $winner=if($Fighter -eq 'kano'){'0011'}else{'0012'}
        $passed=$passed -and $log.Contains($effect) -and $log -match "MK2KS_NATIVE_WIN[^\r\n]*winner=$winner"
    }
    $arcVerified=$null
    if($AssertNativeArc){
        & python $arcVerifier "$out/run.log" --side $Side | Out-File -LiteralPath "$out/arc_verification.json" -Encoding utf8
        $arcVerified=$LASTEXITCODE -eq 0
        $passed=$passed -and $arcVerified
    }
    [ordered]@{passed=$passed;fighter=$Fighter;side=$Side;approach_gap=$ApproachGap;retreat_gap=$RetreatGap;expected=$Expected;
        exit_code=$exitCode;seconds=$Seconds;assistance='none';cheats_enabled=$false;position_writes_allowed=$false;
        native_arc_verified=$arcVerified;whole_game_fidelity_verified=$false;input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$out pass=$passed"
    if(-not $passed){throw 'Fatality range case failed'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*' -or $_.Name -like 'MK2_RANGE_*'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
