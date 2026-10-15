"""Full-scope checkpoint: candidate Bicycle miss and repaired rendering tests.

The original five full-port groups and isolated candidate promotion gate stay
open. Repaired tests require identical-path positive controls and intentional
failure conditions, not unrelated missing-empty-event KeyErrors. No gameplay,
launcher, ZIP or saved historical evidence is modified by this checkpoint.
"""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT
PREVIOUS=ROOT/'audit_v3060_native_cpu_mobility_hit_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3094_native_cpu_bicycle_full_scope_checkpoint'
def save():
    need=assembly.need;prior=json.loads(PREVIOUS.read_text());inherited=dict(prior['inputHashes']);fresh={}
    need(prior['goalStatus']=='active'and len(prior['remaining'])==5 and len(prior['candidatePromotionGates'])==1 and
      prior['candidateUnderTest']==assembly.NAME and not prior['fullPortAcceptance']and not prior['finishedRelease']and
      len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'],
      'Entire original natural game scope, no broad acceptance or premature release')
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute()else ROOT/path).resolve())
        value=assembly.sha(key)if wanted is None else wanted
        need(key not in inherited or inherited[key]==value,'Never replace immutable historical evidence '+key)
        need(key not in fresh or fresh[key]==value,'Consistent fresh actual source '+key);fresh[key]=value
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['passed']and not value['fullPortAcceptance'],'Accepted bounded real-input proof '+leaf)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    phase,phase_path=proof('audit_v3066_native_cpu_bicycle_candidate_checked')
    phases_negative,phases_negative_path=proof('audit_v3070_native_cpu_bicycle_candidate_units')
    render,render_path=proof('audit_v3068_native_cpu_bicycle_render_new_kano_checked')
    erase,erase_path=proof('audit_v3072_native_cpu_bicycle_erase_checked')
    erase_negative,erase_negative_path=proof('audit_v3076_native_cpu_bicycle_erase_units')
    render_negative,render_negative_path=proof('audit_v3078_native_cpu_bicycle_render_units')
    square_hit_negative,square_hit_negative_path=proof('audit_v3082_native_cpu_square_render_units')
    square_miss_negative,square_miss_negative_path=proof('audit_v3084_native_cpu_square_render_units')
    ring_negative,ring_negative_path=proof('audit_v3086_native_cpu_ring_render_units')
    timing,timing_path=proof('audit_v3092_native_cpu_bicycle_contact_inventory_checked')
    bike=phase['cases']['new_kano']['phase'];bridge=phase['cases']['new_kano']['cleanSpecialBridge']
    need(phase['actualCandidateBicycleMissAccepted']and phase['actualCleanSquareToBicycleBridgeAccepted']and
      phase['entireOriginalBicyclePhaseChecksRetained']and phase['actualCandidateFirstChanceResult']==126 and
      not phase['candidateBicycleHitOrBlockedAccepted']and bike['fields']==61 and bike['fractionalLandingY']==40960 and
      bridge['previousSquare']==3224 and bridge['previousSquareRegain']==3278 and bridge['firstBicycle']==3279 and
      bridge['cleanBetweenSpecials']and bridge['independentInitialWritesAccepted']and phase['cases']['new_sonya']['noBicycleScenario'],
      'Original full Bicycle miss/landing/individual locks and real clean Square-to-Bicycle bridge, no invented mirror coverage')
    need(render['sampledFrames']==render['exactReplayedFrames']==91 and render['exactScreenPixels']==9245600 and
      render['nativeShadowCopies']==7117 and render['allOriginalBicyclePosesVisible']and not render['allMoveGroundShadowAudioAccepted'],
      'All9 actual original Bicycle poses, complete native palettes/FIFO/queued camera/black shadows/exact91scenes only')
    need(erase['continuousExactPreBuffers']==erase['continuousExactFlips']==91 and erase['nativeShiftTransfers']==11557 and
      erase['originalContinuousReplayContractUnchanged']and erase['oneInitialBaseOnlyPerActualFixture']and not erase['laterBuffersUsedAsAnchors'],
      'Every chronological native load/shift/FILL/CPU/DMA operation from one initial base, no later scene anchoring')
    need(phases_negative['actualCounterexamplesRejected']==38 and erase_negative['actualOriginalEraseCounterexamplesRejected']==18 and
      render_negative['actualCounterexamplesRejected']==16,'All72 genuine candidate miss/bridge/art/erase corruptions')
    for label,value,count in [('bike',render_negative,16),('square_hit',square_hit_negative,16),('square_miss',square_miss_negative,32),('ring',ring_negative,63)]:
        actual_count=value.get('actualCounterexamplesRejected',value.get('actualOriginalRenderCounterexamplesRejected'))
        need(actual_count==count and value['sameMockedPathPositiveControlAccepted']and value['unrelatedMissingEventExceptionsNeverAccepted'],
          'Actual unmodified same-mock path must pass and deliberate rendering faults must reject '+label)
        for test in value['counterexamples']:
            if test['errorType']=='KeyError':
                need(label=='ring'and test['name']in('physical_publication_missing_from_full_inventory','child_publication_missing_from_full_inventory')and
                  'inventory[key]'in test['rejectedCondition'],'Only deliberately removed inventory tuple, never unrelated empty-event KeyError')
            else:need(test['errorType']in('AssertionError','ValueError'),'No unrelated exception accepted as a rendering fault')
    # Previous v3073/v3050/v3018/v2987 copies discarded defaultdict semantics.
    # Preserve their bytes but explicitly withdraw their faulty negative-test credit.
    superseded=[]
    for old,new in [('audit_v3074_native_cpu_bicycle_render_units',render_negative_path),
                    ('audit_v3051_native_cpu_square_hit_render_units',square_hit_negative_path),
                    ('audit_v3019_native_cpu_square_render_units',square_miss_negative_path),
                    ('audit_v2988_native_cpu_ring_render_units',ring_negative_path)]:
        path=ROOT/old/'report.json';value=json.loads(path.read_text());pin(path)
        bad=[r for r in value['counterexamples']if r['errorType']=='KeyError']
        need(bad and all(r['error']in("'FLOOR_CHILD_SPAWN'","'FLOOR_POINTER_STORE'","'FLOOR_HELD'")for r in bad),'Actual old unrelated-key false rejection provenance')
        superseded.append(dict(report=str(path),supersededBy=new,withdrawnUnrelatedKeyRejections=len(bad),
          reason='Plain dict dropped defaultdict empty-event semantics; same-mock positive control absent. Fresh tests preserve parser semantics and qualify intended conditions.'))
    need(timing['actualPhysicalFixtures']==2 and timing['wholeNativeStateHealthSourceAndChoicesAccepted']and
      timing['actualBicycleEntries']==0 and timing['actualSquareEntries']==1 and timing['originalPhysicalDriverUnchanged']and
      not timing['guestStateAIHealthStageRNGChanged']and not timing['fullContactPhaseOrArtAudioOrPortAccepted'],
      'Two genuine confirmation-timing trials retained as no-Bicycle coverage gaps, not contact acceptance')
    for leaf,script,count in [('audit_v3062_native_cpu_mobility_guard_dispatch','run_native_cpu_mobility_guard_dispatch_v3061.py',2),
                            ('audit_v3088_native_cpu_bicycle_contact_dispatch','run_native_cpu_bicycle_contact_dispatch_v3087.py',2)]:
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['allRunnersTerminal']and value['allRunnerExitsZero']and len(value['cases'])==count,'Actual capture processes terminal zero')
        pin(ROOT/'tools'/script,value['sourceSHA256']);pin(ROOT/leaf/script,value['sourceSHA256'])
    pin(PREVIOUS);pin(__file__)
    for path,wanted in {
      'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
      'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():pin(ROOT/path,wanted)
    print('Revalidating current genuine Bicycle/repair/discovery files:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            need(actual==wanted,'Immutable fresh actual native evidence '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),
      previousGoalTurnClassification='no progress: status-only response; current results inspected, next available safe work resumed',
      thisGoalTurnClassification='progress: actual candidate Bicycle miss/clean Square-to-Bicycle bridge and all91scenes/native black shadows/continuous erase accepted; unrelated-key rendering negative-test flaw found, withdrawn and repaired with identical mocked-path positive controls and intended failure conditions for Bicycle, Square hit/miss and Ring; two additional real confirmation-timing games fully checked and kept as genuine no-Bicycle scenarios. No game or public artifact edits; all original full-port requirements remain open.',
      candidateUnderTestNativeBicycleMissAccepted=True,candidateUnderTestNativeBicycleHitOrBlockedAccepted=False,
      candidateUnderTestNativeBicycleAccepted=False,
      candidateUnderTestNativeBicyclePhaseReport=phase_path,candidateUnderTestNativeBicyclePhase=bike,
      candidateUnderTestNativeBicycleCleanSquareBridge=bridge,
      candidateUnderTestNativeBicycleRenderReport=render_path,candidateUnderTestNativeBicycleEraseReport=erase_path,
      candidateUnderTestNativeBicyclePhaseUnits=phases_negative_path,candidateUnderTestNativeBicycleRenderUnits=render_negative_path,
      candidateUnderTestNativeBicycleEraseUnits=erase_negative_path,
      candidateUnderTestNativeBicycleOriginalArtPaletteShadowEraseMissAccepted=True,
      candidateUnderTestNativeBicycleExactScenes=91,candidateUnderTestNativeBicycleNativeShadowCopies=7117,
      candidateUnderTestNativeBicycleActualCorruptionsRejected=72,
      candidateUnderTestNativeSquareHitRenderUnits=square_hit_negative_path,
      candidateUnderTestNativeSquareRenderUnits=square_miss_negative_path,
      candidateUnderTestReachedCPURingRenderUnits=ring_negative_path,
      currentRenderingNegativeProofsRetestedWithSameMockedPathPositiveControls=True,
      priorRenderingUnrelatedExceptionClaimsWithdrawn=superseded,
      currentRealMobilityConfirmationTimingReport=timing_path,currentRealMobilityConfirmationTimingCases=timing['cases'],
      candidateUnderTestPhysicalP2CPUCaptureCount=prior['candidateUnderTestPhysicalP2CPUCaptureCount']+4,
      candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,candidateUnderTestAllArenaMoveGroundShadowAcceptance=False,
      inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      oldBuildFoldersDeletedThisTurn=0,nativeDifficultyHealthAIPositionStageRNGModified=False,
      actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      nextAction='Keep2753 isolated. Candidate actual Bicycle miss now has entire original61-field physics/initial writes/clean Square3278-to-Bicycle3279 bridge, all9donor poses, native palettes/queued geometry/black shadows/91exactscenes and one-base continuous erase. Need actual Bicycle hit/blocked/interrupt/KO, other victims/mirrors/arenas, further Square contexts, CPU/morph/overlap/art/audio. Two268/272normal confirmation-timing games produced zero Bicycle; no invented contact acceptance. Rendering negatives repaired for all recent Ring/Square/Bicycle reports, unrelated-empty-key credit explicitly withdrawn. Preserve all five original scope groups, natural full boss campaigns/own endings/attract and final UI/audio/cleanup/release requirements.',
      inputHashes=inherited)
    return prior
if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable full original-scope Bicycle checkpoint')
    value=save();OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(value,indent=2)+'\n')
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    assembly.need(result.returncode==0,'Lossless checkpoint compression')
    print(json.dumps(dict(goalStatus='active',candidateBicycleMissAccepted=True,candidateBicycleHitOrBlockedAccepted=False,
      actualBicycleMissCorruptions=72,repairedRenderingCounterexamples=127,
      originalRemainingGroups=len(value['remaining']),remainingCandidateGates=len(value['candidatePromotionGates']),
      actualFullShaoMatchClears=0,fullPortAcceptance=False,finishedRelease=False,
      revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
