"""Keep original complete goal, failed physical probes and exact current live jobs."""
import json,re,subprocess
from pathlib import Path
import run_mirror_guard_zoning_campaign_ram_v4187 as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
PARENT=ROOT/'audit_v4165_ready_campaign_terminal_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4199_mirror_zoning_live_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'Inherited shared immutable evidence unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);digest=pins.get(key) or sha(p)
        need(wanted is None or digest==wanted,'Actual bounded evidence hash');pins[key]=digest
    pin(PARENT);pin(__file__)
    completed={}
    for name in ('audit_v4167_cpu_busy_attack_windows','audit_v4173_terminal_ready_probe_log_seal','audit_v4193_mirror_guard_zoning_source_preflight'):
        p=ROOT/name/'report.json';r=json.loads(p.read_text());need(r['passed'] and not r['fullPortAcceptance'],'Actual completed bounded evidence');completed[name]=r;pin(p)
        for p,h in r['inputHashes'].items():pin(p,h)
    analysis=completed['audit_v4167_cpu_busy_attack_windows']
    need(analysis['actualCompletedUppercutWindows']==analysis['windowsBeginningWithCpuBusyFlag']==analysis['windowsBeginningWithCpuBodyAttackLock']==analysis['windowsWithOwnDamageBeforeHP']==38 and analysis['actualBothUnlockedCloseMileenaFields']==0,'All actual terminal attack attempts began while CPU locks active; not safe stance from303 category')
    failures=[]
    for cap,out in ((4170,4171),(4176,4177),(4180,4181),(4184,4185)):
        folder=next(ROOT.glob(f'audit_v{cap}_current_sonya_p2_*'))
        p=next(ROOT.glob(f'audit_v{out}_current_sonya_p2_*'))/'report.json'
        r=json.loads(p.read_text());need(r['passed'] is False and json.loads((folder/'result.json').read_text())['exit_code']==0,'Native runtime terminal, independent diagnostic stays false')
        failures.append(dict(report=str(p),capture=str(folder),error=r['error']));pin(p)
        for path in folder.rglob('*'):
            if path.is_file():pin(path)
        need(not any(path.suffix in ('.bin','.png','.wav') for path in folder.rglob('*') if path.is_file()),'Failed raw timeout image removed; no new raw guest/raster/audio copies remain')
    fastest=ROOT/'audit_v4184_current_sonya_p2_block_release_uppercut_transition_ram/run.log'
    text=fastest.read_text()
    need('MK2_HSPECIAL_COMMAND frame=1661 ' in text and 'command=1661 entry=-1 recovered=-1' in text and 'reason=no_activation_or_full_recovery' in text,'Actual fast HP1..3 failed against passive opponent, not a CPU timing solution')
    stale=ROOT/'audit_v4191_mirror_guard_zoning_source_preflight/report.json';pin(stale)
    need(json.loads(stale.read_text())['inputHashes'][str((ROOT/'tools/run_mirror_guard_zoning_campaign_ram_v4187.py').resolve())]!=sha(ROOT/'tools/run_mirror_guard_zoning_campaign_ram_v4187.py'),'Old preflight runner binding knowingly superseded before boot, never accepted as current')
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId=132964 OR ProcessId=60736 OR ProcessId=102752" | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and q.stdout.strip(),'Current authoritative job check')
    processes=json.loads(q.stdout)
    if isinstance(processes,dict):processes=[processes]
    by={p['ProcessId']:p for p in processes}
    need(132964 in by and 60736 in by and by[132964]['ParentProcessId']==60736 and capture.LUA in by[132964]['CommandLine'] and 'run_mirror_guard_zoning_campaign_ram_v4187.py' in by[60736]['CommandLine'],'Exact new genuine physical campaign live now')
    folder=ROOT/'audit_v4188_sonya_mirror_guard_zoning_p2_campaign'
    need(not (folder/'result.json').exists(),'New native campaign not terminal')
    for name in ('process.json','guest_memory_proof.json','input_hashes_before.json','source_snapshot_paths.json'):pin(folder/name)
    proof=json.loads((folder/'guest_memory_proof.json').read_text());need(proof['everyActualByteComparedInRAM'] and proof['guestDumpFilesWritten']==0,'Actual entire3836 initialized guest remains independently RAM-bound')
    for name in ('mk2ks_block_release_uppercut_ram_v4168.lua','tools/run_block_release_uppercut_ram_v4169.py','tools/seal_terminal_ready_and_probe_logs_v4172.py','mk2ks_block_release_uppercut_ready_ram_v4174.lua','tools/run_block_release_uppercut_ready_ram_v4175.py','mk2ks_block_release_uppercut_both_guards_ram_v4178.lua','tools/run_block_release_uppercut_both_guards_ram_v4179.py','mk2ks_block_release_uppercut_transition_ram_v4182.lua','tools/run_block_release_uppercut_transition_ram_v4183.py','mk2ks_mirror_guard_zoning_campaign_ram_v4186.lua','tools/run_mirror_guard_zoning_campaign_ram_v4187.py','tools/qualify_mirror_guard_zoning_source_v4190.py','tools/qualify_mirror_guard_zoning_source_v4192.py'):pin(ROOT/name)
    pendingWhole=state['pendingSonyaP2GuardCampaign']
    if 102752 in by:
        need('verify_guard_uppercut_ready_whole_campaign_v4160.py' in by[102752]['CommandLine'],'Exact prior whole qualifier live, not stale state')
        pendingWhole.update(wholeQualifierLiveProcesses=[by[102752]],status='Native4146 terminal0 and consumed23118; full whole qualifier1580/PID102752 still confirmed live')
    else:
        need((ROOT/'audit_v4161_guard_uppercut_ready_whole_campaign_checked/report.json').exists(),'Terminal qualifier report when process missing')
        pin(ROOT/'audit_v4161_guard_uppercut_ready_whole_campaign_checked/report.json');pendingWhole['status']='Whole qualifier native process missing with actual terminal4161 report; consume exact1580 next'
    cleanup=completed['audit_v4173_terminal_ready_probe_log_seal']
    need(cleanup['reclaimedAllocatedBytes']==30187233 and cleanup['deletedFiles']==1,'Only single-count current lossless logs plus exact unwanted timeout screenshot')
    with (folder/'run.log').open() as stream:
        rows=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in stream if line.startswith(('MK2_NAT_CAMPAIGN_STAGE ','MK2_NAT_CAMPAIGN_LOSS '))]
    state.update(inputHashes=pins,previousCheckpoint=str(PARENT),inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Preserve complete inherited goal/exclusions and every immutable shared input.'),previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: prior full campaign qualifier1580/PID102752 revalidated live, never restarted. Actual terminal4146 analysis proves all38 uppercut attempts began with CPU busy/body locks and all suffered damage before HP. Four physical block-release probes preserved false: initial readiness predicates omitted native guard/duck-transition categories; final corrected guard preparation120 fields and HP1..3 command actually ran but produced no HUMAN107 against passive SubZero. Do not install that shortcut or credit intended input as activation. Original clean P2 uppercut4157 still valid. New physical policy changes only dispatch to guard true mirror18; restores original zoning for all other standard roster, native boss/ending code unchanged. Superseded initial preflight baseline hash labels and stale unexecuted-runner binding are preserved, fresh4193 has exact actual wrapper/expanded controller/current runner pins before boot. New true3836 SonyaP2 campaign49138/native132964/collector60736 confirmed live. Losslessly sealed terminal logs30138368B and removed one unwanted48865B timeout PNG (30187233B reclaimed once); no game/public build/ZIP change. Full original remaining five groups retained.',
      pendingSonyaP2GuardCampaign=pendingWhole,
      currentSonyaP2CpuLockDiagnosis=dict(report=str(ROOT/'audit_v4167_cpu_busy_attack_windows/report.json'),actualWindows=38,cpuBusyAndBodyLocksInAllWindows=True,ownDamageBeforeHPInAllWindows=True,observationalOnly=True),
      currentSonyaP2BlockReleaseProbeFailures=failures,currentSonyaP2FastBlockReleaseRejected=True,
      pendingSonyaP2MirrorZoningCampaign=dict(execSession=49138,nativePID=132964,collectorPID=60736,currentLiveProcesses=[by[132964],by[60736]],capture=str(folder),runner=str(ROOT/'tools/run_mirror_guard_zoning_campaign_ram_v4187.py'),preflight=str(ROOT/'audit_v4193_mirror_guard_zoning_source_preflight/report.json'),observationReport=str(ROOT/'audit_v4189_mirror_guard_zoning_campaign_observed/report.json'),lastNativeStageOrLoss=rows[-1],completed=False,towerClearAccepted=False,endingPixelsAccepted=False,completeCampaignAudioAccepted=False),
      supersededPreflight=dict(report=str(stale),reason='Old baseline wrapper/expanded hash labels and runner pin superseded before capture boot by exact4193; old report never used as current acceptance'),
      currentTurnReclaimedAllocatedBytes=30187233,currentTurnDeletedFiles=1,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,
      cleanupAccounting='30187233B new reclamation only:30138368B lossless terminal logs +48865B single unwanted automatic timeout PNG removed permanently. Historical39129088B,720896B,54194176B were already recorded; never add again.',
      nextImplementationAction='Poll exact1580/PID102752 full old ready-campaign qualifier and49138/native132964/collector60736 new mirror-only guard + original zoning campaign. Both live now; no restart on observation timeout. Consume only real terminal handles and inspect4161 and4188result/4189observer. Qualify complete new actual mirror input replay and whole original native campaign/health/schedule/paidcontinue/ending/boss-input grammar using fresh source/report, not copied green prefix. New policy aims full natural SonyaP2 clear by combining successful mirror handling with original zoning that actually previously reachedstage12; no prediction accepted as a clear. Do not use rejected HP1..3 shortcut or CPU303=duck/CPU507=uppercut guesses. Full original five groups including all arenas/move phases/ground shadows/audio/finishers/victims/morphs/secrets/cinematics, full native tower own endings/attract, combined UI/ladder/names/audio and dependency-aware cleanup/refreshed ZIP remain open. Original clean P2 uppercut4157 is bounded only. Public1836/ZIP, installed binary and dirty sources unchanged.',
      gameSourceAndPlayableBytesChangedThisTurn=False,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Full original goal unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),currentNativePID=132964,currentExecSession=49138,reclaimedAllocatedBytes=30187233,goalStatus='active',fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
