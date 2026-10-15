"""Positive voice contribution and complete post-clear output convergence."""
import json,copy
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_twohuman_hit_pcm import pcm
from qualify_bounded_twohuman_hit_voice_state import load

def gate(on,off,hit,clear):
    assert len(on)==len(off)==148
    assert all(Decimal(b['seconds'])-Decimal(a['seconds'])==Decimal('.02') for a,b in zip(on,on[1:]))
    for a,b in zip(on,off):assert all(a[k]==b[k] for k in ('frame','seconds','bytes','writes','assistance','raw_media'))
    before=[(a,b) for a,b in zip(on,off) if Decimal(a['seconds'])<hit]
    after=[(a,b) for a,b in zip(on,off) if Decimal(a['seconds'])-Decimal('.02')>=clear]
    assert any(a['sha256']!=b['sha256'] for a,b in before)
    assert len(after)>100 and all(a==b for a,b in after)
    assert 0<Decimal(after[0][0]['seconds'])-clear<Decimal('.04')
    assert Decimal(after[-1][0]['seconds'])>hit+Decimal('1.5')
    return dict(updates=148,completePostClearIdenticalUpdates=len(after),firstCompleteWindowEndSeconds=after[0][0]['seconds'],lastWindowEndSeconds=after[-1][0]['seconds'],settlingAllowanceSeconds=0)

def main():
    out=sync.ROOT/'audit_bounded_twohuman_square_hit_pcm_checked';assert not out.exists()
    proof_path=sync.ROOT/'audit_bounded_twohuman_square_slot_positions_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed'];results={}
    for side in (1,2):
        base=sync.ROOT/f'audit_bounded_twohuman_square_p{side}_rise_counter_runtime'
        p=proof['results'][f'p{side}'];assert sync.sha(base/'run.log')==p['logSHA256']
        oldrows,oldfields=load(base);oldvoices=[r for tag,r in oldrows if tag in ('MK2_HSPECIAL_VOICE_OWNER','MK2_HSPECIAL_VOICE_CHANNEL')]
        captures=[];terminals=[];pins={}
        for label in ('samples','nosamples'):
            folder=sync.ROOT/f'audit_bounded_twohuman_square_p{side}_pcm_{label}_runtime'
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            rows,fields=load(folder);assert fields==oldfields
            if label=='samples':assert [r for tag,r in rows if tag in ('MK2_HSPECIAL_VOICE_OWNER','MK2_HSPECIAL_VOICE_CHANNEL')]==oldvoices
            captures.append(pcm(folder));terminals.append(t);pins[str(folder/'run.log')]=sync.sha(folder/'run.log')
        hit,clear=Decimal(p['hitSeconds']),Decimal(p['firstClearedSeconds'])
        on,off=captures;positive=gate(on,off,hit,clear);faults=[]
        bad=copy.deepcopy(off);next(r for r in bad if Decimal(r['seconds'])-Decimal('.02')>=clear)['sha256']='0'*64
        try:gate(on,bad,hit,clear)
        except AssertionError:faults.append('first_complete_window_difference')
        else:raise AssertionError('Lingering output fault accepted')
        try:gate(off,off,hit,clear)
        except AssertionError:faults.append('absent_positive_voice')
        else:raise AssertionError('Positive fault accepted')
        results[f'p{side}']=dict(**positive,rejectedFaults=faults,terminals=terminals,logPins=pins)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),ownerProofSHA256=sync.sha(proof_path),checkerSHA256=sync.sha(Path(__file__)),heardQualityAccepted=False,intraUpdateBoundaryAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,results={key:value['completePostClearIdenticalUpdates'] for key,value in results.items()})))

if __name__=='__main__':main()
