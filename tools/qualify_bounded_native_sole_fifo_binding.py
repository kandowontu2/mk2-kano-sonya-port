"""Bind every sparse body DMA to event-time FIFO, not later animated cache."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync
ROOT=sync.ROOT
BASE=ROOT/'audit_bounded_native_sole_fifo_runtime'
RX=re.compile(r'(\w+)=([^\s]+)')
def gate(data):
    queues=data['MK2_BOUNDED_SOLE_FIFO']
    draws=data['MK2_BOUNDED_SOLE_DMA']+data['MK2_BOUNDED_SOLE_UNMATCHED']
    def qkey(r):
        size=int(r['size'],16);xy=int(r['xy'],16)
        return (r['frame'],r['slot'],r['id'],r['source'],size&0x3ff,(size>>16)&0x3ff,
            (int(r['command'],16)>>16)&0xffff,xy&0x3ff,(xy>>16)&0x1ff)
    def dkey(r):
        return (r['frame'],r['slot'],r['id'],r['source'],int(r['width']),int(r['height']),
            int(r['command'],16),int(r['x']),int(r['y']))
    assert queues and len(queues)==len(draws)
    assert len({qkey(r) for r in queues})==len(queues)
    assert sorted(qkey(r) for r in queues)==sorted(dkey(r) for r in draws)
    assert all(r['pc']=='FF804420' and r['id']==('17' if r['slot']=='1' else '18') for r in queues)
    legs=[r for r in queues if r['frame']=='1898' and r['slot']=='2']
    assert [r['source'] for r in legs]==['1055E5DA','105527C8','1055410E']
    assert all(r['pose']=='FF02DFA0' for r in legs)
    later=[r for r in data['MK2_BOUNDED_STANCE_PART'] if r['frame']=='1898' and r['slot']=='2']
    assert [r['source'] for r in later]==['1055E5DA','105557FE']
    assert all(r['pose']=='FF02E020' for r in later)
    assert all(r['actor']=='010350A0' and r['main']=='0106BF30' for r in legs+later)
    return dict(allObservedBodyCopiesBound=len(draws),previouslyUnmatchedLegCopiesBound=2,
        actualQueuedPose='FF02DFA0',actualLaterCachePose='FF02E020',
        physicalActorAndMainUnchanged=True)
def main():
    out=BASE/'fifo_binding_check.json';assert not out.exists()
    terminal=json.loads((BASE/'terminal.json').read_text());assert terminal['exitCode']==0 and not terminal['limitReason']
    data={k:[] for k in ('MK2_BOUNDED_SOLE_FIFO','MK2_BOUNDED_SOLE_DMA','MK2_BOUNDED_SOLE_UNMATCHED','MK2_BOUNDED_STANCE_PART')}
    with (BASE/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            tag=line.split(' ',1)[0].strip()
            if tag in data:data[tag].append(dict(RX.findall(line)));assert len(data[tag])<200
    positive=gate(data);faults=[]
    for key,value in (('source','105527CA'),('size','0055001C'),('xy','008E0127'),('pose','FF02E020'),('id','17')):
        bad=copy.deepcopy(data)
        next(r for r in bad['MK2_BOUNDED_SOLE_FIFO'] if r['source']=='105527C8')[key]=value
        try:gate(bad)
        except AssertionError:faults.append(key)
        else:raise AssertionError('FIFO fault admitted '+key)
    assert gate(data)==positive
    result=dict(passed=True,nativeExit=0,peakWorkingSetBytes=terminal['peakWorkingSetBytes'],
        actualFIFOBodyBinding=positive,rejectedFaults=faults,
        graphicalStandingSoleParityAccepted=False,fullGoalComplete=False,
        limitation='FIFO A6 is scale, not the effective palette; do not interpret legacy palette label as bank provenance',
        sourceSync=sync.verify(),logSha256=sync.sha(BASE/'run.log'),checkerSha256=sync.sha(Path(__file__)))
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,binding=positive,rejectedFaults=faults)))
if __name__=='__main__':main()
