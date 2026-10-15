"""Correct one prose count; keep authoritative qualification and old bytes."""
import json, subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
ROOT, need, sha = current.ROOT, current.need, current.sha


def main():
    parentpath=ROOT/'audit_challenger_retained_precombat_progress_storage/report.json'
    parent=json.loads(parentpath.read_text()); pins={str(parentpath):sha(parentpath)}
    doc=ROOT/'CURRENT_PLAYTEST_STATUS.md'; old=ROOT/'status_history_challenger_precombat_count_correction/CURRENT_PLAYTEST_STATUS.md'
    need(old.read_bytes().replace(b'sixteen sound-ROM faults',b'eight sound-ROM faults',1)==doc.read_bytes(), 'Only prose16-to8 correction, no source or test change')
    for p,h in parent['inputHashes'].items():
        path=Path(p)
        if path==doc:path=old
        need(sha(path)==h,'Exact prior evidence or historical prose bytes unchanged'); pins[str(path)]=h
    proofpath=ROOT/'audit_challenger_retained_precombat_checked/report.json'; proof=json.loads(proofpath.read_text())
    need(parent['waveformDACROMFaultsRejected']==18 and len(proof['wholeSoundROM']['faults'])==8, 'Authoritative count is8ROM,18combined; underlying proof already correct')
    for path in (doc,old,Path(__file__)):
        h=sha(path); need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Exact corrected prose/source compression');pins[str(path)]=h
    out=ROOT/'audit_challenger_precombat_count_correction';need(not out.exists(),'Fresh immutable correction')
    report=dict(passed=True,goalStatus='active',fullPortAcceptance=False,parent=str(parentpath),sourceProofUnchanged=True,
        soundROMFaultsRejected=8,waveformDACROMFaultsRejected=18,semanticFaultsRejected=16,
        intentionalDocumentationPinMigration=dict(path=str(doc),historicalBytes=str(old),historicalSHA256=sha(old),currentSHA256=sha(doc)),
        remaining=parent['remaining'],nextAction=parent['nextAction'],newBuilds=0,newNativeBoots=0,newRawMedia=0,inputHashes=pins)
    out.mkdir();path=out/'report.json';path.write_text(json.dumps(report,indent=2)+'\n');h=sha(path)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Exact correction checkpoint')
    print(json.dumps(dict(passed=True,soundROMFaultsRejected=8,proseCountCorrected=True,newBuilds=0)),flush=True)


if __name__=='__main__':main()
