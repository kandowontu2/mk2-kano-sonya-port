"""Full original natural-port checkpoint, bounded fresh human morph evidence.

Preserves all five original groups, CPU contact, natural boss/ending and release
gates. No gameplay bytes or public build were changed. Not broad morph credit.
"""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT
PREVIOUS=ROOT/'audit_v3143_native_cpu_bicycle_round_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3164_current_morph_full_scope_checkpoint'
need=assembly.need

def save():
    need(not OUT.exists(),'Never overwrite full-scope checkpoint')
    prior=json.loads(PREVIOUS.read_text())
    need(prior['goalStatus']=='active'and len(prior['remaining'])==5 and len(prior['candidatePromotionGates'])==1 and
      prior['candidateUnderTest']==assembly.NAME and not prior['fullPortAcceptance']and not prior['finishedRelease']and
      len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and
      not prior['actualEndingsAccepted']and not prior['candidateUnderTestNativeBicycleHitOrBlockedAccepted'],
      'Full original game scope, contact/CPU/natural boss/endings and promotion/release gates preserved')
    inherited=dict(prior['inputHashes']);fresh={}
    def pin(path,wanted=None):
        path=Path(path);path=(path if path.is_absolute()else ROOT/path).resolve()
        actual=assembly.sha(path)if wanted is None else wanted
        key=str(path)
        need(key not in inherited or inherited[key]==actual,'Never rewrite historical evidence '+key)
        need(key not in fresh or fresh[key]==actual,'Consistent immutable current evidence')
        fresh[key]=actual
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['passed']and not value['fullPortAcceptance'],'Actual bounded independent report')
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    rendering,render_path=proof('audit_v3151_current_morph_suite_checked')
    units,units_path=proof('audit_v3157_current_morph_actual_counterexamples')
    commands,commands_path=proof('audit_v3162_current_morph_commands_checked')
    dispatch,dispatch_path=proof('audit_v3159_current_morph_command_dispatch')
    need(rendering['physicalCases']==4 and rendering['allGameplayFields']==4004 and
      rendering['actualTransitionFields']==96 and rendering['actualComponentFields']==320 and
      rendering['exactOriginalOpaqueComponentPixels']==498624 and
      rendering['originalHumanAndRenderCriteriaUnchanged']and
      rendering['ownNativeTimedRestorationAndPostRestoreControlsAccepted']and
      not rendering['allFloorShadowsAndContinuousEraseAccepted']and not rendering['allMorphBranchesAccepted'],
      'All four real native transformations/restores, exact320component draws and entire4004-field lifecycle, no shadow/all-morph waiver')
    need(commands['physicalCases']==32 and commands['allGameplayFields']==32032 and
      commands['SonyaChordVariantCases']==6 and commands['invalidAndAirborneRejectionCases']==20 and
      commands['originalStockMorphFallbackCases']==6 and commands['originalWholeHumanNativeCriteriaUnchanged']and
      commands['allActualInitializedGuestsSourceBound']and not commands['allCPUMorphsOrArenasAccepted']and
      not commands['allPixelsFloorShadowsAndAudioAccepted']and not commands['gameplaySourceOrPlayableBytesChanged'],
      'All32specified native chord/invalid/airborne/stock cases,32032complete fields and no forced guest state')
    need(dispatch['captures']==32 and not dispatch['fullPortAcceptance']and
      units['physicalCases']==4 and units['actualCounterexamplesRejected']==56 and
      units['sameMockedPathPixelPositiveControlsAccepted']and units['unrelatedExceptionsNeverAccepted']and
      units['originalNativeAndRasterCriteriaUnchanged'],'32native process exits and56 meaningful actual source/raster corruptions')
    failure_notes=[]
    for file,cause in(
      ('tools/test_current_morph_suite_v3152.py','First descriptor/pivot corruption targeted a pre-transition component outside accepted inventory; qualified assertion failed, no false rejection credit.'),
      ('tools/test_current_morph_suite_v3154.py','Mechanical successor did not retarget descriptor/pivot expressions; qualified assertion failed again. Current3156 explicitly targets an actual accepted draw frame.')):
        pin(ROOT/file);failure_notes.append(dict(source=str(ROOT/file),sourceSHA256=assembly.sha(ROOT/file),
          accepted=False,cause=cause))
    pin(ROOT/'tools/run_human_shang_probe_v3144.ps1');pin(ROOT/'mk2ks_morph_guest_probe_v3145.lua')
    pin(ROOT/'tools/test_current_morph_suite_v3156.py');pin(PREVIOUS);pin(__file__)
    for file,wanted in{
      'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
      'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():pin(ROOT/file,wanted)
    print('Rehashing fresh native morph source/evidence pins: '+str(len(fresh)),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            need(actual==wanted,'Every fresh current native source/evidence hash '+file)
    inherited.update(fresh)
    prior.update(
      previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: user-requested status inspection/report only; no running process or implemented change.',
      previousGoalTurnNoProgressRevalidated=True,
      thisGoalTurnClassification='progress:36fresh normal-input current2753Shang games. All4004render-suite and32032command-suite fields/source guests checked with original full criteria unchanged. Four nativeKano/SonyaP1/P2morph/512timer/restore/bodyfloor/projectile/control cycles;24transition holds and16earlybodyhandoffs percase;320original component draws/498624opaque pixels exact at actual2-fieldbufferdelay. Six Sonya chord variants,20invalid/airborne rejections,six original stock morph fallbacks accepted.56specific native/raster corruptions rejected; actual same mocked pixelpath positive controls. Two test-harness wrong-frame derivations failed qualification and preserved, never credited. No game/exe/CMD/ZIP changes; all broad morphology/shadow/CPU/arena/audio/finisher/boss/ending gates remain.',
      currentNativeHumanMorphRenderingReport=render_path,
      currentNativeHumanMorphCommandReport=commands_path,
      currentNativeHumanMorphCounterexamplesReport=units_path,
      currentNativeHumanMorphDispatchReport=dispatch_path,
      currentNativeHumanMorphCaptureCases=36,
      currentNativeHumanMorphAllGameplayFields=36036,
      currentNativeHumanMorphTransitionFields=96,
      currentNativeHumanMorphOriginalComponentDraws=320,
      currentNativeHumanMorphExactOpaqueComponentPixels=498624,
      currentNativeHumanMorphActualCorruptionsRejected=56,
      currentNativeHumanMorphBothSlotsPrimaryGrammarStateRestoreControlsAccepted=True,
      currentNativeHumanMorphFourPrimaryTransitionsAndEarlyBodyPaletteHandoffsAccepted=True,
      currentNativeHumanMorphFloorShadowsContinuousEraseAllArenasAccepted=False,
      currentNativeHumanMorphCPUChoiceInterruptKOVictimAllBranchesAccepted=False,
      currentNativeHumanMorphCases=rendering['cases'],
      currentNativeHumanMorphCommandCases=commands['cases'],
      currentNativeHumanMorphVerifierDerivationFailuresPreserved=failure_notes,
      candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
      inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      oldBuildFoldersDeletedThisTurn=0,nativeDifficultyHealthAIPositionStageRNGModified=False,
      actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      nextAction='Keep2753isolated. Current primary humanKano/SonyaShangmorph input grammar,realIDs,normal eligibility,512native timer,restoration,postrestore controls,ownprojectiles,and four exact native art/palette/bodyhandoffs now verified with original criteria. Next close actual native floor-shadow ownership/geometry and continuous erase through forward/reverse morphs; then natural CPU morphs/interrupts/KO/victims and remaining finishers/stage branches. Bicycle hit/blocked/KO, all-arena/audio/CPU/repetition cases, actual natural full boss clears/own endings/attract, finalUI/cleanup/refreshedZIP remain required. OriginalMK3far Bicycle also naturally misses;192pixel candidate miss alone does not justify altering collisions/CPUdistance.',
      inputHashes=inherited)
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(prior,indent=2)+'\n')
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0,'Lossless checkpoint compression')
    print(json.dumps(dict(goalStatus='active',freshHumanMorphCases=36,allGameplayFields=36036,
      exactOriginalComponentDraws=320,meaningfulCorruptionsRejected=56,
      originalRemainingGroups=len(prior['remaining']),remainingPromotionGates=len(prior['candidatePromotionGates']),
      fullPortAcceptance=False,finishedRelease=False,gameplayBytesChanged=False,
      revalidatedFreshRelevantFilePins=len(fresh)),indent=2),flush=True)

if __name__=='__main__':save()
