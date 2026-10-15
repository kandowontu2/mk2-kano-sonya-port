"""Independent all-actor draw inventory bound to four earned arm-rip traces."""
import json,re
from pathlib import Path
from qualify_bounded_stock_head_body_footprints import PREFIX
import verify_native_source_sync as sync

def states(folder,fighter,side):
    rows=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
            m=PREFIX.match(line);assert m and (m[3],m[4],m[5],m[6],m[7])==(fighter,str(side),'jax','0','none')
            rows.append((m[1],dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return rows

def main():
    out=sync.ROOT/'audit_bounded_jax_arms_draw_census_checked';assert not out.exists();results={}
    for side in (1,2):
        name='audit_bounded_jax_arms_finisher_checked' if side==1 else 'audit_bounded_p2_jax_arms_finisher_checked'
        proof=json.loads((sync.ROOT/name/'report.json').read_text());assert proof['passed']
        for fighter,ident in [('sonya',18),('kano',17)]:
            baseline=sync.ROOT/(f'audit_bounded_{fighter}_jax_arms_finisher_runtime' if side==1 else f'audit_bounded_p2_{fighter}_jax_arms_finisher_runtime')
            assert sync.sha(baseline/'run.log')==proof['results'][fighter]['logSha256']
            folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_draw_census_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
            assert states(folder,fighter,side)==states(baseline,fighter,side)
            bodies={s:dict(ages=set(),sources=set(),draws=0) for s in ('1','2')};actors={}
            with (folder/'run.log').open() as stream:
                for line in stream:
                    if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));age=int(r['age'])
                    assert 1<=age<=147 and r['writes']=='0' and r['assistance']=='none'
                    if r['physical']!='0':
                        slot=r['physical'];assert int(r['id'])==(ident if int(slot)==side else 11);a=bodies[slot]
                    else:
                        a=actors.setdefault(r['actor'],dict(ages=set(),sources=set(),draws=0,ids=set()));a['ids'].add(r['id'])
                    a['ages'].add(age);a['sources'].add(r['source']);a['draws']+=1
            assert all(a['ages']==set(range(1,148)) for a in bodies.values())
            def summarize(a):return dict(firstAge=min(a['ages']),lastAge=max(a['ages']),fields=len(a['ages']),sources=sorted(a['sources']),draws=a['draws'])
            new={actor:dict(**summarize(a),ids=sorted(a['ids'])) for actor,a in actors.items() if min(a['ages'])>1}
            assert new
            results[f'{fighter}P{side}']=dict(bodies={s:summarize(a) for s,a in bodies.items()},newNonphysicalActors=new,terminal=terminal,logSha256=sync.sha(folder/'run.log'),unchangedEarnedTrace=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),renderedPixelsAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={key:dict(bodyDraws=sum(a['draws'] for a in r['bodies'].values()),newActors=len(r['newNonphysicalActors'])) for key,r in results.items()})))

if __name__=='__main__':main()
