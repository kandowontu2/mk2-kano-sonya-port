"""Keep full native-character goal active after exact CPU knife visual proof."""
import json
from pathlib import Path
import verify_current_cpu_knife_display_v1978 as current

ROOT=current.ROOT;PREVIOUS=ROOT/'audit_v1965_current_kano_cpu_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v1979_current_cpu_knife_visual_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'
    pins=dict(prior['inputHashes'])
    def pin(file,wanted=None):
        file=Path(file);actual=current.state.launch.sha(file)
        assert wanted is None or actual==wanted,'Changed evidence '+str(file)
        assert str(file)not in pins or pins[str(file)]==actual,'Conflicting pinned evidence'
        pins[str(file)]=actual
    pin(PREVIOUS);accepted={}
    for leaf in('audit_v1978_current_cpu_knife_display_checked','audit_v1977_current_cpu_knife_erase_checked'):
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text())
        assert proof['passed']and proof['candidate']==prior['currentCandidate']and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():pin(file,wanted)
        pin(path);accepted[leaf]=proof
    failures={}
    for leaf in('audit_v1969_current_cpu_knife_display_checked','audit_v1970_current_cpu_knife_erase_checked',
        'audit_v1973_current_cpu_knife_display_checked','audit_v1974_current_cpu_knife_erase_checked','audit_v1976_current_cpu_knife_display_checked'):
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text());assert not proof['passed'];pin(path);failures[leaf]=proof['error']
    for file in('mk2ks_physical_p2_cpu_knife_display_v1966.lua','tools/run_current_physical_p2_cpu_knife_display_v1967.ps1',
        'tools/verify_current_cpu_knife_display_v1969.py','tools/check_current_cpu_knife_erase_v1970.py',
        'tools/run_current_physical_p2_cpu_knife_display_v1971.ps1','tools/verify_current_cpu_knife_display_v1973.py',
        'tools/check_current_cpu_knife_erase_v1974.py','tools/inspect_current_cpu_knife_raster_v1975.py',
        'tools/verify_current_cpu_knife_display_v1976.py','tools/check_current_cpu_knife_erase_v1977.py',
        'tools/verify_current_cpu_knife_display_v1978.py'):
        pin(ROOT/file)
    pin(Path(__file__).resolve())
    for file,wanted in pins.items():assert current.state.launch.sha(file)==wanted,'Changed authoritative input '+file
    visual=accepted['audit_v1978_current_cpu_knife_display_checked'];erase=accepted['audit_v1977_current_cpu_knife_erase_checked']
    elevated=[r for r in visual['soleObservations']if r['slot']==2 and r['action']==4 and r['offset']<-2]
    return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='progress: exact P2 Kano mirror choke/knife/block-button/KO/reset proof and 50 rejecting corruptions saved in v1965',
        thisGoalTurnClassification='progress: both owned CPU knives now have original donor/composite/FIFO/palette/pixel/native shadow and continuous erase evidence through genuine round reset; isolated original pointer teardown and scaled drawing paths; raised-phase sole measurements retained for further fidelity investigation',
        currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentCPUVisual=dict(sampledFrames=visual['sampledFrames'],exactScreenPixels=visual['exactScreenPixels'],exactOwnedPixels=visual['exactOwnedPixels'],
            donorPiecesCompared=visual['originalDonorPiecesCompared'],fullOwnedPaletteChecks=visual['fullOwnedPaletteChecks'],nativeShadowCopies=visual['nativeShadowCopies'],
            nativeShadowComponents=visual['nativeShadowComponents'],completePhaseCoverage=visual['completePhaseCoverage'],originalRoundPointerTeardown=visual['originalRoundPointerTeardown']),
        currentCPUContinuousErase=dict(exactPreBuffers=erase['continuousExactPreBuffers'],exactFlips=erase['continuousExactFlips'],
            originalClearLoads=erase['shiftLoads'],originalClearFills=erase['shiftFills'],nativeShiftTransfers=erase['nativeShiftTransfers'],
            oneInitialBaseOnly=erase['oneInitialBaseOnly'],laterBuffersUsedAsAnchors=erase['laterBuffersUsedAsAnchors']),
        groundingInvestigation=dict(measurements=elevated,confirmedPortBug=False,
            reason='Three knife release pose samples have final visible body-mask sole7px above computed native ground; most knife/ordinary samples are1px above. Donor artwork and native floor/source rendering are exact, but intrinsic original choreography, projected shadow/foreground occlusion and artistic grounding have not yet been separated. Do not shift poses or claim universal grounding from this test.'),
        failedVerifierAttemptsPreserved=failures,
        correctedVerifierAssumptions=['Current graphics builder returns bytes; the verifier needs its own bytearray for source-bound effect allocation.',
            'Fresh v1972 launch pins both actual unchanged CPU graphics/operations source files; the earlier v1968 capture lacks those inputs and is not accepted for the continuous erase proof.',
            'Original mode6 legitimately clears both physical fighter pointers, then the original mode7 factories republish the same true actors. Every recorded halfword, PC and unchanged MOVE opcode is checked.',
            'Original round banner uses scaled DMA. The unchanged independently unit-tested v1716 fixed-point source iterator extends the existing replay; no command is skipped or later buffer used as an anchor.',
            'The original factory instruction is opcode0788 (MOVE A8,@physical,1), not0708. Failed expectation is preserved.'],
        acceptedReports={leaf:str(ROOT/leaf/'report.json')for leaf in accepted},
        redundantUnacceptedCapture='audit_v1968_current_kano_p2_cpu_knife_display',
        scopeCaveats=['Both full knife body/intro/impact phases and every actually executed flight phase are visible and source-exact; short natural flight contacts do not execute every possible rotation.',
            'Complete native shadow row stepping and black shadow pen pass for both physical Kano fighters. All-move artistic grounding, other victims/arenas/audio are still not accepted.',
            'All148 retained scenes have exact pixel proof. The continuous erase check covers every intervening original clear/CPU/DMA operation from one base, but not every unsampled displayed screenshot.',
            'No gameplay source, playable executable, CMD or ZIP changed. Current package remains a playtest, not a finished release.'],
        remaining=prior['remaining'],
        nextAction='Separate measured knife-phase sole elevation from original donor choreography and shadow/foreground occlusion before changing any original-art placement; remaining CPU/move art/shadow/audio/arena paths and finishers/victims/morphs/secrets/cinematics; genuine campaign/boss clear, own endings/attract; dependency-aware archive of redundant unaccepted captures/obsolete builds; final combined regression and finished release.',
        inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
        allMoveArtGroundShadowAudioAccepted=False,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
        allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,finishedRelease=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed checkpoint'
    result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=result['goalStatus'],sampledFrames=result['currentCPUVisual']['sampledFrames'],
        nativeShadowCopies=result['currentCPUVisual']['nativeShadowCopies'],nativeClearTransfers=result['currentCPUContinuousErase']['nativeShiftTransfers'],
        groundingInvestigationOpen=True,pinnedFiles=len(result['inputHashes']),finishedRelease=False)),flush=True)
