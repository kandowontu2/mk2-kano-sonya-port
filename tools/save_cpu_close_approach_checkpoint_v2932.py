"""Full-scope checkpoint after four actual native CPU walking approaches.

Two additional Kano pair/ordinary contracts accepted. Both Sonya fixtures stay
rejected for ordinary continuation; actual repeated/signature branches require
their own complete contracts. No public game, launcher or ZIP bytes changed.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_cpu_close_approach_v2928 as model

ROOT=model.ROOT
PREVIOUS=ROOT/'audit_v2924_friendship_audio_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2933_cpu_close_approach_full_scope_checkpoint'

def save():
    prior=json.loads(PREVIOUS.read_text())
    need=model.assembly.need
    need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
         len(prior['remaining'])==5 and len(prior['candidatePromotionGates'])==1 and
         prior['candidateUnderTest']==model.assembly.NAME and prior['candidateUnderTestFriendshipOriginalPCMAndAudibleOverlapAccepted'] and
         len(prior['currentSourceBoundBossCampaigns'])==70 and prior['currentRealShaoKahnMatchClears']==0 and
         not prior['actualEndingsAccepted'] and prior['candidateUnderTestBoundedPhysicalP2CPUAcceptedCount']==9 and
         not prior['candidateUnderTestPhysicalP2CPUSonyaMirrorAccepted'], 'Entire original goal, prior accepted and incomplete work')
    inherited=dict(prior['inputHashes']);fresh={}
    def pin(path,wanted=None):
        path=Path(path);key=str((path if path.is_absolute()else ROOT/path).resolve())
        wanted=model.assembly.sha(key)if wanted is None else wanted
        need(key not in fresh or fresh[key]==wanted,'Consistent current source/evidence '+key)
        need(key not in inherited or inherited[key]==wanted,'Preserve immutable prior evidence '+key)
        fresh[key]=wanted
    def proof(leaf):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        need(value['passed'] and value['candidate']==model.assembly.NAME and not value['fullPortAcceptance'],'Actual bounded terminal proof '+leaf)
        for file,wanted in value['inputHashes'].items():pin(file,wanted)
        return value,str(path)
    inventory,inventory_path=proof('audit_v2929_native_cpu_close_approach_checked')
    units,units_path=proof('audit_v2931_native_cpu_close_approach_units')
    need(inventory['diagnosticInventoryOnly'] and inventory['originalTypedContractsUnchanged'] and
         len(inventory['cases'])==4 and inventory['acceptedPairFixtures']==2 and inventory['scenarioMisses']==0 and
         inventory['originalContractRejectedFixtures']==2 and inventory['acceptedPairsByActualCPU']=={'kano':2,'sonya':0} and
         not inventory['allFixturesGameplayAccepted'] and not inventory['allCPUAccepted'], 'No scenario or repeated/signature branch promoted as ordinary gameplay')
    need(units['acceptedFixturesTested']==2 and units['actualOriginalCounterexamplesRejected']==40 and
         units['originalTypedContractsUnchanged'] and units['mutationNonVacuityRequired'] and
         units['actualCapturesUnmodified'] and not units['gameBytesChanged'], 'All forty actual physical role/phase/health/floor/cleanup corruptions rejected')
    accepted=[v for v in inventory['cases']if v['status']=='accepted_original_pair_and_ordinary_followup']
    rejected=[v for v in inventory['cases']if v['status']=='original_contract_rejected']
    need({v['case']for v in accepted}=={'audit_v2927_native_cpu_close_human_sonya_boot607','audit_v2927_native_cpu_close_human_kano_boot614'},'Two previously missed Kano CPU contexts actually reached and accepted')
    for value in accepted:
        contract=value['typedContract']['originalContract']
        need(contract['passed'] and not contract['errors'] and contract['held_fields']==70 and contract['damage']==32 and
             contract['native_followup']['kind']=='ordinary' and value['floorAnchorsChecked'] and not value['rawFloorDifferences'] and
             value['wholeActualGuestReconstructed'], 'Full unchanged paired state, floor/source, damage and actual ordinary continuation')
    sonya=[]
    for value in rejected:
        need(value['actualCPU']==18 and not value['originalContract']['passed'] and value['originalContract']['errors'] and
             value['typedContract']is None and value['wholeActualGuestReconstructed'], 'Both actual Sonya fixtures retained unaccepted')
        path=ROOT/value['case']/'run.log'
        log=path.read_text(encoding='utf-8-sig')
        entries=model.MODEL.rows(log,'ENTRY');complete=model.MODEL.rows(log,'COMPLETE')
        sonya.append(dict(case=value['case'],player=value['player'],actualCPU=18,
                          nativeEntries=[dict(frame=r['frame'],cycle=r['cycle'],id=r['id'],victim=r['vid'])for r in entries],
                          recordedCompletions=[dict(frame=r['frame'],cycle=r['cycle'])for r in complete],
                          originalOrdinaryContractErrors=value['originalContract']['errors'],
                          completedRepeatedOrSignatureContractAccepted=False))
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
    print('Revalidating fresh CPU dependencies:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,wanted),actual in zip(fresh.items(),pool.map(model.assembly.sha,fresh)):
            need(actual==wanted,'Changed actual CPU evidence '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=prior['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: four fresh unassisted cold P1 human/P2 CPU fixtures used the original driver and its existing normal walking approach. All four reached actual naturally selected Kano/Sonya opponents and source-bound full guests/owners/floors/store words. Two formerly unreached Kano cases now pass complete unchanged original 22-step/70-held-field/32-damage paired contact, victim flight, individual ready cleanup and actual ordinary follow-up. Forty actual corruptions rejected. Both Sonya runs now recorded real completed leg grabs; ordinary continuation remains rejected due later repeated/signature branches, never relabeled or promoted. Full original natural-character scope and remaining CPU/morph/KO/overlap gate preserved; public game/CMD/ZIP unchanged.',
        candidateUnderTestPhysicalP2CPUCloseApproachInventoryReport=inventory_path,
        candidateUnderTestPhysicalP2CPUCloseApproachUnitsReport=units_path,
        candidateUnderTestPhysicalP2CPUCloseApproachCases=inventory['cases'],
        candidateUnderTestPhysicalP2CPUCloseApproachRejectedSonyaBranches=sonya,
        candidateUnderTestPhysicalP2CPUCaptureCount=prior['candidateUnderTestPhysicalP2CPUCaptureCount']+4,
        candidateUnderTestBoundedPhysicalP2CPUAcceptedFixtures=prior['candidateUnderTestBoundedPhysicalP2CPUAcceptedFixtures']+accepted,
        candidateUnderTestBoundedPhysicalP2CPUAcceptedCount=11,
        candidateUnderTestBoundedPhysicalP2CPUAcceptedByActualCPU={'kano':10,'sonya':1},
        candidateUnderTestPhysicalP2CPURejectedFixtures=prior['candidateUnderTestPhysicalP2CPURejectedFixtures']+rejected,
        candidateUnderTestPhysicalP2CPUActualCounterexamplesRejected=prior['candidateUnderTestPhysicalP2CPUActualCounterexamplesRejected']+40,
        candidateUnderTestPhysicalP2CPUSonyaMirrorAccepted=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,oldBuildFoldersDeletedThisTurn=0,
        nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,
        fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
        nextAction='Keep candidate2753 isolated. Eleven actual P2 CPU pairs/ordinary continuations accepted across ten Kano and one Sonya captures. Sonya mirror original walking reaches the leg pair and a later new leg entry; it is NOT an ordinary-followup pass. Preserve all raw rejected branches and build a dedicated full repeated/signature continuation capture/contract, preferably using existing input-only v1997 plus v1998/1999 read-only all-mode/child observations and a whole-guest capture. Then remaining CPU KO/morph/overlap and all five full original scope groups: arena/victim/mirror/stage effects/audio/full move phases/grounding/floor shadows/other finishers/morphs/secrets/cinematics/natural Kintaro/Shao match clears/own endings/attract/final integration/obsolete dependency cleanup/refreshed ZIP. No public promotion until required gates pass.',
        inputHashes=inherited)
    return prior

if __name__=='__main__':
    model.assembly.need(not OUT.exists(),'Immutable full-scope CPU progress checkpoint')
    value=save();OUT.mkdir();path=OUT/'checkpoint.json'
    path.write_text(json.dumps(value,indent=2)+'\n')
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    model.assembly.need(result.returncode==0,'Lossless checkpoint compression')
    print(json.dumps(dict(goalStatus='active',freshCases=4,newAcceptedOriginalPairs=2,newActualCorruptionsRejected=40,
        totalAcceptedP2CPUFixtures=11,SonyaMirrorAccepted=False,remainingCandidateGates=len(value['candidatePromotionGates']),
        originalRemainingGroups=len(value['remaining']),fullPortAcceptance=False,finishedRelease=False,
        revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']),indent=2),flush=True)
