"""All published sparse copies accounted; report raw pose-specific differences."""
import collections,copy,json,re
from pathlib import Path
import verify_native_source_sync as sync
ROOT=sync.ROOT
RX=re.compile(r'(\w+)=([^\s]+)')
def key(r,queue=False):
    if queue:
        size=int(r['size'],16);xy=int(r['xy'],16)
        return (r['frame'],r['slot'],r['id'],r['pose'],r['source'],size&0x3ff,size>>16,
            (int(r['command'],16)>>16)&0xffff,xy&0x3ff,(xy>>16)&511)
    return (r['frame'],r['slot'],r['id'],r['pose'],r['source'],int(r['width']),int(r['height']),
        int(r['command'],16),int(r['x']),int(r['y']))
def gate(queues,copies,count):
    assert len(queues)==len(copies)==count
    assert len({key(r) for r in copies})==count
    assert sorted(key(r,True) for r in queues)==sorted(key(r) for r in copies)
    assert all(int(r['opaque'])>0 and int(r['bits'])>0 and
        int(r['unclipped_opaque_bottom_y'])==(int(r['y'])+int(r['bottom']))&511 for r in copies)
    groups=collections.defaultdict(list)
    for r in copies:groups[int(r['frame']),int(r['slot'])].append(r)
    observations=[]
    for frame in sorted({f for f,s in groups}):
        first,second=groups[frame,1],groups[frame,2]
        assert first and second
        a=max(int(r['unclipped_opaque_bottom_y']) for r in first)
        b=max(int(r['unclipped_opaque_bottom_y']) for r in second)
        grounded=all(r['actor_y']==r['floor'] for r in first+second)
        observations.append(dict(frame=frame,ids=[int(first[0]['id']),int(second[0]['id'])],
            poses=[first[0]['pose'],second[0]['pose']],actions=[first[0]['action'],second[0]['action']],
            unclippedOpaqueBottomRows=[a,b],p2MinusP1=b-a,bothPhysicalOriginsGrounded=grounded))
    return observations
def main():
    out=ROOT/'audit_bounded_native_owned_opaque_census_checked';assert not out.exists()
    cases=[];faults=[]
    for boot,count in ((608,30),(604,28)):
        base=ROOT/f'audit_bounded_native_owned_opaque_boot{boot}_runtime'
        terminal=json.loads((base/'terminal.json').read_text());assert terminal['exitCode']==0 and not terminal['limitReason']
        queues=[];copies=[]
        with (base/'run.log').open() as stream:
            for line in stream:
                assert len(line)<1048576 and '[LUA ERROR]' not in line
                if line.startswith('MK2_BOUNDED_SOLE_FIFO '):queues.append(dict(RX.findall(line)))
                elif line.startswith('MK2_BOUNDED_OWNED_OPAQUE '):copies.append(dict(RX.findall(line)))
        positive=gate(queues,copies,count)
        for label,change in (
            ('missing_copy',lambda rows:rows.pop()),
            ('wrong_fifo_owner',lambda rows:rows[0].update(id='18')),
            ('wrong_opaque_endpoint',lambda rows:rows[0].update(unclipped_opaque_bottom_y='0'))):
            bad=copy.deepcopy(copies);change(bad)
            try:gate(queues,bad,count)
            except AssertionError:faults.append(dict(boot=boot,fault=label))
            else:raise AssertionError('Census fault admitted '+label)
        assert gate(queues,copies,count)==positive
        cases.append(dict(boot=boot,terminal=terminal,allPublishedCopiesAccounted=count,
            observations=positive,logSha256=sync.sha(base/'run.log')))
    report=dict(passed=True,cases=cases,rejectedFaults=faults,
        currentStockStandingSoleParityAccepted=False,clipAndScanoutBound=False,
        fullGoalComplete=False,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases=[dict(boot=c['boot'],copies=c['allPublishedCopiesAccounted'],
        groundedDifferences=[r['p2MinusP1'] for r in c['observations'] if r['bothPhysicalOriginsGrounded']]) for c in cases],standingParityAccepted=False)))
if __name__=='__main__':main()
