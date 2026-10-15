"""Current independent all-actor inventory; no inferred pixels or gore identity."""
import collections,inspect,json,re
from pathlib import Path
import qualify_bounded_jax_arms_draw_census as previous
import verify_native_source_sync as sync

namespace=dict(previous.__dict__)
exec(compile(inspect.getsource(previous.states).replace("'jax'","'kung_lao'"),__file__+'::split_states','exec'),namespace)
states=namespace['states']

def main():
    out=sync.ROOT/'audit_bounded_kung_lao_split_draw_census_checked';assert not out.exists()
    proof_path=sync.ROOT/'audit_bounded_kung_lao_split_finisher_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed'];results={}
    for side in (1,2):
        for fighter,ident in [('sonya',18),('kano',17)]:
            key=f'{fighter}P{side}';base=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_finisher_runtime'
            folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_draw_census_runtime'
            assert sync.sha(base/'run.log')==proof['results'][key]['logSha256']
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            assert states(folder,fighter,side)==states(base,fighter,side)
            actors={};bodies={};fields=set()
            with (folder/'run.log').open() as stream:
                for line in stream:
                    if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));age=int(r['age']);fields.add(age)
                    assert 1<=age<=179 and r['writes']=='0' and r['assistance']=='none'
                    slot=int(r['physical'])
                    if slot:assert slot in (1,2) and int(r['id'])==(ident if slot==side else 0)
                    target=bodies if slot else actors
                    actor_key=str(slot) if slot else r['actor']
                    a=target.setdefault(actor_key,dict(ages=set(),sources=set(),poses=set(),ids=set(),draws=0))
                    a['ages'].add(age);a['sources'].add(r['source']);a['poses'].add(r['pose']);a['ids'].add(r['id']);a['draws']+=1
            assert fields==set(range(1,180)) and set(bodies)=={'1','2'}
            assert bodies[str(3-side)]['ages']==set(range(1,180))
            assert bodies[str(side)]['ages'] and actors
            def summarize(a):return dict(firstAge=min(a['ages']),lastAge=max(a['ages']),fields=len(a['ages']),draws=a['draws'],sources=sorted(a['sources']),poses=sorted(a['poses']),ids=sorted(a['ids']))
            results[key]=dict(bodies={k:summarize(v) for k,v in bodies.items()},allNonphysicalActors={k:summarize(v) for k,v in actors.items()},
                observedNativeFields=179,originalControlUnchanged=True,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        controlProofSha256=sync.sha(proof_path),nonphysicalGoreIdentityAccepted=False,renderedPixelsAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:dict(bodies=r['bodies'],nonphysicalActors=len(r['allNonphysicalActors'])) for k,r in results.items()})))

if __name__=='__main__':main()
