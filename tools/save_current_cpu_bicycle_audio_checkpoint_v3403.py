"""Preserve full scope and inherit historical pins by hash, not another giant copy."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_bicycle_block_push_v3382 as current

ROOT=current.ROOT;need=current.need;sha=current.prior.current.assembly.sha
PREVIOUS=ROOT/'audit_v3394_current_bicycle_block_audio_full_scope_checkpoint/checkpoint.json'
REPORT=ROOT/'audit_v3402_current_cpu_bicycle_hit_audio_checked/report.json'
OUT=ROOT/'audit_v3404_current_cpu_bicycle_audio_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Never overwrite executed checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and
         not state['finishedRelease']and not state['actualEndingsAccepted']and
         state['currentRealShaoKahnMatchClears']==0,'Original full natural-port objective retained')
    report=json.loads(REPORT.read_text())
    need(report['passed']and report['fullCapturedNaturalCPUBicycleLaunchCryPlaybackAndOwnershipAccepted']and
         (report['cpuSlot'],report['humanSlot'])==(2,1)and report['rawAudioFilesWritten']==0 and
         report['newBuildsOrROMCopies']==0 and not report['allMoveCPUOrArenaAudioAccepted']and
         not report['fullNativeContactDCSWaveformAccepted']and not report['fullPortAcceptance'],
         'Actual bounded naturally selected CPU launch/cry playback only')
    need(report['phase']['start']==2663 and report['phase']['hit']==2680 and report['phase']['damage']==22 and
         report['phase']['ready']==2742 and report['phase']['victimReady']==2767 and
         report['completedFrames']==[2710,2740]and report['mixedPCMUpdates']==302 and
         report['correlation']>.999 and .699<report['gain']<.701,
         'Complete actual cues, native CPU contact and distinct recoveries')
    fresh=dict(report['inputHashes'])
    for path in (PREVIOUS,REPORT,Path(__file__).resolve()):fresh[str(path.resolve())]=sha(path)
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());need(key in state['inputHashes'],'Retained public playable guard')
        fresh[key]=state['inputHashes'][key]
    failed_path=ROOT/'audit_v3399_current_cpu_bicycle_hit_audio_checked/report.json'
    failed=json.loads(failed_path.read_text());need(not failed['passed'],'Failed comparison retained, not acceptance evidence')
    fresh[str(failed_path)]=sha(failed_path)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):
            need(actual==digest,'Fresh relevant input/capture/public bytes unchanged')
            need(file not in state['inputHashes']or state['inputHashes'][file]==digest,'No relabeling of inherited evidence')
    inherited_count=len(state['inputHashes'])
    # The preceding checkpoint remains immutable. Its complete historical map
    # is inherited by path+SHA; no claim of fresh revalidation of that graph.
    state['inputHashes']=fresh
    state.update(
        inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),
            parentCheckpointSHA256=fresh[str(PREVIOUS)],parentFlattenedPinCount=inherited_count,
            mergeRule='Resolve parent recursively; fresh inputHashes must agree with inherited keys. Historical retired/deleted pins keep the parent exclusion policy and are not recreated or revalidated.'),
        historicalPinMapCopiedAgain=False,
        previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: existing3172 genuine CPU Sonya versus human Kano Bicycle hit, normal UI and three forward-jump inputs; native RNG134 choice unprescribed. All9165 original input/state/HP/choice/provenance records retained. Actual mixed PCM isolates full launch+cry from sample-disabled baseline in RAM, .70 route, native onset, correct physical CPU channels and complete finite owner cleanup. No game/build/public or raw-audio changes. Original five groups retained; inherited historical pin graph referenced by SHA instead of copying34MB again.',
        currentNaturalCPUBicycleLaunchCryPlaybackAccepted=True,
        currentNaturalCPUBicycleLaunchCryPlaybackReport=str(REPORT),
        currentNaturalCPUBicycleLaunchCryProofScope='Only stage0, native physical P2 CPU Sonya18 versus P1 human Kano17, independently captured natural RNG134 Bicycle contact. Actual retained launch/cry asset playback, native onset, finite channels and owner cleanup. Not native contact DCS waveform extraction, opposite CPU slot, other arenas/moves, interruptions/KO/overlap, or full move/port acceptance.',
        currentNaturalCPUBicycleFullContactDCSWaveformAccepted=False,
        currentNativeBicycleBlockedAudioAccepted=False,
        currentNativeBicycleBlockedFullDefenderHorizontalRasterShadowAudioAccepted=False,
        candidateUnderTestNativeBicycleHitOrBlockedAccepted=False,
        candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
        currentCPUBicycleAudioHarnessFailure=dict(report=str(failed_path),
            cause='First verifier filtered a nonexistent render label rather than MK2_NAT_CAMPAIGN_. Both terminal captures were unchanged. Successor3400 excludes only actual intentionally omitted renderer records and verifies all9165 remaining native records against original3308 and disabled baseline; no gameplay edit.'),
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,
        publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
        nextAction='Continue native contact/victim audio and remaining CPU/opposite-slot/arena/repeat/interrupt/KO/overlap contexts. Keep all original five groups: full native arena/victim effects, complete moves/ground/shadow/cleanup, finishers/morphs/secrets/cinematics, natural boss clears/own endings/attract, final integrated UI/audio/cleanup/refreshed release. Do not repeat completed bounded blocked or CPU-hit launch/cry checks. Reuse current build; no raw-audio copies or retired archive recreation. Resolve inputHashInheritance before comparing inherited pins; do not flatten/copy the historical map merely to save a checkpoint.')
    need(state['remaining']==remaining,'Full requirements unchanged')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',originalRemainingGroups=5,
        boundedNaturalCPUBicycleLaunchCryAccepted=True,freshPinsRehashed=len(fresh),
        historicalPinsInherited=inherited_count,checkpointBytes=path.stat().st_size,
        parentCheckpointBytes=PREVIOUS.stat().st_size,rawAudioFilesWritten=0,
        fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
