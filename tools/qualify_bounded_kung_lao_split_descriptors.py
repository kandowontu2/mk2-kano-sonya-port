"""Live terminated pose lists bind every custom split draw's identity/geometry."""
import copy,json,re
from pathlib import Path
from qualify_bounded_kung_lao_split_draw_census import states
import verify_native_source_sync as sync

def gate(draws,ident,specs,side):
    assert draws and any(r['physical']=='0' for r in draws)
    for r in draws:
        assert int(r['id'])==ident and r['physical'] in ('0',str(side))
        spec=specs[r['source']];size=int(r['size'],16)
        assert r['pose']==spec['pose']
        assert (size&1023,(size>>16)&1023)==(int(spec['width']),int(spec['height']))
    return dict(customDraws=len(draws),physicalDraws=sum(r['physical']!='0' for r in draws),
        detachedPartDraws=sum(r['physical']=='0' for r in draws),
        detachedPartSources=sorted({r['source'] for r in draws if r['physical']=='0'}))

def main():
    out=sync.ROOT/'audit_bounded_kung_lao_split_descriptors_checked';assert not out.exists()
    folder=sync.ROOT/'audit_bounded_kung_lao_split_descriptor_lists_runtime'
    t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    baseline=sync.ROOT/'audit_bounded_sonya_p1_kung_lao_split_finisher_runtime'
    assert states(folder,'sonya',1)==states(baseline,'sonya',1)
    descriptors={17:[],18:[]}
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if not line.startswith('MK2_SPLIT_DESCRIPTOR '):continue
            r=dict(re.findall(r'(\w+)=([^\s]+)',line));ident=int(r['id'])
            assert r['writes']=='0' and r['assistance']=='none' and r['flags']=='6000' and r['terminator']=='0000'
            assert r['palette']==('FFFED000' if ident==17 else 'FFFED800')
            assert 0<int(r['width'])<200 and 0<int(r['height'])<200
            descriptors[ident].append(r)
    assert all([int(r['index']) for r in rows]==list(range(6)) for rows in descriptors.values())
    source_sets={ident:{r['source'] for r in rows} for ident,rows in descriptors.items()}
    assert len(source_sets[17])==len(source_sets[18])==6 and source_sets[17].isdisjoint(source_sets[18])
    proof_path=sync.ROOT/'audit_bounded_kung_lao_split_draw_census_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed'];results={}
    all_sources=source_sets[17]|source_sets[18]
    for side in (1,2):
        for fighter,ident in [('sonya',18),('kano',17)]:
            key=f'{fighter}P{side}';census=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_draw_census_runtime'
            assert sync.sha(census/'run.log')==proof['results'][key]['logSha256'];draws=[]
            with (census/'run.log').open() as stream:
                for line in stream:
                    if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if r['source'] in all_sources:draws.append(r)
            specs={r['source']:r for r in descriptors[ident]};accepted=gate(draws,ident,specs,side);faults=[]
            bad=copy.deepcopy(draws);bad[0]['id']='0'
            try:gate(bad,ident,specs,side)
            except AssertionError:faults.append('foreign_id')
            else:raise AssertionError('ID fault accepted')
            bad=copy.deepcopy(draws);bad[0]['pose']='00000000'
            try:gate(bad,ident,specs,side)
            except AssertionError:faults.append('foreign_pose')
            else:raise AssertionError('Pose fault accepted')
            results[key]=dict(**accepted,rejectedFaults=faults,censusLogSha256=sync.sha(census/'run.log'))
    report=dict(passed=True,results=results,descriptors=descriptors,terminal=t,logSha256=sync.sha(folder/'run.log'),
        censusProofSha256=sync.sha(proof_path),sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        actualPaletteDeliveryVerified=False,renderedPixelsAccepted=False,semanticArtworkAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
