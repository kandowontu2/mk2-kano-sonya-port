"""Full original natural-port checkpoint after actual Square hit/control Bike.

Actual native contact, both individual recoveries and source-exact art/shadow/
erase evidence. Candidate Bicycle and broader all-port coverage remain open.
"""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT;PREVIOUS=ROOT/'audit_v3023_native_cpu_square_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3060_native_cpu_mobility_hit_full_scope_checkpoint'

def save():
    need=assembly.need;prior=json.loads(PREVIOUS.read_text());inherited=dict(prior['inputHashes']);fresh={}
    need(prior['goalStatus']=='active'and not prior['fullPortAcceptance']and not prior['finishedRelease']and
         len(prior['remaining'])==5 and len(prior['candidatePromotionGates'])==1 and prior['candidateUnderTest']==assembly.NAME and
         len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted']and
         prior['candidateUnderTestBoundedPhysicalP2CPUAcceptedCount']==11 and prior['candidateUnderTestNativeSquareInitialEntryLocksAccepted'],
         'Entire original full scope, earlier Square miss, still-open CPU/morph/arena/ending gates retained')
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute()else ROOT/path).resolve());actual=assembly.sha(key)if wanted is None else wanted
        need(key not in fresh or fresh[key]==actual,'Consistent fresh mobility evidence '+key)
        need(key not in inherited or inherited[key]==actual,'Never overwrite immutable prior evidence '+key);fresh[key]=actual
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['passed']and not value['fullPortAcceptance'],'Actual source-bound scoped proof '+leaf)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    discovery,discovery_path=proof('audit_v3039_native_cpu_mobility_inventory_checked')
    phases,phase_path=proof('audit_v3041_native_cpu_square_hit_checked')
    units,unit_path=proof('audit_v3043_native_cpu_square_hit_units')
    render,render_path=proof('audit_v3045_native_cpu_square_hit_render_new_kano_checked')
    erase,erase_path=proof('audit_v3047_native_cpu_square_hit_erase_checked')
    render_units,render_unit_path=proof('audit_v3051_native_cpu_square_hit_render_units')
    erase_units,erase_unit_path=proof('audit_v3053_native_cpu_square_hit_erase_units')
    bicycle,bicycle_path=proof('audit_v3056_native_cpu_bicycle_extended_checked')
    bicycle_units,bicycle_unit_path=proof('audit_v3058_native_cpu_bicycle_extended_units')
    need(discovery['actualPhysicalFixtures']==5 and discovery['actualMobilityEntries']==5 and discovery['actualCandidateSquareContact']and
         discovery['actualSquareContactDamage']==27 and discovery['actualControlBicycleMiss']and discovery['genuineNoMobilityScenarios']==1 and
         discovery['wholeNativeStateHealthLedgersAccepted']and not discovery['allMovePhaseOrCPUOrRasterAudioAccepted'],
         'All actual Square hit/repeated misses/control Bicycle/no-move outcomes retained, native identities and RNG untouched')
    hit=phases['cases']['new_kano']['phase']
    need(phases['actualNativeHitAndSeparateRecoveriesAccepted']and phases['actualWholeSourceStateHealthAccepted']and
         phases['cases']['new_kano']['originalPhysicalAndNativeEventsUnchanged']and hit['damage']==27 and hit['fields']==39 and
         hit['ownRiseFields']==8 and hit['actualFlightCollisionChecks']==1 and hit['ownHitPauseFields']==10 and hit['ownFallFields']==16 and
         hit['ownLandingHolds']==4 and hit['victimFlightFields']==34 and hit['ready']==2317 and hit['victimHurtClear']==2327 and hit['victimReady']==2345 and
         hit['separateIndividualRecoveries']and hit['laterOrdinaryOrLegBranchesNotSubstituted'],
         'Every actual own/victim native contact phase/lock/HP and distinct original recovery, not common handoff or idle tail')
    need(render['sampledFrames']==69 and render['exactScreenPixels']==7010400 and render['nativeShadowCopies']==5733 and
         render['allOriginalSquarePosesVisible']and not render['allMoveGroundShadowAudioAccepted'],
         'Complete actual contact-pause/rise/drop/ready donor art, body palette, queued geometry, black floor shadows and exact scenes only')
    need(erase['continuousExactPreBuffers']==69 and erase['continuousExactFlips']==69 and erase['nativeShiftTransfers']==8763 and
         erase['originalContinuousReplayContractUnchanged']and erase['oneInitialBaseOnlyPerActualFixture']and not erase['laterBuffersUsedAsAnchors'],
         'Every actual native continuous CPU/DMA/shift-clear operation from one initial framebuffer')
    need(units['actualCounterexamplesRejected']==44 and render_units['actualCounterexamplesRejected']==16 and
         erase_units['actualOriginalEraseCounterexamplesRejected']==18 and units['actualCapturesUnmodified']and
         render_units['originalCapturesUnchanged']and erase_units['actualCapturesUnmodified'],
         'All78 actual hit/initial/attacker/victim/choice/geometry/palette/shadow/erase corruptions rejected')
    need(bicycle['originalBicycleMissPhaseChecksRetained']and bicycle['actualControlBicycleMissAccepted']and not bicycle['candidateBicycleAccepted']and
         bicycle['cases']['old_kano']['phase']['fields']==61 and bicycle['cases']['old_kano']['phase']['fractionalLandingY']==40960 and
         bicycle['cases']['old_kano']['nativeChoice']['firstRandomResult']==174 and bicycle['cases']['old_kano']['nativeChoice']['secondRandomResult']is None and
         bicycle_units['actualCounterexamplesRejected']==26 and not bicycle_units['candidateBicycleAccepted'],
         'Full original control Bicycle miss/first-chance branch and26corruptions do not become candidate acceptance')
    original=(ROOT/'mk2ks_physical_p2_cpu_square_display_v2039.lua').read_text()
    expected=original.replace("local move='square'","local move='bicycle'").replace('CPU_square_scene','CPU_bicycle_scene').replace('square/recovery','bicycle/recovery').replace('square kick','bicycle kick')
    need((ROOT/'mk2ks_native_cpu_bicycle_display_v3024.lua').read_text().rstrip()==expected.rstrip(),
         'Entire original full native drawing/shift/scanout/shadow observer preserved except selected observation target/comments')
    pin(ROOT/'mk2ks_native_cpu_bicycle_display_v3024.lua');pin(ROOT/'mk2ks_physical_p2_cpu_square_display_v2039.lua')
    failure_path=ROOT/'audit_v3032_native_cpu_mobility_inventory_checked/report.json';failure=json.loads(failure_path.read_text());pin(failure_path)
    need(not failure['passed'],'Executed initial Bicycle router-assumption failure preserved')
    pin(ROOT/'tools/verify_native_cpu_mobility_inventory_v3031.py');pin(ROOT/'tools/native_cpu_mobility_capture_contract_v3030.py')
    for leaf,script,count in(
      ('audit_v3028_native_cpu_mobility_dispatch','run_native_cpu_mobility_dispatch_v3027.py',5),
      ('audit_v3034_native_cpu_square_hit_dispatch','run_native_cpu_square_hit_dispatch_v3033.py',1)):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['allRunnersTerminal']and value['allRunnerExitsZero']and len(value['cases'])==count,'Authoritative terminal actual native input-only captures')
        pin(ROOT/'tools'/script,value['sourceSHA256']);pin(ROOT/leaf/script,value['sourceSHA256'])
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
    print('Revalidating fresh native contact/control dependencies:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            need(actual==wanted,'Immutable actual mobility contact evidence changed '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=prior['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: five real native input-only mobility matches and one full-drawing replica independently reconstruct all guest bytes and complete native state/health ledgers. Candidate naturally selected Square hit against airborne Kano at stage-right boundary; exact27HP and all8rise/first-flight/10pause/16drop/4landing-hold fields, initial locks/39-field own recovery and34-field victim flight/5landing-held fields/own hurt clear/later actual ready accepted. Attacker2317/hurt-clear2327/victim-ready2345 kept distinct; later ordinary/Leg Grab source branches preserved, not idle-tail substitution. All4 actually reached Square hit poses are original donor composites, full native palettes/FIFO/camera/black floor shadows and69scenes/7,010,400pixels/5,733shadow copies exact; original continuous one-base native erase proves69pre-buffers/69flips/8,763shift transfers. All78 hit/render/erase corruptions rejected. Control naturally selected first-chance Bicycle174/250 with no second chance; original61-field miss/ceiling/fall/fractional40960landing/individual locks and26corruptions accepted, never candidate-Bicycle acceptance. Initial wrong generalized six-step Bicycle verifier failure preserved, corrected using actual source-directed first-chance four-entry branch. Whole original scope/all5remaining groups/shared CPU-morph gate/natural boss-ending gaps preserved; no game source/exe/CMD/ZIP edits or promotion.',
      candidateUnderTestNativeMobilityDiscoveryReport=discovery_path,
      candidateUnderTestNativeSquareHitPhaseReport=phase_path,
      candidateUnderTestNativeSquareHitUnits=unit_path,
      candidateUnderTestNativeSquareHitRenderReport=render_path,
      candidateUnderTestNativeSquareHitEraseReport=erase_path,
      candidateUnderTestNativeSquareHitRenderUnits=render_unit_path,
      candidateUnderTestNativeSquareHitEraseUnits=erase_unit_path,
      candidateUnderTestNativeSquareHitPhase=hit,
      candidateUnderTestNativeSquareHitAccepted=True,
      candidateUnderTestNativeSquareHitOriginalArtPaletteShadowEraseAccepted=True,
      candidateUnderTestNativeSquareHitExactScenes=69,candidateUnderTestNativeSquareHitNativeShadowCopies=5733,
      candidateUnderTestNativeSquareHitCorruptionsRejected=78,
      controlNativeBicycleExtendedReport=bicycle_path,controlNativeBicycleExtendedUnits=bicycle_unit_path,
      controlNativeBicycleExtendedMissAccepted=True,candidateUnderTestNativeBicycleAccepted=False,
      actualMobilityNativeChoiceClarification='Native first250/1000 chance branches directly to Bicycle atFFFBC320. Only a failed first chance invokes second400/1000 chance, which selects Square atFFFBC2F0; otherwise Ring. Actual first-chance Bicycle trace has four entries and no invented second RNG result.',
      actualMobilityHealthParserClarification='FLAG before/after are hexadecimal; HEALTH before/after are decimal. Actual contact100to73 is27 damage; no captured data was rewritten.',
      mobilityInitialRouterFailurePreserved=dict(report=str(failure_path),error=failure['error'],supersededBy=discovery_path),
      candidateUnderTestNativeSquareAudioAccepted=False,candidateUnderTestNativeSquareAllArenasAccepted=False,
      candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,candidateUnderTestAllArenaMoveGroundShadowAcceptance=False,
      candidateUnderTestPhysicalP2CPUCaptureCount=prior['candidateUnderTestPhysicalP2CPUCaptureCount']+5,
      inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      oldBuildFoldersDeletedThisTurn=0,nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,
      fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      nextAction='Keep2753 isolated. Actual candidate unblocked airborne-Kano Square hit now has complete native chance/contact/27HP/initial lock/own and victim physics and distinct cleanup/ready plus original art/palettes/native black floor shadows/full raster/continuous erase proof. Need candidate Bicycle reached from original normal-input paths (first250chance, never forced) and its hit/blocked/interrupt/KO plus further Square contexts, CPU/morph/overlap/art/audio/arena coverage. Control61-field Bicycle miss is reference only. Preserve actual missed scenarios and initial verifier failures. Whole native Pit/Tomb/victim/stage effects/audio/finishers/morphs/secrets/cinematics/natural full Kintaro/Shao campaigns/own endings/attract/final UI-ladder-names/audio/cleanup/refreshed ZIP remains required.',
      inputHashes=inherited)
    return prior

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable full-scope actual mobility-hit checkpoint')
    value=save();OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(value,indent=2)+'\n')
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    assembly.need(result.returncode==0,'Lossless full checkpoint compression')
    print(json.dumps(dict(goalStatus='active',nativeSquareHitScenes=69,nativeSquareHitShadowCopies=5733,
      actualHitRenderEraseCorruptionsRejected=78,actualControlBicycleCorruptionsRejected=26,candidateBicycleAccepted=False,
      originalRemainingGroups=len(value['remaining']),remainingCandidateGates=len(value['candidatePromotionGates']),
      fullPortAcceptance=False,finishedRelease=False,revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
