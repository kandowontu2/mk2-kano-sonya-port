param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [string[]]$Pairs=@('kano:sonya','kano:jax','kano:sub_zero',
        'sonya:kano','sonya:jax','sonya:sub_zero'),
    [switch]$FineSnapshots,
    [switch]$PostFinishSceneSnapshots,
    [switch]$TraceSound,
    [ValidateRange(75,180)][int]$Seconds=95,
    [switch]$RequireCpuResume,
    [switch]$FirstSkeletonFields,
    [switch]$AssertSkeletonSync,
    [switch]$AssertWinnerHold,
    [switch]$AssertVictimSync,
    [switch]$RequireCpuWin,
    [switch]$VictimPhaseSnapshots,
    [switch]$AssertNativeJaxBody,
    [switch]$AssertNativeStockBody
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') {throw 'Use a simple evidence prefix'}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $root 'mk2ks_finish_state_trace.lua'
$holdHarness=Join-Path $root 'mk2ks_kano_winner_hold_test.lua'
$jaxBodyHarness=Join-Path $root 'mk2ks_native_jax_body_test.lua'
$stockBodyHarness=Join-Path $root 'mk2ks_native_stock_body_test.lua'
$baseHarness=Join-Path $root 'mk2ks_selector_exit_test.lua'
$syncVerifier=Join-Path $PSScriptRoot 'verify_skeleton_sync.py'
$victimVerifier=Join-Path $PSScriptRoot 'verify_kano_victim_sync.py'
$tracked=@($Executable,$payload,$harness,$baseHarness,$PSCommandPath)
if($AssertSkeletonSync -or $AssertVictimSync){$tracked+=$syncVerifier}
if($AssertVictimSync){$tracked+=$victimVerifier}
if($AssertWinnerHold){$tracked+=$holdHarness}
if($AssertNativeJaxBody){
    if(-not $AssertWinnerHold){throw 'Native Jax body assertion includes the winner-hold gate'}
    $tracked+=$jaxBodyHarness
}
if($AssertNativeStockBody){
    if($AssertNativeJaxBody){throw 'Choose the stock or legacy Jax observer, not both'}
    if(-not $AssertWinnerHold -or -not $AssertVictimSync){throw 'Stock body acceptance requires winner and six-phase victim gates'}
    if($Seconds -lt 100){throw 'Stock palette ownership requires the next native scene reset'}
    $tracked+=$stockBodyHarness
}
$hashes=@{}
foreach ($path in $tracked) {$hashes[$path]=(Get-FileHash -LiteralPath $path).Hash}
$saved=@{}
Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
    ForEach-Object {$saved[$_.Name]=$_.Value}
