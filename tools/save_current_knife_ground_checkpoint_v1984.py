"""Retain full goal after resolving a wrong-phase camera sole measurement.

No game-byte changes and no broad grounding, campaign or release claim.
The earlier observations and failed counterexample harness are preserved.
"""
import json
from pathlib import Path
import verify_current_knife_publication_ground_v1981 as current

ROOT=current.ROOT;PREVIOUS=ROOT/'audit_v1979_current_cpu_knife_visual_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v1984_current_knife_ground_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'
    pins=dict(prior['inputHashes'])
    def pin(file,wanted=None):
        file=Path(file);actual=current.current.state.launch.sha(file)
        assert wanted is None or actual==wanted,'Changed evidence '+str(file)
        assert str(file)not in pins or pins[str(file)]==actual,'Conflicting evidence'
        pins[str(file)]=actual
    pin(PREVIOUS)
    accepted={}
    for leaf in('audit_v1981_current_knife_publication_ground','audit_v1983_current_knife_publication_ground_counterexamples'):
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text())
        assert proof['passed']and proof['candidate']==prior['currentCandidate']and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():pin(file,wanted)
        pin(path);accepted[leaf]=proof
    diagnostic=ROOT/'audit_v1980_current_knife_sole_layers/report.json'
    pin(diagnostic);observation=json.loads(diagnostic.read_text())
    assert observation['passed']and observation['observationOnly']
    failed=ROOT/'audit_v1982_current_knife_publication_ground_counterexamples/report.json'
    pin(failed);failure=json.loads(failed.read_text());assert not failure['passed']
    for file in('tools/inspect_current_knife_sole_layers_v1980.py','tools/verify_current_knife_publication_ground_v1981.py',
        'tools/test_current_knife_publication_ground_v1982.py','tools/test_current_knife_publication_ground_v1983.py'):
        pin(ROOT/file)
    pin(Path(__file__).resolve())
    for file,wanted in pins.items():assert current.current.state.launch.sha(file)==wanted,'Changed authoritative input '+file
    ground=accepted['audit_v1981_current_knife_publication_ground']
    counter=accepted['audit_v1983_current_knife_publication_ground_counterexamples']
    assert ground['allEightBodyPosesInspected']and ground['sourceBoundQueuedProjection']and ground['knifeReleaseContactAccepted']
    assert len(ground['records'])==50 and len(counter['counterexamples'])==11
    raised=[r for r in ground['records']if r['previousLateCameraOffset']<-2]
    assert [r['frame']for r in raised]==[2550,2556,2562]
    assert all(r['publicationCameraY']==-8 and r['lateDMAObservedCameraY']==-14 and
        r['originalOffset']==r['unoccludedOffset']==r['finalOffset']==-1 for r in raised)
    return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='no progress: status-only reply; authoritative v1979 checkpoint and all pinned current inputs revalidated before resuming work',
        thisGoalTurnClassification='progress: all eight current CPU knife release poses in both throws have source-bound queued camera/cache/display coordinates and normal native floor contact; false raised-sole measurement resolved; 11 actual coordinate/camera/source corruptions rejected',
        currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentKnifeReleaseGround=dict(sampledFrames=50,bodyPoses=8,actualThrows=2,normalNativeSoleOffset=-1,
            sourceBoundQueuedProjection=True,unoccludedOriginalCompositeMatches=True,noFootContactRowLostToOtherLayers=True,
            previousRaisedReadings=[{k:r[k]for k in('frame','publicationCameraY','lateDMAObservedCameraY','previousLateCameraOffset','finalOffset')}for r in raised],
            confirmedPortOffsetBug=False,
            explanation='Original FF804150 subtracts the publication A4 camera, FF804290 subtracts cached part offsets, FF804400 adds display A5 and FF804410 publishes the resulting FIFO XY. DMA uses that queued XY unchanged. Reading the later global camera for that already queued body introduced a false 6px discrepancy. No sprite or actor Y shift is warranted for these poses.'),
        counterexamplesRejected=len(counter['counterexamples']),
        priorDiagnosticPreserved=str(diagnostic),failedAttemptPreserved=dict(report=str(failed),error=failure['error'],
            correction='The first counterexample harness cloned the same row twice in one Python expression; argument evaluation updated a detached dictionary. The fresh v1983 harness copies each row once before mutation. Every intended mutation now reaches the tested in-memory trace and is rejected; actual evidence files remain unchanged.'),
        acceptedReports={leaf:str(ROOT/leaf/'report.json')for leaf in accepted},
        scopeCaveats=['These are current physical P2 Kano CPU mirror knife release poses in the two actual throws already source/render/lifecycle bound by v1978. Other moves, slots, victims, stages and audio remain outside this new grounding gate.',
            'The prior v1980 observations used late DMA-time camera values for the independent composite measurement. They remain preserved as diagnostics; v1981 separately binds the correct camera at actual native publication.',
            'No game source, executable, ROM, CMD, ZIP or existing capture/report was changed, and no old build folder was deleted this turn.',
            'All full-port, full campaign/ending and finished-release gates remain open.'],
        remaining=prior['remaining'],
        nextAction='Proceed to the remaining opposite-slot Sonya CPU special rendering/ground-shadow and actual recovery/overlap paths, using natural physical controls and source-bound queued transforms; then broader move/arena/audio, remaining finishers/victims/morphs/secrets/cinematics, genuine boss/campaign clears and own endings/attract, dependency-aware obsolete-build cleanup and final combined release regression.',
        inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
        allMoveArtGroundShadowAudioAccepted=False,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
        allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,
        finishedRelease=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed checkpoint'
    result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=result['goalStatus'],sampledFrames=50,bodyPoses=8,actualThrows=2,
        counterexamplesRejected=result['counterexamplesRejected'],pinnedFiles=len(result['inputHashes']),finishedRelease=False)),flush=True)
