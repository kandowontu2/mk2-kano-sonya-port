"""Actual true-ID native throw router and victim-owned animation selection."""
import copy,json,re,struct
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace

def gate(rows,ident,victimroot,victimsequence):
    assert len(rows)==3
    for r,(entry,pc,op) in zip(rows,(
        ('FF8B6E30','FF8B6E40','C080'),('FFFE1140','FFFE1150','0D5F'),
        ('FF8B6E80','FF8B6E90','4D2B'))):
        assert (r['entry'],r['pc'],r['op'])==(entry,pc,op) and r['frame']=='1418'
        assert r['id1']==str(ident) and r['id2']=='4'
        assert r['a8']==r['actor1'] and r['a13']==r['main1'] and r['a10']==r['actor2']
    assert int(rows[0]['a9'],16)==ident
    assert int(rows[1]['a9'],16)==43
    assert int(rows[2]['a0'],16)==victimroot and int(rows[2]['a9'],16)==victimsequence

def main():
    out=sync.ROOT/'audit_bounded_ground_throw_dispatch_checked';assert not out.exists()
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    victimroot=struct.unpack_from('<I',stock,0x020c2a+4*4)[0]
    victimsequence=struct.unpack_from('<I',stock,(victimroot-0xff800000)//8+43*4)[0]
    results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_ground_throw_dispatch_runtime'
        baseline=sync.ROOT/f'audit_bounded_{fighter}_added_ground_throw_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,_=trace(folder);oldfields,oldhits,_=trace(baseline)
        assert fields==oldfields and hits==oldhits and len(fields)==480 and len(hits)==1
        assert hits[0]['slot']=='2' and hits[0]['before']=='161' and hits[0]['after']=='129'
        rows=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                if '_THROW_DISPATCH ' in line:rows.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        gate(rows,ident,victimroot,victimsequence)
        faults=[]
        for index,key,value in ((0,'a9','00000001'),(1,'a9','0000003B'),
                                (2,'a0','FF000000'),(1,'a8','00000000')):
            bad=copy.deepcopy(rows);bad[index][key]=value
            try:gate(bad,ident,victimroot,victimsequence)
            except AssertionError:faults.append(key+str(index))
            else:raise AssertionError('Fault accepted')
        results[fighter]=dict(actualNativeThrowRouter=True,trueAttackerID=ident,
            victimID=4,victimAnimation=43,victimRoot=f'{victimroot:08X}',
            victimSequence=f'{victimsequence:08X}',damage=32,
            identicalObservedGameplay=True,rejectedFaults=faults,
            terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),
        checkerSha256=sync.sha(Path(__file__)),fullThrowArtAccepted=False,
        allThrowContextsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
