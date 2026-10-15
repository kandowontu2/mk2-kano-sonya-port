"""Record actual failed physical acid probe without mislabeling a success."""
import json
import verify_native_source_sync as sync
from qualify_current_native_tomb_case import load

def main():
    source=sync.verify();folder=sync.ROOT/'audit_current_native_deadpool_probe_kano_p1_runtime'
    out=sync.ROOT/'audit_current_native_deadpool_probe_kano_p1_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_deadpool_probe_preparation/stage.lua')
    assert not (folder/'stderr.log').read_text().strip() and not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=load(folder/'run.log');assert all(r['writes']=='0' and r['assistance']=='none' and r['side']=='1' and r['winner']=='kano' for records in rows.values() for r in records)
    assert [(r['match'],r['arena'],r['ids']) for r in rows['MATCH']]==[('1','0','17,18')]
    hits=rows['DAMAGE'];assert all(r['pc']=='FF836700' and 0<=int(r['after'])<int(r['before'])<=161 for r in hits)
    assert sum(int(r['before'])-int(r['after']) for r in hits)==322 and sum(r['after']=='0' for r in hits)==2
    assert not rows.get('ACID_UPPERCUT_ENTRY') and not rows.get('FIELD')
    assert rows['RESULT'][0]['action']=='-1' and rows['REJECT_END'][0]['mode']=='3' and rows['REJECT_END'][0]['arena']=='1'
    begin=int(rows['COMMAND'][0]['frame'])
    for age in range(44):
        keys={r['button'] for r in rows['INPUT'] if int(r['frame'])==begin+age}
        expected=set()
        if 5<=age<44:expected|={'Low_Punch','Low_Kick'}
        if 16<=age<44:expected.add('Down')
        if 32<=age<36:expected.add('High_Punch')
        assert keys==expected
    report=dict(passedObservationChecks=True,sourceSync=source,terminal=terminal,earnedNativeKOs=2,
        intendedPhysicalInputVerified=True,actualUppercutEntryObserved=False,acidFinisherAccepted=False,
        logSHA256=sync.sha(folder/'run.log'),fullPortAcceptance=False,
        scope='Failed current earned KanoP1/SonyaP2 heldLP/LK crouchHP DeadPool probe, no native uppercut entry observed, clean next-arena exit. No claim of acid activation or diagnosis of port defect; actual action chronology still needed.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passedObservationChecks=True,acidFinisherAccepted=False)))

if __name__=='__main__':main()
