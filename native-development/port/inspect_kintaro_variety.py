"""Check actual queue-based decisions and sampled activations, never infer wins."""
import csv
import json
import subprocess
import sys
from collections import Counter
from itertools import zip_longest
from inspect_normal_runtime import BASE, PORT, sha
from refresh_special_videos import FLAGS
from kintaro_variety_policy import next_move, air_attack_age

MOVES={'mixkick':0x200,'mixpunch':0x201,'readyknife':0x211}


def compare_prefix(reference,observed,before_frame):
    count=0
    for old,new in zip_longest(reference,observed):
        if new is not None and int(new['frame'])>=before_frame:
            return dict(matches=True,rowsCompared=count,beforeFrame=before_frame)
        if old!=new:
            return dict(matches=False,rowsCompared=count,beforeFrame=before_frame,
                        firstMismatchFrame=int(new['frame']) if new else None)
        count+=1
    raise AssertionError('Neither trace reached the requested comparison boundary')


def reactive_attack_ages(rows):
    states={}
    for row in rows:
        request=int(row['requestFrame']);age=int(row['age'])
        state=states.setdefault(request,dict(age=0,attack=None,plan=row['plan']))
        assert row['plan']==state['plan'] and age==state['age']+1
        assert int(row['frame'])==request+age and row['windup'] in ('0','1')
        if state['attack'] is None and ((age>=6 and row['windup']=='1') or age>=28):state['attack']=age
        assert int(row['attackAt'])==(state['attack'] if state['attack'] is not None else -1)
        pressed=state['attack'] is not None and state['attack']<=age<=state['attack']+3
        assert row['hk']==('1' if pressed and row['plan']=='mixkick' else '0')
        assert row['hp']==('1' if pressed and row['plan']=='mixpunch' else '0')
        state['age']=age
    return {frame:state['attack'] for frame,state in states.items()}


def retreat_summary(rows):
    """Count contiguous logged retreat fields; gaps are not assumed observed."""
    longest=length=total=0
    previous=None
    for row in rows:
        frame=int(row['frame'])
        assert previous is None or frame>previous, 'Nonmonotonic decision trace'
        if row['decision']=='retreat':
            length=length+1 if previous==frame-1 else 1
            total+=1
            longest=max(longest,length)
        else: length=0
        previous=frame
    return dict(observedRetreatFields=total,longestContiguousRetreatFields=longest)


def validate_decision(row,finishing=False):
    history=[int(value,16) for value in row['history'].split(':')]
    assert len(history)==6
    assert int(row['kicks'])==history.count(0x200)
    assert int(row['punches'])==history.count(0x201)
    if row['decision'] in MOVES:
        assert row['decision']==next_move(history,int(row['enemyHP']) if finishing else None,finishing)
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
    finishing='--campaign-kano-kintaro-varied-finish' in receipt['testArguments']
    requests=[row for row in decisions if validate_decision(row,finishing)]
    assert requests,'No native boss attack request observed'
    adaptive='--campaign-kano-kintaro-varied-adaptive' in receipt['testArguments']
    reactive='--campaign-kano-kintaro-varied-reactive' in receipt['testArguments']
    timing={}
    if reactive:
        with (run/'kintaro_air_timing.csv').open() as stream:timing=reactive_attack_ages(csv.DictReader(stream))
    for row in requests:
        if row['decision']!='readyknife':
            expected=air_attack_age(int(row['distance'])) if adaptive else 28
            assert int(row.get('airAttackAge',28))==expected
    with (run/'campaign.csv').open() as stream:rows=list(csv.DictReader(stream))
    index={int(row['frame']):row for row in rows}
    observed=[]
    for number,request in enumerate(requests):
        frame=int(request['frame']);kind=request['decision']
        attack_age=int(request.get('airAttackAge',28))
        if reactive and kind!='readyknife':
            assert frame in timing
            attack_age=timing[frame]
            if attack_age is None:
                observed.append(dict(requestFrame=frame,requestedPlan=kind,nativeAction=MOVES[kind],sampledEntryFrame=None))
                continue
        earliest=frame+(12 if kind=='readyknife' else max(0,attack_age-4))
        latest=min(frame+40,int(requests[number+1]['frame'])-1 if number+1<len(requests) else frame+40)
        entry=next((f for f in range(earliest,latest+1) if f in index and index[f]['mode']=='2' and
            index[f]['p1char']=='17' and index[f]['p2char']=='12' and int(index[f]['p1action'])==MOVES[kind]),None)
        observed.append(dict(requestFrame=frame,requestedPlan=kind,nativeAction=MOVES[kind],sampledEntryFrame=entry))
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    rounds=[r for r in audit['rounds'] if r['opponent']==12]
    wins=[r for r in audit['nativeWinningRounds'] if r['opponent']==12]
    overrides=[dict(frame=int(r['frame']),enemyHP=int(r['enemyHP'])) for r in requests
        if finishing and r['decision']!=next_move([int(v,16) for v in r['history'].split(':')])]
    prefix=None
    if overrides:
        with (BASE/'stock_wolf_2219_kano_kintaro_varied/campaign.csv').open() as reference,(run/'campaign.csv').open() as current:
            prefix=compare_prefix(csv.DictReader(reference),csv.DictReader(current),overrides[0]['frame'])
    report=dict(scope='Finite read-only six-hit queue decisions and sampled native activations; not attributed damage',
        requests=dict(Counter(r['decision'] for r in requests)),
        observedActivations=dict(Counter(r['requestedPlan'] for r in observed if r['sampledEntryFrame'] is not None)),
        cases=observed,allLoggedQueueCountsAndRequestsValidated=True,
        bossRounds=len(rounds),bestObservedBossHP=min(r['minimumCPUHP'] for r in rounds),
        nativeKintaroRoundWins=wins,retreat=retreat_summary(decisions),fullPortVerified=False,
        reactiveAttackAges=dict(Counter(age for age in timing.values() if age is not None)),
        lowHPFinishingKickOverrides=overrides,originalVarietyPrefixComparison=prefix,
        pins={str(p):sha(p) for p in (run/'execution.json',run/'autoboot.lua',run/'campaign.csv',run/'kintaro_variety.csv',
            *((run/'kintaro_air_timing.csv',) if reactive else ()))})
    (run/'KINTARO_VARIETY_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Requested',report['requests'],'observed',report['observedActivations'],'native round wins',len(wins))


if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
