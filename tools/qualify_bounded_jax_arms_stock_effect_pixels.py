"""Complete stock blood FIFO/DMA/clip/source/presentation proof per victim slot."""
import collections,copy,json,re,sys
from pathlib import Path
from qualify_bounded_jax_arm_prop_pixels import coverage_gate
from qualify_bounded_jax_clap_effect_pixels import fifo_at,summaries_at
from qualify_bounded_jax_arms_draw_census import states
import verify_native_source_sync as sync

def main(side):
    assert side in (1,2)
    out=sync.ROOT/f'audit_bounded_jax_arms_stock_effect_pixels_p{side}_checked';assert not out.exists();results={}
    path=sync.ROOT/'audit_bounded_jax_arms_nonphysical_sources/report.json'
    proof=json.loads(path.read_text());assert proof['passed']
    census_proof=json.loads((sync.ROOT/'audit_bounded_jax_arms_draw_census_checked/report.json').read_text());assert census_proof['passed']
    for fighter in ('sonya','kano'):
        key=f'{fighter}P{side}';actors=proof['results'][key]['stockEffectActors'];sources={s for a in actors.values() for s in a['sources']}
        census=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_draw_census_runtime'
        assert sync.sha(census/'run.log')==census_proof['results'][key]['logSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_stock_effect_pixels_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        old=states(census,fighter,side);tags={tag for tag,r in old}
        assert [row for row in states(folder,fighter,side) if row[0] in tags]==old
        ready=int(next(r for tag,r in old if tag=='ACTION')['frame'])
        expected=fifo_at(census,sources);assert sum(expected.values())==sum(a['draws'] for a in actors.values())
        assert fifo_at(folder,sources)==expected;dma=collections.Counter()
        with (folder/'run.log').open() as stream:
            for line in stream:
                if not line.startswith('MK2_CLAP_EFFECT_DMA '):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['pc']=='FF804640'
                dma[(int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16))]+=1
        assert dma==expected
        groups=summaries_at(folder);positive=coverage_gate(groups,ready,expected);faults=[]
        for fault in ('visible_mismatch','missing_draw','wrong_clip'):
            bad=copy.deepcopy(groups)
            if fault=='visible_mismatch':bad['COMPLETE_FOOTPRINT'][0]['display_fail']='1'
            elif fault=='missing_draw':bad['IDLE_OPAQUE'].pop(0)
            else:bad['IDLE_OPAQUE'][0]['native_clipped']='9999'
            try:coverage_gate(bad,ready,expected)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Fault accepted')
        results[fighter]=dict(**positive,rejectedFaults=faults,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,physicalVictimSlot=side,results=results,sourceSync=sync.verify(),classificationSha256=sync.sha(path),checkerSha256=sync.sha(Path(__file__)),subjectiveAllArtAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,side=side,results={f:{k:v for k,v in r.items() if k not in ('terminal','logSha256')} for f,r in results.items()})))

if __name__=='__main__':main(int(sys.argv[1]))
