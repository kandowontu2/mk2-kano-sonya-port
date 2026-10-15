# Preserve the full goal and live handles; running campaigns are never accepted.
$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskOut=Join-Path $taskRoot 'audit_v2636_current_cooldown_retreat_verified_pending'
if(Test-Path -LiteralPath $taskOut){throw 'Immutable live-wait evidence'}
$taskCheckpointPath=Join-Path $taskRoot 'audit_v2623_current_walking_retreat_full_scope_checkpoint/checkpoint.json'
$taskCheckpoint=Get-Content -LiteralPath $taskCheckpointPath -Raw | ConvertFrom-Json
if($taskCheckpoint.goalStatus -ne 'active' -or $taskCheckpoint.fullPortAcceptance -or $taskCheckpoint.finishedRelease -or @($taskCheckpoint.currentSourceBoundBossCampaigns.PSObject.Properties).Count -ne 68){throw 'Full original unfinished checkpoint required'}
$taskBoundaryPath=Join-Path $taskRoot 'audit_v2632_cooldown_retreat_source_boundary_checked/report.json'
$taskBoundary=Get-Content -LiteralPath $taskBoundaryPath -Raw | ConvertFrom-Json
if(-not $taskBoundary.passed -or -not $taskBoundary.fullSourceInverse -or -not $taskBoundary.wholeLauncherInverse -or -not $taskBoundary.wholeGuestAndPayloadReconstructed -or @($taskBoundary.rejectedSpecificSourceCounterexamples).Count -ne 9){throw 'Actual nine-negative cooldown-only source boundary required'}
$taskPins=@{}
foreach($taskPin in $taskBoundary.inputHashes.PSObject.Properties){
 if((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value){throw "Changed actual source-boundary dependency: $($taskPin.Name)"}
 $taskPins[$taskPin.Name]=$taskPin.Value
}
foreach($taskPath in @($taskCheckpointPath,$taskBoundaryPath,$PSCommandPath)){$taskPins[$taskPath]=(Get-FileHash -LiteralPath $taskPath).Hash}
$taskProcesses=@(Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe' -and $_.CommandLine -match 'audit_v2633_current_(kano|sonya)_p1_shao_cooldown_retreat_campaign'})
if($taskProcesses.Count -ne 2){throw 'Both exact physical captures must be confirmed live now; inspect terminal output instead'}
foreach($taskProcess in $taskProcesses){
 if($taskProcess.CommandLine -notmatch 'diagnostic_v1836_ball_register_boundary' -or $taskProcess.CommandLine -notmatch 'mk2ks_natural_campaign_boss_shao_cooldown_retreat_v2628.lua' -or $taskProcess.CommandLine -notmatch '-nocheat' -or $taskProcess.UserModeTime -le 0){throw 'Actual unchanged current-build, physical-only live process required'}
}
$taskResult=[ordered]@{
 goalStatus='active'
 objective=$taskCheckpoint.objective
 previousGoalTurnClassification='no progress: user-requested status only'
 thisGoalTurnClassification='progress and verified live wait: two walking-retreat campaigns fully accepted with ordered ledgers,28 specific input negatives per fighter and exact original prefixes. Six individual jump-plan/store/motion proofs and a measured cooldown diagnostic passed. Only physical stage16 cooldown60-to48 differs in the nine-negative source-bound successor. Current captures confirmed live; no game changes or match/ending acceptance.'
 previousFullCheckpoint=$taskCheckpointPath
 previousFullCheckpointSHA256=$taskPins[$taskCheckpointPath]
 completedPhysicalContexts=68
 completedFreshNaturalShaoRoundWins=2
 actualShaoMatchClears=0
 actualEndingsAccepted=$false
 fullPortAcceptance=$false
 finishedRelease=$false
 remaining=$taskCheckpoint.remaining
 allOriginalUnfinishedGatesRetained=$true
 currentCandidate=$taskCheckpoint.currentCandidate
 currentCMD=$taskCheckpoint.currentCMD
 currentPlaytestZIP=$taskCheckpoint.currentPlaytestZIP
 currentCooldownOnlySourceBoundary=$taskBoundaryPath
 cooldownChangeScope='Only stage16 physical jump-attempt cooldown changes60-to48. Direction, hold duration, native eligibility, ordinary/Kintaro controls and every observer are exact predecessor bytes. Measured grounded48-to59 damage motivated the test; improved outcomes are not assumed.'
 pendingCampaigns=@(
  @{fighter='kano';humanSlot=1;capture='audit_v2633_current_kano_p1_shao_cooldown_retreat_campaign';unifiedExecSession=65629;accepted=$false},
  @{fighter='sonya';humanSlot=1;capture='audit_v2633_current_sonya_p1_shao_cooldown_retreat_campaign';unifiedExecSession=89262;accepted=$false}
 )
 authoritativeLiveProcessesObservedUTC=[DateTime]::UtcNow.ToString('o')
 authoritativeLiveProcesses=@($taskProcesses | Select-Object ProcessId,CreationDate,CommandLine,UserModeTime,KernelModeTime)
 resumeSameHandlesWithoutRestartOnObservationTimeout=$true
 campaignResultsNeverAcceptedFromIntentOrTimer=$true
 gameChanged=$false
 inputHashes=$taskPins
 nextAction='Resume actual sessions65629/89262 or their verified own PIDs. Only after terminal exit, run verify_current_boss_shao_cooldown_retreat_v2630.py into fresh audit_v2634 current fighter checked leaves. Preserve all failed/accepted evidence, independently verify complete actual inputs/action/health/wins and earlier trajectory, then inspect actual owned Shao match/ending outcomes. Continue every original full-port fidelity gate and both-slot requirements.'
}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskResult | ConvertTo-Json -Depth 8 | Out-File -LiteralPath (Join-Path $taskOut 'pending.json') -Encoding utf8
[pscustomobject]$taskResult | Select-Object goalStatus,completedPhysicalContexts,completedFreshNaturalShaoRoundWins,actualShaoMatchClears,actualEndingsAccepted,fullPortAcceptance,gameChanged,authoritativeLiveProcessesObservedUTC,pendingCampaigns | ConvertTo-Json -Depth 4
