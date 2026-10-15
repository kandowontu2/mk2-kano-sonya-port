param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kung_lao','liu_kang','cage','baraka','kitana','mileena',
        'shang_tsung','raiden','sub_zero','reptile','scorpion','jax')]
    [string[]]$Victims=@('kung_lao','liu_kang','cage','baraka','kitana','mileena',
        'shang_tsung','raiden','sub_zero','reptile','scorpion','jax'),
    [switch]$AssertWinnerHold,
    [switch]$AssertSkeletonSync,
    [switch]$AssertVictimSync,
    [switch]$AssertNativeJaxBody,
    [switch]$AssertNativeStockBody,
    [ValidateRange(74,180)][int]$Seconds=74
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') {throw 'Use a simple evidence prefix'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $root 'mk2ks_finish_state_trace.lua'
$baseHarness=Join-Path $root 'mk2ks_selector_exit_test.lua'
$holdHarness=Join-Path $root 'mk2ks_kano_winner_hold_test.lua'
$jaxBodyHarness=Join-Path $root 'mk2ks_native_jax_body_test.lua'
$stockBodyHarness=Join-Path $root 'mk2ks_native_stock_body_test.lua'
$syncVerifier=Join-Path $PSScriptRoot 'verify_skeleton_sync.py'
$victimVerifier=Join-Path $PSScriptRoot 'verify_kano_victim_sync.py'
$tracked=@($Executable,$payload,$harness,$baseHarness,$PSCommandPath)
if($AssertWinnerHold){$tracked+=$holdHarness}
if($AssertNativeJaxBody){
    if(-not $AssertWinnerHold){throw 'Native Jax body assertion includes the winner-hold gate'}
    if($Seconds -lt 100){throw 'Native Jax palette ownership requires observing the next native scene reset'}
    $tracked+=$jaxBodyHarness
}
if($AssertNativeStockBody){
    if($AssertNativeJaxBody){throw 'Choose the stock or legacy Jax observer, not both'}
    if(-not $AssertWinnerHold -or -not $AssertVictimSync){throw 'Stock body acceptance requires winner and six-phase victim gates'}
    if($Seconds -lt 100){throw 'Stock palette ownership requires the next native scene reset'}
    $tracked+=$stockBodyHarness
}
if($AssertSkeletonSync -or $AssertVictimSync){$tracked+=$syncVerifier}
if($AssertVictimSync){$tracked+=$victimVerifier}
$runHarness=if($AssertWinnerHold){$holdHarness}else{$harness}
if($AssertNativeJaxBody){$runHarness=$jaxBodyHarness}
if($AssertNativeStockBody){$runHarness=$stockBodyHarness}
$hashes=@{}
foreach ($file in $tracked) {$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
    ForEach-Object {$saved[$_.Name]=$_.Value}
$failed=@()
Push-Location $root
try {
    foreach ($victim in $Victims) {
        foreach ($file in $tracked) {
            if ((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) {throw "Input changed: $file"}
        }
        $reference=Get-Content -LiteralPath (Join-Path $root "diagnostic_v151_stock_prone_${victim}\run.log") -Raw
        $held=[regex]::Match($reference,'MK2_STOCK_VICTIM_HELD[^\r\n]*id=(\d+) health=0 pose=([0-9A-F]{8})')
        if (-not $held.Success) {throw "Missing reference held pose: $victim"}
        $idHex='{0:X4}' -f [int]$held.Groups[1].Value
        $pose=$held.Groups[2].Value
        # Native Jax body acceptance uses the fatality's headless final floor
        # pose, not his ordinary knockdown or the rejected MK3 donor body.
        if ($victim -eq 'jax') {$pose=if($AssertNativeJaxBody){'FF997BE0'}else{'FE9B3330'}}
        if($AssertNativeStockBody){
            $stockExpected=& python -c "import sys,json;sys.path.insert(0,sys.argv[1]);from verify_kano_victim_sync import VICTIMS;i,g=VICTIMS[sys.argv[2]];print(json.dumps({'id':i,'pose':format(g[-1],'08X')}))" $PSScriptRoot $victim | ConvertFrom-Json
            if($LASTEXITCODE -ne 0 -or $stockExpected.id -ne [int]$held.Groups[1].Value){throw 'Native reference identity mismatch'}
            $pose=$stockExpected.pose
        }
        if($AssertNativeJaxBody -and $victim -ne 'jax'){throw 'Native Jax body observer requires Jax versus Kano'}
        Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
            Remove-Item
        $env:MK2KS_TEST_FIGHTER=$victim
        $env:MK2KS_P2_FIGHTER='kano'
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_TEST_ROUND_LOSS='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2_TRACE_NATIVE_FINISH='kano'
        $env:MK2_TRACE_NATIVE_FINISH_SIDE='2'
        $env:MK2_TRACE_INPUT_ONLY_APPROACH='1'
        $env:MK2_TRACE_FINISH_ACTORS='1'
        $env:MK2_TRACE_SKELETON_OBJECT='1'
        if($AssertNativeJaxBody){$env:MK2_TRACE_VICTIM_PHASE_SNAPSHOTS='1'}
        if($AssertNativeStockBody){$env:MK2_TRACE_VICTIM_PHASE_SNAPSHOTS='1'}
        if($AssertWinnerHold){
            $env:MK2_TRACE_EXPECT_VICTIM_HELD_POSE=$pose
            $env:MK2_TRACE_EXPECT_VICTIM_ID=$idHex
        }
        $case="${CasePrefix}_${victim}"
        $out=Join-Path $root $case
        if (Test-Path -LiteralPath $out) {throw "Evidence exists: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        & $Executable mk2ks -rompath "$PayloadRomDirectory;$root\roms_v22_clean;$root\roms" `
            -artpath "$root\artwork" -skip_gameinfo -video none -sound none -nothrottle `
            -str $Seconds -snapsize 400x300 -cfg_directory "$out\cfg" `
            -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $runHarness 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $posePattern="MK2_FINISH_ACTORS[^\r\n]*age=(?:2[5-9]\d|3\d\d)[^\r\n]*p1=[^\r\n]*:${idHex}:${pose}:"
        # Without the flex, actor-state change logging no longer repeats the
        # unchanged victim at age 272. Assert the actual published victim on
        # every winner field instead of depending on that incidental log line.
        $heldValidated=if($AssertWinnerHold){
            $log.Contains('MK2_KANO_VICTIM_HOLD_RESULT pass=true ')
        }else{$log -match $posePattern}
        $passed=$exitCode -eq 0 -and $heldValidated -and
            $log.Contains('MK2_FINISH_INPUT_APPROACH ') -and
            $log.Contains('MK2_FINISH_SKELETON ') -and
            $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
            $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
            $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
            $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
            $log -match 'MK2KS_NATIVE_WIN[^\r\n]*winner=0011' -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        if ($victim -eq 'jax' -and -not $AssertNativeStockBody) {
            $passed=$passed -and $(if($AssertNativeJaxBody){
                $log.Contains('MK2_NATIVE_JAX_BODY_RESULT pass=true ')
            }else{$log.Contains('MK2_FINISH_JAX_VICTIM_PALETTE ')})
        }
        $stockBodyValidated=$null
        if($AssertNativeStockBody){
            $stockBodyValidated=$log.Contains('MK2_NATIVE_STOCK_BODY_RESULT pass=true ')
            $passed=$passed -and $stockBodyValidated
        }
        $holdValidated=$null
        if($AssertWinnerHold){
            $holdValidated=$log.Contains('MK2_KANO_WINNER_HOLD_RESULT pass=true ')
            $passed=$passed -and $holdValidated
        }
        $syncValidated=$null
        $victimSyncValidated=$null
        if($AssertVictimSync){
            & python $victimVerifier "$out\run.log" --side 2 --victim $victim |
                Out-File -LiteralPath "$out\victim_sync.json" -Encoding utf8
            $victimSyncValidated=$LASTEXITCODE -eq 0
            $passed=$passed -and $victimSyncValidated
        }
        if($AssertSkeletonSync){
            & python $syncVerifier "$out\run.log" --side 2 |
                Out-File -LiteralPath "$out\skeleton_sync.json" -Encoding utf8
            $syncValidated=$LASTEXITCODE -eq 0
            $passed=$passed -and $syncValidated
        }
        [ordered]@{case=$case;passed=$passed;victim=$victim;held_pose=$pose;
            seconds=$Seconds;native_jax_body_asserted=$AssertNativeJaxBody.IsPresent;
            native_stock_body_validated=$stockBodyValidated;
            native_stock_body_harness_sha256=if($AssertNativeStockBody){$hashes[$stockBodyHarness]}else{$null};
            native_jax_body_harness_sha256=if($AssertNativeJaxBody){$hashes[$jaxBodyHarness]}else{$null};
            exit_code=$exitCode;executable_sha256=$hashes[$Executable];
            payload_sha256=$hashes[$payload];harness_sha256=$hashes[$harness];
            base_harness_sha256=$hashes[$baseHarness];skeleton_sync_validated=$syncValidated;
            victim_sync_validated=$victimSyncValidated;
            victim_sync_verifier_sha256=if($AssertVictimSync){$hashes[$victimVerifier]}else{$null};
            victim_hold_validated=$heldValidated;
            winner_hold_validated=$holdValidated;
            winner_hold_harness_sha256=if($AssertWinnerHold){$hashes[$holdHarness]}else{$null}} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed held_pose=$pose"
        if (-not $passed) {$failed+=$case}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
        Remove-Item
    foreach ($key in $saved.Keys) {Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
if ($failed.Count) {throw "P2 finisher victim cases failed: $($failed -join ', ')"}
