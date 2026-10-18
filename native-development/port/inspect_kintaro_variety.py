"""Check actual queue-based decisions and sampled activations, never infer wins."""
import csv
import json
import subprocess
import sys
from collections import Counter
from inspect_normal_runtime import BASE, PORT, sha
from refresh_special_videos import FLAGS
from kintaro_variety_policy import next_move

MOVES={'mixkick':0x200,'mixpunch':0x201,'readyknife':0x211}


def validate_decision(row):
    history=[int(value,16) for value in row['history'].split(':')]
    assert len(history)==6
    assert int(row['kicks'])==history.count(0x200)
    assert int(row['punches'])==history.count(0x201)
    if row['decision'] in MOVES:
        assert row['decision']==next_move(history)
        assert int(row['ownAction'])==0x303 and int(row['ownFlags'])&0x1c==0
        assert row['ownHeight']=='0' and int(row['ownHP'])>0
        return True
    return False


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    assert '--campaign-kano-kintaro-varied' in receipt['testArguments']
    subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),name],check=True,
                   stdout=subprocess.DEVNULL,creationflags=FLAGS)
    with (run/'kintaro_variety.csv').open() as stream:
        decisions=list(csv.DictReader(stream))
    requests=[row for row in decisions if validate_decision(row)]
    assert requests,'No native boss attack request observed'
    with (run/'campaign.csv').open() as stream:rows=list(csv.DictReader(stream))
    index={int(row['frame']):row for row in rows}
    observed=[]
    for number,request in enumerate(requests):
        frame=int(request['frame']);kind=request['decision']
        earliest=frame+(12 if kind=='readyknife' else 24)
        latest=min(frame+40,int(requests[number+1]['frame'])-1 if number+1<len(requests) else frame+40)
        entry=next((f for f in range(earliest,latest+1) if f in index and index[f]['mode']=='2' and
            index[f]['p1char']=='17' and index[f]['p2char']=='12' and int(index[f]['p1action'])==MOVES[kind]),None)
        observed.append(dict(requestFrame=frame,requestedPlan=kind,nativeAction=MOVES[kind],sampledEntryFrame=entry))
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    rounds=[r for r in audit['rounds'] if r['opponent']==12]
    wins=[r for r in audit['nativeWinningRounds'] if r['opponent']==12]
    report=dict(scope='Finite read-only six-hit queue decisions and sampled native activations; not attributed damage',
        requests=dict(Counter(r['decision'] for r in requests)),
        observedActivations=dict(Counter(r['requestedPlan'] for r in observed if r['sampledEntryFrame'] is not None)),
        cases=observed,allLoggedQueueCountsAndRequestsValidated=True,
        bossRounds=len(rounds),bestObservedBossHP=min(r['minimumCPUHP'] for r in rounds),
        nativeKintaroRoundWins=wins,fullPortVerified=False,
        pins={str(p):sha(p) for p in (run/'execution.json',run/'autoboot.lua',run/'campaign.csv',run/'kintaro_variety.csv')})
    (run/'KINTARO_VARIETY_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Requested',report['requests'],'observed',report['observedActivations'],'native round wins',len(wins))


if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
