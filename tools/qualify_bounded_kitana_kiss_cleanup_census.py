"""Finite actual victim FIFO retirement, not framebuffer erase acceptance."""
import collections,copy,json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    control=[];fifo=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if line.startswith('MK2_STOCK_HEAD_V921_'):control.append(line.strip())
            if line.startswith('MK2_EFFECT_CENSUS_FIFO '):
                fifo.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return control,fifo

def gate(rows,side,ident):
    last=355 if side==1 else 356;winner=3-side
    physical=[r for r in rows if r['physical']!='0']
    assert all(r['writes']=='0' and r['assistance']=='none' for r in rows)
    assert all(int(r['id'])==(ident if int(r['physical'])==side else 4) for r in physical)
    victim=[r for r in physical if int(r['physical'])==side]
    own=[r for r in physical if int(r['physical'])==winner]
    assert {int(r['age']) for r in victim}==set(range(1,last+1))
    assert {int(r['age']) for r in own}==set(range(1,396))
    final='FFFD8EC0' if ident==18 else 'FFFD8D40'
    assert all(r['pose']==final for r in victim if int(r['age'])>=last-10)
    assert not any(int(r['age'])>last for r in victim)
    return dict(lastVictimDrawAge=last,firstVictimAbsentAge=last+1,
        winnerDrawFields=395,victimAbsentFields=395-last,victimDraws=len(victim))

def main():
    out=sync.ROOT/'audit_bounded_kitana_kiss_cleanup_census_checked';assert not out.exists()
    results={}
    for side in (1,2):
        for fighter,ident in [('sonya',18),('kano',17)]:
            folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kitana_kiss_cleanup_census_runtime'
            base=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kitana_kiss_draw_census_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            control,rows=load(folder);old_control,old_rows=load(base)
            assert control==old_control
            assert collections.Counter(tuple(sorted(r.items())) for r in rows if int(r['age'])<=276)==collections.Counter(tuple(sorted(r.items())) for r in old_rows)
            accepted=gate(rows,side,ident)
            bad=copy.deepcopy(rows)
            extra=copy.deepcopy(next(r for r in rows if int(r['physical'])==side));extra['age']='390';bad.append(extra)
            try:gate(bad,side,ident)
            except AssertionError:pass
            else:raise AssertionError('Late victim draw fault accepted')
            results[f'{fighter}P{side}']=dict(**accepted,originalControlUnchanged=True,
                first276FieldInventoryUnchanged=True,rejectedLateDrawFault=True,
                logSha256=sync.sha(folder/'run.log'),baselineLogSha256=sync.sha(base/'run.log'),terminal=terminal)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        framebufferEraseAccepted=False,heardAudioAccepted=False,allFinishersAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results={k:{a:r[a] for a in ('lastVictimDrawAge','firstVictimAbsentAge','victimAbsentFields')} for k,r in results.items()})))

if __name__=='__main__':main()
