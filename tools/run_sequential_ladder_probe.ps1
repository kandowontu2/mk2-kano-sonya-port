param(
    [Parameter(Mandatory=$true)][string]$CasePrefix,
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$PayloadRomDirectory,
    [ValidateSet('kano','sonya','liu_kang')][string[]]$Fighters=@('kano','sonya'),
    [int]$Seconds=1000,
    [Nullable[int]]$StageIndex=$null,
    [ValidateSet(14,15,16,17,18)][Nullable[int]]$DiagnosticCpuId=$null,
    [int]$ResetTraceStart=0,
    [int]$ResetTraceEnd=0,
    [Nullable[int]]$ResetTraceStage=$null,
    [int]$ResetTraceStageAge=2100,
    [Nullable[int]]$SaveStage=$null,
    [Nullable[int]]$TraceCpuStage=$null,
    [int]$TraceCpuAge=1400,
    [switch]$TraceCpuOwnedSpecials,
    [switch]$TraceAiVariety,
    [switch]$EndingTrace,
    [switch]$EndingStackTrace,
    [switch]$AuditMissingAnimations,
    [switch]$AnimationAuditActorState,
    [switch]$AnimationAuditSnapshots,
    [switch]$AnimationAuditTraceFirstMain,
    [string]$AnimationAuditTraceKey='',
    [switch]$AnimationAuditDirect48,
    [switch]$AnimationAuditStockLiu59,
    [switch]$StageVisualSnapshots,
    [string[]]$MappedMainKeys=@(),
    [switch]$NoAssistance,
    [ValidateSet('stock','projectile_zone','guard_uppercut','sweep_lk','standing_hk','rapid_uppercut')]
    [string]$RoundWinStrategy='stock',
    [switch]$RequireComplete
)
$ErrorActionPreference='Stop'
$portRoot=Split-Path $PSScriptRoot -Parent
if ($CasePrefix -notmatch '^[a-zA-Z0-9_-]+$') {throw 'Use a simple evidence prefix.'}
if ($null -ne $StageIndex -and ($StageIndex -lt 0 -or $StageIndex -gt 16)) {throw 'StageIndex must be 0..16.'}
if ($null -ne $DiagnosticCpuId -and $RequireComplete) {throw 'Diagnostic opponent injection cannot prove natural full-ladder completion.'}
if (($ResetTraceStart -gt 0) -ne ($ResetTraceEnd -gt 0) -or $ResetTraceEnd -lt $ResetTraceStart) {throw 'Supply a valid reset trace interval.'}
if ($AnimationAuditTraceKey -and $AnimationAuditTraceKey -notmatch '^((kano|sonya):main:(48|59|60|61)|liu:main:59)$') {throw 'Use a tracked main animation key.'}
foreach($key in $MappedMainKeys){if($key -notmatch '^(kano|sonya):main:(48|59|60|61)$'){throw "Invalid mapped main animation key: $key"}}
$Executable=(Resolve-Path -LiteralPath $Executable).Path
$PayloadRomDirectory=(Resolve-Path -LiteralPath $PayloadRomDirectory).Path
$romPath="$PayloadRomDirectory;$portRoot\roms_v22_clean;$portRoot\roms"
$payload=Join-Path $PayloadRomDirectory 'mk2ks\mk2ks.mdata'
$harness=Join-Path $portRoot 'mk2ks_cpu_ladder_trace.lua'
$auditHarness=Join-Path $portRoot 'mk2ks_missing_animation_probe.lua'
$baseHarness=Join-Path $portRoot 'mk2ks_selector_exit_test.lua'
$tracked=@($Executable,$payload,$harness,$baseHarness,$PSCommandPath)
if($AuditMissingAnimations){$tracked+=$auditHarness}
$hashes=@{}
foreach ($file in $tracked) {$hashes[$file]=(Get-FileHash -LiteralPath $file).Hash}
& $Executable mk2ks -rompath $romPath -verifyroms
if ($LASTEXITCODE -ne 0) {throw 'Candidate/payload failed ROM verification.'}
$savedEnvironment=@{}
Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | ForEach-Object {$savedEnvironment[$_.Name]=$_.Value}
Push-Location $portRoot
try {
    foreach ($fighter in $Fighters) {
        foreach ($file in $tracked) {
            if ((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) {throw "Input changed: $file"}
        }
        Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
        $env:MK2KS_TEST_FIGHTER=$fighter
        $env:MK2KS_P2_FIGHTER='stock'
        $env:MK2KS_TEST_CONFIRM='hp'
        $env:MK2KS_TEST_CONFIRM_HOLD='8'
        $env:MK2KS_TWO_PLAYER='0'
        $env:MK2KS_TEST_ROUND_WIN='1'
        $env:MK2KS_ROUND_WIN_STRATEGY=$RoundWinStrategy
        if ($NoAssistance) {$env:MK2KS_ALLOW_NATURAL_LOSS='1'}
        if ($null -eq $StageIndex) {$env:MK2KS_DIAGNOSTIC_ALL_STAGES='1'}
        else {$env:MK2KS_DIAGNOSTIC_LADDER_INDEX="$StageIndex"}
        if ($null -ne $DiagnosticCpuId) {$env:MK2KS_DIAGNOSTIC_CPU_ID="$DiagnosticCpuId"}
        if (-not $NoAssistance) {
            $env:MK2KS_DIAGNOSTIC_CPU_HEALTH='1'
            $env:MK2KS_DIAGNOSTIC_P1_REGEN='1'
        }
        $env:MK2KS_ASSERT_MULTI_PROGRESS_MIN_STAGE='16'
        if ($RequireComplete) {$env:MK2KS_STOP_ON_CAMPAIGN_COMPLETE='1'}
        if ($ResetTraceStart -gt 0) {
            $env:MK2KS_RESET_TRACE_START="$ResetTraceStart"
            $env:MK2KS_RESET_TRACE_END="$ResetTraceEnd"
        }
        if ($null -ne $ResetTraceStage) {
            $env:MK2KS_RESET_TRACE_STAGE="$ResetTraceStage"
            $env:MK2KS_RESET_TRACE_STAGE_AGE="$ResetTraceStageAge"
        }
        if ($fighter -ne 'liu_kang') {
            $env:MK2KS_ASSERT_NATIVE_DISPLAY='1'
            $env:MK2KS_ASSERT_HUD_SHADOW='1'
        }
        $case="${CasePrefix}_${fighter}"
        $out=Join-Path $portRoot $case
        if (Test-Path -LiteralPath $out) {throw "Refusing to overwrite evidence: $out"}
        New-Item -ItemType Directory -Path $out | Out-Null
        if ($null -ne $SaveStage) {
            $env:MK2KS_SAVE_STAGE="$SaveStage"
            $env:MK2KS_SAVE_STATE_PATH=Join-Path $out "stage${SaveStage}.sta"
        }
        if ($null -ne $TraceCpuStage) {
            $env:MK2KS_CPU_TRACE_STAGE="$TraceCpuStage"
            $env:MK2KS_CPU_TRACE_AGE="$TraceCpuAge"
            $env:MK2KS_CPU_TRACE_PATH=Join-Path $out 'cpu_trace.log'
        }
        if ($EndingTrace) {$env:MK2KS_ENDING_TRACE_ALL='1'}
        if ($EndingStackTrace) {$env:MK2KS_ENDING_STACK_TRACE='1'}
        if ($AuditMissingAnimations) {$env:MK2KS_ANIM_PROBE_BASE='mk2ks_cpu_ladder_trace.lua'}
        if ($AnimationAuditActorState) {$env:MK2KS_ANIM_AUDIT_ACTOR_STATE='1'}
        if ($AnimationAuditSnapshots) {$env:MK2KS_ANIM_AUDIT_SNAPSHOTS='1'}
        if ($AnimationAuditTraceFirstMain) {$env:MK2KS_ANIM_AUDIT_TRACE_FIRST_MAIN='1'}
        if ($AnimationAuditTraceKey) {$env:MK2KS_ANIM_AUDIT_TRACE_KEY=$AnimationAuditTraceKey}
        if ($AnimationAuditDirect48) {$env:MK2KS_ANIM_AUDIT_DIRECT48='1'}
        if ($AnimationAuditStockLiu59) {$env:MK2KS_ANIM_AUDIT_STOCK_LIU59='1'}
        if ($StageVisualSnapshots) {$env:MK2KS_STAGE_VISUAL_SNAPSHOTS='1'}
        if ($TraceCpuOwnedSpecials) {$env:MK2KS_TRACE_CPU_OWNED_SPECIALS='1'}
        if ($TraceAiVariety) {$env:MK2KS_TRACE_AI_VARIETY='1'}
        $debugArgs=if ($null -ne $TraceCpuStage) {@('-debug','-debugger','none')} else {@()}
        $autobootScript=if($AuditMissingAnimations){$auditHarness}else{$harness}
        & $Executable mk2ks -rompath $romPath -artpath "$portRoot\artwork" -skip_gameinfo `
            -video none -sound none -nothrottle -str $Seconds -snapsize 400x300 @debugArgs `
            -cfg_directory "$out\cfg" -nvram_directory "$out\nvram" -snapshot_directory "$out\snap" `
            -autoboot_script $autobootScript 2>&1 | Out-File -LiteralPath "$out\run.log" -Encoding utf8
        $exitCode=$LASTEXITCODE
        foreach ($file in $tracked) {
            if ((Get-FileHash -LiteralPath $file).Hash -ne $hashes[$file]) {throw "Input changed: $file"}
        }
        $log=Get-Content -LiteralPath "$out\run.log" -Raw
        $summary=($log -split "`n" | Where-Object {$_ -match '^MK2KS_MULTI_FINAL '}) | Select-Object -Last 1
        $exitSummary=($log -split "`n" | Where-Object {$_ -match '^MK2KS_EXIT_RESULT '}) | Select-Object -Last 1
        $health=($log -split "`n" | Where-Object {$_ -match '^MK2KS_CPU_DIAGNOSTIC_HEALTH_RESULT '}) | Select-Object -Last 1
        $regen=($log -split "`n" | Where-Object {$_ -match '^MK2KS_CPU_DIAGNOSTIC_P1_REGEN_RESULT '}) | Select-Object -Last 1
        $cpuSpecialCounts=[regex]::Match($log,'MK2KS_CPU_OWNED_SPECIAL_RESULT kano=(\d+) sonya=(\d+)')
        $missingMainEntries=[regex]::Matches($log,'MK2KS_ANIM_AUDIT_ENTRY key=((?:kano|sonya):main:\d+) reads=(\d+)')
        $stockLiu59=([regex]::Match($log,'MK2KS_ANIM_AUDIT_ENTRY key=liu:main:59 reads=(\d+)')).Groups[1].Value
        $missingMainReads=0
        $mappedMainReads=0
        foreach($entry in $missingMainEntries){
            if($MappedMainKeys -contains $entry.Groups[1].Value){$mappedMainReads+=[int]$entry.Groups[2].Value}
            else{$missingMainReads+=[int]$entry.Groups[2].Value}
        }
        $animationAuditValidated=-not $AuditMissingAnimations -or
            ($missingMainEntries.Count -eq 7 -and $missingMainReads -eq 0)
        $direct48Entries=[regex]::Matches($log,'MK2KS_ANIM_DIRECT48_RESULT key=sonya:main:48:direct\d reads=(\d+)')
        $direct48Reads=0
        foreach($entry in $direct48Entries){$direct48Reads+=[int]$entry.Groups[1].Value}
        $direct48Validated=-not $AnimationAuditDirect48 -or
            ($direct48Entries.Count -eq 2 -and $direct48Reads -eq 0)
        $baselineValidated=$exitCode -eq 0 -and
            $exitSummary -match '^MK2KS_EXIT_RESULT pass=true ' -and
            $log -match 'MK2KS_STABILITY stalled_frames=0 trap_frames=0' -and
            ($fighter -eq 'liu_kang' -or (
                $log -match 'MK2KS_DISPLAY_RESULT pass=true ' -and
                $log -match 'MK2KS_HUD_SHADOW_RESULT pass=true ')) -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]'
        $unassistedValidated=-not $NoAssistance -or (
            $health -match 'requested=nil .*writes=0' -and
            $regen -match 'enabled=false writes=0')
        $visualFiles=@(Get-ChildItem -LiteralPath "$out\snap" -Filter 'stage_visual_*.png' -File -ErrorAction SilentlyContinue)
        $visualMarkers=[regex]::Matches($log,'MK2KS_STAGE_VISUAL frame=\d+ stage=(\d+) arena=(\d+) p1=(\d+) p2=(\d+)')
        $stageVisualValidated=-not $StageVisualSnapshots -or
            ($visualMarkers.Count -gt 0 -and $visualMarkers.Count -eq $visualFiles.Count)
        $diagnosticCpuValidated=$null -eq $DiagnosticCpuId -or (
            $log -match "MK2KS_CPU_DIAGNOSTIC_RESULT requested=$DiagnosticCpuId injected=true" -and
            $log -match "MK2KS_CPU_STATE frame=\d+ roster=$DiagnosticCpuId actor_id=$DiagnosticCpuId action=0303" -and
            $summary -match 'identity_errors=0 stage_errors=0' -and
            $exitSummary -match '^MK2KS_EXIT_RESULT pass=true ' -and
            $log -match 'MK2KS_STABILITY stalled_frames=0 trap_frames=0' -and
            $log -match 'MK2KS_DISPLAY_RESULT pass=true ' -and
            $log -match 'MK2KS_HUD_SHADOW_RESULT pass=true ' -and
            $log -notmatch '(?i)fatal error|exception at|access violation|\[LUA ERROR\]')
        $savePath=if ($null -ne $SaveStage) {Join-Path $out "stage${SaveStage}.sta"} else {''}
        [ordered]@{case=$case;exit_code=$exitCode;seconds=$Seconds;fighter=$fighter;
            diagnostic_health_assistance=(-not $NoAssistance.IsPresent);round_win_strategy=$RoundWinStrategy;
            sequential_no_index_jump=($null -eq $StageIndex);stage_index=$StageIndex;
            diagnostic_cpu_id=$DiagnosticCpuId;
            diagnostic_cpu_validated=$diagnosticCpuValidated;
            baseline_validated=$baselineValidated;
            unassisted_required=$NoAssistance.IsPresent;
            unassisted_validated=if($NoAssistance){$unassistedValidated}else{$null};
            save_stage=$SaveStage;save_state_path=$savePath;save_state_exists=($savePath -and (Test-Path -LiteralPath $savePath));
            cpu_trace_stage=$TraceCpuStage;cpu_trace_age=$TraceCpuAge;
            ending_trace=$EndingTrace.IsPresent;
            ending_stack_trace=$EndingStackTrace.IsPresent;
            missing_animation_audit=$AuditMissingAnimations.IsPresent;
            animation_audit_actor_state=$AnimationAuditActorState.IsPresent;
            animation_audit_snapshots=$AnimationAuditSnapshots.IsPresent;
            animation_audit_trace_first_main=$AnimationAuditTraceFirstMain.IsPresent;
            animation_audit_trace_key=$AnimationAuditTraceKey;
            mapped_main_keys=$MappedMainKeys;
            mapped_main_reads=$mappedMainReads;
            animation_audit_direct48=$AnimationAuditDirect48.IsPresent;
            animation_audit_stock_liu59=$AnimationAuditStockLiu59.IsPresent;
            stage_visual_snapshots=$StageVisualSnapshots.IsPresent;
            stage_visual_validated=$stageVisualValidated;
            stage_visual_count=$visualMarkers.Count;
            stock_liu59_reads=if($stockLiu59){[int]$stockLiu59}else{$null};
            direct48_entries=$direct48Entries.Count;
            direct48_reads=$direct48Reads;
            direct48_validated=$direct48Validated;
            missing_main_cells_checked=$missingMainEntries.Count;
            missing_main_reads=$missingMainReads;
            missing_animation_audit_validated=$animationAuditValidated;
            cpu_special_trace_enabled=$TraceCpuOwnedSpecials.IsPresent;
            cpu_kano_special_entries=if($cpuSpecialCounts.Success){[int]$cpuSpecialCounts.Groups[1].Value}else{$null};
            cpu_sonya_special_entries=if($cpuSpecialCounts.Success){[int]$cpuSpecialCounts.Groups[2].Value}else{$null};
            executable_sha256=$hashes[$Executable];payload_sha256=$hashes[$payload];
            harness_sha256=$hashes[$harness];summary=$summary;health=$health;regen=$regen} |
            ConvertTo-Json | Out-File -LiteralPath "$out\result.json" -Encoding utf8
        Write-Output $summary
        Write-Output $exitSummary
        Write-Output $health
        Write-Output $regen
        if ($exitCode -ne 0 -or -not $summary) {throw "Sequential probe failed to finish: $case"}
        if (-not $baselineValidated) {throw "Campaign stability/display failed: $case"}
        if (-not $unassistedValidated) {throw "Unassisted campaign wrote health or regeneration: $case"}
        if (-not $stageVisualValidated) {throw "Stage visual capture missing: $case"}
        if (-not $diagnosticCpuValidated) {throw "Diagnostic opponent identity/display/stability failed: $case"}
        if (-not $animationAuditValidated) {throw "Missing-animation main dispatch was read: $case"}
        if (-not $direct48Validated) {throw "Sonya main-48 direct Liu frame was read: $case"}
        if ($RequireComplete) {
            if ($null -ne $StageIndex) {throw 'RequireComplete needs a sequential ladder without an index jump.'}
            $requiredStages=@(0..12)+@(14,15)
            $winsExpected=@($requiredStages | ForEach-Object {"${_}:2"})
            $winsOk=@($winsExpected | Where-Object {$summary -notmatch "(?<![0-9])$([regex]::Escape($_))(,|\s)"}).Count -eq 0
            if($StageVisualSnapshots){
                foreach($stage in $requiredStages){
                    $stageFile=Join-Path "$out\snap" ('stage_visual_{0:D2}.png' -f $stage)
                    if(-not (Test-Path -LiteralPath $stageFile)){
                        throw "Missing in-fight stage visual for stage $stage in $case"
                    }
                }
            }
            $complete=$summary -match 'identity_errors=0 stage_errors=0 ended=true completed=true diagnostic=false,false' -and
                $summary -match '16:1' -and $winsOk -and
                $exitSummary -match '^MK2KS_EXIT_RESULT pass=true ' -and
                $log -match 'MK2KS_STABILITY stalled_frames=0 trap_frames=0' -and
                $log -match 'MK2KS_CAMPAIGN_END_RESULT lost=false unexpected_resets=0 completed=true'
            if (-not $complete) {throw "Assisted full-ladder assertions failed: $case"}
        }
    }
} finally {
    Pop-Location
    Get-ChildItem Env: | Where-Object Name -Like 'MK2KS_*' | Remove-Item
    foreach ($key in $savedEnvironment.Keys) {Set-Item -LiteralPath "Env:$key" -Value $savedEnvironment[$key]}
}
