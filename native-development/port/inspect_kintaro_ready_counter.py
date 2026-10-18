"""Finite controller readiness/activation audit; requests and damage are not wins."""
import csv
import json
import subprocess
import sys
from inspect_normal_runtime import BASE,sha
from refresh_special_videos import PORT,FLAGS

def ready_request(row,maximum_distance=115):
    assert maximum_distance in (84,104,115)
    return (row['phase']=='fire' and row['hp']=='1' and int(row['ownHP'])>0 and
            int(row['ownHeight'])==0 and int(row['enemyHeight'])==0 and
            int(row['ownFlags'])&0x1c==0 and int(row['bodyHeight'])<=96 and
            int(row['distance'])<=maximum_distance and row['buttonTable']==row['duckTable'])

def ready_recovery_request(row):
    return ready_request(row,104) and row['enemyRecovery']=='1'

def ready_finishing_request(row,threshold=20):
    assert threshold in (13,20)
    return ready_request(row,104) and 0<int(row['enemyHP'])<=threshold

def valid_recovery_approach(row):
    return (row['phase']=='approach' and row['enemyRecovery']=='1' and
        104<int(row['distance'])<=180 and row['ownHeight']==row['enemyHeight']=='0' and
        int(row['ownFlags'])&0x1c==0 and int(row['ownHP'])>0 and
        row['toward']=='1' and row['down']==row['block']=='0')

def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    hybrid='--campaign-kano-kintaro-varied-counter' in receipt['testArguments']
    recovery='--campaign-kano-kintaro-recovery-counter' in receipt['testArguments']
    finishing='--campaign-kano-kintaro-varied-finish-uppercut' in receipt['testArguments']
    assert '--campaign-kano-kintaro-ready-counter' in receipt['testArguments'] or hybrid or recovery or finishing
    maximum=int(next((arg.split('=',1)[1] for arg in receipt['testArguments']
        if arg.startswith('--campaign-kano-kintaro-ready-range=')),'104' if hybrid or recovery or finishing else '115'))
    subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),name],check=True,
                   stdout=subprocess.DEVNULL,creationflags=FLAGS)
    log=(run/'mame.log').read_text();assert 'Fatal error:' not in log and '[LUA ERROR]' not in log
    request_file=run/('kintaro_recovery_counter.csv' if recovery else 'kintaro_ready_counter.csv')
    with request_file.open() as stream:requests=list(csv.DictReader(stream))
    fired=[r for r in requests if r['phase']=='fire']
    assert fired and all(ready_request(r,maximum) for r in fired)
    if recovery:assert all(ready_recovery_request(r) for r in fired)
    threshold=int(next((arg.split('=',1)[1] for arg in receipt['testArguments'] if
        arg.startswith('--campaign-finish-uppercut-threshold=')),'20'))
    if finishing:assert all(ready_finishing_request(r,threshold) for r in fired)
    approaches=[r for r in requests if r['phase']=='approach']
    if approaches:
        assert recovery and '--campaign-kano-kintaro-recovery-approach' in receipt['testArguments']
        assert all(valid_recovery_approach(r) for r in approaches)
    assert all(int(b['frame'])-int(a['frame'])>=6 for a,b in zip(fired,fired[1:]))
    with (run/'campaign.csv').open() as stream:campaign=list(csv.DictReader(stream))
    index={int(r['frame']):r for r in campaign}
    activations=[];missed=[]
    for request in fired:
        frame=int(request['frame'])
        entry=next((f for f in range(frame,frame+9) if f in index and index[f]['mode']=='2' and
                    index[f]['p1char']=='17' and index[f]['p2char']=='12' and index[f]['p1action']=='263'),None)
        if entry is None:missed.append(frame)
        else:activations.append(entry)
    activations=sorted(set(activations));drops=[]
    for before,after in zip(campaign,campaign[1:]):
        if before['mode']!=after['mode'] or after['mode']!='2':continue
        if before['p2char']!=after['p2char'] or after['p2char']!='12':continue
        if (before['attempt'],before['round'])!=(after['attempt'],after['round']):continue
        delta=int(before['p2hp'])-int(after['p2hp']);frame=int(after['frame'])
        if delta>0 and any(entry<=frame<=entry+8 for entry in activations):drops.append(dict(frame=frame,damage=delta))
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    wins=[r for r in audit['nativeWinningRounds'] if r['opponent']==12]
    report=dict(scope='Observed ready requests, sampled native entries and linked damage windows; only native counters prove wins',
        requests=len(fired),requestDistanceLimit=maximum,allRequestReadinessChecksPassed=True,nativeUppercutEntriesWithin8Fields=len(activations),
        requestsWithoutObservedEntry=missed,linkedDamageWindows=drops,nativeKintaroRoundWins=wins,
        validatedApproachFields=len(approaches),fullPortVerified=False,pins={str(p):sha(p) for p in
            (run/'execution.json',run/'autoboot.lua',run/'campaign.csv',request_file)})
    (run/'KINTARO_READY_COUNTER_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Ready requests',len(fired),'native uppercuts',len(activations),'linked damage windows',len(drops),'native round wins',len(wins))

if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
