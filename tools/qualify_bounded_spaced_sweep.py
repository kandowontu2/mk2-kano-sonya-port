"""Finite native sweep contact, true-ID fall and recovery."""
import json,re,struct
from pathlib import Path
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify

def main():
    out=sync.ROOT/'audit_bounded_spaced_sweep_checked';assert not out.exists()
    payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes()
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    stockroot=struct.unpack_from('<I',stock,0x020c2a+4*4)[0]
    results={}
    for fighter,ident,root in (('sonya',18,0xff020000),('kano',17,0xff000000)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_spaced_sweep_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        own=[];stockrows=[];hits=[];ended=False
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line and '_FAILED ' not in line
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if '_FIELD ' in line:
                    assert r['id']==r['roster']==(str(ident) if r['slot']=='1' else '4')
                    assert r['owner']==r['actor'] and r['state']=='1' and r['writes']=='0'
                    (own if r['slot']=='1' else stockrows).append(r)
                elif '_CONTACT_HEALTH ' in line:hits.append(r)
                elif '_IDLE_TERMINAL ' in line:ended=r['fields']=='240'
        assert ended and len(own)==len(stockrows)==240 and len(hits)==1
        hit=hits[0]
        assert hit['frame']=='1430' and hit['slot']=='1' and hit['before']=='161' and hit['after']=='141'
        assert hit['pc']=='FF836700' and hit['mask']=='FFFF'
        assert all(r['hp']=='161' for r in stockrows)
        assert len({r['floor'] for r in own})==1
        assert all(r['hp']=='141' and r['y']==r['floor'] and r['action']=='771'
            and all(int(r[k],16)==0 for k in ('vx','vy','gravity')) for r in own[-20:])
        census=classify(payload,0xfe800000,root,sorted({r['pose'] for r in own}))
        stockcensus=classify(stock,0xff800000,stockroot,sorted({r['pose'] for r in stockrows}))
        animations=sorted({a for refs in census.values() for a in refs})
        stockanimations=sorted({a for refs in stockcensus.values() for a in refs})
        assert {22,23}.issubset(animations),animations
        assert 21 in stockanimations and 33 not in stockanimations,stockanimations
        results[fighter]=dict(damage=20,addedAnimationReferences=animations,
            stockAnimationReferences=stockanimations,finalGroundedRecoveryFields=20,
            unchangedFloor=int(own[0]['floor']),terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),
        checkerSha256=sync.sha(Path(__file__)),fullRenderedArtAccepted=False,
        allReactionContextsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
