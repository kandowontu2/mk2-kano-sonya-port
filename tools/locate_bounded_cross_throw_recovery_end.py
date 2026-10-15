"""Derive actual paired throw entry through persistent native idle recovery."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify
from qualify_bounded_sweep_presentation import trace

def main():
    out=sync.ROOT/'audit_bounded_cross_throw_recovery_end';assert not out.exists()
    payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes();results={}
    prior=sync.ROOT/'audit_bounded_cross_added_ground_throws_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed']
    for fighter in ('sonya','kano'):
        folder=sync.ROOT/f'audit_bounded_{fighter}_cross_added_ground_throw_runtime'
        assert sync.sha(folder/'run.log')==proof['results'][fighter]['logSha256']
        fields,hits,_=trace(folder);assert len(fields)==480 and len(hits)==1
        ready=min(int(r['frame']) for r in fields);strike=int(hits[0]['frame'])
        censuses={}
        for ident,root in ((17,0xff000000),(18,0xff020000)):
            censuses[str(ident)]=classify(payload,0xfe800000,root,
                sorted({r['pose'] for r in fields if r['id']==str(ident)}))
        nonidle=[]
        for r in fields:
            frame=int(r['frame'])
            if frame<strike:continue
            refs=censuses[r['id']][r['pose']]
            idle=(0 in refs and r['y']==r['floor'] and r['action']=='771'
                and all(int(r[k],16)==0 for k in ('vx','vy','gravity','trail'))
                and int(r['flags'],16)&0x1c==0 and int(r['body'],16)&0x0c==0)
            if not idle:nonidle.append(frame)
        assert nonidle
        recovered=max(nonidle)+1
        assert max(int(r['frame']) for r in fields)-recovered>=20
        entries=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                if '_THROW_DISPATCH ' in line:
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if r['entry']=='FF8B6E30':entries.append(int(r['frame']))
        assert len(entries)==1 and entries[0]<strike<recovered
        results[fighter]=dict(readyFrame=ready,nativeThrowEntryAge=entries[0]-ready,
            actualDamageAge=strike-ready,lastNonIdleAge=recovered-ready-1,
            firstPersistentPairedIdleAge=recovered-ready,
            finalStableFields=max(int(r['frame']) for r in fields)-recovered+1,
            logSha256=sync.sha(folder/'run.log'))
    out.mkdir();(out/'report.json').write_text(json.dumps(dict(passed=True,results=results,
        sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        fullRenderedRecoveryAccepted=False,fullGoalComplete=False),indent=2)+'\n')
    print(json.dumps(results))

if __name__=='__main__':main()
