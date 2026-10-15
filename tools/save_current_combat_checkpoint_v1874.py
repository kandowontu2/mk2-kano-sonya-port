"""Save bounded current combat progress while preserving the full port scope."""
import json
from pathlib import Path
import verify_current_interrupt_v1870 as current
import verify_current_ko_v1872 as ko
from verify_human_special_phases_v1767 import sha

ROOT=current.ROOT
OUT=ROOT/'audit_v1874_current_combat_checkpoint'
PREVIOUS=ROOT/'audit_v1868_current_presentation_release_checkpoint/checkpoint.json'
REPORTS=[current.OUT/'report.json',ko.OUT/'report.json',ROOT/'audit_v1873_current_interrupt_ko_units/report.json']

def verify():
    old=json.loads(PREVIOUS.read_text())
    assert old['goalStatus']=='active' and old['currentCandidate']==current.NAME
    pins={str(PREVIOUS):sha(PREVIOUS)};summaries={};reports=[]
    for path in REPORTS:
        report=json.loads(path.read_text())
        assert report['passed'] and report['candidate']==current.NAME and not report['fullPortAcceptance']
        for file,wanted in report['inputHashes'].items():
            if file in pins:assert pins[file]==wanted,'Conflicting pinned inputs'
            pins[file]=wanted
        pins[str(path)]=sha(path);reports.append(report)
        summaries[path.parent.name]={key:report[key]for key in ('passed','candidate','pairedFields','actualFields','methods','scope')if key in report}
    fixed={
        'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
        'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
        'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
        'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
    }
    for file,wanted in fixed.items():pins[str(ROOT/file)]=wanted
    for file in ('tools/save_current_combat_checkpoint_v1874.py','audit_v1873_current_interrupt_ko_units/unit-tests.log'):
        pins[str(ROOT/file)]=sha(ROOT/file)
    for file,wanted in pins.items():assert sha(file)==wanted,'Changed verified current evidence '+file
    return dict(goalStatus='active',objective=old['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='no progress: read-only status response; revalidated latest authoritative checkpoint before fresh runtime work',
        thisGoalTurnClassification='progress: ten fresh current startup interruptions/retries, ten repeated earned KO/following-round paths including six expanded native-victim cases, and 31 unchanged/expanded counterexample unit methods',
        currentCandidate=current.NAME,currentCMD=old['currentCMD'],
        currentPlaytestZIP='release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip',
        gameSourceAndPlayableBytesChangedThisTurn=False,
        newRuntimeCases=20,interruptionPairedFields=reports[0]['pairedFields'],
        koPairedFields=reports[1]['actualFields'],earnedKnockouts=10,
        followingRoundSuccessfulSpecials=10,unitMethods=reports[2]['methods'],
        acceptedReports=summaries,inputHashes=pins,
        remaining=old['remaining'],
        nextAction='Broader native CPU integration and unexercised interruption/overlap families, victims/arenas and audio; remaining finishers/morphs/cinematics, actual boss clears/own endings/attract return, final combined regression and dependency-aware old-build cleanup. These new combat gates do not substitute for that full objective.',
        currentSelectionAndGroundingReportsRemainHistoricalAccepted=True,
        allInterruptPointsAccepted=False,allKOPathsAccepted=False,allCPUAccepted=False,
        actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
        allFinishersVictimsMorphsSecretsCinematicsAccepted=False,
        allOldBuildFoldersRemoved=False,finishedRelease=False,fullPortAcceptance=False,
        scope='Current two-human startup interruptions/retries for blade/bicycle/leg; repeated blade/bicycle native-victim and stock-reference first-KO/next-round paths. Not every move, interrupt phase, CPU, pixel, opponent, arena, sound, finishing state or campaign. Prior checkpoint linked and unchanged; its entire historical pinned inventory is not reaudited by this bounded combat checkpoint.')

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed checkpoint'
    report=verify();OUT.mkdir()
    (OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key]for key in ('goalStatus','currentCandidate','newRuntimeCases','interruptionPairedFields','koPairedFields','earnedKnockouts','followingRoundSuccessfulSpecials','unitMethods','finishedRelease')})+' pinnedFiles='+str(len(report['inputHashes'])),flush=True)
