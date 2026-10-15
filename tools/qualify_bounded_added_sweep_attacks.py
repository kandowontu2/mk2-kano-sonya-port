"""Actual added sweep activation, damage and native stock victim recovery."""
import json,struct
from pathlib import Path
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify
from qualify_bounded_sweep_presentation import trace

def main():
    out=sync.ROOT/'audit_bounded_added_sweep_attacks_checked';assert not out.exists()
    payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes()
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    stockroot=struct.unpack_from('<I',stock,0x020c2a+4*4)[0]
    results={}
    for fighter,ident,root in (('sonya',18,0xff020000),('kano',17,0xff000000)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_added_sweep_attack_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,_=trace(folder)
        assert len(fields)==480 and len(hits)==1
        own=[r for r in fields if r['slot']=='1'];victim=[r for r in fields if r['slot']=='2']
        assert len(own)==len(victim)==240
        for r in fields:
            assert r['id']==r['roster']==(str(ident) if r['slot']=='1' else '4')
            assert r['owner']==r['actor'] and r['state']=='1' and r['writes']=='0'
        hit=hits[0]
        assert hit['frame']=='1433' and hit['slot']=='2' and hit['before']=='161' and hit['after']=='141'
        assert hit['pc']=='FF836700' and hit['mask']=='FFFF'
        assert all(r['hp']=='161' for r in own)
        for rows,hp in ((own,'161'),(victim,'141')):
            assert len({r['floor'] for r in rows})==1
            assert all(r['hp']==hp and r['y']==r['floor'] and r['action']=='771'
                and all(int(r[k],16)==0 for k in ('vx','vy','gravity')) for r in rows[-20:])
        census=classify(payload,0xfe800000,root,sorted({r['pose'] for r in own}))
        stockcensus=classify(stock,0xff800000,stockroot,sorted({r['pose'] for r in victim}))
        animations=sorted({a for refs in census.values() for a in refs})
        victimanimations=sorted({a for refs in stockcensus.values() for a in refs})
        assert 21 in animations and 33 not in animations
        assert {22,23}.issubset(victimanimations)
        results[fighter]=dict(realSweepActivation=True,damage=20,
            addedAnimationReferences=animations,stockVictimAnimationReferences=victimanimations,
            finalStationaryGroundedFields=20,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        fullRenderedArtAccepted=False,allMovesContextsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
