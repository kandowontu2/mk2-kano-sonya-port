# Preserve the full goal and live handles; running campaigns are never accepted.
$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskOut=Join-Path $taskRoot 'audit_v2619_current_walking_retreat_verified_pending'
if(Test-Path -LiteralPath $taskOut){throw 'Immutable live-wait evidence'}
$taskCheckpointPath=Join-Path $taskRoot 'audit_v2606_current_standing_jump_full_scope_checkpoint/checkpoint.json'
$taskCheckpoint=Get-Content -LiteralPath $taskCheckpointPath -Raw | ConvertFrom-Json
if($taskCheckpoint.goalStatus -ne 'active' -or $taskCheckpoint.fullPortAcceptance -or $taskCheckpoint.finishedRelease -or @($taskCheckpoint.currentSourceBoundBossCampaigns.PSObject.Properties).Count -ne 66){throw 'Full original unfinished checkpoint required'}
$taskBoundaryPath=Join-Path $taskRoot 'audit_v2613_walking_retreat_source_boundary_checked/report.json'
$taskBoundary=Get-Content -LiteralPath $taskBoundaryPath -Raw | ConvertFrom-Json
if(-not $taskBoundary.passed -or -not $taskBoundary.fullSourceInverse -or -not $taskBoundary.wholeLauncherInverse -or -not $taskBoundary.wholeGuestAndPayloadReconstructed -or @($taskBoundary.rejectedSpecificSourceCounterexamples).Count -ne 8){throw 'Actual eight-negative walking-only source boundary required'}
$taskPins=@{}
foreach($taskPin in $taskBoundary.inputHashes.PSObject.Properties){
 if((Get-FileHash -LiteralPath $taskPin.Name).Hash -ne $taskPin.Value){throw "Changed actual source-boundary dependency: $($taskPin.Name)"}
 $taskPins[$taskPin.Name]=$taskPin.Value
}
foreach($taskPath in @($taskCheckpointPath,$taskBoundaryPath,$PSCommandPath)){$taskPins[$taskPath]=(Get-FileHash -LiteralPath $taskPath).Hash}
$taskProcesses=@(Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe' -and $_.CommandLine -match 'audit_v2611_current_(kano|sonya)_p1_shao_walking_retreat_campaign'})
if($taskProcesses.Count -ne 2){throw 'Both exact physical captures must be confirmed live now; inspect terminal output instead'}
foreach($taskProcess in $taskProcesses){
 if($taskProcess.CommandLine -notmatch 'diagnostic_v1836_ball_register_boundary' -or $taskProcess.CommandLine -notmatch 'mk2ks_natural_campaign_boss_shao_walking_retreat_v2607.lua' -or $taskProcess.CommandLine -notmatch '-nocheat' -or $taskProcess.UserModeTime -le 0){throw 'Actual unchanged current-build, physical-only live process required'}
}
$taskResult=[ordered]@{
 goalStatus='active'
 objective=$taskCheckpoint.objective
 previousGoalTurnClassification='no progress: user-requested status only'
 thisGoalTurnClassification='progress and verified live wait: complete archive cross-check accepted, four physical campaigns independently verified, and a walking-only backward-jump successor source boundary passed before both actual captures were started. No game or balance changes and no match/ending acceptance.'
 previousFullCheckpoint=$taskCheckpointPath
 previousFullCheckpointSHA256=$taskPins[$taskCheckpointPath]
 completedPhysicalContexts=66
 completedFreshNaturalShaoRoundWins=3
 actualShaoMatchClears=0
 actualEndingsAccepted=$false
 fullPortAcceptance=$false
 finishedRelease=$false
 remaining=$taskCheckpoint.remaining
 allOriginalUnfinishedGatesRetained=$true
 currentCandidate=$taskCheckpoint.currentCandidate
 currentCMD=$taskCheckpoint.currentCMD
 currentPlaytestZIP=$taskCheckpoint.currentPlaytestZIP
 currentWalkingOnlySourceBoundary=$taskBoundaryPath
 walkingChangeScope='Only native walk0 is additionally eligible for physical backward-jump attempts; direction, timing, ordinary/Kintaro controls and observers are exact predecessor bytes. Forward-jump trials were not an improvement.'
 pendingCampaigns=@(
  @{fighter='kano';humanSlot=1;capture='audit_v2611_current_kano_p1_shao_walking_retreat_campaign';unifiedExecSession=52505;accepted=$false},
  @{fighter='sonya';humanSlot=1;capture='audit_v2611_current_sonya_p1_shao_walking_retreat_campaign';unifiedExecSession=96984;accepted=$false}
 )
 authoritativeLiveProcessesObservedUTC=[DateTime]::UtcNow.ToString('o')
 authoritativeLiveProcesses=@($taskProcesses | Select-Object ProcessId,CreationDate,CommandLine,UserModeTime,KernelModeTime)
 resumeSameHandlesWithoutRestartOnObservationTimeout=$true
 campaignResultsNeverAcceptedFromIntentOrTimer=$true
 gameChanged=$false
 inputHashes=$taskPins
 nextAction='Resume actual sessions52505/96984 or their verified own PIDs. Only after terminal exit, run verify_current_boss_shao_walking_retreat_v2609.py into fresh audit_v2612 current fighter checked leaves. Preserve all failed/accepted evidence, independently verify complete actual inputs/action/health/wins and earlier trajectory, then inspect actual owned Shao match/ending outcomes. Continue every original full-port fidelity gate and both-slot requirements.'
}
New-Item -ItemType Directory -Path $taskOut | Out-Null
$taskResult | ConvertTo-Json -Depth 8 | Out-File -LiteralPath (Join-Path $taskOut 'pending.json') -Encoding utf8
$taskResult | Select-Object goalStatus,completedPhysicalContexts,completedFreshNaturalShaoRoundWins,actualShaoMatchClears,actualEndingsAccepted,fullPortAcceptance,gameChanged,authoritativeLiveProcessesObservedUTC,pendingCampaigns | ConvertTo-Json -Depth 4
