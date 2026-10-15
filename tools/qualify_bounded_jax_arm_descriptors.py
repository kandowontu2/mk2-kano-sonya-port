"""Bind live five-frame descriptors to every native detached-arm candidate draw."""
import json,re
from pathlib import Path
from qualify_bounded_jax_arms_draw_census import states
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_jax_arm_descriptors_checked';assert not out.exists()
    folder=sync.ROOT/'audit_bounded_jax_arm_descriptors_runtime'
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    baseline=sync.ROOT/'audit_bounded_sonya_jax_arms_finisher_runtime'
    assert states(folder,'sonya',1)==states(baseline,'sonya',1)
    descriptors={17:[],18:[]}
    with (folder/'run.log').open() as stream:
        for line in stream:
            if not line.startswith('MK2_ARM_DESCRIPTOR '):continue
            r=dict(re.findall(r'(\w+)=([^\s]+)',line));ident=int(r['id'])
            assert r['writes']=='0' and r['assistance']=='none'
            assert r['flags']=='6000' and r['terminator']=='0000' and r['palette']==('FFFED000' if ident==17 else 'FFFED800')
            descriptors[ident].append(r)
    assert all([int(r['index']) for r in rows]==list(range(5)) for rows in descriptors.values())
    assert {r['source'] for r in descriptors[17]}.isdisjoint({r['source'] for r in descriptors[18]})
    classification_path=sync.ROOT/'audit_bounded_jax_arms_nonphysical_sources/report.json'
    classification=json.loads(classification_path.read_text());assert classification['passed'];results={}
    for side in (1,2):
        for fighter,ident in [('sonya',18),('kano',17)]:
            key=f'{fighter}P{side}';actors=classification['results'][key]['customSourcePropCandidates']
            expected_sources={r['source'] for r in descriptors[ident]}
            assert all(set(a['sources'])==expected_sources for a in actors.values())
            census=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_draw_census_runtime';draws=[]
            with (census/'run.log').open() as stream:
                for line in stream:
                    if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if r['actor'] not in actors:continue
                    assert r['physical']=='0' and r['id']=='0'
                    age=int(r['age']);index=min((age-actors[r['actor']]['firstAge'])//4,4)
                    spec=descriptors[ident][index];size=int(r['size'],16)
                    assert r['source']==spec['source'] and (size&1023,(size>>16)&1023)==(int(spec['width']),int(spec['height']))
                    draws.append(r)
            assert len(draws)==118
            for actor,a in actors.items():assert {int(r['age']) for r in draws if r['actor']==actor}==set(range(a['firstAge'],148))
            results[key]=dict(nativePropActors=2,sourceBoundDraws=118,fiveDescriptorSources=sorted(expected_sources),censusLogSha256=sync.sha(census/'run.log'))
    report=dict(passed=True,results=results,descriptors=descriptors,terminal=terminal,logSha256=sync.sha(folder/'run.log'),classificationSha256=sync.sha(classification_path),checkerSha256=sync.sha(Path(__file__)),sourceSync=sync.verify(),actualPaletteDeliveryVerified=False,renderedPixelsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
