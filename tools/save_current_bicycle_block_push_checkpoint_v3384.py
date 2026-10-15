"""Keep full natural-port scope; add actual both-slot blocked horizontal proof."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_bicycle_block_push_v3382 as current

ROOT=current.ROOT;OUT=ROOT/'audit_v3385_current_bicycle_block_push_full_scope_checkpoint'
PREVIOUS=ROOT/'audit_v3369_current_bicycle_block_render_full_scope_checkpoint/checkpoint.json'
need=current.need;sha=current.prior.current.assembly.sha

def main():
    need(not OUT.exists(),'Never overwrite executed full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance'] and
         not state['finishedRelease'] and not state['actualEndingsAccepted'] and
         state['currentRealShaoKahnMatchClears']==0 and state['currentNativeBicycleBlockedCapturedRasterShadowEraseAccepted'],
         'Original full objective and completed bounded visual proof retained')
    fresh={}
    def pin(path,digest=None):
        path=Path(path).resolve();key=str(path);digest=digest or sha(path)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh actual bytes')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Never relabel inherited evidence')
        fresh[key]=digest
    def proof(relative):
        path=ROOT/relative;value=json.loads(path.read_text())
        need(value['passed'] and not value['fullPortAcceptance'],'Actual bounded executed evidence only');pin(path)
        for file,digest in value['inputHashes'].items():pin(file,digest)
        return value
    checked=proof('audit_v3383_current_bicycle_block_push_checked/report.json')
    units=proof('audit_v3381_current_bicycle_block_push_counterexamples/report.json')
    need(checked['physicalSlots']==2 and checked['actualBothPhysicalSlotsNativeBlockedHorizontalAccepted'] and
         checked['actualNativeWaits']==12 and checked['horizontalPhysicalFields']==688 and
         checked['requestedVelocityFields']==720 and checked['sourceBoundRequestHalfStores']==32 and
         checked['noGameOrPublicBuildChanges'] and checked['noNewExecutableROMOrAudioCopies'] and
         not checked['allCPUOrArenasKOAudioAccepted'],'Actual both-slot original dispatch/halfstores/waits/requested and physical movement')
    need([(c['guardEntry'],c['guardStop'],c['defenderPushPixels'])for c in checked['cases']]==[(1602,1614,24),(1601,1613,24)] and
         all(c['defenderGuardReturnAccepted'] and c['bothCapturedHorizontalTrajectoriesAccepted']for c in checked['cases']),
         'Original linked-process physical ordering, exact native duration and natural standing block return')
    need(units['physicalSlots']==2 and units['actualCounterexamplesRejected']==64 and
         units['samePathPositiveControlsAccepted'] and units['specificRejectionReasonsRequired'] and
         units['unrelatedMissingEventExceptionsNeverAccepted'] and units['sourceCaptureAndGameUnchanged'],
         'All actual horizontal faults rejected by qualified intended invariant')
    for relative in (state['currentCMD'],'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata',state['currentPlaytestZIP']):
        path=(ROOT/relative).resolve();key=str(path)
        need(key in state['inputHashes'],'Existing public playable guard');pin(path,state['inputHashes'][key])
    failures=[]
    for report,cause in (
        ('audit_v3377_current_bicycle_block_push_checked/report.json','Harness incorrectly assumed unchanged guard callback/main animation lookup operands. The full independently assembled port intentionally relocates the nineteen-ID tables; successor binds exactly both four-byte pointers and full tables while preserving every original movement/control opcode.'),
        ('audit_v3379_current_bicycle_block_push_checked/report.json','Harness miscounted eight thirty-two-bit writes as nine and assumed every defender starts one field later. Actual both-half trace has sixteen stores per case. Original linked-process order permits same-field P2 or next-field P1 guard dispatch; successor checks actual instruction/causal order and exact native twelve-field loop, all state/input trajectories unchanged.')):
        path=ROOT/report;value=json.loads(path.read_text());need(not value['passed'],'Preserve failed harness evidence');pin(path)
        failures.append(dict(report=str(path),error=value['error'],cause=cause))
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):
            need(actual==digest,'Fresh executed input/capture/source/public bytes unchanged')
    state['inputHashes'].update(fresh)
    state.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: existing3172, read-only compressed both-human native blocked push traces. Entire original3347human and blocked state/event trajectories exactly retained. Actual descriptor selects original guard handler8230, requests signed2px, executes6two-field sleeps across3cycles, clears at12fields and returns to genuine block. Both native lookup relocations and whole19-ID tables independently assembled; all original movement/wait/stop/control opcodes exact.688horizontalfields/720desiredcallbacks/32actual16-bit halfstores/12actualwaits,24pxpush each.64specificactualcounterexamples plus same-path positives. No gameplay/guest/build/audio/public changes; original five groups remain unfinished.',
        currentNativeBicycleBlockedFullDefenderHorizontalReplayAccepted=True,
        currentNativeBicycleBlockedNativePushReport=str(current.OUT/'report.json'),
        currentNativeBicycleBlockedNativePushCounterexampleReport=str(ROOT/'audit_v3381_current_bicycle_block_push_counterexamples/report.json'),
        currentNativeBicycleBlockedHorizontalPhysicalFields=688,
        currentNativeBicycleBlockedRequestedVelocityFields=720,
        currentNativeBicycleBlockedSourceBoundRequestHalfStores=32,
        currentNativeBicycleBlockedActualNativeWaits=12,
        currentNativeBicycleBlockedHorizontalQualifiedCorruptions=64,
        currentNativeBicycleBlockedHorizontalProofScope='Only both genuine human slots on stage0, Sonya Bicycle versus standing-block Kano: native guard dispatch, 12field/24px push, both physical horizontal integrations through180field callbacks and return to block. Not close/max body-push branches, every CPU/arena/KO/overlap, audio or whole-move acceptance.',
        currentNativeBicycleBlockedPushObserverPrototype=str(ROOT/'mk2ks_human_bicycle_block_push_v3370.lua'),
        currentNativeBicycleBlockedPushPrototypeIsNotAcceptanceEvidence=True,
        currentNativeBicycleBlockedPushPrototypeLimitation='Only observed low sixteen-bit request writes; successor3373 explicitly records both halves, correct masked full32-bit before/after and entire callback ledger. Prototype captures retained compressed, no game change.',
        currentNativeBicycleBlockedNewHarnessFailuresPreserved=failures,
        currentNativeBicycleBlockedAudioAccepted=False,currentNativeBicycleBlockedFullDefenderHorizontalRasterShadowAudioAccepted=False,
        currentNativeBicycleBlockedAllArenasAudioKOOverlapAccepted=False,
        candidateUnderTestNativeBicycleHitOrBlockedAccepted=False,candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
        nextAction='Continue existing3172native blocked/hit move audio and remaining CPU/arenas/KO/overlap/morph contexts. Both-human captured blocked horizontal state and full visual/shadow/erase proofs completed; do not redo or promote as whole-game acceptance. Keep original full native arenas/effects/victims/audio, move-phase/CPU/adversity, finishers/morphs/secrets/cinematics, natural boss clears/own endings/attract, final integrated UI/audio/cleanup/refreshed release. Reuse builds and bounded losslessly compressed captures, never recreate retired rawaudio/archive.')
    need(state['remaining']==remaining and not state['actualEndingsAccepted'] and state['currentRealShaoKahnMatchClears']==0,
         'Original full natural-port requirements not narrowed')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless full checkpoint compression verified')
    print(json.dumps(dict(saved=str(path),goalStatus='active',originalRemainingGroups=5,physicalSlots=2,
                         horizontalPhysicalFields=688,requestedVelocityFields=720,nativeHalfStores=32,
                         actualWaits=12,qualifiedCorruptions=64,freshPinsRehashed=len(fresh),
                         blockedAudioAccepted=False,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
