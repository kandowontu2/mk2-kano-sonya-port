"""Complete original goal retained; real terminal campaign and exact live qualifiers/storage."""
import hashlib,json,subprocess
from pathlib import Path
import run_mirror_guard_zoning_campaign_ram_v4187 as current

ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v4199_mirror_zoning_live_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4209_mirror_terminal_storage_live_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'Every immutable inherited logical byte unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);digest=pins.get(key) or sha(p)
        need(wanted is None or digest==wanted,'Actual completed evidence hash: '+key);pins[key]=digest
    pin(PARENT);pin(__file__)
    reports={}
    for name in ('audit_v4161_guard_uppercut_ready_whole_campaign_checked','audit_v4195_mirror_guard_zoning_actual_prefix_checked','audit_v4189_mirror_guard_zoning_campaign_observed','audit_v4205_frozen_friendship_storage_sample'):
        p=ROOT/name/'report.json';r=json.loads(p.read_text());need(r['passed'] and not r['fullPortAcceptance'],'Actual completed bounded proof');pin(p);reports[name]=r
        for p,h in r.get('inputHashes',{}).items():pin(p,h)
        for p,h in r.get('case',{}).get('inputHashes',{}).items():pin(p,h)
    old=reports['audit_v4161_guard_uppercut_ready_whole_campaign_checked']
    need(not old['actualNaturalSonyaP2TowerClearAccepted'] and old['case']['paid_continue_losses']==102 and old['case']['actualWholeGuardInputReplay']['actualCompleteGuardFields']==138520 and old['case']['actualWholeGuardInputReplay']['actualNativeHumanUppercut107Stores']==0,'Whole original grammar and138520control fields accepted as bounded observation, never a tower clear')
    prefix=reports['audit_v4195_mirror_guard_zoning_actual_prefix_checked']
    need(prefix['prefixProofOnly'] and not prefix['completedWholeCampaignAccepted'] and not prefix['campaignClearAccepted'] and prefix['actualCapturedPrefix']['actualCompleteGuardFields']==10041 and prefix['actualCapturedPrefix']['actualNativeLegActivations']==8 and len(prefix['actualRowFaultsRejected'])==14,'Real supplemental complete mirror-only replay,14actual state/input/action faults, not all zoning/controller acceptance')
    folder=ROOT/'audit_v4188_sonya_mirror_guard_zoning_p2_campaign'
    meta=json.loads((folder/'result.json').read_text())
    need(meta['exit_code']==0 and meta['actualNativeFrameCallbacks']==411 and meta['rawRasterFilesWritten']==meta['raw_audio_files_written']==meta['guestDumpFilesWritten']==0,'Actual native terminal0 and411RAMonlyframes')
    with (folder/'run.log').open('rb') as stream:raw=stream.read(prefix['nativeLogPrefixBytes'])
    need(hashlib.sha256(raw).hexdigest().upper()==prefix['nativeLogPrefixSHA256'],'Exact independently replayed native prefix retained')
    for p in folder.rglob('*'):
        if p.is_file():pin(p)
    observed=reports['audit_v4189_mirror_guard_zoning_campaign_observed']['observations'][0]
    need(observed['stages']==list(range(10)) and observed['endingStarts']==observed['endingCompletions']==0,'New combined policy failed to reach own ending, not a predicted clear')
    sample=reports['audit_v4205_frozen_friendship_storage_sample'];need(sample['reclaimedAllocatedBytes']==41115648 and sample['deletedFiles']==0,'Only completed current sample counted once')
    inventory=ROOT/'audit_v4201_current_port_storage_inventory/inventory.json';pin(inventory)
    inv=json.loads(inventory.read_text());need(inv['readOnly'] and any('known live native capture' in p for p in inv['skippedReparsePoints']),'Actual live capture excluded from read-only space inventory')
    bulk=ROOT/'audit_v4207_frozen_friendship_set_compaction';plan=bulk/'plan.json';pin(plan)
    need(len(json.loads(plan.read_text())['targets'])==33517,'Exact bounded ten frozen-leaf compaction plan, no current binaries selected')
    ledger=bulk/'files.jsonl'
    with ledger.open('rb') as stream:prefix_raw=stream.read(ledger.stat().st_size)
    prefix_raw=prefix_raw[:prefix_raw.rfind(b'\n')+1]
    partial=[json.loads(line) for line in prefix_raw.splitlines()]
    need(partial and not any('batchError' in r for r in partial),'Actual verified partial compaction ledger, no completed matrix claim')
    partialSavings=sum(r['reclaimed'] for r in partial)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId=126724 OR ProcessId=118888 OR ProcessId=102752 OR ProcessId=132964 OR ProcessId=60736" | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and q.stdout.strip(),'Current authoritative process check')
    processes=json.loads(q.stdout)
    if isinstance(processes,dict):processes=[processes]
    by={p['ProcessId']:p for p in processes}
    need(all(pid not in by for pid in (102752,132964,60736)),'Old verifier and combined native campaign/collector really terminal')
    need(126724 in by and 'verify_mirror_guard_zoning_whole_campaign_v4196.py' in by[126724]['CommandLine'],'Exact full combined-policy qualifier2326/PID126724 confirmed live')
    need(118888 in by and 'compact_frozen_friendship_sets_v4206.py' in by[118888]['CommandLine'],'Exact bounded storage7745/PID118888 confirmed live')
    need(not (ROOT/'audit_v4197_mirror_guard_zoning_whole_campaign_checked/report.json').exists() and not (bulk/'report.json').exists(),'Two complete qualifications remain genuinely pending')
    for name in ('tools/verify_mirror_guard_zoning_prefix_v4194.py','tools/verify_mirror_guard_zoning_whole_campaign_v4196.py','tools/inventory_current_port_storage_v4200.py','tools/compact_frozen_friendship_sample_v4202.py','tools/compact_frozen_friendship_sample_v4204.py','tools/compact_frozen_friendship_sets_v4206.py'):pin(ROOT/name)
    need(not (ROOT/'audit_v4203_frozen_friendship_storage_sample').exists(),'Original self-matching process preflight failure preserved, no physical compaction happened in4202')
    state.update(inputHashes=pins,previousCheckpoint=str(PARENT),inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='All inherited full-scope requirements/exclusions preserved; compression changes no logical shared bytes.'),previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: consumed old1580 terminal0 with complete original campaign/health/schedule/paidcontinue/ending/boss algorithms and independent138520guard fields/52927ownedstores;102losses/noHUMAN107/noending is bounded failure, not clear. Combined physical mirror+zoning49138 native terminal0 at322771fields/99losses/100selections/411RAMonlyframes/stages0..9/noending; no retry identical losing policy. Actual supplemental mirror prefix passes10041controlfields/8true native Leg tasks/14actual owner/mask/field/inputfaults, explicitly outside other-roster zoning replay and whole-clear claims. Started complete original combined campaign qualifier2326/PID126724 confirmed live. Current read-only hardlink-aware inventory4201 excludes native live leaf and identifies frozen historical evidence bulk; initial4202 storage preflight self-matched its own PowerShell command and made0changes, fresh4204 native-name filter preserves failure. Actual4205 three-file LZX sample saved41115648B with all SHA/size unchanged. Exact ten-frozen-leaf33517file reversible compaction7745/PID118888 running confirmed live with verified partial ledger; full result pending. No native media copies/deletions/new builds, public1836/ZIP and dirty12file source diff preserved. All original five remaining groups intact.',
      currentDevelopmentSonyaP2ReadyWholeReport=str(ROOT/'audit_v4161_guard_uppercut_ready_whole_campaign_checked/report.json'),
      completedReadyCampaignQualifier=dict(execSession=1580,terminalExitCode=0,actualCompleteGuardFields=138520,actualNativeGuardedActionStores=52927,actualHuman107Stores=0,actualPaidLosses=102,towerClearAccepted=False,endingPixelsAccepted=False,completeCampaignAudioAccepted=False),
      currentDevelopmentSonyaP2MirrorPrefixReport=str(ROOT/'audit_v4195_mirror_guard_zoning_actual_prefix_checked/report.json'),currentDevelopmentSonyaP2MirrorPrefix=dict(actualFields=10041,nativeLegTasks=8,actualFaultsRejected=14,prefixOnly=True,nonMirrorZoningReplayAccepted=False,towerClearAccepted=False),
      pendingSonyaP2MirrorZoningCampaign=dict(execSession=49138,terminalExitCode=0,nativePIDMissing=True,collectorPIDMissing=True,capture=str(folder),actualNativeFrameCallbacks=411,actualPaidLosses=99,actualSelections=100,seenStages=list(range(10)),ownEndingReached=False,wholeQualifierExecSession=2326,wholeQualifierPID=126724,wholeQualifierCurrentProcess=by[126724],wholeQualifierReport=str(ROOT/'audit_v4197_mirror_guard_zoning_whole_campaign_checked/report.json'),fullIndependentCampaignAccepted=False),
      currentStorageInventory=str(inventory),pendingFrozenFriendshipCompaction=dict(execSession=7745,pythonPID=118888,currentLiveProcess=by[118888],plan=str(plan),report=str(bulk/'report.json'),exactSelectedFiles=33517,complete=False,partialVerifiedFiles=len(partial),partialVerifiedReclaimedBytes=partialSavings,partialLedgerPrefixBytes=len(prefix_raw),partialLedgerPrefixSHA256=hashlib.sha256(prefix_raw).hexdigest().upper(),partialSavingsAreNotCompletedTotals=True),
      currentTurnReclaimedAllocatedBytes=41115648,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,
      preservedStoragePreflightFailure=dict(source='tools/compact_frozen_friendship_sample_v4202.py',terminalExitCode=1,outputNeverCreated='audit_v4203_frozen_friendship_storage_sample',reason='Broad CIM CommandLine filter matched its own query process; no target was compacted. Fresh4204 limits native process names, changes no storage semantics.'),
      cleanupAccounting='41115648B completed sample reclamation counted once this turn. Active4207 partial row savings are recorded separately as pending; upon complete4207 use only its report total, never add partial rows or previous sample twice. Historical30187233B/39129088B/720896B/54194176B and large Oct5 deletions were already counted.',
      nextImplementationAction='Poll exact2326/PID126724 complete combined-campaign verifier and7745/PID118888 exact ten-leaf storage compactor, both confirmed live. Never restart on observation timeout. Only real terminal report4197/4207 confirms complete proof/savings; immutable failures require fresh source/leaf repairs. Combined mirror+zoning native run still lost99paidcontinues atMileena9; do not label20/21roundwins or prefix replay as towerclear and do not repeat identical losing policy. Further physical strategy must use actual native action/collision/command feedback, no AI/difficulty/health/position/RNG/roster assistance and no rejected HP1..3 shortcut. Advance other original open groups independently: native Jax arm-rip full audio still pending; inspected4057/4059/4058 headclap full PCM/DCS/queue paired framework and4073/4074/4078 original147field arm task/palette proof. An arm audio adaptation must use true11killer and17/18victims, actualBBBBlowPunch gap96 and entryFF8BE240, preserve original1074 earned state/palette grammar and RAM-only full initialized guest/PCM; never copy headclap codes/188wrap or claim samples-on/off equality without actual evidence. All original five groups remain: broader Pit/Tomb branches/mirrors/victim/stage audio; all move art/ground/shadows/cleanup/CPU/repeat/KO/overlap arenas; other finishers/victims/morphs/secrets/cinematics; full natural towers/own endings/attract; combined UI/ladder/names/audio, dependency-aware cleanup and final refreshedZIP. Current public1836 installed/dirty sources unchanged. No retired dependency resurrection or broad rejected deletion retries.',
      gameSourceAndPlayableBytesChangedThisTurn=False,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Full original goal unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writing')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),currentCompletedSampleSavings=41115648,pendingCompactionVerifiedFiles=len(partial),pendingCompactionPartialSavings=partialSavings,fullCampaignQualifierExec=2326,storageExec=7745,goalStatus='active',fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
