"""Full native-character goal retained after source-bound blade scene resolution.

No public launcher promotion. Complete historical graph is retained; all fresh
relevant dependencies are revalidated. Both changed endpoint scenes are accepted
through original blood/RNG/render/continuous-erasure evidence, not masked pixels.
All broader original requirements and remaining candidate gates stay open.
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
PREVIOUS=ROOT/'audit_v2799_native_palette_ui_special_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2818_native_blade_blood_full_scope_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());fresh={};inherited=dict(prior['inputHashes'])
    assembly.need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
        len(prior['remaining'])==5 and len(prior['currentSourceBoundBossCampaigns'])==70 and
        prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'] and
        prior['candidateUnderTest52CaseHumanStateMatrixAccepted'] and prior['candidateUnderTestFourNativeUIRegressionAccepted'] and
        len(prior['candidateUnderTestUnresolvedBladeEndpointDifferences'])==2,'Original entire unfinished goal and prior actual UI/special evidence retained')
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute() else ROOT/path).absolute())
        if wanted is None:wanted=assembly.sha(key)
        assembly.need(key not in fresh or fresh[key]==wanted,'Consistent fresh source dependency '+key)
        assembly.need(key not in inherited or inherited[key]==wanted,'Immutable retained historical dependency '+key)
        fresh[key]=wanted
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        assembly.need(value['passed'] and not value.get('fullPortAccepted',False) and not value.get('fullPortAcceptance',False),'Actual bounded terminal proof '+leaf)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    blood,blood_path=proof('audit_v2814_native_blade_blood_cause_checked')
    units,units_path=proof('audit_v2816_native_blade_blood_cause_units')
    assembly.need(blood['candidate']==assembly.NAME and blood['bothPreviouslyUnresolvedBladeRecoveryScenesAccepted'] and
        blood['sourceBoundNativeBloodAndRNGAccepted'] and blood['completeCurrentAndPriorConsecutiveScanouts']==258 and
        blood['currentConsecutiveScanouts']==129 and len(blood['cases'])==2,'Both actual source-bound native blood scene differences resolved')
    cases={}
    for side in (1,2):
        case=blood['cases'][f'p{side}']
        assembly.need(case['passed'] and case['changedPixels']==(804 if side==1 else 1068) and
            case['allDifferencesAreOriginalNativeBlood'] and case['changedPixelsOutsideOriginalBlood']==0 and
            case['everyNonBloodRecoveryPixelUnchanged'],'Every changed pixel belongs to original blood, every other pixel unchanged')
        for version,key in ((2802,'current'),(2803,'prior')):
            value=case[key]
            assembly.need(value['sourceBoundFullDrawingAndContinuousErasureAccepted'] and value['completeScanouts']==(65 if side==1 else 64) and
                value['rng']['originalRNGCodeAndEveryObservedArithmeticResultAccepted'] and
                not value['rng']['seedOrHardwareCounterWrittenByObserver'] and value['nativeBloodDraws']>100 and
                value['fullOriginalBloodPaletteChecks']>100 and not value['pixelsOrDMAOperationsAltered'],
                'Actual complete original palettes, projection/FIFO/DMA, pixel operations and RNG instructions accepted')
            render,_=proof(f'audit_v2806_native_blade_blood_{version}_p{side}_render_checked')
            erase,_=proof(f'audit_v2809_native_blade_blood_{version}_p{side}_erase_checked' if version==2802 else f'audit_v2811_native_blade_blood_prior_p{side}_erase_checked')
            assembly.need(render['exactConsecutiveScanouts']==erase['continuousExactPreBuffers']==erase['continuousExactFlips']==value['completeScanouts'] and
                erase['oneInitialBaseOnly'] and not erase['laterBuffersUsedAsAnchors'],'No later framebuffer anchors or unmodeled erasure')
        cases[f'p{side}']=dict(changedPixels=case['changedPixels'],sourceProvenOriginalBloodOnly=True,
            currentScanouts=case['current']['completeScanouts'],priorScanouts=case['prior']['completeScanouts'],
            currentRNGCalls=case['current']['rng']['completeCalls'],priorRNGCalls=case['prior']['rng']['completeCalls'],
            firstNativeHardwareCountDivergence=case['firstObservedNativeRNGDivergence'])
    assembly.need(units['candidate']==assembly.NAME and units['actualOriginalCounterexamplesRejected']==80 and
        units['actualCaptureFilesUnmodified'],'Actual original RNG and blood provenance corruptions rejected')
    failed=[]
    for leaf in ('audit_v2809_native_blade_blood_2803_p1_erase_checked',
        'audit_v2809_native_blade_blood_2803_p2_erase_checked','audit_v2812_native_blade_blood_cause_checked'):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text())
        assembly.need(not value['passed'] and value.get('error'),'Executed diagnostic failure preserved')
        pin(path);failed.append(dict(report=str(path),error=value['error'],accepted=False))
    for name in ('run_native_blade_blood_v2801.ps1','run_native_blade_blood_v2804.ps1',
        'verify_native_blade_blood_render_v2805.py','verify_native_blade_blood_cause_v2807.py',
        'inspect_native_blade_blood_erase_v2808.py','inspect_native_blade_blood_erase_v2810.py',
        'verify_native_blade_blood_cause_v2813.py','test_native_blade_blood_cause_v2815.py'):
        pin(ROOT/'tools'/name)
    pin(ROOT/'mk2ks_human_blade_native_blood_v2800.lua');pin(PREVIOUS);pin(__file__)
    for path,wanted in {
        'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
        'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
        'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
        'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():pin(ROOT/path,wanted)
    print('Revalidating fresh complete native blood proof graph:',len(fresh),'actual files',flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            assembly.need(actual==wanted,'Changed fresh relevant proof '+file)
    inherited.update(fresh)
    resolved=prior['candidateUnderTestUnresolvedBladeEndpointDifferences']
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='progress: four native UI and 52 human move-state fixtures accepted, with two explicit unresolved blade recovery scenes',
        thisGoalTurnClassification='progress: four cold physical blade scenes captured on isolated v2753 and checked v1836, both player slots with unchanged controls and read-only original blood/palette/RNG/CPU/DMA/shift/latch observer. 258 complete source-perfect scanouts and continuous pre-buffer/flip/erasure targets passed. All 804/1068 changed recovery pixels independently classified as original native blood through exact palette/cache/projection/FIFO/DMA provenance; every non-blood pixel unchanged. Original seed/overflow/carry/hardware HCOUNT rotate/stack return verified for all actual calls, with first HCOUNT/result divergence observed without forced seed values. Eighty actual original RNG/blood corruptions rejected. Parser and overly generic projection/control harness failures preserved and corrected in immutable successors. Public build/launcher/ZIP untouched, full original goal still unfinished.',
        candidateUnderTestNativeBladeBloodCauseReport=blood_path,candidateUnderTestNativeBladeBloodUnitsReport=units_path,
        candidateUnderTestNativeBladeBloodSpecificCounterexamples=80,candidateUnderTestNativeBladeScenes=cases,
        candidateUnderTestBothChangedBladeRecoveryScenesSourceAccepted=True,candidateUnderTestCurrentBladeConsecutiveScanouts=129,
        candidateUnderTestCurrentAndPriorBladeConsecutiveScanouts=258,candidateUnderTestBladeContinuousErasureAccepted=True,
        candidateUnderTestResolvedBladeEndpointDifferences=resolved,candidateUnderTestUnresolvedBladeEndpointDifferences=[],
        candidateUnderTestBladeBloodCauseInferredNotProven=False,candidateUnderTestExactCheckedBuildEndpointScenes=154,
        candidateUnderTestAll52CaseEndpointScenesAccepted=True,candidateUnderTestAllEndpointScenesAccepted=True,
        candidateUnderTestEndpointSceneAcceptanceScope='Only the 156 endpoints in the fresh 52-case human state matrix: 154 byte-exact to checked build, 2 source-bound original native blood with whole-scene drawing/continuous erasure. Not every move phase/victim/arena/effect/audio.',
        candidatePromotionGates=['Repeated natural bubble palette allocation/release across matches and both slots',
            'Broader affected move/morph/ordinary-combat/CPU/KO/overlap regressions after shared allocator/reset routing change (fresh native UI, 52 human states and both blade blood scenes accepted)',
            'Fresh full original Friendship audible PCM/tail/overlap checks, including actual randomized Sonya variants'],
        preservedNativeBladeDiagnosticFailures=failed,
        preservedNativeBladeParserFailure='v2801 retained: four runner invocations exited 1 before any capture due to JavaScript replacement dollar-quote expansion; v2804 generated safely and parser validated, four actual captures terminal exit zero',
        originalNativeSingleSpriteProjectionBypassesMultipartFrameOffsets=True,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,oldBuildFoldersDeletedThisTurn=0,
        nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
        nextAction='Keep v2753 isolated. Next establish repeated natural bubble palette allocation/ownership/release/reuse across matches in both slots; then fresh affected morph/CPU/KO/overlap and full original Friendship audible PCM/tail/overlap with matched samples-off controls for actual randomized Sonya variants. Only after all promotion gates pass change the launcher. Source-perfect variable native blood is now proven for both changed blade recovery scenes; do not force the previous RNG sequence. Entire original arena/victim/mirror/stage effects/move-phase/grounding/floor shadows/other finishers/secrets/cinematics/full natural Kintaro/Shao match clears/own endings/attract/final integration/dependency-aware cleanup/refreshed release requirements remain.',
        inputHashes=inherited)
    return prior

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable full original-goal successor')
    report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=report['goalStatus'],publicCandidate=report['currentCandidate'],
        candidateUnderTest=report['candidateUnderTest'],originalNativeBloodBothSlotsAccepted=True,
        currentCompleteBladeScanouts=129,controlCompleteBladeScanouts=129,
        unresolvedBladeScenes=0,fullPortAcceptance=False,finishedRelease=False,
        revalidatedFreshRelevantFilePins=report['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
