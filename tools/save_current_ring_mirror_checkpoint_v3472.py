"""Current blocked mirror Ring phase/art/shadow/erase; measured campaign stays pending."""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_cpu_ring_mirror_v3468 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3466_current_guarded_highkick_pending_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3473_current_ring_mirror_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Immutable full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining'];fresh={}
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance']
         and not state['finishedRelease'] and not state['actualEndingsAccepted'],'All original unfinished groups remain')
    def pin(path,digest=None):
        key=str(Path(path).resolve());digest=digest or sha(key)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh relevant proof')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel parent evidence')
        fresh[key]=digest
    def checked(relative):
        path=ROOT/relative;value=json.loads(path.read_text())
        need(value['passed'] and not value['fullPortAcceptance'],'Actual bounded verification only')
        pin(path)
        for file,digest in value['inputHashes'].items():pin(file,digest)
        return value
    scene=checked('audit_v3469_current_cpu_ring_mirror_checked/report.json')
    faults=checked('audit_v3471_current_cpu_ring_mirror_counterexamples/report.json')
    need(scene['candidate']=='diagnostic_v3172_native_morph_shadow' and scene['human']=='sonya'
         and scene['independentWholeCurrentGuestAndPayloadAccepted'] and scene['originalPhysicalAndNativeTrajectoryUnchanged']
         and scene['sampledFrames']==scene['continuousExactFlips']==87 and scene['exactScreenPixels']==8839200
         and scene['nativeShadowCopies']==9645 and scene['sourceBoundProjections']==481
         and scene['firstCompleteRingPhaseArtShadowEraseAccepted'] and scene['scene']['state']['blocked']
         and scene['scene']['state']['damage']==6 and scene['scene']['state']['victim']==18
         and not scene['allRepeatedRingArtAccepted'] and not scene['allCPUContextsArenasKOOverlapAudioAccepted'],
         'Fresh actual guarded mirror phase/6chip/donor-art/cache/FIFO/palette/ground/shadow/raster/continuous erase')
    need(faults['qualifiedRejectedCount']==6 and faults['samePathOriginalSceneAndErasePositiveAccepted']
         and not faults['actualCaptureOrGameChanged'],'Six intended actual source/scene/erase invariants, not unrelated failures')
    need(not (ROOT/'audit_v3462_current_sonya_natural_guarded_highkick_campaign/result.json').exists(),
         'Measured campaign still pending; never relabel as a terminal result')
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
        'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
        'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());pin(key,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):
            need(actual==digest,'Every fresh capture/source/public byte unchanged')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),
        parentCheckpointSHA256=fresh[str(PREVIOUS)],mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual fresh current3172 ordinary-controls-only CPU Sonya Ring against human Sonya3467 terminal77703 exit0.3469 whole independently assembled guest/payload/compiled inputs/full original trajectory/native state/HP/guard/6chip/owner/parent/lifetime/recovery plus87scenes8839200pixels9645shadowcopies481projections/87one-base erase/flips passed41196. Six actual one-pixel floor/camera/cache/orphan/shift-source faults reject specific original invariants3471 with same-path positive66470. Manually viewed actual2960launch and3032post-retirement: native poses/ground/shadow/no remaining projectile; not broad UI/audio acceptance. Existing measured guard105campaign3462 still live84580; stage16observed100927, no acceptance. No game/public/build/WAV changes; all five groups kept.',
        current3172NativeCPUBlockedMirrorRingSceneAccepted=True,
        current3172NativeCPUBlockedMirrorRingReport=str(ROOT/'audit_v3469_current_cpu_ring_mirror_checked/report.json'),
        current3172NativeCPUBlockedMirrorRingFaultReport=str(ROOT/'audit_v3471_current_cpu_ring_mirror_counterexamples/report.json'),
        current3172NativeCPUBlockedMirrorRingSampledFrames=87,current3172NativeCPUBlockedMirrorRingShadowCopies=9645,
        current3172NativeCPUBlockedMirrorRingQualifiedFaults=6,current3172NativeCPUBlockedMirrorRingChip=6,
        current3172NativeCPUBlockedMirrorRingManuallyViewedFrames=[2960,3032],
        current3172AllRepeatedRingArtOrAllCPUContextsAccepted=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,newExecutableROMOrRawAudioCopiesThisTurn=0,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
        nextAction='Poll exact live84580 for3462;77703/41196/66470 terminal0. Do not restart completed3467 or rerun3469/3471 for continuity. On3462 terminal execute3461 whole verifier into fresh report, compare normalized complete pre-Shao chronology to current3426/3446 (labels only), then ordered damage/activation/guard/exposure/wins/ending outcomes. Preserve actual both current Kintaro matches, Ring Kano hit and Sonya guarded mirror source/art/shadow/erase/fault proofs without promoting all CPU/repeat/KO/arena/audio. All five original full-port groups remain. No new build/WAV copies, retired recoveries, broad historical rehash or pin-map flattening.')
    need(state['remaining']==remaining,'Original full objective not narrowed')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',remainingGroups=5,currentMirrorRingAccepted=True,
        campaignPending=84580,freshPins=len(fresh),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
