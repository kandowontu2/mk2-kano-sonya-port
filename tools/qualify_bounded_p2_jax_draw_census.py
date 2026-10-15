"""Physical bodies and independently spawned effects across 188 native fields."""
import json,re
from pathlib import Path
from qualify_bounded_p2_jax_voice_priority import read
import qualify_bounded_p2_jax_clap_control as control
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_p2_jax_draw_census_checked';assert not out.exists();results={}
    for fighter,ident in [('sonya',18),('kano',17)]:
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_jax_draw_census_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
        rows,_=read(folder,fighter);old,_=read(sync.ROOT/f'audit_bounded_p2_{fighter}_jax_clap_audio_route_runtime',fighter)
        assert rows==old;physical=control.gate(rows,[],ident)
        bodies={slot:dict(ages=set(),draws=0,sources=set()) for slot in ('1','2')};actors={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));age=int(r['age'])
                assert r['writes']=='0' and r['assistance']=='none' and 1<=age<=188
                if r['physical']!='0':
                    slot=r['physical'];assert int(r['id'])==(11 if slot=='1' else ident)
                    a=bodies[slot]
                else:
                    a=actors.setdefault(r['actor'],dict(ages=set(),draws=0,sources=set(),ids=set()))
                    a['ids'].add(r['id'])
                a['ages'].add(age);a['draws']+=1;a['sources'].add(r['source'])
        assert all(a['ages']==set(range(1,189)) for a in bodies.values())
        def summary(a):return dict(firstAge=min(a['ages']),lastAge=max(a['ages']),fields=len(a['ages']),draws=a['draws'],sources=sorted(a['sources']))
        new={actor:dict(**summary(a),ids=sorted(a['ids'])) for actor,a in actors.items() if min(a['ages'])>1}
        assert new
        results[fighter]=dict(physical=physical,bodies={s:summary(a) for s,a in bodies.items()},newNonphysicalActors=new,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),renderedPixelsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={f:dict(bodyDraws=sum(a['draws'] for a in r['bodies'].values()),newActors=len(r['newNonphysicalActors']),effectDraws=sum(a['draws'] for a in r['newNonphysicalActors'].values())) for f,r in results.items()})))

if __name__=='__main__':main()
