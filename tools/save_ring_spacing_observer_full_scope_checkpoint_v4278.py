"""Terminal Ring-spacing feedback and observer repair; original full goal intact."""
import json,subprocess
from pathlib import Path
import verify_mileena_observer_slot_reuse_source_v4276 as repair
ROOT,need,sha=repair.ROOT,repair.need,repair.sha
PARENT=ROOT/'audit_v4258_mileena_throw_diagnosis_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4279_ring_spacing_observer_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-goal checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'All inherited native/source/public bytes unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);h=sha(p)
        need(key not in pins or pins[key]==h,'Inherited/shared actual source unchanged')
        need(wanted is None or h==wanted,'Exact evidence digest');pins[key]=h
    pin(PARENT);pin(__file__)
    names=('audit_v4262_mileena_ring_spacing_source_preflight',
      'audit_v4270_mileena_ring_spacing_actual_prefix_checked',
      'audit_v4268_mileena_ring_spacing_whole_campaign_checked',
      'audit_v4274_mileena_ring_spacing_throw_windows_observed',
      'audit_v4277_mileena_observer_slot_reuse_source_checked')
    reports={}
    for name in names:
        path=ROOT/name/'report.json';r=json.loads(path.read_text())
        need(r['passed'] and not r.get('fullPortAcceptance',False),'Actual bounded proof, not complete port');pin(path);reports[name]=r
        for p,h in r.get('inputHashes',r.get('case',{}).get('inputHashes',{})).items():pin(p,h)
    whole=reports[names[2]];c=whole['case'];r=reports[names[3]];fixed=reports[names[4]]
    need(c['passed'] and c['actualWholeCampaignGrammarRetained'] and c['actual3836P2WholeCampaignAlgorithmRetained'] and
         not c['unassisted_clear_proven'] and not whole['actualNaturalSonyaP2TowerClearAccepted'],
         'Full original native campaign grammar retained; never turn bounded loss into clear')
    need(c['stages_reached']==list(range(10)) and c['native_own_round_wins']==20 and c['paid_continue_losses']==17 and
         c['ending_starts']==c['ending_completions']==0,'Actual terminal route/wins/losses/no ending')
    need(c['actualWholeRingSpacingInputReplay']['actualNativeOwnRingTasks']==164 and
         r['actualOriginalCpuThrowStores']==33 and r['actualSameFieldOwnedVictimCapturePairs']==26 and
         r['actualMissingHumanCapturePairsExplainedByMainAddressSideReuse']==7 and
         not r['completeNativeThrowInventoryAccepted'],'Genuine own Ring and CPU throw stores; actual observer gap retained')
    need(fixed['actualPredicateChecks']==33988 and
         fixed['originalObserverPredicateModel']['wrongFrozenSidePredicateChecks']==14057 and
         fixed['repairedObserverPredicateModel']['wrongFrozenSidePredicateChecks']==0 and
         fixed['physicalControllerAndGameUnchanged'] and not fixed['nativeRepairedObserverRuntimeProven'],
         'Exact source/model observer fix qualified, runtime still explicitly outstanding')
    windows=r['actualNativeThrowWindows']
    guard=[w for w in windows if w['actualPhysicalDecision']['reason']=='grounded_guard']
    need(len(guard)==24 and all(int(w['actualField']['h_floor'])-int(w['actualField']['h_y'])<=8 for w in guard),
         'Native throw fields remain grounded despite prior Up attempts; never assume jump activation')
    for name in ('mk2ks_mileena_ring_spacing_campaign_ram_v4259.lua','tools/run_mileena_ring_spacing_campaign_v4260.py',
      'tools/qualify_mileena_ring_spacing_source_v4261.py','tools/verify_mileena_ring_spacing_prefix_v4265.py',
      'tools/verify_mileena_ring_spacing_whole_campaign_v4267.py','tools/verify_mileena_ring_spacing_prefix_v4269.py',
      'tools/analyze_mileena_ring_spacing_throw_windows_v4271.py','tools/analyze_mileena_ring_spacing_throw_windows_v4273.py',
      'mk2ks_mileena_ring_spacing_campaign_ram_v4275.lua','tools/verify_mileena_observer_slot_reuse_source_v4276.py'):pin(ROOT/name)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command',
      'Get-CimInstance Win32_Process -Filter "ProcessId=131984 OR ProcessId=124944 OR ProcessId=135716 OR ProcessId=124292" | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Actual collector/native/prefix/whole processes terminal; handles consumed')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Every original full-goal requirement/exclusion and inherited logical byte retained.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: new physical SonyaP2 Ring/backjump spacing only versus nativeMileena; all selection/mirror/other opponents/boss/ownending/attract code unchanged. Native run1596 collector131984/emulator124944 terminal0 consumed:20ownroundwins17paidlosses/stages0..9/noending. Whole original campaign grammar preserved/passed bounded state;16994rangefields164realownRingentries33actualnativeCPUthrow507stores45loggedvictimclears, not a clear. Prefix18754/whole25129/observermodel29079 consumed terminal0. Actual33CPUthrowwrites have genuine PCFF8B6FA0/A0=507;26paired actualnativehuman victim clears,7missingduefrozen-side tracekeyafterMainreuse. Old trace suppressed predicates on9030CPU+5027human fields; repaired4275 keys byslot/Main, all33988actual field predicate modelchecks admitcorrectside,4sourcefaultsreject; native repaired observer runtime still pending.24of33actualCPUthrowwrites occurgroundedguard,allactualhumanheight<=8despitepriorUpattempts6..37fieldsold. Future controller must use actual jump acknowledgment, not40field attempt cooldown. Preserved wrong4265RingfetchPC430 assumption (actual420) and4271everypairassumption, no original capture rerun/rewrites for checkerrepair. No playable/game/public/ZIP edits, new EXE/ROM/native rawmedia, all5originalgroups intact.',
      currentDevelopmentCampaignObservation=str(ROOT/'audit_v4264_mileena_ring_spacing_campaign_observed/report.json'),
      currentDevelopmentCampaignReport=str(ROOT/'audit_v4268_mileena_ring_spacing_whole_campaign_checked/report.json'),
      currentNativeRangeObserverCoverageReport=str(ROOT/'audit_v4274_mileena_ring_spacing_throw_windows_observed/report.json'),
      currentNativeRangeObserverRepairReport=str(ROOT/'audit_v4277_mileena_observer_slot_reuse_source_checked/report.json'),
      currentTerminalMileenaRingSpacing=dict(capture=str(repair.physical.FOLDER),execHandle=1596,terminalExitCode=0,
        collectorPID=131984,nativePID=124944,completeNativeRangeFields=16994,trueHumanID=18,trueOpponentID=5,
        actualOwnRingTaskEntries=164,actualCpuGroundThrowStoresLogged=33,actualVictimClearsLogged=45,
        actualSameFieldThrowCapturePairs=26,missingPairsDueToNativeMainSideReuse=7,
        completeNativeThrowInventoryAccepted=False,wholeOriginalCampaignGrammarRetained=True,
        actualOwnRoundWins=20,actualPaidLosses=17,stagesReached=list(range(10)),
        actualGroundedGuardThrowFields=24,earlierUpAttemptsNotAcceptedAsAirborne=True,
        naturalTowerClearAccepted=False,endingAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False),
      currentReadOnlyObserverSlotReuseRepair=dict(source=str(repair.NEW),sourceReport=str(ROOT/'audit_v4277_mileena_observer_slot_reuse_source_checked/report.json'),
        key='actual slot + native Main address',allNativeOwnershipAndStoreGuardsUnchanged=True,
        originalObservedWrongFrozenSidePredicates=14057,actualNativeFieldPredicateModelChecks=33988,
        repairedModelWrongFrozenSidePredicates=0,actualSourceCounterexamplesRejected=4,
        physicalInputsAndGameUnchanged=True,nativeRuntimeProven=False,oldMissingEventsNotRecreated=True),
      preservedThisTurnFailedAssumptions=[
        dict(source='tools/verify_mileena_ring_spacing_prefix_v4265.py',outputNotCreated='audit_v4266_mileena_ring_spacing_actual_prefix_checked',
             error='Wrong strict native Ring fetch PCFFFFB430; real original dispatcher log and next instruction PCFFFFB420. Fresh4269/4270 corrected checker only.'),
        dict(source='tools/analyze_mileena_ring_spacing_throw_windows_v4271.py',outputNotCreated='audit_v4272_mileena_ring_spacing_throw_windows_observed',
             error='Every native throw was assumed to have a logged same-field victim clear. Actual7gaps caused frozen side/Main observer reuse. Fresh4273/4274 explicitly rejects complete inventory claim.')],
      nextImplementationAction='Do not repeat identical losing1500Ring/backjump40cooldown policy. All24groundedguardthrowfields show Upattemptdidnotyieldairborne; change physical test controller to retry/release Up based on actual native airborne acknowledgment and handle corners, or protected actual Sonya LegGrab. Use fresh Lua based on4275slot/Main observer repair, keeporiginalnativeCPU/difficulty/RNG/health/identity/positions andfullboss/ending/attract scope. Native runtime observer repair stillneedsproof; do not claim model creates missingactualevents. SonyaP2fullnaturalclear/ownending/attract stillopen. Continue all5originalgroups: broadPit/Tombvictims/mirrors/branches/stageaudio, allmoveart/ground/shadows/cleanup/allarenas/CPU/repeat/KO/overlap, otherfinishers/victims/morphs/secrets/cinematics, fulltowers/endings/attract, finalcombinedselection/ladder/names/audio/dependencycleanup/finalZIP. Public1836 unchangedplaytest, notfinal.',
      currentTurnReclaimedAllocatedBytes=0,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,
      cleanupAccounting='No new deletion or reclaimed bytes this turn; native run.log32275174B already NTFS compressed. Historical4207savings3392749568B not counted again.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Every original goal group retained exactly')
    for p,h in pins.items():need(sha(p)==h,'All actual new/inherited logical evidence bytes unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress checkpoint before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),actualNativeOwnRingTasks=164,
      actualCpuGroundThrowStoresLogged=33,observerMissingPairExclusions=7,observerRepairedRuntimeProven=False,
      wholeCampaignGrammarPassed=True,naturalTowerClearAccepted=False,allOriginalRemainingGroups=len(remaining),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
