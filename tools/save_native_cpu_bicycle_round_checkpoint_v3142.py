"""Full natural-port checkpoint after ordinary-human holds and round boundary.

Four true cold CPU games, one original61-field Bicycle miss beginning across
mode7-to-live transition, exact91native scenes/shadows/erase and71fault tests.
No Bicycle contact acceptance, no broad CPU/all-arena/ending/port completion.
"""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT
PREVIOUS=ROOT/'audit_v3094_native_cpu_bicycle_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3143_native_cpu_bicycle_round_full_scope_checkpoint'
def save():
    need=assembly.need;prior=json.loads(PREVIOUS.read_text());inherited=dict(prior['inputHashes']);fresh={}
    need(prior['goalStatus']=='active'and len(prior['remaining'])==5 and len(prior['candidatePromotionGates'])==1 and
      prior['candidateUnderTest']==assembly.NAME and prior['candidateUnderTestNativeBicycleMissAccepted']and
      not prior['candidateUnderTestNativeBicycleHitOrBlockedAccepted']and not prior['fullPortAcceptance']and not prior['finishedRelease']and
      len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'],
      'Entire original natural game requirements and all outstanding promotion/ending/contact gates retained')
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute()else ROOT/path).resolve());actual=assembly.sha(key)if wanted is None else wanted
        need(key not in inherited or inherited[key]==actual,'Never overwrite historical source/evidence '+key)
        need(key not in fresh or fresh[key]==actual,'Consistent fresh actual source/evidence '+key);fresh[key]=actual
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['passed']and not value['fullPortAcceptance'],'Actual bounded independently checked evidence '+leaf)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    hold,hold_path=proof('audit_v3112_native_cpu_human_hold_inventory_checked')
    close,close_path=proof('audit_v3126_native_cpu_human_close_inventory_checked')
    boundary,boundary_path=proof('audit_v3129_native_cpu_bicycle_round_boundary_checked')
    render,render_path=proof('audit_v3131_native_cpu_bicycle_round_render_new_kano_checked')
    erase,erase_path=proof('audit_v3133_native_cpu_bicycle_round_erase_checked')
    initial_units,initial_unit_path=proof('audit_v3135_native_cpu_bicycle_round_boundary_units')
    render_units,render_unit_path=proof('audit_v3137_native_cpu_bicycle_round_render_units')
    erase_units,erase_unit_path=proof('audit_v3139_native_cpu_bicycle_round_erase_units')
    phase_units,phase_unit_path=proof('audit_v3141_native_cpu_bicycle_round_phase_units')
    total_fields=0;native_cases={}
    for value in(hold,close):
        need(value['actualPhysicalFixtures']==2 and value['wholeNativeStateHealthSourceAndChoicesAccepted']and
          value['originalNativeObserverBodiesUnchanged']and value['onlyPhysicalHumanButtonsChanged']and
          not value['CPUIdentityOrMoveOrRNGPrescribed'],'Only actual normal human controller responses changed; native CPU unrestricted')
        for key,case in value['cases'].items():
            need(case['health']['allModePhysicalFields']==3602 and case['stateLedger']['allRawLiveStateChangesSourceBound']and
              case['cold']['human_id']==17 and case['cold']['cpu_id']==18 and case['selection']['checks']==50 and case['selection']['errors']==0,
              'Each complete true17/18cold selection and whole3602-field source-bound health/state history')
            total_fields+=case['health']['allModePhysicalFields'];native_cases[key]=case
    need(total_fields==14408 and native_cases['guard_hold']['branches']==[]and native_cases['approach_hold']['branches']==[]and
      len(native_cases['jump_hold']['branches'])==1 and native_cases['jump_hold']['branches'][0]['move']=='square'and
      not native_cases['jump_hold']['branches'][0]['nativeContact']and
      len(native_cases['neutral_hold']['branches'])==1 and native_cases['neutral_hold']['branches'][0]['move']=='bicycle'and
      not native_cases['neutral_hold']['branches'][0]['nativeContact'],'All genuine reached and unreached outcomes retained, no contact invented')
    bike=boundary['cases']['new_kano']['phase']
    need(boundary['originalNativeMissPhysicsAndIndividualRecoveryRetained']and boundary['actualRoundRevealToLiveBoundaryAccepted']and
      boundary['actualInitialEntrySourceWriteChainsAccepted']and not boundary['missingInteriorFieldsPermitted']and
      not boundary['candidateBicycleHitOrBlockedAccepted']and bike['start']==2663 and bike['ready']==2724 and bike['fields']==61 and
      bike['fractionalLandingY']==40960 and boundary['cases']['new_kano']['actualNativeChoice']['firstRandomResult']==134,
      'Real source-directed first-chance Bicycle, mode7boundary before actual mode2 entry, all61original phases and individual cleanup')
    need(render['sampledFrames']==render['exactReplayedFrames']==91 and render['exactScreenPixels']==9245600 and
      render['nativeShadowCopies']==8597 and render['allOriginalBicyclePosesVisible']and not render['allMoveGroundShadowAudioAccepted'],
      'All9original donor Bicycle poses, owned palette/FIFO/queued projection/black floor shadows and91exactscenes, no all-arena/audio waiver')
    need(erase['continuousExactPreBuffers']==erase['continuousExactFlips']==91 and erase['nativeShiftTransfers']==11557 and
      erase['originalContinuousReplayContractUnchanged']and erase['oneInitialBaseOnlyPerActualFixture']and not erase['laterBuffersUsedAsAnchors'],
      'Exact chronological native CPU/DMA/shift/FILL loads/clears and every buffer from only one initial base')
    need(initial_units['actualBoundaryCounterexamplesRejected']==11 and initial_units['sameMockedPathPositiveControlAccepted']and
      render_units['actualCounterexamplesRejected']==16 and render_units['sameMockedPathPositiveControlAccepted']and
      render_units['unrelatedMissingEventExceptionsNeverAccepted']and erase_units['actualOriginalEraseCounterexamplesRejected']==18 and
      phase_units['actualCounterexamplesRejected']==26,'All71actual boundary/startup/physics/RNG/render/shadow/erase corruptions rejected')
    for leaf,script,count in [('audit_v3109_native_cpu_human_hold_dispatch','run_native_cpu_human_hold_dispatch_v3108.py',2),
                            ('audit_v3122_native_cpu_human_close_dispatch','run_native_cpu_human_close_dispatch_v3121.py',2)]:
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['allRunnersTerminal']and value['allRunnerExitsZero']and len(value['cases'])==count,'Authoritative capture processes terminal zero')
        pin(ROOT/'tools'/script,value['sourceSHA256']);pin(ROOT/leaf/script,value['sourceSHA256'])
    # Preserve the failed host dofile-redirection attempt. A zero native process
    # exit never overrides actual fatal-autoboot output or missing guest capture.
    failure_path=ROOT/'audit_v3099_native_cpu_human_hold_dispatch/report.json'
    failure=json.loads(failure_path.read_text());pin(failure_path);failed_boots=[]
    for item in failure['cases']:
        folder=ROOT/item['case'];log=(folder/'run.log').read_text(encoding='utf-8-sig')
        need('Fatal error: Error running autoboot script'in log and 'Only real human continuation buttons'in log and
          not(folder/'guest_maincpu.bin').exists(),'Actual failed host-script startup retained, never counted as a successful native match')
        for file in folder.rglob('*'):
            if file.is_file():pin(file)
        failed_boots.append(dict(case=item['case'],nativeExitReported=item['runnerExit'],accepted=False,
          cause='Host dofile override did not propagate into MAME chunk environments; original1997 correctly rejected unsupported policy. Direct immutable observer load-links fixed the harness; no game changed.'))
    need(len(failed_boots)==2,'Both actual startup-only failures preserved')
    for file in('tools/run_native_cpu_human_hold_dispatch_v3098.py','tools/run_native_cpu_human_hold_v3097.ps1','mk2ks_native_cpu_human_hold_wrapper_v3096.lua'):
        pin(ROOT/file)
    pin(PREVIOUS);pin(__file__)
    for file,wanted in {
      'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
      'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():pin(ROOT/file,wanted)
    print('Revalidating current genuine human-input/round-boundary files:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            need(actual==wanted,'Immutable fresh true native evidence '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=prior['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: four real cold17/18CPU games with normal standing-guard, neutral, jump-hold and walking-forward human buttons. All14408all-modefields and entire native state/HP/AIchoice source checked; genuine no-contact outcomes retained. Neutral run naturally chose first-chance Bicycle134/250 at the next-round reveal-to-live boundary, not a fabricated previous FIELD. Both real entry snapshots and all initial source write chains plus original no-op pre-entry AI clear proved; entire61original startup/seek/ceiling/fall/fractional40960landing/individual recovery retained. All9donor poses/native palettes/queued projection/8597black floor-shadow copies/91scenes exact; original continuous erase91prebuffers/91flips/11557shifttransfers from onebase. All71boundary/physics/choice/render/shadow/erase faults rejected with meaningful positive controls. Failed host dofile redirection boot preserved, direct observer bodies unchanged except explicit load-links. No game/exe/CMD/ZIP edits, no Bicycle contact or full-port completion.',
      currentNativeCPUHumanHoldReport=hold_path,currentNativeCPUHumanCloseReport=close_path,
      currentNativeCPUHumanButtonCases=native_cases,currentNativeCPUHumanButtonAllModeFields=14408,
      candidateUnderTestNativeBicycleRoundBoundaryPhaseReport=boundary_path,
      candidateUnderTestNativeBicycleRoundBoundaryPhase=bike,
      candidateUnderTestNativeBicycleRoundBoundaryInitialSourceChainsAccepted=True,
      candidateUnderTestNativeBicycleRoundBoundaryRenderReport=render_path,
      candidateUnderTestNativeBicycleRoundBoundaryEraseReport=erase_path,
      candidateUnderTestNativeBicycleRoundBoundaryInitialUnits=initial_unit_path,
      candidateUnderTestNativeBicycleRoundBoundaryPhaseUnits=phase_unit_path,
      candidateUnderTestNativeBicycleRoundBoundaryRenderUnits=render_unit_path,
      candidateUnderTestNativeBicycleRoundBoundaryEraseUnits=erase_unit_path,
      candidateUnderTestNativeBicycleRoundBoundaryMissAccepted=True,
      candidateUnderTestNativeBicycleRoundBoundaryExactScenes=91,
      candidateUnderTestNativeBicycleRoundBoundaryNativeShadowCopies=8597,
      candidateUnderTestNativeBicycleRoundBoundaryActualCorruptionsRejected=71,
      candidateUnderTestNativeBicycleHitOrBlockedAccepted=False,candidateUnderTestNativeBicycleAccepted=False,
      candidateUnderTestPhysicalP2CPUCaptureCount=prior['candidateUnderTestPhysicalP2CPUCaptureCount']+4,
      nativeHumanHoldStartupHarnessFailuresPreserved=failed_boots,
      candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,candidateUnderTestAllArenaMoveGroundShadowAcceptance=False,
      inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      oldBuildFoldersDeletedThisTurn=0,nativeDifficultyHealthAIPositionStageRNGModified=False,
      actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      nextAction='Keep2753isolated. Actual neutral-holder Bicycle now fully checked across the natural next-round mode7-to-mode2 boundary, exact61native phases,9donor poses/91scenes/black floor shadows/continuous erase and71corruptions. Normal guard/jump/approach controllers and full14408fields are proved, but no new Bicycle contact: neutral began192pixels apart and missed; jumping produced Square miss; guard/approach no mobility. Next seek actual normal-input Bicycle contact/blocked/interrupt/KO and assess source/native CPU distance choice if evidence warrants an implementation change, not repeated false contact credit or forced RNG. Original five full-port groups, all victims/arenas/audio/finishers/morphs/secrets/cinematics/natural boss campaigns/own endings/attract/UI/regression/cleanup/ZIP remain required.',
      inputHashes=inherited)
    return prior
if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable full original-scope round-boundary checkpoint')
    value=save();OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(value,indent=2)+'\n')
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    assembly.need(result.returncode==0,'Lossless checkpoint compression')
    print(json.dumps(dict(goalStatus='active',actualNormalHumanCases=4,allModePhysicalFields=14408,
      candidateBicycleRoundBoundaryMissAccepted=True,candidateBicycleHitOrBlockedAccepted=False,
      actualBoundaryPhysicsRenderEraseCorruptions=71,originalRemainingGroups=len(value['remaining']),
      remainingCandidateGates=len(value['candidatePromotionGates']),actualFullShaoMatchClears=0,
      fullPortAcceptance=False,finishedRelease=False,revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
