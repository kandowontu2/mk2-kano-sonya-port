"""Actual uppercut observed, ordinary landing must not count as acid success."""
import json
import verify_native_source_sync as sync
from qualify_current_native_tomb_case import load

def main():
    source=sync.verify();folder=sync.ROOT/'audit_current_native_deadpool_late_hold_kano_p1_runtime'
    out=sync.ROOT/'audit_current_native_deadpool_late_hold_kano_p1_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_deadpool_late_hold_preparation/stage.lua')
    assert not (folder/'stderr.log').read_text().strip() and not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=load(folder/'run.log');assert all(r['writes']=='0' and r['assistance']=='none' and r['winner']=='kano' and r['side']=='1' for records in rows.values() for r in records)
    assert rows['MATCH'][0]['ids']=='17,18' and rows['MATCH'][0]['arena']=='0' and len(rows['MATCH'])==1
    hits=rows['DAMAGE'];assert sum(int(r['before'])-int(r['after']) for r in hits)==322 and sum(r['after']=='0' for r in hits)==2
    assert all(r['pc']=='FF836700' and 0<=int(r['after'])<int(r['before'])<=161 for r in hits)
    entry=rows['ACID_UPPERCUT_ENTRY'][0];assert len(rows['ACID_UPPERCUT_ENTRY'])==1
    assert entry['entry']=='FF870DC0' and entry['pc']=='FF870DD0' and entry['id']=='17' and entry['actor']==entry['a8'] and entry['main']==entry['a13']
    command=int(rows['COMMAND'][0]['frame']);assert int(entry['frame'])==command+50
    fields={int(r['age']):r for r in rows['FIELD']};assert len(fields)==len(rows['FIELD']) and all(a in fields for a in range(801))
    for age in range(801):
        row=fields[age];assert int(row['frame'])==int(entry['frame'])+age
        if row['own']!='00000000':assert row['id']=='17'
        if row['victim']!='00000000':assert row['victim_id']=='18'
    assert fields[60]['victim_y']=='-19' and fields[120]['victim_y']=='81'
    assert fields[400]['mode']=='3' and fields[400]['arena']=='1' and fields[400]['own']==fields[400]['victim']=='00000000'
    result=rows['RESULT'][0];assert int(result['frame'])-int(entry['frame'])>=1100
    report=dict(passedObservationChecks=True,sourceSync=source,terminal=terminal,actualNativeUppercutObserved=True,
        uppercutEntry=entry,consecutiveSceneFields=801,ordinaryVictimLandingObserved=True,acidFinisherAccepted=False,
        logSHA256=sync.sha(folder/'run.log'),fullPortAcceptance=False,
        scope='Earned true Kano17/Sonya18 current DeadPool: freshHP before heldlowbuttons enters native uppercut, launches victim then ordinary floor landing and retirement. No acid action/success claim, all roles/raster/audio or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passedObservationChecks=True,nativeUppercut=True,acidFinisherAccepted=False)))

if __name__=='__main__':main()
