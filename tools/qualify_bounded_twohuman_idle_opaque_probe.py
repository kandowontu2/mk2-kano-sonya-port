"""Actual neutral DMA source bounds, explicitly not final scanout pixels."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;case=root/'audit_bounded_twohuman_sonya_kitana_idle_opaque_runtime'
    terminal=json.loads((case/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    log=(case/'run.log').read_text();assert '[LUA ERROR]' not in log and '_FAILED ' not in log
    assert 'pending=0' in log and 'IDLE_TERMINAL frame=1424' in log
    stance=json.loads((root/'audit_bounded_twohuman_idle_checked/report.json').read_text())['stanceReferenceCensus']
    queued=[];drawn=[];endpoints={}
    for line in log.splitlines():
        r=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if '_IDLE_FIFO ' in line:queued.append(r)
        if '_IDLE_OPAQUE ' not in line:continue
        assert r['id']=={'1':'18','2':'4'}[r['slot']]
        assert 0 in stance[r['id']][r['pose']]
        assert int(r['opaque'])>0 and int(r['endpoint'])==(int(r['y'])+int(r['bottom']))&511
        assert r['scaleX']==r['scaleY']=='256'
        match=[q for q in queued if all(q[k]==r[k] for k in ('frame','slot','id','pose','source'))]
        assert len(match)==1
        q=match[0];size=int(q['size'],16);xy=int(q['xy'],16)
        assert (size&1023,size>>16&1023,xy&1023,xy>>16&511)==tuple(int(r[k]) for k in ('width','height','x','y'))
        assert int(q['command'],16)>>16==int(r['command'],16)
        drawn.append(r);key=(int(r['frame']),int(r['slot']))
        endpoints[key]=max(endpoints.get(key,-1),int(r['endpoint']))
    assert len(queued)==len(drawn)==60
    differences=[endpoints[(f,1)]-endpoints[(f,2)] for f in sorted({f for f,s in endpoints})]
    assert len(differences)==15
    out=root/'audit_bounded_twohuman_idle_opaque_checked';out.mkdir(exist_ok=False)
    result=dict(passed=True,actualOwnedCopies=60,sonyaMinusKitanaUnclippedEndpoints=differences,
        finalDisplayedPixelsProven=False,standingSoleParityAccepted=False,fullGoalComplete=False,
        sourceSync=sync.verify(),terminal=terminal,logSha=sync.sha(case/'run.log'),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(copies=60,sonyaMinusKitanaUnclippedEndpoints=differences)))

if __name__=='__main__':main()
