"""Save current overlap/P2-CPU progress without narrowing the full objective."""
import json,re
from pathlib import Path
import verify_current_physical_p2_cpu_v1916 as p2
import verify_current_cpu_overlap_v1911 as overlap

ROOT=p2.ROOT;OUT=ROOT/'audit_v1926_current_cpu_overlap_checkpoint'
PREVIOUS=ROOT/'audit_v1904_current_cpu_round_checkpoint/checkpoint.json'
ACCEPTED=('audit_v1911_current_cpu_overlap_checked','audit_v1912_current_cpu_overlap_counterexamples',
          'audit_v1916_current_physical_p2_cpu_checked','audit_v1922_current_physical_p2_cpu_counterexamples')
PROBES=('audit_v1917_current_p2_cpu_human_kano_boot605','audit_v1918_current_p2_cpu_human_sonya_boot605',
        'audit_v1919_current_p2_cpu_human_kano_boot603','audit_v1920_current_p2_cpu_human_sonya_boot603',
        'audit_v1923_current_p2_cpu_human_kano_boot600','audit_v1924_current_p2_cpu_human_kano_confirm265',
        'audit_v1925_current_p2_cpu_human_kano_confirm266')

def verify():
    prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and prior['currentCandidate']==p2.launch.NAME
    pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=p2.sha(PREVIOUS);accepted={}
    def pin(path,wanted=None):
        path=Path(path);actual=p2.sha(path);assert wanted is None or wanted==actual,'Changed evidence '+str(path)
        assert str(path)not in pins or pins[str(path)]==actual,'Conflicting frozen evidence'
        pins[str(path)]=actual
    for leaf in ACCEPTED:
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text())
        assert proof['passed'] and proof['candidate']==p2.launch.NAME and not proof['fullPortAcceptance']
        for file,value in proof['inputHashes'].items():pin(file,value)
        pin(path);accepted[leaf]=proof
    probes=[]
    for leaf in PROBES:
        folder=ROOT/leaf;meta=p2.matched(folder,pins)
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        cold=p2.original.rows_prefix(log,'MK2_P2CPU_COLD_LIVE ');assert len(cold)==1
        terminal=p2.original.rows(log,'RESULT');assert len(terminal)==1
        checked=p2.original.verify_log(log,meta['player'])
        probes.append(dict(capture=leaf,exitCode=meta['exit_code'],human=meta['player'],actualCPU=cold[0]['cpu_id'],
            actualNativeSchedule=f"{cold[0]['schedule']:08X}",actualCycles=terminal[0]['cycles'],
            acceptance=False,diagnosticOriginalOrdinaryContractPassed=checked['passed'],diagnosticErrors=checked['errors'],
            reason='No opposite-slot Kano CPU selected; no new CPU, signature, repeated or KO acceptance claimed for these probes.'))
    failures={}
    for leaf in ('audit_v1910_current_cpu_overlap_checked','audit_v1921_current_physical_p2_cpu_counterexamples'):
        path=ROOT/leaf/'report.json';report=json.loads(path.read_text());assert not report['passed']
        pin(path);failures[leaf]=report['error']
    for file in ('tools/inspect_cpu_overlap_v1905.py','tools/verify_current_cpu_overlap_v1909.py',
                 'tools/verify_current_cpu_overlap_v1910.py','tools/test_current_physical_p2_cpu_v1921.py'):
        pin(ROOT/file)
    pin(Path(__file__).resolve())
    for file,value in pins.items():assert p2.sha(file)==value,'Changed accepted input '+file
    o=accepted[ACCEPTED[0]];physical=accepted[ACCEPTED[2]]
    return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='no progress: status-only reply; authoritative v1904 checkpoint revalidated before taking the next safe CPU action',
        thisGoalTurnClassification='progress: fresh source-bound all-cycle trace resolves intermediate native leg cleanup and owned blocked ring; physical P2 Sonya CPU against both new humans accepted; 56 corrupted inputs rejected',
        currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentThreeSonyaCPUGrabs=o['grabs'],currentSonyaCPUOwnedRing=o['ring'],
        legacyIncompleteExplained=o['legacyIncompleteExplained'],
        currentPhysicalP2SonyaCPU={player:dict(start=r['originalContract']['start'],release=r['originalContract']['release'],
            complete=r['originalContract']['complete'],damage=r['originalContract']['damage'],
            pairedFields=r['originalContract']['paired_fields'],allRecordedFields=r['allRecordedFields'],
            nativeStores=r['sourceBoundStores'],followup=r['originalContract']['native_followup'])for player,r in physical['cases'].items()},
        counterexamplesRejected=sum(len(accepted[leaf]['counterexamples'])for leaf in (ACCEPTED[1],ACCEPTED[3])),
        failedModelAttemptsPreserved=failures,
        failedSyntaxAttemptPreserved=dict(file='tools/verify_current_cpu_overlap_v1909.py',
            reason='Unparenthesized generator assignment; successor v1910 fixes syntax. No capture or game was altered.'),
        correctedModelAssumptions=['Original leg preserves incoming victim body flags; cycle3 enters with body12, cycles1/2 with body1A. All incoming flags, holds and original mask-clear stores are checked, not a forced body8 assumption.',
            'Native ready can call cleanup twice in one field; negative opcode test targets the actual first changed store, not an ambiguous pair of records.'],
        otherPhysicalColdStarts=probes,
        scopeCaveats=['All three P1 Sonya CPU leg releases in this fresh natural two-round run have exact native holds, damage, flight, floor and first original cleanup proof. Original complete/regain labels remain unchanged.',
            'Cycle2 ring has full native child ownership, every flight/impact field, six-chip source-owned contact, seven four-field burst poses, retirement and original own handoff. Native pixels and audio are not certified by this state observer.',
            'Cycle2 later ordinary attacks contribute another34 damage after the ring6. The all-mode health ledger/source writers are checked, but complete typed ordinary attack/art/audio acceptance remains open.',
            'P2 Sonya CPU has one full leg contact plus ordinary-follow-up cleanup against P1 Kano and P1 Sonya. All opponents, repeat/KO streams and P2 signature moves remain open.',
            'Opposite-slot Kano CPU is not accepted. Additional real cold starts selected Sonya or Baraka, not Kano; their diagnostic labels are not turned into accepted cases.'],
        remaining=prior['remaining'],
        nextAction='Actual opposite-slot Kano CPU and additional opponents; P2 signature/overlap/KO streams; full move-phase art/shadow/erase/audio across stages; remaining finishers/victims/morphs/secrets/cinematics; natural boss/campaign clears, own endings and attract return; final combined regression, dependency-aware cleanup and finished release.',
        acceptedReports={leaf:str(ROOT/leaf/'report.json')for leaf in ACCEPTED},inputHashes=pins,
        allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
        actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
        allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,
        finishedRelease=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed checkpoint'
    result=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=result['goalStatus'],candidate=result['currentCandidate'],
        exactNativeLegReleases=len(result['currentThreeSonyaCPUGrabs']),physicalP2CPUOpponents=len(result['currentPhysicalP2SonyaCPU']),
        counterexamplesRejected=result['counterexamplesRejected'],pinnedFiles=len(result['inputHashes']),finishedRelease=False)),flush=True)
