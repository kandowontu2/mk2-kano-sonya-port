"""Actual attack references identify whether intended sweep occurred."""
import json,re,struct
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify

def main():
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    root=struct.unpack_from('<I',stock,0x020c2a+4*4)[0]
    out=sync.ROOT/'audit_bounded_held_back_sweep_attack_checked'
    assert not out.exists()
    results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_held_back_sweep_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=[];hits=[];own=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line and '_FAILED ' not in line
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if '_FIELD ' in line:
                    assert r['id']==r['roster']==(str(ident) if r['slot']=='1' else '4')
                    assert r['owner']==r['actor'] and r['writes']=='0'
                    (own if r['slot']=='1' else rows).append(r)
                elif '_CONTACT_HEALTH ' in line:hits.append(r)
        assert len(rows)==len(own)==240 and len(hits)==1
        assert hits[0]['before']=='161' and hits[0]['after']=='145' and hits[0]['pc']=='FF836700'
        poses=sorted({r['pose'] for r in rows if 1416<=int(r['frame'])<=1430})
        refs=classify(stock,0xff800000,root,poses)
        animations={a for entries in refs.values() for a in entries}
        assert 33 in animations and 21 not in animations
        assert all(r['y']==r['floor'] and r['hp']=='145' for r in own[-20:])
        results[fighter]=dict(stockAttackReferences=refs,actualCloseKneeNotSweep=True,
                              damage=16,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    out.mkdir();(out/'report.json').write_text(json.dumps(dict(passedAttackIdentification=True,
        results=results,sourceSync=sync.verify(),sweepReactionAccepted=False,fullGoalComplete=False),indent=2)+'\n')
    print(json.dumps(dict(passedAttackIdentification=True,actualAttack='close knee33',sweepOccurred=False)))

if __name__=='__main__':main()
