"""Full original scope checkpoint after actual ring raster/shadow/erase proof.

Original reached blocked/unblocked/mirror/fractional source paths retained.
No all-arena/CPU/morph/KO/audio/endings/goal claim or public promotion.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT=assembly.ROOT
PREVIOUS=ROOT/'audit_v2980_repeated_cpu_ring_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2992_cpu_ring_render_full_scope_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());need=assembly.need
    need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
         len(prior['remaining'])==5 and len(prior['candidatePromotionGates'])==1 and
         prior['candidateUnderTest']==assembly.NAME and prior['candidateUnderTestSonyaMirrorRepeatedOriginalPairPhasesAccepted'] and
         prior['candidateUnderTestBoundedPhysicalP2CPUAcceptedCount']==11 and
         len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and
         not prior['actualEndingsAccepted'], 'Entire original goal and still-open natural campaign/ending/CPU/morph coverage retained')
    inherited=dict(prior['inputHashes']);fresh={}
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute()else ROOT/path).resolve())
        wanted=assembly.sha(key)if wanted is None else wanted
        need(key not in fresh or fresh[key]==wanted,'Consistent actual rendered CPU evidence '+key)
        need(key not in inherited or inherited[key]==wanted,'Preserve immutable historical evidence '+key)
        fresh[key]=wanted
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['passed'] and not value['fullPortAcceptance'],'Actual passed bounded native render proof '+leaf)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    render,render_path=proof('audit_v2984_native_cpu_ring_render_checked')
    erase,erase_path=proof('audit_v2986_native_cpu_ring_erase_checked')
    render_units,render_units_path=proof('audit_v2988_native_cpu_ring_render_units')
    erase_units,erase_units_path=proof('audit_v2990_native_cpu_ring_erase_units')
    need(render['actualPhysicalFixtures']==3 and render['sampledFrames']==253 and
         render['exactScreenPixels']==25704800 and render['nativeShadowCopies']==24861 and
         render['allOriginalPhysicalCallbacksUnchanged'] and render['allRetainedScenesExact'] and
         not render['allMoveGroundShadowAccepted'] and not render['allArenaAudioCPUAccepted'],
         'Complete reached ring body/child art, native FIFO/camera/palettes/black shadow copies and actual raster only')
    need(erase['originalContinuousReplayContractUnchanged'] and erase['continuousExactPreBuffers']==253 and
         erase['continuousExactFlips']==253 and erase['nativeShiftTransfers']==32131 and
         erase['oneInitialBaseOnlyPerActualFixture'] and not erase['laterBuffersUsedAsAnchors'],
         'Full original one-anchor native CPU/DMA/shift clear replay, no later expected-image anchors')
    need(render_units['actualOriginalRenderCounterexamplesRejected']==63 and
         erase_units['actualOriginalEraseCounterexamplesRejected']==54 and
         render_units['actualCapturesUnmodified'] and erase_units['actualCapturesUnmodified'] and
         not render_units['gameChanged'] and not erase_units['gameChanged'],
         'All117 nonvacuous actual pixel/floor/owner/shadow/palette/retirement/erase counterexamples rejected')
    for key,case in render['cases'].items():
        need(case['allRetainedScenesExact'] and case['originalPhysicalTrajectoryUnchanged'] and
             case['noPhysicalPointerReplacement'] and case['originalChargePaletteSamples']>0 and
             case['restoredReleaseBodyPaletteSamples']>0 and
             case['completePhaseCoverage'][0]['bodyPoses']==5 and
             case['completePhaseCoverage'][0]['impactPoses']==7 and
             case['completePhaseCoverage'][0]['postRetirementSamples']==14,
             'All reached ring body/impact phases visible, original charging/restored palettes, fourteen post-retirement samples '+key)
    dispatch_path=ROOT/'audit_v2977_native_cpu_ring_display_dispatch/report.json'
    dispatch=json.loads(dispatch_path.read_text());pin(dispatch_path)
    need(dispatch['allRunnersTerminal'] and dispatch['allRunnerExitsZero'] and len(dispatch['cases'])==3,
         'All three complete actual rendered CPU fixtures terminal')
    pin(ROOT/'tools/run_native_cpu_ring_display_dispatch_v2976.py',dispatch['sourceSHA256'])
    pin(ROOT/'audit_v2977_native_cpu_ring_display_dispatch/run_native_cpu_ring_display_dispatch_v2976.py',dispatch['sourceSHA256'])
    failure_path=ROOT/'audit_v2982_native_cpu_ring_render_checked/report.json'
    failure=json.loads(failure_path.read_text());pin(failure_path)
    need(not failure['passed'],'Executed first mirror renderer derivation failure preserved')
    pin(ROOT/'tools/verify_native_cpu_ring_render_v2981.py')
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
    print('Revalidating fresh rendered CPU dependencies:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,wanted),actual in zip(fresh.items(),pool.map(assembly.sha,fresh)):
            need(actual==wanted,'Actual native render source/capture changed '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=prior['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: three full native CPU ring drawing replicas preserve every original physical/guard/child/round/health/state event. Both candidate blocked Sonya mirror and unblocked Kano victim plus actual fractional-height control pass complete original donor body/flight/seven-impact art, source-bound native FIFO/cache/DMA/camera projections, all owned and charge/restored palettes, exact compressed black shadow rows and253 consecutive scenes/25,704,800pixels/24,861native shadow copies. Full original chronological continuous erase replay proves253pre-buffers/253flips/32,131native shift transfers from one initial base per fixture, never later expected screenshot anchors. All117 actual render/erase corruptions rejected. No universal grounding/shadow/CPU/morph/KO/audio acceptance or natural campaign/ending claim. Entire original five remaining groups and shared allocator/reset candidate gate preserved. Public game/CMD/ZIP unchanged.',
        candidateUnderTestReachedCPURingRenderReport=render_path,
        candidateUnderTestReachedCPURingEraseReport=erase_path,
        candidateUnderTestReachedCPURingRenderUnits=render_units_path,
        candidateUnderTestReachedCPURingEraseUnits=erase_units_path,
        candidateUnderTestReachedCPURingNativeRenderCases={k:v for k,v in render['cases'].items()if k.startswith('new')},
        controlReachedCPURingNativeRenderCases={k:v for k,v in render['cases'].items()if k.startswith('old')},
        candidateUnderTestReachedCPURingOriginalArtPaletteShadowsAndEraseAccepted=True,
        candidateUnderTestReachedCPURingRenderActualCorruptionsRejected=117,
        candidateUnderTestSonyaMirrorAllCPUArtAudioAcceptance=False,
        candidateUnderTestAllArenaMoveGroundShadowAcceptance=False,
        candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
        renderedRingInitialDerivationFailurePreserved=dict(report=str(failure_path),error=failure['error'],supersededBy=render_path),
        candidateUnderTestPhysicalP2CPUCaptureCount=prior['candidateUnderTestPhysicalP2CPUCaptureCount']+2,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,oldBuildFoldersDeletedThisTurn=0,
        nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
        nextAction='Keep2753 isolated. Actual reached ring state/art/charging/restored palettes/native black shadow/complete continuous erase now accepted for mirror blocked and Kano unblocked victims; fractional-height control also accepted. Extend original read-only native CPU choice/fall/render observers for actual bicycle/Square branches already reached by unchanged physical1997 matches, then deeper interrupted/KO/morph/overlap/CPU other-character contexts. Preserve raw rejected ordinary pair labels and debug sole offsets, never turn narrow source/raster passes into universal grounding/CPU acceptance. Full original arena/victim/mirror/stage effects/audio/other finishers/morphs/secrets/cinematics/natural full Kintaro/Shao campaigns/own endings/attract/final integration and refreshed release ZIP still required.',
        inputHashes=inherited)
    return prior

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable full original-scope native render checkpoint')
    value=save();OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(value,indent=2)+'\n')
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    assembly.need(result.returncode==0,'Lossless full checkpoint compression')
    print(json.dumps(dict(goalStatus='active',nativeRingScenes=253,actualNativeShadowCopies=24861,
        nativeContinuousPreBuffers=253,nativeContinuousFlips=253,renderAndEraseCorruptionsRejected=117,
        remainingCandidateGates=len(value['candidatePromotionGates']),originalRemainingGroups=len(value['remaining']),
        fullPortAcceptance=False,finishedRelease=False,revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
