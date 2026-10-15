"""Complete P2 effect coverage: Sonya full run and Kano disjoint windows."""
import collections,copy,json,re
from pathlib import Path
from qualify_bounded_jax_clap_effect_pixels import fifo_at,coverage_gate,summaries_at
from qualify_bounded_p2_jax_voice_priority import read
from qualify_bounded_p2_jax_clap_control import gate
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_p2_jax_effect_windows_checked';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_p2_jax_draw_census_checked/report.json').read_text());assert proof['passed']
    results={}
    for fighter,ident in [('sonya',18),('kano',17)]:
        census=sync.ROOT/f'audit_bounded_p2_{fighter}_jax_draw_census_runtime'
        assert sync.sha(census/'run.log')==proof['results'][fighter]['logSha256']
        old,_=read(census,fighter);physical=gate(old,[],ident);ready=physical['actionFrame']
        actors=proof['results'][fighter]['newNonphysicalActors'];sources={s for a in actors.values() for s in a['sources']}
        expected=fifo_at(census,sources);assert sum(expected.values())==sum(a['draws'] for a in actors.values())
        windows=[('audit_bounded_p2_sonya_jax_effect_pixels_runtime',1,188)] if fighter=='sonya' else [(f'audit_bounded_p2_kano_jax_effect_{label}_runtime',first,last) for label,first,last in [('opening',1,100),('completion',101,188)]]
        groups={'IDLE_OPAQUE':[],'COMPLETE_FOOTPRINT':[]};dma=collections.Counter();receipts=[];covered=set()
        for name,first,last in windows:
            folder=sync.ROOT/name;t=json.loads((folder/'terminal.json').read_text())
            assert t['exitCode']==0 and t['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
            rows,_=read(folder,fighter);tags={tag for tag,r in old}
            assert [row for row in rows if row[0] in tags]==old
            assert fifo_at(folder,sources)==expected
            ages=set(range(first,last+1));assert not covered&ages;covered|=ages
            part=summaries_at(folder)
            groups['IDLE_OPAQUE'] += [r for r in part['IDLE_OPAQUE'] if first<=int(r['frame'])-ready<=last]
            groups['COMPLETE_FOOTPRINT'] += [r for r in part['COMPLETE_FOOTPRINT'] if first<=int(r['frame'])-1-ready<=last]
            with (folder/'run.log').open() as stream:
                for line in stream:
                    if not line.startswith('MK2_CLAP_EFFECT_DMA '):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['pc']=='FF804640'
                    assert first<=int(r['frame'])-ready<=last
                    dma[(int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16))]+=1
            receipts.append(dict(folder=name,actionAges=[first,last],terminal=t,logSha256=sync.sha(folder/'run.log')))
        assert covered==set(range(1,189)) and dma==expected
        positive=coverage_gate(groups,ready,expected);faults=[]
        for fault in ('visible_mismatch','missing_draw','wrong_clip'):
            bad=copy.deepcopy(groups)
            if fault=='visible_mismatch':bad['COMPLETE_FOOTPRINT'][0]['display_fail']='1'
            elif fault=='missing_draw':bad['IDLE_OPAQUE'].pop(0)
            else:bad['IDLE_OPAQUE'][0]['native_clipped']='9999'
            try:coverage_gate(bad,ready,expected)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Fault accepted')
        results[fighter]=dict(**positive,rejectedFaults=faults,runs=receipts,unchangedEarnedDriverTrace=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),subjectiveAllArtAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results={f:{k:v for k,v in r.items() if k!='runs'} for f,r in results.items()})))

if __name__=='__main__':main()
