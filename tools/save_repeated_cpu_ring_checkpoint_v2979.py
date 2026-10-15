"""Preserve full native-character scope after repeated CPU/round/ring proof.

No ordinary/signature waiver, experimental promotion, public game/CMD/ZIP
change, broad shadow/art/audio completion or natural ending claim.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_cpu_ring_v2971 as model

ROOT=model.ROOT
PREVIOUS=ROOT/'audit_v2933_cpu_close_approach_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2980_repeated_cpu_ring_full_scope_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text());need=model.need
    need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
         len(prior['remaining'])==5 and len(prior['candidatePromotionGates'])==1 and
         prior['candidateUnderTest']==model.assembly.NAME and len(prior['currentSourceBoundBossCampaigns'])==70 and
         prior['currentRealShaoKahnMatchClears']==0 and not prior['actualEndingsAccepted'] and
         prior['candidateUnderTestBoundedPhysicalP2CPUAcceptedCount']==11,
         'Preserve entire original goal, all prior accepted work, natural boss and open promotion gates')
    inherited=dict(prior['inputHashes']);fresh={}
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute()else ROOT/path).resolve())
        wanted=model.assembly.sha(key)if wanted is None else wanted
        need(key not in fresh or fresh[key]==wanted,'Consistent fresh repeated CPU evidence '+key)
        need(key not in inherited or inherited[key]==wanted,'Preserve immutable prior dependency '+key)
        fresh[key]=wanted
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['passed'] and not value['fullPortAcceptance'],'Actual scoped passed terminal report '+leaf)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    extended,extended_path=proof('audit_v2947_native_extended_cpu_checked')
    coverage_units,coverage_units_path=proof('audit_v2949_native_extended_cpu_units')
    ring,ring_path=proof('audit_v2972_native_cpu_ring_checked')
    units,units_path=proof('audit_v2974_native_cpu_ring_units')
    need(extended['actualPhysicalFixtures']==ring['actualPhysicalFixtures']==4 and
         extended['allModePhysicalFields']==ring['allModePhysicalFields']==14408 and
         ring['wholeNativeStateAndHealthLedgersAccepted'] and ring['threeActualSonyaMirrorPairsAccepted'] and
         ring['originalPairPhaseInvariantsRetained'] and ring['threeActualRepeatedRingPhaseContractsAccepted'] and
         ring['readOnlyGuardObservationEveryOriginalPhysicalCallbackUnchanged'] and
         not ring['ordinaryFollowupSubstituted'] and not ring['allCPUOrMorphsAccepted'] and
         not ring['allRoundsOrKOAccepted'] and not ring['fullSignatureOrChildPhaseAcceptance'],
         'Strict cross-stream coverage, original repeated pairs, source-bound native health/state and complete reached rings only')
    need(coverage_units['actualCounterexamplesRejected']==76 and units['actualCounterexamplesRejected']==158 and
         units['actualRingCounterexamplesRejected']==82 and units['actualCapturesUnmodified'] and not units['gameChanged'],
         'Missing-frame gap corrected and all actual phase/physical Block/geometry/lifetime/ownership corruptions rejected')
    need([(r['blocked'],r['damage'],r['victim'])for r in ring['acceptedRings']]==[(True,6,18),(False,22,17),(False,22,18)] and
         all(r['impactGroups']==7 and r['bodyFields']==50 for r in ring['acceptedRings']),
         'Real blocked mirror and unblocked Kano/Sonya branch, no chip or victim relabeling')
    need(ring['acceptedRings'][0]['nativeMode7EntryBoundary'] and
         ring['acceptedRings'][2]['sourceDerivedImpactOrigin']['incomingProjectileFraction']==32768 and
         ring['acceptedRings'][2]['sourceDerivedImpactOrigin']['victimFraction']==0,
         'Complete native round-start boundary and source-derived original fractional impact alignment')
    failures=[]
    for leaf in ('audit_v2941_native_extended_cpu_checked','audit_v2945_native_extended_cpu_units',
                 'audit_v2956_native_cpu_ring_checked','audit_v2964_native_cpu_ring_checked','audit_v2967_native_cpu_ring_checked'):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(not value['passed'],'Preserve executed diagnostic failure '+leaf)
        failures.append(dict(report=str(path),error=value['error'],supersededBy=ring_path if leaf!='audit_v2945_native_extended_cpu_units'else coverage_units_path))
    for file in ('tools/verify_native_extended_cpu_v2940.py','tools/verify_native_extended_cpu_v2942.py',
                 'tools/test_native_extended_cpu_v2944.py','tools/verify_native_cpu_ring_v2955.py',
                 'tools/native_repeated_cpu_ring_contract_v2957.py','tools/verify_native_cpu_ring_v2963.py',
                 'tools/native_repeated_cpu_ring_contract_v2962.py','tools/verify_native_cpu_ring_v2966.py',
                 'tools/native_repeated_cpu_ring_contract_v2965.py'):
        pin(ROOT/file)
    for leaf,script in (('audit_v2937_native_cpu_continuation_dispatch','tools/run_native_cpu_continuation_dispatch_v2936.py'),
                        ('audit_v2953_native_cpu_ring_dispatch','tools/run_native_cpu_ring_dispatch_v2952.py')):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['allRunnersTerminal'] and value['allRunnerExitsZero'] and len(value['cases'])==4,
             'All eight actual CPU captures terminal, no inferred timeout or restart')
        pin(ROOT/script,value['sourceSHA256']);pin(ROOT/leaf/Path(script).name,value['sourceSHA256'])
    for file,wanted in {
        'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
        'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
        'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
        'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
        'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():pin(ROOT/file,wanted)
    pin(PREVIOUS);pin(__file__)
    print('Revalidating fresh repeated/round/ring dependencies:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,wanted),actual in zip(fresh.items(),pool.map(model.assembly.sha,fresh)):
            need(actual==wanted,'Actual source/capture changed '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='progress: terminal corruption report exposed a missing live-field verifier gap, changing the next action to independent cross-stream coverage; not a gameplay acceptance claim',
        thisGoalTurnClassification='progress: corrected missing live-field coverage; all seventy-six initial actual pair/state corruptions rejected. Four fresh original input-only extended native CPU matches plus four exact read-only guard replicas preserve all actual events. Three complete Sonya mirror leg pairs retain every original phase, 46 holds, 35 damage and individual cleanup. Full all-mode health/state streams include earned KOs and actual original resets, without claiming complete KO/morph coverage. Three reached ring lifetimes retain full body/flight/seven impacts/retirement/independent parent recovery with actual physical blocked mirror chip and two unblocked victims. All158 fresh logical corruptions rejected, including82 ring and boundary tests. Native mode7 startup stores and original fractional impact alignment independently source-derived. Historical rejected ordinary pair branches and all five original remaining scope groups preserved. Public game/CMD/ZIP unchanged; experimental candidate not promoted.',
        candidateUnderTestPhysicalP2CPUCaptureCount=prior['candidateUnderTestPhysicalP2CPUCaptureCount']+4,
        candidateUnderTestRepeatedCPUActualFixtures=extended['cases'],
        candidateUnderTestRepeatedCPUStreamReport=extended_path,
        candidateUnderTestRepeatedCPUStrictCoverageUnits=coverage_units_path,
        candidateUnderTestRepeatedCPURingReport=ring_path,
        candidateUnderTestRepeatedCPURingUnits=units_path,
        candidateUnderTestRepeatedCPURingCases=ring['cases'],
        candidateUnderTestSonyaMirrorRepeatedOriginalPairPhasesAccepted=True,
        candidateUnderTestSonyaMirrorRepeatedLegPairs=3,
        candidateUnderTestReachedRingPhaseContractsAccepted=ring['acceptedRings'][:2],
        controlReachedRingPhaseContractsAccepted=ring['acceptedRings'][2:],
        candidateUnderTestExtendedCPUIndividualCounterexamplesRejected=158,
        candidateUnderTestExtendedCPUInitialCoverageCounterexamplesRetested=76,
        candidateUnderTestExtendedCPUOrdinaryFollowupNotSubstituted=True,
        candidateUnderTestExtendedCPUObservedEarnedKOsAndResets={key:dict(earnedKOs=value['health']['earnedKOs'],actualRoundResets=value['health']['actualRoundResets'])for key,value in ring['cases'].items()},
        candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
        repeatedCPUVerifierFailuresPreserved=failures,
        candidateUnderTestSonyaMirrorAllCPUArtAudioAcceptance=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,oldBuildFoldersDeletedThisTurn=0,
        nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
        nextAction='Keep2753 isolated. Complete actual CPU ring raster/FIFO/palette/ground/shadow/erase proof for mirror blocked contact, Kano unblocked contact and fractional-height Sonya control via unchanged read-only2014 observer; original physical trajectories must remain exact. Then broader signature/KO/morph/CPU contexts and full move/arena/victim/finisher/stage effects/audio/morphs/secrets/cinematics; true natural full Kintaro/Shao campaigns and own endings/attract; final integration and refreshed release ZIP. Eleven ordinary original paired fixtures remain accepted, three additional mirror paired phases and two candidate ring branches do not substitute for full ordinary/signature/KO/morph acceptance or all-natural-character scope.',
        inputHashes=inherited)
    return prior

if __name__=='__main__':
    model.need(not OUT.exists(),'Immutable full original scope checkpoint')
    value=save();OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(value,indent=2)+'\n')
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    model.need(result.returncode==0,'Lossless checkpoint compression')
    print(json.dumps(dict(goalStatus='active',actualCandidateRepeatedMirrorPairs=3,actualCandidateRingBranches=2,
        actualOriginalCorruptionsRejected=158,allRoundsOrKOOrMorphsAccepted=False,
        remainingCandidateGates=len(value['candidatePromotionGates']),originalRemainingGroups=len(value['remaining']),
        fullPortAcceptance=False,finishedRelease=False,revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
