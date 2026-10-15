"""Save completed current P2 CPU bicycle evidence without shrinking the full goal."""
import json
from pathlib import Path
import verify_current_sonya_p2_cpu_bicycle_display_v2007 as current

ROOT=current.ROOT
PREVIOUS=ROOT/'audit_v1996_current_sonya_p2_cpu_display_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2012_current_sonya_cpu_bicycle_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
    pins=dict(prior['inputHashes'])
    def pin(file,wanted=None):
        file=Path(file);actual=current.state.sha(file)
        assert wanted is None or actual==wanted,'Changed authoritative evidence '+str(file)
        assert str(file)not in pins or pins[str(file)]==actual,'Conflicting evidence '+str(file)
        pins[str(file)]=actual
    pin(PREVIOUS);accepted={}
    leaves=('audit_v2007_current_sonya_p2_cpu_bicycle_display_kano_checked',
        'audit_v2008_current_sonya_p2_cpu_bicycle_erase_checked',
        'audit_v2011_current_sonya_p2_cpu_bicycle_counterexamples')
    for leaf in leaves:
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text())
        assert proof['passed']and proof['candidate']==prior['currentCandidate']and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():pin(file,wanted)
        pin(path);accepted[leaf]=proof
    scene,clear,counter=(accepted[leaf]for leaf in leaves)
    assert scene['allOriginalBicyclePosesVisible']and not scene['heldOriginalScanouts']
    assert scene['sampledFrames']==scene['exactReplayedFrames']==clear['continuousExactFlips']==91
    assert clear['continuousExactPreBuffers']==91 and clear['oneInitialBaseOnly']and not clear['laterBuffersUsedAsAnchors']
    assert len(counter['counterexamples'])==26 and all(r['rejected']for r in counter['counterexamples'])
    failed=ROOT/'audit_v2009_current_sonya_p2_cpu_bicycle_counterexamples/report.json'
    failure=json.loads(failed.read_text());assert not failure['passed'];pin(failed)
    pin(ROOT/'tools/test_current_sonya_p2_cpu_bicycle_v2009.py')
    # This extended run has a different real-human policy. It is discovery
    # evidence, not the original paired fixture or an accepted ring contract.
    diagnostic=ROOT/'audit_v2010_sonya_p2_cpu_jump_guard_kano'
    meta=current.state.matched(diagnostic,pins)
    assert (meta['player'],meta['boot_frame'],meta['confirm_age'],meta['policy'],meta['approach'])==('kano',604,264,'jump_guard','guard_until_close')
    log=(diagnostic/'run.log').read_text(encoding='utf-8-sig')
    events=current.bicycle.overlap(log,'EVENT')
    ring=[r for r in events if r['kind']=='ring'];assert len(ring)==1
    entry=ring[0];assert entry['id']==18 and entry['entry']==0xffffb400 and entry['pc']==0xffffb410
    children=current.bicycle.overlap(log,'CHILD');retired=current.bicycle.overlap(log,'RETIRE')
    assert len(children)==len(retired)==1
    born,retire=children[0],retired[0]
    assert born['shot_owner']==retire['shot_owner']==entry['a8']and born['a8']==retire['a8']and born['a13']==retire['a13']
    regained=next(r for r in events if r['kind']=='regain'and r['frame']>entry['frame']and r['a8']==entry['a8']and r['a13']==entry['a13'])
    discovery=dict(folder=str(diagnostic),terminalExit=meta['exit_code'],policy=meta['policy'],
        actualRingEntry=entry['frame'],actualChildBirth=born['frame'],actualOwnRegain=regained['frame'],actualChildRetirement=retire['frame'],
        acceptedRingContactRenderOrRecovery=False,
        scope='source-pinned natural physical-input discovery only; complete typed ring contact/child/visual/recovery proof remains required')
    for file in ('mk2ks_physical_p2_cpu_bicycle_trace_v2002.lua','mk2ks_physical_p2_cpu_bicycle_display_v2003.lua',
        'tools/run_current_physical_p2_cpu_bicycle_display_v2004.ps1','tools/current_sonya_cpu_bicycle_contract_v2006.py',
        'tools/verify_current_sonya_p2_cpu_bicycle_display_v2007.py','tools/check_current_sonya_p2_cpu_bicycle_erase_v2008.py',
        'tools/test_current_sonya_p2_cpu_bicycle_v2011.py'):
        pin(ROOT/file)
    pin(Path(__file__).resolve())
    for file,wanted in pins.items():assert current.state.sha(file)==wanted,'Changed evidence '+file
    bike=scene['state']
    return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='no progress: the user-requested status turn inspected saved results but changed no implementation or acceptance evidence; revalidated and advanced the next safe physical CPU-special check',
        thisGoalTurnClassification='progress: naturally selected current P2 Sonya bicycle miss has exact startup/seek/ceiling/fall/fractional landing/native cleanup, nine donor poses, all91 scanouts, original floor shadows and one-base erase; all26 corruption cases rejected; a separate natural ring discovery changes the next action',
        currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentP2SonyaBicycle=dict(human='kano',CPU_slot=2,human_slot=1,stage=0,contact='miss',
            start=bike['start'],fall=bike['fall'],ready=bike['ready'],activeFields=bike['fields'],damage=bike['damage'],
            nativeFractionalLandingY=bike['fractionalLandingY'],completeOriginalPoses=len(bike['poses']),
            subsequentOriginalLegAndOrdinaryTrajectoryUnchanged=True),
        totalSampledFrames=scene['sampledFrames'],exactScreenPixels=scene['exactScreenPixels'],
        exactOwnedPixels=scene['exactOwnedPixels'],fullPhysicalPaletteChecks=scene['fullPhysicalPaletteChecks'],
        nativeShadowCopies=scene['nativeShadowCopies'],sourceBoundProjections=scene['sourceBoundProjections'],
        originalDonorPieces=scene['originalHeldDonorPieces'],nativeShiftTransfers=clear['nativeShiftTransfers'],
        counterexamplesRejected=26,acceptedReports={leaf:str(ROOT/leaf/'report.json')for leaf in leaves},
        failedHarnessPreserved=dict(report=str(failed),error=failure['error'],
            correction='The in-memory mutation helper double-escaped its regex and newline literals, causing duplicate-field matching before state counterexamples ran. Fresh v2011 fixes only the harness escaping, reruns every corruption and confirms the untouched actual capture still passes. No gameplay/capture/model contract was relaxed.'),
        nextRingDiscovery=discovery,
        scopeCaveats=['Only this genuine current P2 Sonya bicycle miss against human Kano at Dead Pool is newly accepted; collision damage, interruption, other CPU bicycle contacts/slots/arenas/audio remain separate gates.',
            'All nine original startup/cycling poses and eleven original donor parts have visible source-bound scanouts. Original shared fall, cleanup and ready code is unchanged. Native integer floor clamp retains fractional Y A000; no arbitrary foot offset was introduced.',
            'Thirty actual post-regain scene fields are retained. Native CPU immediately walking or choosing an ordinary attack is not mistaken for a stuck special or suppressed to manufacture idle frames.',
            'Full91-scene erase replay begins from one original base; every later buffer is a target, not a new anchor. Floor shadows retain the original compressed quarter-row routine and black pen.',
            'No old folder was deleted. New captured evidence is losslessly NTFS compressed. No playable executable, game source, ROM, CMD or ZIP changed.',
            'Other moves/AI/arenas/audio, finishers/victims/morphs/secrets/cinematics, genuine full boss/campaign clears, own endings and attract return remain unfinished or unverified. Existing ZIP is a playtest.'],
        remaining=prior['remaining'],
        nextAction='Use the naturally chosen P2 Sonya ring in source-pinned audit_v2010 (entry2963, child2978, ownregain3013, childretire3019) to obtain full typed native collision/child/recovery and exact consecutive visual/shadow/erase proof. Continue Square Wave and all remaining contacts/moves/arenas/audio, finishers/victims/morphs/secrets/cinematics, genuine boss/ladder clears and own endings/attract, dependency-aware old-build cleanup and final combined release regression.',
        inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
        allMoveArtGroundShadowAudioAccepted=False,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
        allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,finishedRelease=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve existing checkpoint'
    result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('goalStatus','totalSampledFrames','exactScreenPixels','nativeShadowCopies','nativeShiftTransfers','counterexamplesRejected','finishedRelease')}),flush=True)
