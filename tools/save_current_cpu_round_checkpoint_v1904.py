"""Record current CPU recovery/earned round-reset progress; keep full port active."""
import json
from pathlib import Path
import verify_ball_register_source_v1837 as current
from verify_human_special_phases_v1767 import sha

ROOT=current.ROOT
OUT=ROOT/'audit_v1904_current_cpu_round_checkpoint'
PREVIOUS=ROOT/'audit_v1890_current_cpu_checkpoint/checkpoint.json'
ACCEPTED=('audit_v1902_current_kano_cpu_floor_signature_checked',
          'audit_v1900_current_cpu_round_repeat_checked',
          'audit_v1903_current_cpu_round_and_kano_counterexamples')

def verify():
    prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and prior['currentCandidate']==current.NAME
    pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=sha(PREVIOUS);proofs={}
    for leaf in ACCEPTED:
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text())
        assert proof['passed'] and proof['candidate']==current.NAME and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():
            assert file not in pins or pins[file]==wanted,'Conflicting frozen evidence'
            pins[file]=wanted
        pins[str(path)]=sha(path);proofs[leaf]=proof
    failed={}
    for leaf in ('audit_v1897_current_cpu_round_repeat_checked','audit_v1898_current_cpu_round_repeat_checked',
                 'audit_v1901_current_cpu_round_and_kano_counterexamples'):
        path=ROOT/leaf/'report.json';report=json.loads(path.read_text());assert not report['passed']
        pins[str(path)]=sha(path);failed[leaf]=report['error']
    for leaf in ('audit_v1893_current_kano_cpu_signature_checked','audit_v1899_current_cpu_round_repeat_checked'):
        path=ROOT/leaf/'report.json';report=json.loads(path.read_text());assert report['passed']
        pins[str(path)]=sha(path)
    pins[str(Path(__file__).resolve())]=sha(Path(__file__).resolve())
    for file,wanted in pins.items():assert sha(file)==wanted,'Changed accepted input '+file
    kano=proofs[ACCEPTED[0]]['proof'];rounds=proofs[ACCEPTED[1]];units=proofs[ACCEPTED[2]]
    return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='progress: current natural Sonya CPU leg/Square typed recovery, exact 77 sampled scene passes and 21 counterexamples',
        thisGoalTurnClassification='progress: current natural Kano CPU mirror choke/blade typed recovery, exact 79 sampled scenes and constant native Main floor anchors; earned Sonya CPU KO, complete original reset/fill and two complete leg contacts across rounds; 24 corruption checks',
        currentCandidate=current.NAME,currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentKanoCPUChokeBlade=dict(paired=kano['paired'],sampledScenes=kano['sampled_frames'],
            exactBodyPixels=kano['exact_body_pixels'],exactScreenPixels=kano['exact_screen_pixels'],
            physicalPaletteChecks=kano['fullPhysicalPaletteSamples'],newVictimFloorAnchorAcrossReleaseChecked=True),
        currentSonyaCPUNaturalRoundRepeat={key:rounds[key]for key in ('allModePairedFields','nativeHealthStores','pairs',
            'earnedKOFrame','originalResetFrame','originalFillSentinelProven')},
        counterexamplesRejected=len(units['counterexamples']),
        failuresPreserved=failed,
        originalFillCode='Whole FF9DEC90..FF9DEF80 equals original MK2: MOVI FFFF,A0 sentinel; both real health stores; A10 starts at4, ADDK2 until160, then161. Only this mode-7 same-field sentinel is accepted; every health callback/store and original writer opcode is checked. Live invalid health remains rejected.',
        scopeCaveats=['Two declared completed Sonya leg contacts lie before/after one natural earned round reset. Intervening entry cycle2 is not claimed fully accepted; its health/identity callbacks are still included in the all-mode ledger.',
            'Both complete leg contacts require exact poses/grips/damage/native flight and individual zero-lock ready handoffs. All later CPU attacks, busy states, renderer fields and sounds are not thereby accepted.',
            'Kano CPU remains physical P1 against P2 human Kano; both CPU physical slots and all opponents remain incomplete. Native palette mirror and sampled scene pixels are exact.',
            'New current full live actor/Main ownership checks cover every mode-2 state0/1 callback, not unrelated allocations outside gameplay.',
            'Earlier single-pair driver still has its preserved historical repeated_pairs scope string; actual schema8 and accepted proof claim one typed signature follow-up, not a repeated-pair stream.'],
        remaining=prior['remaining'],
        nextAction='Current native CPU checks in the other physical slot and additional opponents; fully resolve every contact/interruption/overlap in repeated and KO streams rather than waive missed/extra entries. Remaining full move/art/shadow/erase/audio, finishers/victims/morphs/secrets/cinematics, genuine boss clears/own endings/attract return, final combined regression and dependency-aware old-build cleanup remain required.',
        acceptedReports={leaf:str(ROOT/leaf/'report.json')for leaf in ACCEPTED},inputHashes=pins,
        allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
        actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
        allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,
        finishedRelease=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed checkpoint'
    report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=report['goalStatus'],candidate=report['currentCandidate'],
        sampledKanoCPUScenes=report['currentKanoCPUChokeBlade']['sampledScenes'],
        nativeRoundPairedFields=report['currentSonyaCPUNaturalRoundRepeat']['allModePairedFields'],
        counterexamplesRejected=report['counterexamplesRejected'],pinnedFiles=len(report['inputHashes']),finishedRelease=False)),flush=True)
