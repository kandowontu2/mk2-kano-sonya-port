"""Preserve full unfinished port scope; record bounded both-human blocked visuals."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_bicycle_block_render_v3362 as current

ROOT=current.ROOT;OUT=ROOT/'audit_v3369_current_bicycle_block_render_full_scope_checkpoint'
PREVIOUS=ROOT/'audit_v3355_current_bicycle_block_full_scope_checkpoint/checkpoint.json'
need=current.need;sha=current.state.current.assembly.sha

def main():
    need(not OUT.exists(),'Never overwrite executed full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance'] and
         not state['finishedRelease'] and not state['actualEndingsAccepted'] and
         state['currentRealShaoKahnMatchClears']==0 and state['currentNativeBicycleBothHumanSlotsBlockedStateAccepted'],
         'Original full scope and bounded previous block proof remain intact')
    fresh={}
    def pin(path,digest=None):
        path=Path(path).resolve();key=str(path);digest=digest or sha(path)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh executed bytes')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel inherited evidence')
        fresh[key]=digest
    def proof(relative):
        path=ROOT/relative;value=json.loads(path.read_text())
        need(value['passed'] and not value['fullPortAcceptance'],'Bounded executed positive evidence only')
        pin(path)
        for file,digest in value['inputHashes'].items():pin(file,digest)
        return value
    checked=proof('audit_v3360_current_bicycle_block_display_state_checked/report.json')
    visual=proof('audit_v3363_current_bicycle_block_render_erase_checked/report.json')
    raster=proof('audit_v3365_current_bicycle_block_render_counterexamples/report.json')
    erase=proof('audit_v3367_current_bicycle_block_erase_counterexamples/report.json')
    need(checked['physicalFixtures']==2 and checked['nativeFields']==720 and checked['sourceBoundStateStores']==24 and
         checked['actualBothPhysicalSlotsBlockedChipAndRecoveryAccepted'], 'Both actual physical human roles and entire original state/input trajectories checked')
    need(visual['physicalFixtures']==2 and visual['fullCapturedBlockedNativeBodyPaletteShadowEraseAccepted'] and
         visual['sampledFrames']==134 and visual['exactScreenPixels']==13614400 and
         visual['nativeShadowCopies']==15212 and visual['sourceBoundProjections']==484 and
         visual['continuousExactFlips']==134 and not visual['fullDefenderHorizontalPushAndAudioAccepted'] and
         not visual['allCPUOrArenasKOOverlapAccepted'], 'Every captured native blocked body/palette/shadow/erase; broader gates stay open')
    for unit,count in ((raster,32),(erase,36)):
        need(unit['physicalSlots']==2 and unit['actualCounterexamplesRejected']==count and
             unit['samePathPositiveControlsAccepted'] and unit['specificRejectionReasonsRequired'] and
             unit['unrelatedMissingEventExceptionsNeverAccepted'] and unit['actualCapturesUnmodified'],
             'Each qualified actual mutation rejected with same-path positive controls')
    for relative in (state['currentCMD'], 'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata',state['currentPlaytestZIP']):
        path=(ROOT/relative).resolve();key=str(path)
        need(key in state['inputHashes'],'Existing public playable guard');pin(path,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):
            need(actual==digest,'Fresh actual sources/capture/evidence/public bytes unchanged')
    state['inputHashes'].update(fresh)
    state.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: existing3172, two compressed both-human-slot blocked Bicycle display captures. All original human-input and native state/event trajectories exactly match prior3347;720nativefields/24writers/2100inputfields remain accepted. Independently source-derived full rendering:134consecutive scenes/13,614,400pixels/15,212native floor-shadow copies/484projections and134native erase/flip replays from one base per case. Original32raster and36erase corruptions specifically rejected with same-path positive controls; captured bytes unchanged. No game edits/builds/EXE/ROM/rawaudio copies/public promotion. Defender horizontal push/audio and all five original groups remain unfinished.',
        currentNativeBicycleBlockedCapturedRasterShadowEraseAccepted=True,
        currentNativeBicycleBlockedDisplayStateReport=str(ROOT/'audit_v3360_current_bicycle_block_display_state_checked/report.json'),
        currentNativeBicycleBlockedRenderEraseReport=str(current.OUT/'report.json'),
        currentNativeBicycleBlockedRasterCounterexampleReport=str(ROOT/'audit_v3365_current_bicycle_block_render_counterexamples/report.json'),
        currentNativeBicycleBlockedEraseCounterexampleReport=str(ROOT/'audit_v3367_current_bicycle_block_erase_counterexamples/report.json'),
        currentNativeBicycleBlockedCapturedScenes=134,currentNativeBicycleBlockedExactScreenPixels=13614400,
        currentNativeBicycleBlockedNativeShadowCopies=15212,currentNativeBicycleBlockedSourceBoundProjections=484,
        currentNativeBicycleBlockedOneInitialBasePerCase=True,currentNativeBicycleBlockedExactEraseFlips=134,
        currentNativeBicycleBlockedQualifiedRasterCorruptions=32,currentNativeBicycleBlockedQualifiedEraseCorruptions=36,
        currentNativeBicycleBlockedFullDefenderHorizontalReplayAccepted=False,currentNativeBicycleBlockedAudioAccepted=False,
        currentNativeBicycleBlockedFullDefenderHorizontalRasterShadowAudioAccepted=False,
        currentNativeBicycleBlockedAllArenasAudioKOOverlapAccepted=False,
        candidateUnderTestNativeBicycleHitOrBlockedAccepted=False,candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
        currentNativeBicycleBlockedCapturedVisualScope='Both genuine human slots, stage0, blocked Sonya Bicycle versus Kano, 67 consecutive frames each: actual startup/seven executed cycle poses/rebound/landing/ready+30. No unexecuted late cycle poses, all CPU/arenas/KO/overlap/audio or full-move acceptance implied.',
        currentNativeBicycleBlockedObserverLegacyDiagnosticLabelsNotOwnershipOracle=True,
        currentNativeBicycleBlockedPythonDynamicSourceWhitespaceWarningHarmless=True,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
        nextAction='Continue existing3172 bounded blocked defender native horizontal push/audio, then remaining move/CPU/arena/KO/overlap contexts and original full-port groups. Captured both-human blocked visuals/floor shadows/cleanup now independently verified; do not redo or promote them as whole-game acceptance. All five groups stay open, including finishers/morphs/secrets/cinematics, natural boss clears/own endings/attract, final integrated UI/audio and refreshed release. Reuse builds, bounded compressed captures, no obsolete recovery/rawaudio recreation.')
    need(state['remaining']==remaining and not state['actualEndingsAccepted'] and state['currentRealShaoKahnMatchClears']==0,
         'Do not narrow original full natural-port goal')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless checkpoint compression verified')
    print(json.dumps(dict(saved=str(path),goalStatus='active',originalRemainingGroups=5,physicalSlots=2,
                         capturedScenes=134,nativeShadowCopies=15212,qualifiedCorruptions=68,
                         freshPinsRehashed=len(fresh),blockedHorizontalOrAudioAccepted=False,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