$failed=@()
Push-Location $root
try {
    foreach ($pair in $Pairs) {
        if ($pair -notmatch '^(kano|sonya):(kano|sonya|kung_lao|liu_kang|cage|baraka|kitana|mileena|shang_tsung|raiden|sub_zero|reptile|scorpion|jax)$') {
            throw "Unsupported finisher pair: $pair"
        }
        $fighter=$Matches[1]; $victim=$Matches[2]
        if($AssertWinnerHold -and $fighter -ne 'kano'){throw 'Winner-hold assertion is specific to Kano'}
        if($AssertVictimSync -and $fighter -ne 'kano'){throw 'Victim-pull synchronization is specific to Kano'}
        $runHarness=if($AssertWinnerHold){$holdHarness}else{$harness}
        if($AssertNativeJaxBody){
            if($pair -ne 'kano:jax'){throw 'Native Jax body observer requires Kano versus Jax'}
            $runHarness=$jaxBodyHarness
        }
        $stockExpected=$null
        if($AssertNativeStockBody){
            if($fighter -ne 'kano'){throw 'Stock body observer requires Kano as attacker'}
            $stockExpected=& python -c "import sys,json;sys.path.insert(0,sys.argv[1]);from verify_kano_victim_sync import VICTIMS;i,g=VICTIMS[sys.argv[2]];print(json.dumps({'id':i,'pose':format(g[-1],'08X')}))" $PSScriptRoot $victim | ConvertFrom-Json
            if($LASTEXITCODE -ne 0 -or $stockExpected.id -ge 12){throw 'Stock observer requires a native stock victim'}
            $runHarness=$stockBodyHarness
        }
        foreach ($path in $tracked) {
            if ((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$path]) {
                throw "Input changed: $path"
            }
        }
        Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
            Remove-Item
        $env:MK2KS_TEST_FIGHTER=$fighter
        $env:MK2KS_P2_FIGHTER=$victim
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER='1'
        $env:MK2KS_TEST_ROUND_WIN='1'
        $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
        $env:MK2KS_ASSERT_HUD_SHADOW='1'
        $env:MK2_TRACE_NATIVE_FINISH=$fighter
        $env:MK2_TRACE_NATIVE_FINISH_SIDE='1'
        $env:MK2_TRACE_INPUT_ONLY_APPROACH='1'
        $env:MK2_TRACE_FINISH_SNAPSHOTS='1'
        $env:MK2_TRACE_FINISH_ACTORS='1'
        if ($FineSnapshots) {$env:MK2_TRACE_FINISH_FINE_SNAPSHOTS='1'}
        if ($PostFinishSceneSnapshots) {$env:MK2_TRACE_POST_FINISH_SCENE_SNAPSHOTS='1'}
        if ($TraceSound) {$env:MK2_TRACE_FINISH_SOUND='1'}
        if ($fighter -eq 'kano') {$env:MK2_TRACE_SKELETON_OBJECT='1'}
        if($AssertNativeJaxBody){
            $env:MK2_TRACE_EXPECT_VICTIM_HELD_POSE='FF997BE0'
            $env:MK2_TRACE_EXPECT_VICTIM_ID='000B'
        }
        if($AssertNativeStockBody){
            $env:MK2_TRACE_EXPECT_VICTIM_HELD_POSE=$stockExpected.pose
            $env:MK2_TRACE_EXPECT_VICTIM_ID='{0:X4}' -f $stockExpected.id
        }
        if ($FirstSkeletonFields -and $fighter -eq 'kano') {$env:MK2_TRACE_SKELETON_FIRST_FIELDS='1'}
        if ($VictimPhaseSnapshots -and $fighter -eq 'kano') {$env:MK2_TRACE_VICTIM_PHASE_SNAPSHOTS='1'}
        $case="${CasePrefix}_${fighter}_vs_${victim}"
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
        $effect=if ($fighter -eq 'kano') {'MK2_FINISH_SKELETON '} else {'MK2_FINISH_FIRE_PALETTE '}
        $winnerId=if ($fighter -eq 'kano') {'0011'} else {'0012'}
        $passed=$exitCode -eq 0 -and
            $log.Contains('MK2_FINISH_INPUT_APPROACH ') -and
            $log.Contains($effect) -and
            $log -match "MK2KS_NATIVE_WIN[^\r\n]*winner=$winnerId" -and
            $log.Contains('MK2KS_EXIT_RESULT pass=true ') -and
            $log.Contains('MK2KS_STABILITY stalled_frames=0 trap_frames=0') -and
            $log.Contains('MK2KS_DISPLAY_RESULT pass=true ') -and
            $log.Contains('MK2KS_HUD_SHADOW_RESULT pass=true ') -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        $soundMarkers=@()
        $markerAges=[ordered]@{}
        $syncValidated=$null
        $victimSyncValidated=$null
        if($AssertVictimSync){
            & python $victimVerifier "$out\run.log" --victim $victim |
                Out-File -LiteralPath "$out\victim_sync.json" -Encoding utf8
            $victimSyncValidated=$LASTEXITCODE -eq 0
            $passed=$passed -and $victimSyncValidated
        }
        $holdValidated=$null
        $jaxBodyValidated=$null
        $stockBodyValidated=$null
        if($AssertNativeJaxBody){
            $jaxBodyValidated=$log.Contains('MK2_NATIVE_JAX_BODY_RESULT pass=true ')
            $passed=$passed -and $jaxBodyValidated
        }
        if($AssertNativeStockBody){
            $stockBodyValidated=$log.Contains('MK2_NATIVE_STOCK_BODY_RESULT pass=true ')
            $passed=$passed -and $stockBodyValidated -and $log.Contains('MK2_KANO_VICTIM_HOLD_RESULT pass=true ')
        }
        if($AssertWinnerHold){
            $holdValidated=$log.Contains('MK2_KANO_WINNER_HOLD_RESULT pass=true ')
            $passed=$passed -and $holdValidated
        }
        if($AssertSkeletonSync -and $fighter -eq 'kano'){
            & python $syncVerifier "$out\run.log" | Out-File -LiteralPath "$out\skeleton_sync.json" -Encoding utf8
            $syncValidated=$LASTEXITCODE -eq 0
            $passed=$passed -and $syncValidated
        }
        $resumeChecks=[regex]::Match($log,'MK2KS_P2_CPU_RESUME_RESULT checks=(\d+)')
        if($RequireCpuResume){
            $passed=$passed -and $resumeChecks.Success -and [int]$resumeChecks.Groups[1].Value -ge 100
        }
        $cpuWinChecks=[regex]::Match($log,'MK2KS_P2_CPU_WIN_RESULT checks=(\d+)')
        if($RequireCpuWin){
            $passed=$passed -and $cpuWinChecks.Success -and [int]$cpuWinChecks.Groups[1].Value -ge 80
        }
        if ($TraceSound) {
            $soundMarkers=if ($fighter -eq 'kano') {@('FFF9')} else {@('FFFA','FFF8','FFF7')}
            foreach ($marker in $soundMarkers) {
                $match=[regex]::Match($log,
                    "MK2_FINISH_SOUND_PORT frame=\d+ age=(\d+) address=01D01030 data=$marker ")
                $passed=$passed -and $match.Success
                if ($match.Success) {$markerAges[$marker]=[int]$match.Groups[1].Value}
            }
            if ($fighter -eq 'sonya' -and $markerAges.Count -eq 3) {
                $passed=$passed -and $markerAges['FFFA'] -lt $markerAges['FFF8'] -and
                    $markerAges['FFF8'] -eq $markerAges['FFF7']
            }
        }
        [ordered]@{case=$case;passed=$passed;fighter=$fighter;victim=$victim;
            exit_code=$exitCode;seconds=$Seconds;require_cpu_resume=$RequireCpuResume.IsPresent;
            cpu_resume_checks=if($resumeChecks.Success){[int]$resumeChecks.Groups[1].Value}else{0};
            cpu_win_checks=if($cpuWinChecks.Success){[int]$cpuWinChecks.Groups[1].Value}else{0};
            executable_sha256=$hashes[$Executable];
            payload_sha256=$hashes[$payload];harness_sha256=$hashes[$harness];
            base_harness_sha256=$hashes[$baseHarness];skeleton_sync_validated=$syncValidated;
            victim_sync_validated=$victimSyncValidated;
            victim_sync_verifier_sha256=if($AssertVictimSync){$hashes[$victimVerifier]}else{$null};
            winner_hold_validated=$holdValidated;
            native_jax_body_validated=$jaxBodyValidated;
            native_stock_body_validated=$stockBodyValidated;
            native_stock_body_harness_sha256=if($AssertNativeStockBody){$hashes[$stockBodyHarness]}else{$null};
            native_jax_body_harness_sha256=if($AssertNativeJaxBody){$hashes[$jaxBodyHarness]}else{$null};
            winner_hold_harness_sha256=if($AssertWinnerHold){$hashes[$holdHarness]}else{$null};
            sound_trace=$TraceSound.IsPresent;sound_marker_ages=$markerAges} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output "$case pass=$passed"
        if (-not $passed) {$failed+=$case}
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object {$_.Name -like 'MK2KS_*' -or $_.Name -like 'MK2_TRACE_*'} |
        Remove-Item
    foreach ($key in $saved.Keys) {Set-Item -LiteralPath "Env:$key" -Value $saved[$key]}
}
if ($failed.Count) {throw "Finisher victim cases failed: $($failed -join ', ')"}
