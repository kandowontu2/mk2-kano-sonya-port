"""Bind actual per-field body/effect draw census to earned Jax clap."""
import collections,json,re
from pathlib import Path
from qualify_bounded_jax_clap_finisher import gate
from qualify_bounded_stock_head_body_footprints import PREFIX
import verify_native_source_sync as sync

def state_at(folder,fighter):
    rows=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
            m=PREFIX.match(line);assert m and (m[3],m[4],m[5],m[6],m[7])==(fighter,'1','jax','0','none')
            rows.append((m[1],dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return rows

def main():
    out=sync.ROOT/'audit_bounded_jax_clap_draw_census_checked';assert not out.exists();results={}
    prior=json.loads((sync.ROOT/'audit_bounded_jax_clap_finisher_checked/report.json').read_text());assert prior['passed']
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_jax_clap_draw_census_runtime'
        baseline=sync.ROOT/f'audit_bounded_{fighter}_jax_clap_finisher_runtime'
        assert sync.sha(baseline/'run.log')==prior['results'][fighter]['logSha256']
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=state_at(folder,fighter);assert rows==state_at(baseline,fighter)
        control=gate(rows,ident);last=control['nativeWrapFrame']-control['nativeActionFrame'];assert last==188
        bodies={slot:dict(ages=set(),sources=set(),draws=0) for slot in ('1','2')};actors={};fields=set()
        with (folder/'run.log').open() as stream:
            for line in stream:
                if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));age=int(r['age'])
                assert r['writes']=='0' and r['assistance']=='none' and 1<=age<=last;fields.add(age)
                if r['physical']!='0':
                    slot=r['physical'];assert int(r['id'])==(ident if slot=='1' else 11)
                    a=bodies[slot];a['ages'].add(age);a['sources'].add(r['source']);a['draws']+=1
                else:
                    a=actors.setdefault(r['actor'],dict(ages=set(),sources=set(),ids=set(),draws=0))
                    a['ages'].add(age);a['sources'].add(r['source']);a['ids'].add(r['id']);a['draws']+=1
        assert fields==set(range(1,last+1)) and all(a['ages']==fields for a in bodies.values())
        body_summary={slot:dict(nativeDrawFields=len(a['ages']),draws=a['draws'],sources=sorted(a['sources'])) for slot,a in bodies.items()}
        added={actor:dict(firstAge=min(a['ages']),lastAge=max(a['ages']),nativeDrawFields=len(a['ages']),
                draws=a['draws'],ids=sorted(a['ids']),sources=sorted(a['sources'])) for actor,a in actors.items() if min(a['ages'])>1}
        assert added
        results[fighter]=dict(nativeDrawFields=last,bodies=body_summary,newNonphysicalActors=added,
            terminal=t,logSha256=sync.sha(folder/'run.log'),unchangedEarnedDriverTrace=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        renderedPixelsAccepted=False,semanticGoreLabelsAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={f:dict(nativeDrawFields=r['nativeDrawFields'],newActors=len(r['newNonphysicalActors'])) for f,r in results.items()})))

if __name__=='__main__':main()
