"""Save natural current P2 CPU ring collision/render/shadow/recovery evidence."""
import json,struct
from pathlib import Path
import verify_current_sonya_p2_cpu_ring_display_v2023 as current

ROOT=current.ROOT
PREVIOUS=ROOT/'audit_v2012_current_sonya_cpu_bicycle_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2034_current_sonya_cpu_ring_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
    pins=dict(prior['inputHashes'])
    def pin(file,wanted=None):
        file=Path(file);actual=current.state.launch.sha(file)
        assert wanted is None or wanted==actual,'Changed authoritative evidence '+str(file)
        assert str(file)not in pins or pins[str(file)]==actual,'Conflicting evidence '+str(file)
        pins[str(file)]=actual
    pin(PREVIOUS);accepted={}
    leaves=('audit_v2023_current_sonya_p2_cpu_ring_display_checked',
        'audit_v2019_current_sonya_p2_cpu_ring_erase_checked',
        'audit_v2031_current_sonya_p2_cpu_ring_counterexamples')
    for leaf in leaves:
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text())
        assert proof['passed']and proof['candidate']==prior['currentCandidate']and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():pin(file,wanted)
        pin(path);accepted[leaf]=proof
    scene,clear,counter=(accepted[leaf]for leaf in leaves)
    assert scene['allRetainedScenesExact']and scene['originalPhysicalTrajectoryUnchanged']and scene['noPhysicalPointerReplacement']
    assert scene['sampledFrames']==clear['continuousExactPreBuffers']==clear['continuousExactFlips']==86
    assert clear['oneInitialBaseOnly']and not clear['laterBuffersUsedAsAnchors']
    assert scene['originalChargePaletteSamples']>0 and scene['restoredReleaseBodyPaletteSamples']>0
    assert len(counter['counterexamples'])==34 and all(r['rejected']for r in counter['counterexamples'])
    failed={}
    explanations={
        'audit_v2018_current_sonya_p2_cpu_ring_display_checked':'Fresh ring verifier retained an old baseline state.CASE reference and old knife-observer filenames. Fresh v2020 names the actual unchanged extended physical chain. No game/capture changed.',
        'audit_v2020_current_sonya_p2_cpu_ring_display_checked':'Native round mode7 ends during the action-entry field. The pre-frame pair driver correctly has no live FIELD at that field. Fresh v2021 requires both all-mode mode7 actors at entry and EVERY subsequent live pair callback; does not invent an entry callback or waive a gap.',
        'audit_v2022_current_sonya_p2_cpu_ring_display_checked':'The generic normal-costume checker was applied to the four deliberate original pink ring-charge poses. Fresh v2023 source-binds all64 donor charge colours/current guest table, positively checks every charge palette and restoration of normal costume on the fifth release pose. It does not drop colour checks or recolour gameplay.',
        'audit_v2024_current_sonya_p2_cpu_ring_counterexamples':'Corruption harness addressed a nonexistent .base alias; this verifier directly uses the common raster object. Fresh v2025 patches only that actual object.',
        'audit_v2025_current_sonya_p2_cpu_ring_counterexamples':'All34 corruptions were rejected and the actual capture passed again, but the harness compared old leg report field names. Fresh v2031 reruns all34 cases and compares the actual ring report fields, including charge/restored palette counts.'}
    for leaf,why in explanations.items():
        path=ROOT/leaf/'report.json';failure=json.loads(path.read_text());assert not failure['passed'];pin(path)
        failed[leaf]=dict(report=str(path),error=failure['error'],correction=why)
    discoveries={}
    for leaf in('audit_v2030_sonya_p2_cpu_jump_back_kano','audit_v2032_sonya_p2_cpu_jump_guard_boot606','audit_v2033_sonya_p2_cpu_jump_guard_mirror'):
        folder=ROOT/leaf;meta=current.state.launch.matched(folder,pins)
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        cold=current.state.one(current.state.P.rows_prefix(log,'MK2_P2CPU_COLD_LIVE '),'Actual diagnostic cold fight')
        events=current.state.original.rows(log,'EVENT')
        signatures=[dict(kind=r['kind'],frame=r['frame'],id=r['id'])for r in events if r['kind']in('square','ring','bicycle')]
        discoveries[leaf]=dict(terminalExit=meta['exit_code'],human=meta['player'],boot=meta['boot_frame'],
            policy=meta['policy'],actualInitialCPU=cold['cpu_id'],actualSchedule=cold['schedule'],
            observedSignatures=signatures,SquareWaveObserved=any(r['kind']=='square'for r in signatures),
            anyContactRenderRecoveryAccepted=False,
            scope='source-pinned physical-input discovery only; Boot606 naturally chose stock Scorpion10 and is NOT Sonya evidence. Backward-jump and mirror runs did not choose P2 Square Wave; do not claim coverage or force an ID/seed/move.')
    guest,_,_=current.state.launch.launch.current.expected()
    def at(address):return(address-0xff800000)//8
    # The current Sonya router encodes separate ring/square/bicycle targets;
    # presence in code is not treated as runtime Square Wave completion.
    router=struct.unpack_from('<27H',guest,0xf7840)
    expected=(0x09c0,250,0x0d5f,0xec20,0xff80,0xc80c,0x09c0,400,0x0d5f,0xec20,0xff80,0xc803,
        0xc080,0xb400,0xffff,0xc080,0xca00,0xffff,0xc080,0xa400,0xfff9)
    assert router[:len(expected)]==expected,'Actual native RNG router includes all three distinct Sonya actions'
    for file in('mk2ks_physical_p2_cpu_ring_trace_v2013.lua','mk2ks_physical_p2_cpu_ring_display_v2014.lua',
        'tools/run_current_physical_p2_cpu_ring_display_v2015.ps1','tools/current_sonya_cpu_ring_contract_v2017.py',
        'tools/verify_current_sonya_p2_cpu_ring_display_v2018.py','tools/check_current_sonya_p2_cpu_ring_erase_v2019.py',
        'tools/verify_current_sonya_p2_cpu_ring_display_v2020.py','tools/current_sonya_cpu_ring_contract_v2021.py',
        'tools/verify_current_sonya_p2_cpu_ring_display_v2022.py','tools/verify_current_sonya_p2_cpu_ring_display_v2023.py',
        'tools/test_current_sonya_p2_cpu_ring_v2024.py','tools/test_current_sonya_p2_cpu_ring_v2025.py',
        'tools/test_current_sonya_p2_cpu_ring_v2031.py','mk2ks_physical_p2_cpu_continuation_v2026.lua',
        'mk2ks_physical_p2_cpu_round_trace_v2027.lua','mk2ks_physical_p2_cpu_overlap_trace_v2028.lua',
        'tools/run_current_physical_p2_cpu_jump_back_v2029.ps1'):
        pin(ROOT/file)
    pin(Path(__file__).resolve())
    for file,wanted in pins.items():assert current.state.launch.sha(file)==wanted,'Changed authoritative evidence '+file
    ring=scene['state']
    return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='progress: current naturally selected P2 Sonya bicycle miss accepted with every native phase, floor shadow, fractional landing and lock cleanup; natural ring discovery changed the next action',
        thisGoalTurnClassification='progress: the natural P2 Sonya ring hit on true Kano now has complete native input/guard branch,22damage,parent cleanup and all41 child callbacks/seven impact holds; all86 consecutive scanouts and original charge/restored palettes/FIFO/projection/shadows/erase pass; all34 corruptions rejected and unchanged capture still passes',
        currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentP2SonyaRing=dict(human='kano',CPU_slot=2,human_slot=1,stage=0,contact='hit',start=ring['start'],
            birth=ring['birth'],hit=ring['hit'],damage=ring['damage'],blocked=ring['blocked'],
            ownReady=ring['ownReady'],childRetirement=ring['retirement'],childFields=ring['childFields'],
            allSevenImpactGroups=ring['impactGroups'],lastScene=ring['lastScene'],
            actualPhysicalBlockReleased=ring['actualPhysicalBlockReleased'],
            nativeMode7To2EntryBoundaryPreserved=ring['nativeMode7To2EntryBoundaryPreserved']),
        totalSampledFrames=scene['sampledFrames'],exactScreenPixels=scene['exactScreenPixels'],
        exactOwnedPixels=scene['exactOwnedPixels'],fullOwnedPaletteChecks=scene['fullOwnedPaletteChecks'],
        originalChargePaletteSamples=scene['originalChargePaletteSamples'],restoredReleaseBodyPaletteSamples=scene['restoredReleaseBodyPaletteSamples'],
        sourceBoundProjections=scene['sourceBoundProjections'],nativeShadowCopies=scene['nativeShadowCopies'],
        nativeShiftTransfers=clear['nativeShiftTransfers'],counterexamplesRejected=34,
        acceptedReports={leaf:str(ROOT/leaf/'report.json')for leaf in leaves},
        failedAttemptsPreserved=failed,naturalChoiceDiscoveries=discoveries,
        currentSonyaRouterAllThreeTargetsPresentButNotRuntimeProof=True,
        scopeCaveats=['Only this genuine P2 Sonya ring HIT on P1 Kano at Dead Pool is newly accepted; blocked/missed/interrupted/mirror/other-arena/audio cases remain separate gates.',
            'Actual victim guard flag1 is not enough to infer a block. Original FF837D40 loads the victim Main, then actual active-low controls show Block released and original FF837AE0 returns CLRC. Ring damage22 is not relabelled as chip6.',
            'The parent starts2963, creates its separate child2978, hits2991, regains3013 and the seven four-field impact poses retire3019. Complete own and child choreography, eleven child poses and thirty post-retirement scenes are retained without suppressing native subsequent actions.',
            'Current donor charge palette64 is required on four release poses; normal costume returns on the fifth. Generic full-bright normal-costume checks are not substituted for original charging colours. Source-bound checks cover both genuine palette states and corruption of either is rejected.',
            'All86 native scanouts are reconstructed. One-base erase accounts for every intervening original CPU/DMA/shift clear; later buffers are targets, never fresh anchors. All9565 original compressed floor-shadow copies and485 queued projections pass without arbitrary XY changes.',
            'Boot606 chose native Scorpion10, not Sonya, and is excluded from added CPU-signature acceptance. Two other natural extended runs still did not choose P2 Square Wave; its real router presence alone is not acceptance.',
            'New captures are losslessly NTFS compressed. No old folder was deleted and no executable, game source, ROM, CMD or ZIP changed. Existing ZIP remains a playtest.',
            'Other contacts/AI/moves/arenas/audio, finishers/victims/morphs/secrets/cinematics and genuine full boss/ladder/own-ending/attract paths remain unfinished or unverified.'],
        remaining=prior['remaining'],
        nextAction='Trace the actual P2 Sonya special router at FFFBC200 and its two original FF80EC20 random comparisons read-only, or obtain another genuine cold physical input route that chooses Square Wave. Never prescribe the CPU ID, move or RNG. Complete Square Wave runtime/contact/render/shadow/recovery and remaining ring contacts, other moves/AI/arenas/audio, finishers/victims/morphs/secrets/cinematics, genuine boss/ladder clears and own endings/attract, dependency-aware old-build cleanup and final release regression.',
        inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
        allMoveArtGroundShadowAudioAccepted=False,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
        allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,finishedRelease=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed checkpoint'
    result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('goalStatus','totalSampledFrames','exactScreenPixels','nativeShadowCopies','nativeShiftTransfers','counterexamplesRejected','finishedRelease')}),flush=True)
