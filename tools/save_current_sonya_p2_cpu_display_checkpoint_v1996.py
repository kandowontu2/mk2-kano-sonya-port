"""Keep full native-character goal active after P2 Sonya leg scene coverage."""
import json
from pathlib import Path
import verify_current_sonya_p2_cpu_leg_display_v1994 as current

ROOT=current.ROOT;PREVIOUS=ROOT/'audit_v1984_current_knife_ground_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v1996_current_sonya_p2_cpu_display_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'
    pins=dict(prior['inputHashes'])
    def pin(file,wanted=None):
        file=Path(file);actual=current.state.sha(file)
        assert wanted is None or actual==wanted,'Changed evidence '+str(file)
        assert str(file)not in pins or pins[str(file)]==actual,'Conflicting input evidence'
        pins[str(file)]=actual
    pin(PREVIOUS);accepted={}
    leaves=('audit_v1994_current_sonya_p2_cpu_leg_display_kano_checked',
        'audit_v1994_current_sonya_p2_cpu_leg_display_sonya_checked',
        'audit_v1990_current_sonya_p2_cpu_leg_erase_checked',
        'audit_v1993_current_sonya_p2_cpu_mirror_leg_erase_checked',
        'audit_v1995_current_sonya_p2_cpu_leg_display_counterexamples')
    for leaf in leaves:
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text())
        assert proof['passed']and proof['candidate']==prior['currentCandidate']and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():pin(file,wanted)
        pin(path);accepted[leaf]=proof
    failed_path=ROOT/'audit_v1988_current_sonya_p2_cpu_leg_display_checked/report.json'
    failed=json.loads(failed_path.read_text());assert not failed['passed'];pin(failed_path)
    predecessor={}
    for leaf in('audit_v1989_current_sonya_p2_cpu_leg_display_checked','audit_v1992_current_sonya_p2_cpu_leg_display_kano_checked'):
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text());assert proof['passed'];pin(path)
        predecessor[leaf]='Preserved earlier source/render pass; the strict v1994 checks additionally bind each tracked publication to full inventory and its exact projection actor/Main, and derive the terminal from original first-ready+30 rather than a fixed fixture frame.'
    for file in('mk2ks_physical_p2_cpu_leg_display_v1985.lua','tools/run_current_physical_p2_cpu_leg_display_v1986.ps1',
        'tools/verify_current_sonya_p2_cpu_leg_display_v1988.py','tools/verify_current_sonya_p2_cpu_leg_display_v1989.py',
        'tools/check_current_sonya_p2_cpu_leg_erase_v1990.py','tools/verify_current_sonya_p2_cpu_leg_display_v1992.py',
        'tools/check_current_sonya_p2_cpu_mirror_leg_erase_v1993.py','tools/verify_current_sonya_p2_cpu_leg_display_v1994.py',
        'tools/test_current_sonya_p2_cpu_leg_display_v1995.py'):
        pin(ROOT/file)
    pin(Path(__file__).resolve())
    for file,wanted in pins.items():assert current.state.sha(file)==wanted,'Changed authoritative evidence '+file
    scenes=[accepted[leaves[i]]for i in(0,1)];clears=[accepted[leaves[i]]for i in(2,3)]
    counter=accepted[leaves[4]]
    assert len(counter['counterexamples'])==28 and all(r['rejected']for r in counter['counterexamples'])
    assert all(s['allFiveHeldOwnAndVictimPosesVisible']and not s['heldOriginalScanouts']for s in scenes)
    assert all(c['oneInitialBaseOnly']and not c['laterBuffersUsedAsAnchors']for c in clears)
    cases={}
    for player,scene,clear in zip(('kano','sonya'),scenes,clears):
        pair=scene['state']['originalContract']
        cases[player]=dict(start=pair['start'],release=pair['release'],complete=pair['complete'],
            damage=pair['damage'],ownReady=pair['own_handoff'],victimReady=pair['victim_handoff'],
            actualFollowup=pair['native_followup'],sampledFrames=scene['sampledFrames'],
            exactScreenPixels=scene['exactScreenPixels'],exactOwnedPixels=scene['exactOwnedPixels'],
            fullPhysicalPaletteChecks=scene['fullPhysicalPaletteChecks'],nativeShadowCopies=scene['nativeShadowCopies'],
            sourceBoundProjections=scene['sourceBoundProjections'],heldDonorPieces=scene['originalHeldDonorPieces'],
            exactPreBuffers=clear['continuousExactPreBuffers'],exactFlips=clear['continuousExactFlips'],
            nativeShiftTransfers=clear['nativeShiftTransfers'])
    return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='progress: v1984 saved source-bound knife queued-camera grounding and rejected shifted camera/geometry evidence',
        thisGoalTurnClassification='progress: current physical P2 Sonya leg grab on Kano and Sonya has every completed native scanout, full own/victim donor poses, FIFO/cache/projection/palettes/shadows, individual recovery and actual ordinary attack; one-base erase replay and 28 rejecting corruptions accepted',
        currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
        gameSourceAndPlayableBytesChangedThisTurn=False,currentP2SonyaLegCases=cases,
        totalSampledFrames=sum(s['sampledFrames']for s in scenes),
        exactScreenPixels=sum(s['exactScreenPixels']for s in scenes),
        exactOwnedPixels=sum(s['exactOwnedPixels']for s in scenes),
        fullPhysicalPaletteChecks=sum(s['fullPhysicalPaletteChecks']for s in scenes),
        nativeShadowCopies=sum(s['nativeShadowCopies']for s in scenes),
        nativeShiftTransfers=sum(c['nativeShiftTransfers']for c in clears),counterexamplesRejected=28,
        acceptedReports={leaf:str(ROOT/leaf/'report.json')for leaf in leaves},
        failedAttemptPreserved=dict(report=str(failed_path),error=failed['error'],
            correction='Original driver requests exit during its terminal register_frame callback, before that callback reaches frame_done. The 175/179 completed scanouts precede the terminal callback; every native paired and ordinary state callback including the terminal remains recorded and exact. No frame gap, pose or native event was discarded.'),
        earlierPassesPreserved=predecessor,
        scopeCaveats=['Both natural CPU choices are Sonya at stage0 Dead Pool. These runs execute full leg grabs and ordinary follow-ups, not Square Wave, bicycle or ring signatures. Do not relabel the ordinary attack as a special.',
            'Each actual pair proves 46 held fields, 23 victim flight fields, native damage35, the exact individual ready handoffs, five complete held own/victim poses and later ordinary cleanup. No arbitrary floor offset or late-camera sole normalization was added.',
            'All354 completed scanouts and complete owned costume palettes match original source/cache/native rendering. Continuous erase uses only the initial base and accounts for every intervening original CPU/DMA/clear operation; later saved buffers are targets, not anchors.',
            'The two new capture leaves inherit lossless NTFS compression. No old folder was deleted and no executable, ROM, source implementation, CMD or ZIP was changed.',
            'Other move/AI/arena/audio paths, finishers/victims/morphs/secrets/cinematics and genuine campaign/boss/own-ending/attract paths remain unfinished or unverified. Current ZIP is still a playtest.'],
        remaining=prior['remaining'],
        nextAction='Obtain natural physical P2 Sonya signature choices (Square Wave/ring/bicycle) and full collision/render/shadow/recovery coverage, without supplying CPU IDs/moves/HP/RNG. Continue remaining move/arena/audio, finishers/victims/morphs/secrets/cinematics, genuine boss/campaign clears and own endings/attract, dependency-aware obsolete-build cleanup and final combined release regression.',
        inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
        allMoveArtGroundShadowAudioAccepted=False,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
        allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,
        finishedRelease=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed checkpoint'
    result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('goalStatus','totalSampledFrames','exactScreenPixels','nativeShadowCopies','nativeShiftTransfers','counterexamplesRejected','finishedRelease')}),flush=True)
