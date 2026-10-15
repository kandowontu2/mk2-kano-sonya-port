"""Matched native idle ownership/source geometry for Kano against stock Kitana."""
import json,re,struct
from pathlib import Path
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify

def main():
    root=sync.ROOT;case=root/'audit_bounded_twohuman_kano_kitana_idle_opaque_runtime'
    terminal=json.loads((case/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
    log=(case/'run.log').read_text();assert '[LUA ERROR]' not in log and '_FAILED ' not in log
    assert 'pending=0' in log and 'IDLE_TERMINAL frame=1424' in log
    fields=[];queued=[];drawn=[];poses={17:set(),4:set()};endpoints={}
    for line in log.splitlines():
        r=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if '_INPUT ' in line:assert int(r['frame'])<1304
        if '_FIELD ' in line:
            assert r['id']=={'1':'17','2':'4'}[r['slot']] and r['roster']==r['id']
            assert r['state']=='1' and r['actor']==r['owner'] and r['y']==r['floor'] and r['hp']=='161'
            assert all(int(r[k],16)==0 for k in ('vx','vy','gravity','trail'))
            assert int(r['flags'],16)&0x1c==0 and int(r['body'],16)&0x0c==0
            fields.append(r);poses[int(r['id'])].add(r['pose'])
        if '_IDLE_FIFO ' in line:queued.append(r)
        if '_IDLE_OPAQUE ' in line:drawn.append(r)
    assert len(fields)==240 and len({(r['frame'],r['slot']) for r in fields})==240
    assert len(queued)==len(drawn)==60
    payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes();stock=(root/'mk2/mk2-maincpu.bin').read_bytes()
    roots={17:0xff000000,4:struct.unpack_from('<I',stock,0x020c2a+4*4)[0]}
    census={str(i):classify(payload if i==17 else stock,0xfe800000 if i==17 else 0xff800000,roots[i],sorted(poses[i])) for i in poses}
    for i,entries in census.items():
        for pose,refs in entries.items():assert 0 in refs and set(refs).issubset({0,62,64}),(i,pose,refs)
    for r in drawn:
        assert 0 in census[r['id']][r['pose']]
        match=[q for q in queued if all(q[k]==r[k] for k in ('frame','slot','id','pose','source'))];assert len(match)==1
        q=match[0];size=int(q['size'],16);xy=int(q['xy'],16)
        assert (size&1023,size>>16&1023,xy&1023,xy>>16&511)==tuple(int(r[k]) for k in ('width','height','x','y'))
        assert int(q['command'],16)>>16==int(r['command'],16)
        assert int(r['opaque'])>0 and int(r['endpoint'])==(int(r['y'])+int(r['bottom']))&511
        assert r['scaleX']==r['scaleY']=='256'
        key=(int(r['frame']),int(r['slot']));endpoints[key]=max(endpoints.get(key,-1),int(r['endpoint']))
    differences=[endpoints[(f,1)]-endpoints[(f,2)] for f in sorted({f for f,s in endpoints})];assert len(differences)==15
    out=root/'audit_bounded_kano_idle_opaque_checked';out.mkdir(exist_ok=False)
    result=dict(passed=True,neutralActorFields=240,actualOwnedCopies=60,stanceReferenceCensus=census,
        kanoMinusKitanaUnclippedEndpoints=differences,finalDisplayedPixelsProven=False,
        standingSoleParityAccepted=False,fullGoalComplete=False,sourceSync=sync.verify(),terminal=terminal,
        logSha=sync.sha(case/'run.log'),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,kanoMinusKitanaUnclippedEndpoints=differences)))

if __name__=='__main__':main()
