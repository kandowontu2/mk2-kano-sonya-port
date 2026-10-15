"""Preserve full natural-port scope after actual CPU Square startup/render proof.

No public promotion, all-CPU/hit/audio/arena or ending claim. Keep every original
remaining group, historical evidence, real branch miss and diagnostic failure.
"""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT;PREVIOUS=ROOT/'audit_v2992_cpu_ring_render_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3023_native_cpu_square_full_scope_checkpoint'

def save():
    need=assembly.need;prior=json.loads(PREVIOUS.read_text());inherited=dict(prior['inputHashes']);fresh={}
    need(prior['goalStatus']=='active'and not prior['fullPortAcceptance']and not prior['finishedRelease']and
         len(prior['remaining'])==5 and len(prior['candidatePromotionGates'])==1 and prior['candidateUnderTest']==assembly.NAME and
         len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and
         not prior['actualEndingsAccepted']and prior['candidateUnderTestBoundedPhysicalP2CPUAcceptedCount']==11,
         'Entire original natural-port scope and still-open CPU/morph/arena/ending gates retained')
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute()else ROOT/path).resolve());actual=assembly.sha(key)if wanted is None else wanted
        need(key not in fresh or fresh[key]==actual,'Consistent fresh input '+key)
        need(key not in inherited or inherited[key]==actual,'Never replace immutable prior evidence '+key)
        fresh[key]=actual
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['passed']and not value['fullPortAcceptance'],'Actual scoped proof '+leaf)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    inventory,inventory_path=proof('audit_v2999_native_cpu_square_inventory_checked')
    phases,phase_path=proof('audit_v3009_native_cpu_square_locks_checked')
    phase_units,phase_unit_path=proof('audit_v3015_native_cpu_square_locks_units')
    render={};render_paths={}
    for key in ('new_sonya','old_kano'):
        render[key],render_paths[key]=proof(f'audit_v3013_native_cpu_square_render_{key}_checked')
    erase,erase_path=proof('audit_v3017_native_cpu_square_erase_checked')
    render_units,render_unit_path=proof('audit_v3019_native_cpu_square_render_units')
    erase_units,erase_unit_path=proof('audit_v3021_native_cpu_square_erase_units')
    need(inventory['actualPhysicalFixtures']==7 and inventory['actualSquareEntries']==4 and inventory['genuineNoSquareScenarios']==3 and
         inventory['exactNativeMissCollisionChecks']==104 and inventory['wholeStateHealthLedgersAccepted']and
         not inventory['fullMovePhaseAcceptance'],'All seven actual real native branch outcomes retained separately')
    need(phases['actualPhysicalFixtures']==2 and phases['actualInitialEntryStoresCaptured']and phases['fullOriginalSquareMissPhaseChecksRetained']and
         phases['sourceBoundNativeCollisionReturns']==52 and not phases['candidateMirrorIdleTailSubstituted'],
         'True two-slot initial boundary/write chain and entire original 54-field Square miss physics/recovery')
    need(phases['cases']['new_sonya']['phase']['postRegainOrdinaryCallbacks']==7 and
         not phases['cases']['new_sonya']['phase']['originalThirtyOneCallbackOrdinaryTailAccepted']and
         phases['cases']['old_kano']['phase']['postRegainOrdinaryCallbacks']==31,
         'Actual later mirror Leg Grab remains a distinct branch, not a claimed ordinary tail')
    scenes=sum(c['sampledFrames']for c in render.values());pixels=sum(c['exactScreenPixels']for c in render.values())
    shadows=sum(c['nativeShadowCopies']for c in render.values())
    need(scenes==168 and pixels==17068800 and shadows==15542 and all(c['allOriginalSquarePosesVisible']for c in render.values())and
         all(not c['allMoveGroundShadowAudioAccepted']for c in render.values()),'Complete reached Square original art/palettes/native black floor shadows/exact scanout only')
    need(erase['continuousExactPreBuffers']==168 and erase['continuousExactFlips']==168 and erase['nativeShiftTransfers']==21336 and
         erase['originalContinuousReplayContractUnchanged']and erase['oneInitialBaseOnlyPerActualFixture']and not erase['laterBuffersUsedAsAnchors'],
         'Every native continuous CPU/DMA/shift-load/FILL clear from one actual initial base')
    need(phase_units['actualCounterexamplesRejected']==56 and render_units['actualCounterexamplesRejected']==32 and
         erase_units['actualOriginalEraseCounterexamplesRejected']==36 and phase_units['actualCapturesUnmodified']and
         render_units['originalCapturesUnchanged']and erase_units['actualCapturesUnmodified'],
         'All124 nonvacuous actual lock/physics/choice/FIFO/palette/shadow/erase counterexamples rejected')
    failures={}
    for leaf,script,reason in (
      ('audit_v3007_native_cpu_square_locks_checked','verify_native_cpu_square_locks_v3006.py','Unsupported minimum event-count threshold; all9022/8515 actual events were exactly identical. Corrected to independent complete all-mode/live field coverage in3008.'),
      ('audit_v3011_native_cpu_square_locks_units','test_native_cpu_square_locks_v3010.py','Wrong test tag for regain; corrected to actual original overlap tag and physical CPU owner to disambiguate mirror.')):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());need(not value['passed'],'Executed diagnostic failure preserved')
        pin(path);pin(ROOT/'tools'/script);failures[leaf]=dict(report=str(path),error=value['error'],explanation=reason)
    for leaf,script,count in (
      ('audit_v2996_native_cpu_square_dispatch','run_native_cpu_square_dispatch_v2995.py',7),
      ('audit_v3003_native_cpu_square_locks_dispatch','run_native_cpu_square_locks_dispatch_v3002.py',2)):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['allRunnersTerminal']and value['allRunnerExitsZero']and len(value['cases'])==count,'Authoritative terminal real capture dispatcher')
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
    print('Revalidating fresh native Square dependencies:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for(file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            need(actual==wanted,'Immutable actual native Square evidence changed '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: preceding user-requested status-only turn restated the checkpoint; revalidated current terminal dispatchers and took the next original-scope verification action.',
      thisGoalTurnClassification='progress: seven true normal-input native CPU capture outcomes independently source-bound with complete whole guest/state/health ledgers; four actual Square choices/104collision checks and three genuine no-Square scenarios retained. Two unchanged-trajectory replicas now capture both-slot initial entry and all actual initial action/body/flag/HP writers, closing the first-live observer gap. Full original54-field Square miss rise/26-flight/drop/landing/four-hold/individual-ready checks pass on candidate mirror and control. Actual mirror next Leg Grab after seven callbacks is explicitly not a31-field ordinary tail. Complete original donor art/palettes/native black floor-shadow copies and168exact scanouts/17,068,800pixels/15,542shadow copies accepted; original one-base continuous erase proves168pre-buffers/168flips/21,336native shift transfers. All124 actual phase/render/erase corruptions rejected. Two executed verifier/test derivation failures preserved. No gameplay source/executable/CMD/ZIP edits or public promotion; whole original five remaining groups and CPU/morph/natural campaign/ending gates retained.',
      candidateUnderTestNativeSquareInventoryReport=inventory_path,
      candidateUnderTestNativeSquareInitialLockPhaseReport=phase_path,
      candidateUnderTestNativeSquareInitialLockUnits=phase_unit_path,
      candidateUnderTestNativeSquareRenderReports=render_paths,
      candidateUnderTestNativeSquareEraseReport=erase_path,
      candidateUnderTestNativeSquareRenderUnits=render_unit_path,
      candidateUnderTestNativeSquareEraseUnits=erase_unit_path,
      candidateUnderTestNativeSquareActualBranchInventory={k:dict(entries=c['actualSquareEntries'],genuineNoSquareScenario=c['noSquareScenario'])for k,c in inventory['cases'].items()},
      candidateUnderTestNativeSquareInitialEntryLocksAccepted=True,
      candidateUnderTestNativeSquareMissPhaseCases=phases['cases'],
      candidateUnderTestNativeSquareOriginalArtPaletteShadowEraseAccepted=True,
      candidateUnderTestNativeSquareExactScenes=scenes,candidateUnderTestNativeSquareExactPixels=pixels,
      candidateUnderTestNativeSquareNativeShadowCopies=shadows,candidateUnderTestNativeSquareCorruptionsRejected=124,
      candidateUnderTestNativeSquareHitAccepted=False,candidateUnderTestNativeSquareAudioAccepted=False,
      candidateUnderTestNativeSquareAllArenasAccepted=False,candidateUnderTestNativeSquareInitialFailuresPreserved=failures,
      candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
      candidateUnderTestAllArenaMoveGroundShadowAcceptance=False,
      candidateUnderTestPhysicalP2CPUCaptureCount=prior['candidateUnderTestPhysicalP2CPUCaptureCount']+7,
      inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      oldBuildFoldersDeletedThisTurn=0,nativeDifficultyHealthAIPositionStageRNGModified=False,
      actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      nextAction='Keep2753 isolated. Source-bound candidate mirror Square miss now has complete actual startup locks/native choice/54-field original phases/black floor-shadow art/palettes/exact raster and continuous erase proof. Need actual Square hit/blocked/interrupted/KO and Bicycle branch coverage from normal human inputs; preserve original CPU move choice/RNG, actual physical role/identity and all branch misses. Then broader morph/overlap/CPU/art/audio/arena and full native Pit/Tomb/victim/stage-effect/finisher/secret/cinematic coverage, natural full Kintaro/Shao campaigns/own endings/attract and final combined UI/ladder/names/audio/cleanup/refreshed ZIP. Original scope never reduced to scoped passes.',
      inputHashes=inherited)
    return prior

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable full-scope native Square checkpoint')
    value=save();OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(value,indent=2)+'\n')
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    assembly.need(result.returncode==0,'Lossless full checkpoint compression')
    print(json.dumps(dict(goalStatus='active',nativeSquareScenes=168,nativeShadowCopies=15542,
      sourceBoundPhaseRenderEraseCorruptionsRejected=124,originalRemainingGroups=len(value['remaining']),remainingCandidateGates=len(value['candidatePromotionGates']),
      fullPortAcceptance=False,finishedRelease=False,revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
