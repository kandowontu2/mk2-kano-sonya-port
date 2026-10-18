"""Observe buy-in-to-selection latency, not raw coin/start pin transitions."""
import csv
import json
import sys
from inspect_normal_runtime import BASE, sha


def transitions(rows):
    pending=None
    result=[]
    for row in rows:
        if row['phase']=='buyin':
            pending=row
        elif row['phase']=='selection' and pending:
            assert (row['attempt'],row['map'])==(pending['attempt'],pending['map'])
            elapsed=int(row['frame'])-int(pending['frame'])
            assert elapsed>0
            result.append(dict(attempt=int(row['attempt']),map=int(row['map']),
                               buyinFrame=int(pending['frame']),selectionLatency=elapsed))
            pending=None
    return result


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name
    execution=json.loads((run/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut']
    assert '--campaign-boss-continue-delay=60' in execution['testArguments']
    path=run/'campaign_continues.csv'
    with path.open() as stream:observed=transitions(csv.DictReader(stream))
    baseline=BASE/'stock_wolf_2219_kano_kintaro_varied_finish_uppercut13/campaign_continues.csv'
    with baseline.open() as stream:reference=transitions(csv.DictReader(stream))
    assert reference and all(r['selectionLatency']==141 for r in reference)
    assert observed and all(r['selectionLatency']==(201 if r['map']>=15 else 141) for r in observed)
    assert any(r['map']>=15 for r in observed),'Boss delay not exercised'
    report=dict(scope='Native buy-in/selection event latency; not direct raw-input trace or win proof',
        transitions=observed,originalLatency=141,bossLatency=201,fullPortVerified=False,
        pins={str(p):sha(p) for p in (path,baseline,run/'execution.json',run/'autoboot.lua')})
    (run/'BOSS_BUYIN_DELAY_OBSERVATIONS.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Observed',len(observed),'purchases; human latency141/boss201, not campaign acceptance')


if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
