param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet(8,14,15,16,17,18)][int]$HiddenId=14,
    [ValidateSet('left','right')][string]$Direction='left',
    [ValidateSet('walk','mid_guard','edge_guard','edge_projectile','edge_projectile_guard','edge_jump','close_jump','pressure_uppercut')][string]$Strategy='walk',
    [Alias('ReactToJump')][switch]$ReactToAirborne,
    [ValidateSet('immediate','guard_then_jump','preemptive_air_block')][string]$ReactionStyle='immediate',
    [ValidateSet('any','action0200')][string]$ReactionTarget='any',
    [switch]$TraceAirbornePrep,
    [switch]$RequireCpuLaunch,
    [switch]$AssistP1Health,
    [Nullable[int]]$StageIndex=$null,
    [ValidateRange(425,475)][int]$JumpStartAge=451,
    [int]$Seconds=140
)
$ErrorActionPreference='Stop'
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence name.'}
if($null -ne $StageIndex -and ($StageIndex -lt 0 -or $StageIndex -gt 16)){
    throw 'StageIndex must be 0..16.'
}
$root=Split-Path $PSScriptRoot -Parent
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $root 'mk2ks_hidden_cpu_corner_probe.lua'
$tracked=@($Executable,$payload,$harness,(Join-Path $root 'mk2ks_cpu_ladder_trace.lua'),
    (Join-Path $root 'mk2ks_selector_exit_test.lua'),$PSCommandPath)
$hashes=@{}
foreach($file in $tracked){$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
$out=Join-Path $root $CaseName
if(Test-Path -LiteralPath $out){throw "Evidence exists: $out"}
New-Item -ItemType Directory -Path $out | Out-Null
$saved=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' |
    ForEach-Object {$saved[$_.Name]=$_.Value}
Push-Location $root
try {
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    $env:MK2KS_TEST_FIGHTER='kano'
    $env:MK2KS_TEST_CONFIRM='hp'
    $env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_TEST_ROUND_WIN='1'
    $env:MK2KS_ALLOW_NATURAL_LOSS='1'
    if($AssistP1Health){
        $env:MK2KS_DIAGNOSTIC_P1_REGEN='1'
        if($null -eq $StageIndex){$env:MK2KS_DIAGNOSTIC_ALL_STAGES='1'}
    }
    $env:MK2KS_DIAGNOSTIC_CPU_ID="$HiddenId"
    if($null -ne $StageIndex){$env:MK2KS_DIAGNOSTIC_LADDER_INDEX="$StageIndex"}
    $env:MK2KS_HIDDEN_CORNER_DIRECTION=$Direction
    $env:MK2KS_HIDDEN_CORNER_STRATEGY=$Strategy
    $env:MK2KS_HIDDEN_JUMP_START_AGE="$JumpStartAge"
    if($ReactToAirborne){$env:MK2KS_HIDDEN_AIRTHROW_REACT='1'}
    $env:MK2KS_HIDDEN_REACTION_STYLE=$ReactionStyle
    $env:MK2KS_HIDDEN_REACTION_TARGET=$ReactionTarget
    if($TraceAirbornePrep){$env:MK2KS_HIDDEN_TRACE_AIRBORNE_PREP='1'}
    $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
    $env:MK2KS_ASSERT_HUD_SHADOW='1'
    & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
        -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
        -str $Seconds -snapsize 400x300 -cfg_directory "$out\cfg" `
        -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
        -autoboot_script $harness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($file in $tracked){
        if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}
    }
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    $summary=[regex]::Match($log,'MK2KS_HIDDEN_CPU_EDGE_RESULT[^\r\n]*').Value
    $injectionOk=if($HiddenId -le 16){
        $log.Contains("MK2KS_CPU_DIAGNOSTIC_RESULT requested=$HiddenId injected=true")
    } else {
        $log -match "MK2KS_CPU_DIAGNOSTIC_RESULT requested=$HiddenId injected=(true|false)"
    }
    $candidateMatch=[regex]::Match($summary,'(?:^|\s)non_launch_airborne_episodes=(\d+)')
    $nonLaunchObserved=$candidateMatch.Success -and [int]$candidateMatch.Groups[1].Value -gt 0
    $knifeMatch=[regex]::Match($summary,'(?:^|\s)knife_entries=(\d+)')
    $knifeCount=if($knifeMatch.Success){[int]$knifeMatch.Groups[1].Value}else{0}
    $launchMatch=[regex]::Match($summary,'(?:^|\s)launch_like_episodes=(\d+)')
    $damageMatch=[regex]::Match($summary,'(?:^|\s)cpu_damage=(\d+)')
    $launched=$launchMatch.Success -and [int]$launchMatch.Groups[1].Value -gt 0 -and
        $damageMatch.Success -and [int]$damageMatch.Groups[1].Value -gt 0
    $knifeRequired=$Strategy -in @('edge_projectile','edge_projectile_guard')
    $passed=$exitCode -eq 0 -and
        $injectionOk -and
        $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
        $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
        $summary -match 'entered=true active=[1-9]' -and
        $summary -match "id=$HiddenId(\s|$)" -and
        (-not $knifeRequired -or $knifeCount -gt 0) -and
        (-not $RequireCpuLaunch -or $launched) -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    [ordered]@{case=$CaseName;passed=$passed;opponent_id=$HiddenId;direction=$Direction;
        diagnostic_stage_index=$StageIndex;
        react_to_airborne=$ReactToAirborne.IsPresent;require_cpu_launch=$RequireCpuLaunch.IsPresent;
        reaction_style=$ReactionStyle;reaction_target=$ReactionTarget;
        trace_airborne_prep=$TraceAirbornePrep.IsPresent;
        diagnostic_p1_health_assistance=$AssistP1Health.IsPresent;
        strategy=$Strategy;cpu_non_launch_airborne_observed=$nonLaunchObserved;
        jump_start_age=$JumpStartAge;
        cpu_launch_observed=$launched;
        knife_entries=$knifeCount;projectile_activated=($knifeCount -gt 0);exit_code=$exitCode;
        summary=$summary;executable_sha256=$hashes[$Executable];
        payload_sha256=$hashes[$payload];harness_sha256=$hashes[$harness]} |
        ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
    Write-Output "$CaseName match_pass=$passed cpu_non_launch_airborne_observed=$nonLaunchObserved $summary"
    if(-not $passed){throw "Hidden CPU edge probe failed: $CaseName"}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
