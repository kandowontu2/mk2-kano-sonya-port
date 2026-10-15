"""No settling allowance after observed owner retirement; native-only match."""
import copy,json,re
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync
import qualify_bounded_twohuman_hit_voice_state as state

def pcm(folder):
    rows=[];stops=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if line.startswith('MK2_HSPECIAL_PCM '):rows.append(r)
            elif line.startswith('MK2_HSPECIAL_PCM_STOP '):stops.append(r)
    assert len(stops)==1 and int(stops[0]['updates'])==len(rows)
    return rows

def gate(on,off,hit,cleared):
    assert len(on)==len(off)>100
    assert all(Decimal(b['seconds'])-Decimal(a['seconds'])==Decimal('.02') for a,b in zip(on,on[1:]))
    for a,b in zip(on,off):
        assert all(a[k]==b[k] for k in ('frame','seconds','bytes','writes','assistance','raw_media'))
        assert a['writes']=='0' and a['assistance']=='none' and a['raw_media']=='none' and int(a['bytes'])>0 and int(a['bytes'])%4==0
    before=[(a,b) for a,b in zip(on,off) if Decimal(a['seconds'])<hit]
    after=[(a,b) for a,b in zip(on,off) if Decimal(a['seconds'])>cleared]
    assert any(a['sha256']!=b['sha256'] for a,b in before)
    assert len(after)>100 and all(a==b for a,b in after)
    assert 0<Decimal(after[0][0]['seconds'])-cleared<Decimal('.02')
    assert Decimal(after[-1][0]['seconds'])>hit+Decimal('1.5')
    return dict(updates=len(on),postCleanupIdenticalUpdates=len(after),firstNativeOnlyUpdateSeconds=after[0][0]['seconds'],lastObservedSeconds=after[-1][0]['seconds'],settlingAllowanceSeconds=0)

def main():
    base=sync.ROOT/'audit_bounded_twohuman_hit_voice_state_runtime'
    proof=json.loads((base/'voice_state_check.json').read_text());assert proof['passed']
    assert sync.sha(base/'run.log')==proof['pins'][str(base/'run.log')]
    _,original=state.load(base);captures=[];terminals=[];pins={}
    for label in ('samples','nosamples'):
        folder=sync.ROOT/f'audit_bounded_twohuman_hit_pcm_{label}_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows,fields=state.load(folder);assert fields==original
        if label=='samples':assert state.gate(rows,66523)['stoppedCrySample']==3174
        captures.append(pcm(folder));terminals.append(t);pins[str(folder/'run.log')]=sync.sha(folder/'run.log')
    hit=Decimal(proof['hitSeconds']);cleared=Decimal(proof['firstClearedOwnerSeconds'])
    on,off=captures;positive=gate(on,off,hit,cleared);faults=[]
    bad=copy.deepcopy(off);next(r for r in bad if Decimal(r['seconds'])>cleared)['sha256']='0'*64
    try:gate(on,bad,hit,cleared)
    except AssertionError:faults.append('first_post_cleanup_difference')
    else:raise AssertionError('Lingering output fault accepted')
    try:gate(off,off,hit,cleared)
    except AssertionError:faults.append('missing_positive_voice_contribution')
    else:raise AssertionError('Absent voice fault accepted')
    out=sync.ROOT/'audit_bounded_twohuman_hit_pcm_checked';assert not out.exists()
    report=dict(passed=True,**positive,unchangedPhysicalInputsAndActorFields=True,rejectedFaults=faults,
        terminals=terminals,logPins=pins,sourceSync=sync.verify(),heardQualityAccepted=False,
        intraUpdateSampleBoundaryAccepted=False,fullGoalComplete=False,checkerSHA256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,**positive)))

if __name__=='__main__':main()
