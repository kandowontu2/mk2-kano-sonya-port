param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [ValidateSet('kano','sonya')][string]$Fighter='sonya',
    [ValidateSet('kano','sonya','sub_zero')][string]$Opponent='kano',
    [string]$CandidateName='diagnostic_v272_blue_palette_trial',
    [ValidateRange(110,1800)][int]$Seconds=150,
    [ValidateSet('existing','uppercut','standing_hk','projectile_guard')][string]$Strategy='existing',
    [switch]$RequireAdvance,
    [switch]$AssertIndependent,
    [switch]$ObserveScene,
    [switch]$TraceCyan,
    [switch]$StopOnLoss,
    [switch]$RequireBaseAcceptance
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence name'}
if($CandidateName -notmatch '^diagnostic_v[0-9]+_[a-z0-9_]+$'){throw 'Use a versioned candidate'}
$candidate=Join-Path $root $CandidateName
$exe=Join-Path $candidate 'mkport_candidate.exe'
$rompath=Join-Path $candidate 'roms'
$campaignHarness=Join-Path $root 'mk2ks_p2_campaign_probe.lua'
$harness=if($TraceCyan){Join-Path $root 'mk2ks_cyan_background_trace.lua'}elseif($ObserveScene){Join-Path $root 'mk2ks_p2_visual_probe.lua'}else{$campaignHarness}
$tracked=@($exe,(Join-Path $rompath 'mk2ks/mk2ks.mdata'),$harness,$PSCommandPath,
    (Join-Path $root 'mk2ks_finish_range_test.lua'),(Join-Path $root 'mk2ks_finish_state_trace.lua'),
    (Join-Path $root 'mk2ks_selector_exit_test.lua'),(Join-Path $root 'mk2ks_native_shang_morph.lua'))
if($ObserveScene -or $TraceCyan){$tracked+=$campaignHarness}
$verifier=Join-Path $PSScriptRoot 'verify_p2_campaign.py'
if($AssertIndependent){$tracked+=@($verifier,(Join-Path $root 'mk2/mk2-maincpu.bin'))}
if($RequireAdvance -and -not $AssertIndependent){throw 'RequireAdvance needs the independent schedule verifier'}
$hashes=@{}
foreach($path in $tracked){$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw 'Refusing to overwrite evidence'}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_CAMPAIGN_)'} | ForEach-Object {$saved[$_.Name]=$_.Value}
New-Item -ItemType Directory -Path $out | Out-Null
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_CAMPAIGN_)'} | Remove-Item
    $env:MK2KS_TEST_FIGHTER=$Opponent;$env:MK2KS_P2_FIGHTER=$Fighter
    $env:MK2KS_TEST_CONFIRM='hp';$env:MK2KS_TEST_CONFIRM_HOLD='8';$env:MK2KS_TWO_PLAYER='1'
    $env:MK2KS_TEST_ROUND_LOSS='1';$env:MK2KS_ASSERT_NATIVE_DISPLAY='1';$env:MK2KS_ASSERT_HUD_SHADOW='1'
    $env:MK2_TRACE_NATIVE_FINISH=$Fighter;$env:MK2_TRACE_NATIVE_FINISH_SIDE='2'
    $env:MK2_TRACE_INPUT_ONLY_APPROACH='1';$env:MK2_TRACE_FINISH_ACTORS='1'
    $env:MK2_RANGE_EXPECT='activate'
    $env:MK2_RANGE_MULTIPLE_FINISHES='1'
    $env:MK2_P2_CAMPAIGN_STRATEGY=$Strategy
    if($StopOnLoss){$env:MK2_P2_CAMPAIGN_STOP_ON_LOSS='1'}
    if($Fighter -eq 'kano'){$env:MK2_TRACE_SKELETON_OBJECT='1'}
    & $exe mk2ks -rompath "$rompath;$root/roms" -artpath "$root/artwork" -skip_gameinfo -nocheat `
        -video none -sound none -nothrottle -str $Seconds -snapsize 400x300 `
        -cfg_directory "$out/cfg" -nvram_directory "$out/nvram" -snapshot_directory "$out/snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out/run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($path in $tracked){if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]){throw "Input changed: $path"}}
    $log=Get-Content -LiteralPath "$out/run.log" -Raw
    $campaign=$log.Contains('MK2_P2_CAMPAIGN_RESULT pass=true ')
    $base=$log.Contains('MK2KS_EXIT_RESULT pass=true ')
    $independent=$null
    if($AssertIndependent){
        $verifyArgs=@("$out/run.log",'--fighter',$Fighter)
        if($RequireAdvance){$verifyArgs+='--require-advance'}
        & python $verifier @verifyArgs | Out-File -LiteralPath "$out/campaign_verification.json" -Encoding utf8
        $independent=$LASTEXITCODE -eq 0
    }
    $passed=$exitCode -eq 0 -and $campaign -and (-not $RequireBaseAcceptance -or $base) -and
        $log.Contains('MK2_RANGE_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    if($AssertIndependent){$passed=$passed -and $independent}
    [ordered]@{passed=$passed;campaign_identity_passed=$campaign;base_acceptance_passed=$base;
        independent_campaign_passed=$independent;advance_required=[bool]$RequireAdvance;
        base_acceptance_required=[bool]$RequireBaseAcceptance;fighter=$Fighter;opponent=$Opponent;
        stop_on_loss=[bool]$StopOnLoss;
        exit_code=$exitCode;seconds=$Seconds;strategy=$Strategy;assistance='none';cheats_enabled=$false;
        scope='published_p2_campaign_identity_not_whole_game';input_hashes=$hashes} |
        ConvertTo-Json -Depth 4 | Out-File -LiteralPath "$out/result.json" -Encoding utf8
    Write-Output "$CaseName pass=$passed campaign=$campaign base=$base"
    if(-not $passed){throw 'P2 campaign observation failed'}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -match '^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_CAMPAIGN_)'} | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
