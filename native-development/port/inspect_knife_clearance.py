"""Finite request-following windows; distances are observed, not guaranteed safe."""
import csv
import json
import sys
from inspect_normal_runtime import BASE, sha


def windows(requests, rows):
    pending=iter(requests)
    upcoming=next(pending,None)
    active=[]
    results=[]
    for row in rows:
        frame=int(row['frame'])
        while upcoming is not None and int(upcoming['frame'])<=frame:
            results.append(dict(requestFrame=int(upcoming['frame']),
                requestGap=int(upcoming['distance']),samples=0,minimumGap=None,
                nativeKnifeSamples=0,minimumKnifeGap=None,firstPlayerHP=None,
                minimumPlayerHP=None))
            active.append(results[-1]);upcoming=next(pending,None)
        active=[w for w in active if frame<=w['requestFrame']+64]
        eligible=row['mode']=='2' and row['p1char']=='17' and row['p2char']=='12'
        if not eligible:
            active=[]
            continue
        for window in active:
            gap=abs(int(row['p1x'])-int(row['p2x']));hp=int(row['p1hp'])
            if window['firstPlayerHP'] is None:
                window['firstPlayerHP']=hp;window['minimumPlayerHP']=hp;window['minimumGap']=gap
            window['samples']+=1
            window['minimumPlayerHP']=min(window['minimumPlayerHP'],hp)
            window['minimumGap']=min(window['minimumGap'],gap)
            if int(row['p1action'])==0x211:
                window['nativeKnifeSamples']+=1
                window['minimumKnifeGap']=gap if window['minimumKnifeGap'] is None else min(window['minimumKnifeGap'],gap)
    return results


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    with (run/'kintaro_variety.csv').open() as source:
        requests=[r for r in csv.DictReader(source) if r['decision']=='readyknife']
    with (run/'campaign.csv').open() as source:
        observed=windows(requests,csv.DictReader(source))
    report=dict(scope='Sampled64-field post-request distances/HP; not causal grab or complete recovery proof',
        windows=observed,requests=len(requests),nativeKnifeObservedWindows=sum(w['nativeKnifeSamples']>0 for w in observed),
        knifeTagInsideNativeGrabRange=sum(w['minimumKnifeGap'] is not None and w['minimumKnifeGap']<=120 for w in observed),
        fullPortVerified=False,pins={str(p):sha(p) for p in
            (run/'execution.json',run/'campaign.csv',run/'kintaro_variety.csv',run/'autoboot.lua')})
    (run/'KNIFE_CLEARANCE_OBSERVATIONS.json').write_text(json.dumps(report,indent=2)+'\n')
    print({k:v for k,v in report.items() if k not in ('windows','pins')})


if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
