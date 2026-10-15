"""Preserve current CPU progress and unaccepted broader CPU evidence."""
import json
from pathlib import Path
from verify_human_special_phases_v1767 import sha
import verify_ball_register_source_v1837 as current

ROOT=current.ROOT
OUT=ROOT/'audit_v1890_current_cpu_checkpoint'
PREVIOUS=ROOT/'audit_v1874_current_combat_checkpoint/checkpoint.json'
ACCEPTED=ROOT/'audit_v1885_current_cpu_leg_square_checked/report.json'
UNITS=ROOT/'audit_v1889_current_cpu_square_counterexamples/report.json'

def verify():
    prior=json.loads(PREVIOUS.read_text())
    assert prior['goalStatus']=='active' and prior['currentCandidate']==current.NAME
    pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=sha(PREVIOUS)
    proof=json.loads(ACCEPTED.read_text());units=json.loads(UNITS.read_text())
    for path,report in ((ACCEPTED,proof),(UNITS,units)):
        assert report['passed'] and report['candidate']==current.NAME and not report['fullPortAcceptance']
        for file,wanted in report['inputHashes'].items():
            assert file not in pins or pins[file]==wanted,'Conflicting pinned input'
            pins[file]=wanted
        pins[str(path)]=sha(path)
    failures={}
    for folder in ('audit_v1877_current_cpu_first_capture_checked','audit_v1879_current_cpu_first_state_checked',
                   'audit_v1879_current_cpu_guard_wait_checked','audit_v1886_current_cpu_square_counterexamples',
                   'audit_v1887_current_cpu_square_counterexamples','audit_v1888_current_cpu_square_counterexamples'):
        path=ROOT/folder/'report.json';report=json.loads(path.read_text());assert not report['passed']
        pins[str(path)]=sha(path);failures[folder]=report['error']
    historical=ROOT/'audit_v1526_active_launch_repeated_cpu_checked/report.json'
    old=json.loads(historical.read_text());assert old['passed']is False
    pins[str(historical)]=sha(historical)
    for name in ('audit_v1876_sonya_cpu_repeated_p1_human_kano','audit_v1878_sonya_cpu_guard_wait_human_kano',
                 'audit_v1878_sonya_cpu_approach_human_kano'):
        folder=ROOT/name
        for file in ('run.log','result.json','input_hashes_before.json'):
            path=folder/file;pins[str(path)]=sha(path)
        launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        assert launch['exit_code']==0 and launch['candidate']==current.NAME and launch['assistance']=='none'
    pins[str(Path(__file__).resolve())]=sha(Path(__file__).resolve())
    for file,wanted in pins.items():assert sha(file)==wanted,'Changed actual evidence '+file
    native=proof['proof'];paired=native['paired']
    return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='progress: current twenty two-human interruption/KO runtime cases and 31 counterexample methods',
        thisGoalTurnClassification='progress: current native P1 Sonya CPU leg grab followed by real complete Square Wave miss during victim recovery, exact 77 sampled scene passes, 21 state/composite corruptions rejected; prior repeated CPU sample revalidated as failed, not accepted',
        currentCandidate=current.NAME,currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
        gameSourceAndPlayableBytesChangedThisTurn=False,
        acceptedCPUInteraction=dict(cpu='sonya',cpuSlot=1,human='kano',humanSlot=2,
            pairedFields=paired['paired_fields'],heldFields=paired['held_fields'],damage=paired['damage'],
            ownReady=paired['own_handoff'],victimReady=paired['victim_handoff'],
            followup=paired['native_followup'],sampledScenes=native['sampled_frames'],
            exactScreenPixels=native['exact_screen_pixels'],exactBodyPixels=native['exact_body_pixels'],
            ownedPaletteSamples=native['fullPhysicalPaletteSamples']),
        counterexamplesRejected=len(units['counterexamples']),
        preservedFailedReports=failures,
        repeatedCPUProgress='Guard-until-close yielded no grab; original walking approach yielded only one complete grab; standing guard yielded two complete grabs separated by an earned round transition, with a real Square follow-up outside the old ordinary-follow-up contract. No forced health, RNG, position, character IDs or move choice. The whole repeated stream remains unaccepted.',
        historicalV1526RepeatedCPUAccepted=False,
        driverScopeLabelCaveat='Fresh v1880 schema-8 driver stops after first subsequent native ready plus thirty fields; its inherited terminal scope string still says repeated_pairs. The accepted verifier and this checkpoint explicitly claim one actual pair and typed Square continuation, not repeated-pair acceptance. Preserve executed source/log unchanged.',
        remaining=prior['remaining'],
        nextAction='Current Kano CPU choke/owned follow-up (historical natural cold recipe P2 human Kano, boot604/confirm264/guard_until_close), then both CPU slots and repeated/KO/native round streams with complete original health/reset and typed follow-up provenance; other interruptions/victims/arenas/audio, finishers/morphs/cinematics, genuine bosses/own endings/attract return, final regression and old-build cleanup remain in scope.',
        acceptedReports={ACCEPTED.parent.name:str(ACCEPTED),UNITS.parent.name:str(UNITS)},inputHashes=pins,
        allCPUAccepted=False,allRepeatedCPUAccepted=False,actualFullLadderClearAccepted=False,
        actualEndingsAccepted=False,allFinishersVictimsMorphsSecretsCinematicsAccepted=False,
        allOldBuildFoldersRemoved=False,finishedRelease=False,fullPortAcceptance=False,
        scope='One current natural CPU leg catch and typed complete Square Wave miss, physical native handoffs and sampled exact drawing. Not all AI, repeated grabs, CPU KOs, all art/audio/campaigns/endings or complete release.')

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed checkpoint'
    report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=report['goalStatus'],candidate=report['currentCandidate'],
        sampledCPUScenes=report['acceptedCPUInteraction']['sampledScenes'],
        counterexamplesRejected=report['counterexamplesRejected'],pinnedFiles=len(report['inputHashes']),
        allRepeatedCPUAccepted=False,finishedRelease=False)),flush=True)
