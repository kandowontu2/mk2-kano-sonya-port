"""Real cross-added throw dispatch/damage/recovery; no visual acceptance."""
import json,re,struct
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace

def main():
    out=sync.ROOT/'audit_bounded_cross_added_ground_throws_checked';assert not out.exists()
    payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes()
    results={}
    for fighter,attacker,victim,root in (('sonya',18,17,0xff000000),('kano',17,18,0xff020000)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_cross_added_ground_throw_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,_=trace(folder)
        assert len(fields)==480 and len(hits)==1
        for r in fields:
            assert r['id']==r['roster']==str(attacker if r['slot']=='1' else victim)
            assert r['owner']==r['actor'] and r['state']=='1' and r['writes']=='0'
        hit=hits[0]
        assert hit['slot']=='2' and hit['before']=='161' and hit['after']=='129'
        assert hit['pc']=='FF836700' and hit['mask']=='FFFF'
        rows=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                if '_THROW_DISPATCH ' in line:rows.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        assert len(rows)==3 and len({r['frame'] for r in rows})==1
        for r,(entry,pc,op) in zip(rows,(('FF8B6E30','FF8B6E40','C080'),
                ('FFFE1140','FFFE1150','0D5F'),('FF8B6E80','FF8B6E90','4D2B'))):
            assert (r['entry'],r['pc'],r['op'])==(entry,pc,op)
            assert r['id1']==str(attacker) and r['id2']==str(victim)
            assert r['a8']==r['actor1'] and r['a13']==r['main1'] and r['a10']==r['actor2']
        sequence=struct.unpack_from('<I',payload,(root-0xfe800000)//8+43*4)[0]
        assert int(rows[0]['a9'],16)==attacker and int(rows[1]['a9'],16)==43
        assert int(rows[2]['a0'],16)==root and int(rows[2]['a9'],16)==sequence
        for slot,hp in (('1','161'),('2','129')):
            actorrows=[r for r in fields if r['slot']==slot]
            assert len(actorrows)==240 and len({r['floor'] for r in actorrows})==1
            assert all(r['hp']==hp and r['y']==r['floor'] and r['action']=='771'
                and all(int(r[k],16)==0 for k in ('vx','vy','gravity')) for r in actorrows[-20:])
        results[fighter]=dict(attackerID=attacker,victimID=victim,nativeVictimAnimation=43,
            victimRoot=f'{root:08X}',victimSequence=f'{sequence:08X}',damage=32,
            finalGroundedFieldsPerActor=20,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
                fullThrowVisualsAccepted=False,allThrowContextsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
