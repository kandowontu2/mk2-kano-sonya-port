"""Keep the full official-character goal; new isolated native shadow repair.

Original five groups, natural bosses/endings, old candidate CPU contact limits
and promotion gates remain. Historical2753 checks are not transplanted to3172.
"""
import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_human_shang_v3174 as human
ROOT=assembly.ROOT;need=assembly.need
PREVIOUS=ROOT/'audit_v3164_current_morph_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3208_corrected_morph_shadow_full_scope_checkpoint'

def save():
    need(not OUT.exists(),'Never overwrite full-scope evidence')
    prior=json.loads(PREVIOUS.read_text())
    need(prior['goalStatus']=='active'and len(prior['remaining'])==5 and
      len(prior['candidatePromotionGates'])==1 and prior['candidateUnderTest']==assembly.NAME and
      len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and
      not prior['candidateUnderTestNativeBicycleHitOrBlockedAccepted']and
      not prior['actualEndingsAccepted']and not prior['fullPortAcceptance']and not prior['finishedRelease'],
      'All original requirements and unproven contact/natural boss/ending/release gates retained')
    inherited=dict(prior['inputHashes']);fresh={}
    def pin(path,wanted=None):
        path=Path(path);path=(path if path.is_absolute()else ROOT/path).resolve()
        value=assembly.sha(path)if wanted is None else wanted;key=str(path)
        need(key not in inherited or inherited[key]==value,'Never rewrite historical input '+key)
        need(key not in fresh or fresh[key]==value,'Consistent current actual input '+key)
        fresh[key]=value
    def proof(leaf,full_key='fullPortAcceptance'):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text())
        need(value['passed']and not value[full_key],'Actual bounded current result '+leaf)
        pin(path)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    floor,floor_path=proof('audit_v3186_native_morph_floor_projection_checked')
    commands,commands_path=proof('audit_v3192_current_morph_commands_checked')
    geometry,geometry_path=proof('audit_v3200_native_morph_shadow_projection_counterexamples')
    art_units,art_units_path=proof('audit_v3204_corrected_morph_actual_counterexamples')
    ui,ui_path=proof('audit_v3198_native_morph_shadow_ui_checked','fullPortAccepted')
    ui_units,ui_units_path=proof('audit_v3206_corrected_native_ui_units','fullPortAccepted')
    dispatch,dispatch_path=proof('audit_v3189_current_morph_command_dispatch')
    ui_dispatch,ui_dispatch_path=proof('audit_v3195_native_morph_shadow_ui_dispatch')
    bug,bug_path=proof('audit_v3178_native_morph_shadow_bug_reproduced')
    asset=json.loads((ROOT/'audit_v3169_native_morph_shadow_payload/report.json').read_text())
    restore=json.loads((ROOT/human.CANDIDATE/'restoration.json').read_text())
    need(floor['candidate']==commands['candidate']==ui['candidate']==human.CANDIDATE and
      floor['physicalCases']==4 and floor['exactNativeTransitionAndRecoveryScenes']==296 and
      floor['exactScreenPixels']==30073600 and floor['actualNativeShadowCopies']==293778 and
      floor['actualOwnTransitionShadowCopies']==6080 and floor['fullNativeTimerChronologicalEraseAccepted']and
      floor['actualDirectNativeProjectionRegistersAccepted']and not floor['laterBuffersUsedAsAnchors']and
      not floor['allArenasVictimsCPUMorphsInterruptsKOAudioAccepted']and not floor['nativeGuestProgramChanged'],
      'All four actual original native morphology/direct projection/entire chronological erasure fixtures, no broad waiver')
    need(all(c['sampledFrames']==74 and c['native']['gameplay_fields']==1001 and
      c['art']['native_component_fields']==80 and c['continuousErase']['continuousExactFlips']==74
      for c in floor['cases'].values()),'Full original art/control/erase coverage in every current primary fixture')
    need(commands['physicalCases']==32 and commands['allGameplayFields']==32032 and
      (commands['SonyaChordVariantCases'],commands['invalidAndAirborneRejectionCases'],commands['originalStockMorphFallbackCases'])==(6,20,6)and
      commands['originalWholeHumanNativeCriteriaUnchanged']and dispatch['captures']==32 and
      len(ui_dispatch['cases'])==4 and ui['currentBothSlotSelectionLadderFirstMatchAccepted']and
      ui['observedUITablesExactlyIndependentGuest']and not ui['fullLaddersAccepted'],
      'Fresh real commands and full both-side native selection/ladder/first-match invariant, no natural campaign claim')
    need(geometry['actualCounterexamplesRejected']==48 and geometry['verbatimOriginalProjectionCriteria']and
      geometry['sameMockedRowPathPositiveControlsAccepted']and geometry['unrelatedExceptionsNeverAccepted']and
      art_units['actualCounterexamplesRejected']==56 and art_units['sameMockedPathPixelPositiveControlsAccepted']and
      art_units['unrelatedExceptionsNeverAccepted']and ui_units['methods']==46,
      'Actual reached geometry/row/art and UI counterexamples with same-path positive controls')
    need(bug['reproducedFailure']and bug['actualDefectiveTransitionComponents']==48 and
      bug['actualBackwardRowSteps']==720 and not bug['beforeFixRuntimeMorphShadowsAccepted']and
      asset['assetOnly']and len(asset['descriptors'])==12 and asset['payloadSHA256']==human.PAYLOAD and
      restore['passed']and len(restore['restored_actual_preexisting_files'])==4 and not restore['public_build_promoted'],
      'Concrete original stream defect, narrow12descriptor correction and exact actual preexisting source/EXE restoration')
    for file,wanted in restore['restored_actual_preexisting_files'].items():
        pin(file,wanted);pin(restore['backup_files'][file],wanted)
    for file in('audit_v3169_native_morph_shadow_payload/report.json',
      'audit_v3181_native_morph_floor_checked/report.json','tools/verify_native_morph_floor_v3180.py',
      'tools/test_corrected_morph_actual_v3201.py'):
        pin(file)
    failure=json.loads((ROOT/'audit_v3181_native_morph_floor_checked/report.json').read_text())
    need(not failure['passed']and 'quarter-height floor projection' in failure['error'],
      'Failed +5 body-sole assumption retained; real direct native B7=2 evidence replaces it, not a geometry waiver')
    failure_notes=[
      dict(source=str(ROOT/'tools/verify_native_morph_floor_v3180.py'),accepted=False,
        result=str(ROOT/'audit_v3181_native_morph_floor_checked/report.json'),
        cause='Assumed body sole +5 for native floor shadow. Actual read-only direct helper registers prove separate B7=2.3185 retains full original projection formula using actual captured registers.'),
      dict(source=str(ROOT/'tools/test_corrected_morph_actual_v3201.py'),accepted=False,
        cause="Python module alias floor shadowed by local test floor string; UnboundLocalError before source checks/data. Immutable3203 only renames module alias floorproof; actual56counterexamples pass.")
    ]
    pin(PREVIOUS);pin(__file__)
    for file,wanted in{
      'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
      'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'
    }.items():pin(file,wanted)
    print('Rehashing fresh relevant native correction/UI/command evidence: '+str(len(fresh)),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            need(actual==wanted,'Every actual current source/evidence pin '+file)
    historical={k:v for k,v in prior.items()if k.startswith('candidateUnderTest')}
    for key in historical:
        if isinstance(prior[key],bool):prior[key]=False
    inherited.update(fresh)
    prior.update(
      previousCheckpoint=str(PREVIOUS),
      previousGoalTurnClassification='verified wait: user status turn polled live8698 full morph projection/erase verifier, three cases complete and fourth still live. No duplicate capture restarted.',
      thisGoalTurnClassification='progress: completed native morph floor correction verification, all296exact scenes/293778shadow rowcopies/9136direct projected components/fulltimer continuous erase. Narrow12assetdescriptor correction already built3172; whole actual guest remains65CE.32fresh normal-input command games32032fields and four fresh native UI/ladder/first-match games pass on3172.48qualified directgeometry/row corruptions,56actual art/control/raster corruptions and46UItest methods pass; failed +5shadow-offset assumption and Pythonalias harness failure preserved. Full original five groups and CPUcontact/arena/audio/finishers/naturalboss/ending/release gates remain.',
      candidateUnderTest=human.CANDIDATE,
      historicalCandidateUnderTest2753Evidence=historical,
      candidateUnderTestPreviousEvidenceAutomaticallyTransferred=False,
      candidateUnderTestNativeHumanMorphDirectShadowAccepted=True,
      candidateUnderTestNativeHumanMorphChronologicalEraseAccepted=True,
      candidateUnderTestBothSlotNativeUIFirstMatchAccepted=True,
      candidateUnderTestNativeHumanMorphCommandsAccepted=True,
      candidateUnderTestNativeBicycleHitOrBlockedAccepted=False,
      candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
      candidatePromotionGates=[prior['candidatePromotionGates'][0]+' This inherited acceptance applies to2753 only. New3172 twelve-morph-descriptor source/format repair must retain all affected ordinary/move/CPU/KO/overlap and repeated/finisher regressions; four primary human morphology/shadow/erase,32command cases and both-slot UI were freshly checked on3172, not a broad promotion waiver.'],
      currentNativeMorphShadowDefectReport=bug_path,
      currentNativeMorphShadowDescriptorAssetReport=str(ROOT/'audit_v3169_native_morph_shadow_payload/report.json'),
      currentNativeMorphShadowCorrectionExecutableSHA256=human.EXE,
      currentNativeMorphShadowCorrectionPayloadSHA256=human.PAYLOAD,
      currentNativeMorphShadowCorrectionGuestSHA256='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7',
      currentNativeMorphShadowDirectProjectionReport=floor_path,
      currentNativeMorphShadowProjectionCounterexamplesReport=geometry_path,
      currentNativeHumanMorphRenderingReport=floor_path,
      currentNativeHumanMorphCommandReport=commands_path,
      currentNativeHumanMorphCounterexamplesReport=art_units_path,
      currentNativeHumanMorphDispatchReport=dispatch_path,
      currentNativeMorphShadowUIReport=ui_path,
      currentNativeMorphShadowUICounterexamplesReport=ui_units_path,
      currentNativeMorphShadowUIDispatchReport=ui_dispatch_path,
      currentNativeMorphShadowFreshCaptureCases=40,
      currentNativeHumanMorphCaptureCases=36,
      currentNativeHumanMorphAllGameplayFields=36036,
      currentNativeHumanMorphTransitionFields=96,
      currentNativeHumanMorphOriginalComponentDraws=320,
      currentNativeHumanMorphExactOpaqueComponentPixels=sum(v['visible']for c in floor['cases'].values()for v in c['art']['visual']),
      currentNativeHumanMorphActualCorruptionsRejected=56,
      currentNativeHumanMorphFloorShadowsContinuousEraseFourPrimaryCasesAccepted=True,
      currentNativeHumanMorphFloorShadowsContinuousEraseAllArenasAccepted=False,
      currentNativeHumanMorphCPUChoiceInterruptKOVictimAllBranchesAccepted=False,
      currentNativeHumanMorphCases=floor['cases'],currentNativeHumanMorphCommandCases=commands['cases'],
      currentNativeMorphShadowVerifierDerivationFailuresPreserved=failure_notes,
      currentNativeMorphShadowCorrectionActualPreexistingFilesRestored=True,
      inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
      gameSourceAndPlayableBytesChangedThisTurn=True,nativeGuestProgramChangedThisTurn=False,
      publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      oldBuildFoldersDeletedThisTurn=0,nativeDifficultyHealthAIPositionStageRNGModified=False,
      actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      nextAction='Keep3172isolated. Fresh original native morph body/control/art/palette, actual direct native floor projection/compressed rows and full chronological clears, command rejections/stockfallthroughs, both-slot selection/ladder/first-match UI pass. Next pursue unassisted natural CPU transformations/interrupt/KO/repeat/victim coverage and broader affected ordinary/special/finisher overlap regression. Old stage14/health-assisted CPU morph fixtures are diagnostic only, cannot count as natural3172CPU acceptance. Bicycle hit/blocked/KO, all arenas/victims/audio/CPU/repetition, real natural full Kintaro/Shao clears/own endings/attract, final combined regression/cleanup/refreshedZIP remain required; old2753acceptance remains explicitly historical. Do not run health/stage/RNG/identity assistance or promote merely because bounded current cases pass.',
      inputHashes=inherited)
    need(len(prior['remaining'])==5 and prior['currentRealShaoKahnMatchClears']==0,
      'Full objective unchanged after current result binding')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(prior,indent=2)+'\n')
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0,'Lossless full checkpoint compression')
    print(json.dumps(dict(goalStatus='active',candidateUnderTest=human.CANDIDATE,
      freshCaptureCases=40,exactNativeScenes=296,actualNativeShadowCopies=293778,
      geometryRowCorruptionsRejected=48,artControlPixelCorruptionsRejected=56,UITestMethods=46,
      originalRemainingGroups=5,fullPortAcceptance=False,finishedRelease=False,
      publicLauncherAndZIPChanged=False,revalidatedFreshRelevantFilePins=len(fresh)),indent=2),flush=True)

if __name__=='__main__':save()

