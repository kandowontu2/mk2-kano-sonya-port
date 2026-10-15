param(
    [Parameter(Mandatory=$true)][string]$CaseName,
    [Parameter(Mandatory=$true)][string]$Executable,
    [ValidateSet(8,14,15,16)][int]$HiddenId=14,
    [ValidateSet('left','right')][string]$Direction='left',
    [ValidateSet('walk','mid_guard','edge_guard','edge_jump')][string]$Strategy='edge_jump',
    [Nullable[int]]$StageIndex=$null,
    [ValidateRange(425,475)][int]$JumpStartAge=451,
    [switch]$ReactToAirborne,
    [ValidateSet('immediate','guard_then_jump','preemptive_air_block')][string]$ReactionStyle='immediate',
    [switch]$TraceAirbornePrep,
    [switch]$AssistP1Health,
    [int]$Seconds=140
)
$ErrorActionPreference='Stop'
if($CaseName -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Use a simple evidence name.'}
$root=Split-Path $PSScriptRoot -Parent
if($null -ne $StageIndex -and ($StageIndex -lt 0 -or $StageIndex -gt 16)){
    throw 'StageIndex must be 0..16.'
}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$rom=(Resolve-Path -LiteralPath (Join-Path $root 'roms\mk2.zip')).Path
$harness=Join-Path $root 'mk2ks_hidden_cpu_corner_probe.lua'
$tracked=@($Executable,$rom,$harness,(Join-Path $root 'mk2ks_selector_exit_test.lua'),$PSCommandPath)
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
    $env:MK2KS_HIDDEN_STOCK_JAX_CONTROL='1'
    $env:MK2KS_TEST_FIGHTER='jax'
    $env:MK2KS_TEST_CONFIRM='hp'
    $env:MK2KS_TEST_CONFIRM_HOLD='8'
    $env:MK2KS_TWO_PLAYER='0'
    $env:MK2KS_TEST_ROUND_WIN='0'
    $env:MK2KS_DIAGNOSTIC_CPU_ID="$HiddenId"
    $env:MK2KS_HIDDEN_CORNER_DIRECTION=$Direction
    $env:MK2KS_HIDDEN_CORNER_STRATEGY=$Strategy
    $env:MK2KS_HIDDEN_JUMP_START_AGE="$JumpStartAge"
    if($null -ne $StageIndex){$env:MK2KS_DIAGNOSTIC_LADDER_INDEX="$StageIndex"}
    if($ReactToAirborne){$env:MK2KS_HIDDEN_AIRTHROW_REACT='1'}
    $env:MK2KS_HIDDEN_REACTION_STYLE=$ReactionStyle
    if($TraceAirbornePrep){$env:MK2KS_HIDDEN_TRACE_AIRBORNE_PREP='1'}
    if($AssistP1Health){$env:MK2KS_DIAGNOSTIC_P1_REGEN='1'}
    & $Executable mk2 -rompath "$root\roms" -artpath "$root\artwork" `
        -skip_gameinfo -video none -sound none -nothrottle -str $Seconds `
        -snapsize 400x300 -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" `
        -snapshot_directory "$out\snap" -autoboot_script $harness 2>&1 |
        Out-File -LiteralPath "$out\run.log" -Encoding utf8
    $exitCode=$LASTEXITCODE
    foreach($file in $tracked){
        if((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]){throw "Input changed: $file"}
    }
    $log=Get-Content -LiteralPath "$out\run.log" -Raw
    $summary=[regex]::Match($log,'MK2KS_HIDDEN_CPU_EDGE_RESULT[^\r\n]*').Value
    $airMatch=[regex]::Match($summary,'(?:^|\s)non_launch_airborne_episodes=(\d+)')
    $nonLaunchObserved=$airMatch.Success -and [int]$airMatch.Groups[1].Value -gt 0
    $passed=$exitCode -eq 0 -and
        ($null -eq $StageIndex -or $log -match "MK2KS_STOCK_HIDDEN_STAGE frame=1100 old=\d+ requested=$StageIndex") -and
        $log -match "MK2KS_STOCK_HIDDEN_INJECT frame=\d+ old=\d+ requested=$HiddenId" -and
        $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
        $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
        $summary -match 'entered=true active=[1-9]' -and
        $summary -match "id=$HiddenId(\s|$)" -and
        $summary.Contains('stock_jax_control=true stock_injected=true') -and
        $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
    [ordered]@{case=$CaseName;passed=$passed;opponent_id=$HiddenId;
        direction=$Direction;strategy=$Strategy;diagnostic_stage_index=$StageIndex;
        jump_start_age=$JumpStartAge;react_to_airborne=$ReactToAirborne.IsPresent;
        reaction_style=$ReactionStyle;trace_airborne_prep=$TraceAirbornePrep.IsPresent;
        diagnostic_p1_health_assistance=$AssistP1Health.IsPresent;
        cpu_non_launch_airborne_observed=$nonLaunchObserved;
        exit_code=$exitCode;summary=$summary;
        executable_sha256=$hashes[$Executable];stock_rom_sha256=$hashes[$rom];
        harness_sha256=$hashes[$harness]} |
        ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
    Write-Output "$CaseName match_pass=$passed cpu_non_launch_airborne_observed=$nonLaunchObserved $summary"
    if(-not $passed){throw "Stock hidden CPU control failed: $CaseName"}
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach($key in $saved.Keys){Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
