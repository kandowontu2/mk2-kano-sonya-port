"""Retain complete goal scope and exact CPU evidence; no finished-release claim."""
import json,re
from pathlib import Path
import verify_current_kano_cpu_overlap_v1963 as current

ROOT=current.ROOT;OUT=ROOT/'audit_v1965_current_kano_cpu_checkpoint'
PREVIOUS=ROOT/'audit_v1926_current_cpu_overlap_checkpoint/checkpoint.json'
ACCEPTED=('audit_v1934_current_kano_sonya_cpu_display_checked','audit_v1941_current_kano_physical_p2_cpu_checked',
    'audit_v1945_current_kano_cpu_slots_counterexamples','audit_v1963_current_kano_cpu_overlap_checked',
    'audit_v1964_current_kano_cpu_overlap_counterexamples')

def save():
    prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and prior['currentCandidate']==current.launch.launch.NAME
    pins=dict(prior['inputHashes']);accepted={}
    def pin(file,wanted=None):
        file=Path(file);value=current.launch.sha(file)
        assert wanted is None or wanted==value,'Changed evidence '+str(file)
        assert str(file)not in pins or pins[str(file)]==value,'Conflicting pinned input '+str(file)
        pins[str(file)]=value
    pin(PREVIOUS)
    for leaf in ACCEPTED:
        path=ROOT/leaf/'report.json';report=json.loads(path.read_text())
        assert report['passed']and report['candidate']==prior['currentCandidate']and not report['fullPortAcceptance']
        for file,value in report['inputHashes'].items():pin(file,value)
        pin(path);accepted[leaf]=report
    diagnostics=[]
    for folder in sorted(ROOT.iterdir()):
        if not folder.is_dir()or not re.match(r'^audit_v19(?:2[7-9]|3[0-9]|44|48|51|54|57)_',folder.name):continue
        if not(folder/'result.json').is_file():continue
        meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        if meta.get('cpu_slot')!=2:continue # P1 capture is already pinned by its accepted renderer report.
        current.launch.matched(folder,pins)
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        cold=current.P.rows_prefix(log,'MK2_P2CPU_COLD_LIVE ')
        assert len(cold)==1
        diagnostics.append(dict(capture=folder.name,exitCode=meta['exit_code'],human=meta['player'],actualCPU=cold[0]['cpu_id'],
            nativeSchedule=f"{cold[0]['schedule']:08X}",acceptedSeparately=folder.name in('audit_v1939_current_kano_p2_cpu_human_sonya','audit_v1957_current_kano_p2_cpu_knife_guard'),
            note='Diagnostic only unless explicitly covered by the named independent accepted report; no universal CPU or signature acceptance.'))
    failed={}
    for leaf in('audit_v1933_current_kano_cpu_sonya_signature_checked','audit_v1958_current_kano_cpu_overlap_checked',
        'audit_v1959_current_kano_cpu_overlap_checked','audit_v1961_current_kano_cpu_overlap_checked','audit_v1962_current_kano_cpu_overlap_checked'):
        path=ROOT/leaf/'report.json';report=json.loads(path.read_text());assert not report['passed'];pin(path)
        failed[leaf]=report.get('error',report.get('errors'))
    # Executed source and intermediate proofs remain immutable, including the
    # wrong-register diagnostic, missing branch-site observer and false models.
    files=('mk2ks_physical_p2_cpu_knife_trace_v1946.lua','mk2ks_physical_p2_cpu_knife_trace_v1949.lua',
        'mk2ks_physical_p2_cpu_knife_trace_v1952.lua','mk2ks_physical_p2_cpu_knife_trace_v1955.lua',
        'tools/run_current_physical_p2_cpu_knife_v1947.ps1','tools/run_current_physical_p2_cpu_knife_v1950.ps1',
        'tools/run_current_physical_p2_cpu_knife_v1953.ps1','tools/run_current_physical_p2_cpu_knife_v1956.ps1',
        'tools/verify_current_kano_cpu_overlap_v1958.py','tools/verify_current_kano_cpu_overlap_v1959.py',
        'tools/verify_current_kano_cpu_overlap_v1960.py','tools/verify_current_kano_cpu_overlap_v1961.py',
        'tools/verify_current_kano_cpu_overlap_v1962.py','tools/verify_current_kano_cpu_overlap_v1963.py',
        'tools/test_current_kano_cpu_overlap_v1964.py','audit_v1960_current_kano_cpu_overlap_checked/report.json')
    for file in files:pin(ROOT/file)
    pin(Path(__file__).resolve())
    for file,wanted in pins.items():assert current.launch.sha(file)==wanted,'Changed authoritative evidence '+file
    proof=accepted['audit_v1963_current_kano_cpu_overlap_checked'];p1=accepted[ACCEPTED[0]];p2=accepted[ACCEPTED[1]]
    return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification='no progress: status-only reply; current accepted reports and authoritative v1926 checkpoint revalidated before resuming unfinished mirror verification',
        thisGoalTurnClassification='progress: opposite-slot Kano against Sonya and mirror choke/knife/KO/reset stream accepted; physical Block decision source-proven; 90 additional corruptions rejected',
        currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
        gameSourceAndPlayableBytesChangedThisTurn=False,
        currentKanoCPUAgainstSonya=dict(p1ActualOrdinary=p1['proof']['paired']['native_followup'],p2ActualOrdinary=p2['cases']['sonya']['originalContract']['native_followup'],
            p1RenderedScope=p1['scope'],p2StateScope=p2['scope']),
        currentPhysicalP2KanoMirror=dict(grabs=proof['grabs'],knives=proof['knives'],allModePairedFields=proof['allModePairedFields'],
            nativeHealthStores=proof['nativeHealthStores'],earnedKOFrame=proof['earnedKOFrame'],originalResetFrame=proof['originalResetFrame'],
            originalFillSentinelProven=proof['originalFillSentinelProven'],legacyIncompleteExplained=proof['legacyIncompleteExplained']),
        newCounterexamplesRejected=sum(len(accepted[leaf]['counterexamples'])for leaf in(ACCEPTED[2],ACCEPTED[4])),
        failedAttemptsPreserved=failed,
        correctedModelAssumptions=['Native choke releases in the final grip scheduler field; its next callback has victim action506. The unchanged original paired contract permits this exact boundary.',
            'Second knife executes after original mode7->2 switch within the field, so its first callback is start+1. No fabricated mode2 callback at the beginning of that field.',
            'Native attacks legitimately write victim state from the CPU Main, and an owned knife can write victim stun flags. Operand registers and published target/actual owning Main are bound independently.',
            'Original FF837D40 reads victim Main from *A13(170), not victim-object+170. Wrong-register v1948 capture is preserved and not accepted.',
            'Original guard flag1 can linger without Block held. Actual first input query reads FFFFFFFF and original CLRC reject; second reads FFFFFFDF and original SETC accept. Damage22/6 is not inferred solely from displayed guard or flags.'],
        otherPhysicalColdStarts=diagnostics,acceptedReports={leaf:str(ROOT/leaf/'report.json')for leaf in ACCEPTED},
        scopeCaveats=['This precise P2 Kano mirror proves both native choke releases/first cleanup, both owned knives and every recorded child/body field, original block-button test/return, KO/reset/fill. It is not complete typed ordinary-attack, collision-box, raster/audio or universal AI acceptance.',
            'P1 Kano versus Sonya has exact scene rendering; P2 Kano versus Sonya has original paired/ordinary-state acceptance. Do not promote those scopes into every opponent or move.',
            'All existing labels and captured timelines remain unchanged. Added read-only observers reproduce the v1944 native trajectory exactly.',
            'Current CMD, playtest ZIP and game bytes remain unchanged; no completed-port release has been made.'],
        remaining=prior['remaining'],nextAction='Broader CPU special/repeated/KO/overlap paths and original collision/art/shadow/audio across move phases and stages; remaining finishers/victims/morphs/secrets/cinematics; genuine boss/campaign clears, own endings and attract return; final combined regression, dependency-aware obsolete-build cleanup and finished release.',
        inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
        actualFullLadderClearAccepted=False,actualEndingsAccepted=False,allFinishersVictimsMorphsSecretsCinematicsAccepted=False,
        allOldBuildFoldersRemoved=False,finishedRelease=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed checkpoint'
    result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(goalStatus=result['goalStatus'],candidate=result['currentCandidate'],mirrorChokes=len(result['currentPhysicalP2KanoMirror']['grabs']),
        mirrorKnives=len(result['currentPhysicalP2KanoMirror']['knives']),newCounterexamplesRejected=result['newCounterexamplesRejected'],pinnedFiles=len(result['inputHashes']),finishedRelease=False)),flush=True)
