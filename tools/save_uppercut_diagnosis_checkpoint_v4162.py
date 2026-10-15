"""Preserve complete original goal, actual terminal proofs and current live identity."""
import hashlib,json,subprocess
from pathlib import Path
import run_current_clean_uppercut_ram_v4155 as clean

ROOT,need,sha=clean.ROOT,clean.need,clean.sha
PARENT=ROOT/'audit_v4133_guard_punish_live_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4163_uppercut_diagnosis_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining'])
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance'] and not state['finishedRelease'],'Original complete goal remains unproven')
    pins={}
    def pin(path,wanted=None):
        p=Path(path).resolve();key=str(p)
        digest=pins.get(key) or sha(p)
        need(wanted is None or wanted==digest,'Actual immutable evidence hash: '+key)
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Inherited shared pin unchanged')
        pins[key]=digest
    pin(PARENT)
    for p,h in state['inputHashes'].items():pin(p,h)
    names=('audit_v4121_sonya_guard_punish_campaign_observed','audit_v4129_guard_punish_whole_campaign_checked',
      'audit_v4141_guard_uppercut_source_preflight','audit_v4149_guard_uppercut_ready_source_preflight',
      'audit_v4153_guard_terminal_log_compression','audit_v4157_current_sonya_p2_clean_uppercut_checked',
      'audit_v4159_guard_uppercut_actual_windows')
    reports={}
    for name in names:
        p=ROOT/name/'report.json';r=json.loads(p.read_text());need(r['passed'] and not r.get('fullPortAcceptance',False),'Actual bounded proof: '+name)
        reports[name]=r;pin(p)
        for p,h in r.get('inputHashes',{}).items():pin(p,h)
        for p,h in r.get('case',{}).get('inputHashes',{}).items():pin(p,h)
    failed=ROOT/'audit_v4139_sonya_guard_uppercut_campaign_observed/report.json'
    need(json.loads(failed.read_text())['passed'] is False,'Stopped incorrect controller evidence stays false');pin(failed)
    whole=reports['audit_v4129_guard_punish_whole_campaign_checked']
    need(not whole['actualNaturalSonyaP2TowerClearAccepted'] and whole['case']['paid_continue_losses']==100 and whole['case']['stages_reached']==list(range(10)),'Whole old campaign passed observation/state/input grammar but no tower clear')
    ordinary=reports['audit_v4157_current_sonya_p2_clean_uppercut_checked']
    need(ordinary['positive']['side']==2 and ordinary['positive']['fields']==960 and ordinary['positive']['nativeContactDamage']==40 and len(ordinary['actualFaultsRejected'])==5,'Original clean P2 uppercut, full recovery/follow-up and five actual faults')
    analysis=reports['audit_v4159_guard_uppercut_actual_windows']
    need(analysis['observationalOnly'] and analysis['actualCompletedUppercutAttemptWindows']==23 and analysis['actualHuman107Stores']==0 and analysis['windowsWithActualOwnDamage']==23,'Actual interrupted CPU attack windows; no intended command credited')
    folder=ROOT/'audit_v4146_sonya_guard_uppercut_ready_p2_campaign'
    with (folder/'run.log').open('rb') as stream:raw=stream.read(analysis['actualNativeLogPrefixBytes'])
    need(hashlib.sha256(raw).hexdigest().upper()==analysis['actualNativeLogPrefixSHA256'],'Exact observed live prefix retained')
    for name in ('guest_memory_proof.json','input_hashes_before.json','source_snapshot_paths.json','process.json'):pin(folder/name)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId=51464 OR ProcessId=135860 OR ProcessId=135808 OR ProcessId=100384" | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0,'Authoritative current process check')
    processes=json.loads(q.stdout) if q.stdout.strip() else []
    if isinstance(processes,dict):processes=[processes]
    by={p['ProcessId']:p for p in processes}
    need(135808 not in by and 100384 not in by,'Old verifier and clean native test really terminal now')
    pending=dict(execSession=23118,nativePID=51464,collectorPID=135860,processesConfirmedNow=processes,capture=str(folder),
      wholeQualifierSource=str(ROOT/'tools/verify_guard_uppercut_ready_whole_campaign_v4160.py'),wholeQualifierOutput=str(ROOT/'audit_v4161_guard_uppercut_ready_whole_campaign_checked/report.json'))
    if 51464 in by:
        need(135860 in by and by[51464]['ParentProcessId']==135860 and clean.current.LUA in by[51464]['CommandLine'] and folder.name in by[51464]['CommandLine'] and 'run_sonya_guard_uppercut_ready_campaign_v4145.py' in by[135860]['CommandLine'],'Exact existing campaign handles, never observation-timeout restart')
        pending.update(status='live confirmed by actual CIM',wholeQualifierExecuted=False)
    else:
        need((folder/'result.json').exists(),'Terminal native result exists when handle missing');pin(folder/'result.json')
        pending.update(status='native child terminal; consume exact exec23118 and inspect collector report',wholeQualifierExecuted=False)
    for name in ('mk2ks_guard_uppercut_campaign_ram_v4134.lua','tools/run_sonya_guard_uppercut_campaign_v4135.py','tools/qualify_guard_uppercut_source_v4136.py',
      'tools/qualify_guard_uppercut_source_v4140.py','tools/verify_guard_uppercut_prefix_v4142.py','mk2ks_guard_uppercut_ready_campaign_ram_v4144.lua',
      'tools/run_sonya_guard_uppercut_ready_campaign_v4145.py','tools/qualify_guard_uppercut_ready_source_v4148.py','tools/verify_guard_uppercut_ready_prefix_v4150.py',
      'tools/compact_guard_terminal_logs_v4152.py','mk2ks_clean_uppercut_ram_v4154.lua','tools/run_current_clean_uppercut_ram_v4155.py',
      'tools/analyze_guard_uppercut_windows_v4158.py','tools/verify_guard_uppercut_ready_whole_campaign_v4160.py','tools/save_uppercut_diagnosis_checkpoint_v4162.py'):pin(ROOT/name)
    need(not any(p.suffix in ('.bin','.png','.wav') for p in (ROOT/'audit_v4156_current_sonya_p2_clean_uppercut_ram').rglob('*') if p.is_file()),'Clean test wrote no raw native dumps')
    for leaf in ('audit_v4143_guard_uppercut_actual_prefix_checked','audit_v4151_guard_uppercut_ready_actual_prefix_checked','audit_v4161_guard_uppercut_ready_whole_campaign_checked'):
        need(not (ROOT/leaf).exists(),'Unused qualifier stays explicitly unexecuted')
    storage=reports['audit_v4153_guard_terminal_log_compression']
    need(storage['reclaimedAllocatedBytes']==39129088 and storage['deletedFiles']==0,'Historical single-count lossless log compression')
    state.update(inputHashes=pins,inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Retain full inherited scope/exclusions; exact shared immutable pins must agree.'),
      previousCheckpoint=str(PARENT),previousGoalTurnClassification='no progress: acknowledgment-only turn; current continuation revalidated real handles and completed concrete diagnostic work',
      thisGoalTurnClassification='progress: consumed exact old whole-campaign qualifier17453 terminal0; full original native state/health/schedule/paidcontinue/ending/boss grammar and independent142780field physical replay passed, but100paidlosses/stages0..9/20wins is not tower clear. New current3836 clean P2 uppercut960pairedfields/40native damage/clean recovery/walk/jump/punch passed five real faults, original2151controller and whole2153verifier unchanged except RAM sinks. Observed23 genuine CPU uppercut windows all suffered actual own damage and no HUMAN107 activation; do not alter gameplay from failed controller intentions. Existing4146 campaign23118/PIDs51464/135860 rechecked, no restart. Fresh4160 whole qualifier drafted, not executed before native terminal. Full remaining five groups/public1836/installed bytes and dirty source retained.',
      currentDevelopmentSonyaP2GuardWholeReport=str(ROOT/'audit_v4129_guard_punish_whole_campaign_checked/report.json'),
      completedGuardCampaign=dict(execSession=17453,terminalExitCode=0,actualCompleteGuardFields=whole['case']['actualWholeGuardInputReplay']['actualCompleteGuardFields'],actualNativeLegActivations=whole['case']['actualWholeGuardInputReplay']['actualNativeLegActivations'],towerClearAccepted=False,endingPixelsAccepted=False,completeCampaignAudioAccepted=False),
      pendingSonyaP2GuardCampaign=pending,
      currentSonyaP2CleanUppercut=dict(report=str(ROOT/'audit_v4157_current_sonya_p2_clean_uppercut_checked/report.json'),execSession=16829,terminalExitCode=0,actualFields=960,nativeDamage=40,faultsRejected=5,fullMoveArtGroundShadowAudioAccepted=False),
      currentSonyaP2AttackWindowDiagnosis=dict(report=str(ROOT/'audit_v4159_guard_uppercut_actual_windows/report.json'),actualCompletedWindows=23,windowsInterruptedByOwnDamage=23,actualHuman107Stores=0,observationalOnly=True),
      currentSourcePreflightFailurePreserved=dict(source='tools/qualify_guard_uppercut_source_v4136.py',outputNeverCreated='audit_v4137_guard_uppercut_source_preflight',reason='Regex accidentally treated nil-return Lua return end as override; fresh4140 corrects regex only,4141 passed'),
      currentKnownFailedPhysicalController=dict(capture='audit_v4138_sonya_guard_uppercut_p2_campaign',report=str(failed),actualIntendedUppercuts=120,actualHuman107Stores=0,intentionallyStoppedKnownIncorrectTiming=True),
      currentInterpretationCorrections=dict(own110='Native LegGrab task, not low punch',cpu507='Unclassified here, do not label uppercut',cpu303='Native stance category, not proof of ducking',legZeroDamage='Only explicit held native701 duck-block at actual collision in bounded SubZero8 negative fixture; not universal Mileena claim'),
      currentTurnReclaimedAllocatedBytes=0,previousUncheckpointedCompressionBytes=39129088,previousUncheckpointedCompressionReport=str(ROOT/'audit_v4153_guard_terminal_log_compression/report.json'),
      cleanupAccounting='4153 lossless39129088B historical reclamation recorded once. No new deletion/compression/build/native dump copies in this continuation. Never add prior720896B or54194176B again.',
      currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,
      nextImplementationAction='Poll exact existing23118/native51464/collector135860. On real terminal consume handle, inspect4146 result and4147 observer; then execute unused4160 full campaign/physical grammar verifier to4161. Do not restart on timeout. Preserve failed inputs and clean current3836 P2 uppercut proof: actual uppercut works, all23 recorded CPU command windows took own damage before reliable activation. Improve physical battle controller using real native whiff/recovery and damage-state evidence, not proxy identity, forced health/AI/RNG/schedule/positions or CPU507/303 semantic guesses. Do not replay same losing policy as game fix. All original remaining five groups including all arenas/move phases/ground floor shadows/audio/finishers/victims/morphs/secrets/cinematics, natural SonyaP2 full tower/own endings/attract, final UI/ladder/name/audio and dependency-aware cleanup/refreshed ZIP remain intact. Narrow ordinary action proof does not promote public or complete release.',
      gameSourceAndPlayableBytesChangedThisTurn=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','Original scope/current public preserved')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),cleanP2Uppercut=True,actualInterruptedWindows=23,fullPortAcceptance=False,goalStatus='active'),indent=2),flush=True)

if __name__=='__main__':main()
