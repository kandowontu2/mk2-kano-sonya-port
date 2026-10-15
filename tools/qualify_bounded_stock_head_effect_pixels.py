"""All detached-head opaque component pixels; no full-gore/audio claim."""
import copy,json
from pathlib import Path
import qualify_bounded_stock_head_body_footprints_driver as driver
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def gate(groups,ready,ident,sources):
    summaries=groups['COMPLETE_FOOTPRINT'];opaque=groups['IDLE_OPAQUE'];fifo=groups['IDLE_FIFO']
    expected=set(range(ready+59,ready+175))
    assert {int(r['frame']) for r in fifo if 59<=int(r['frame'])-ready<=174}==expected
    assert len(summaries)==116 and {int(r['frame'])-1 for r in summaries}==expected
    observed_sources=set();total=0;cropped=0
    for r in summaries:
        frame=int(r['frame'])-1
        assert int(r['source_age'])==frame-ready and r['source_fail']==r['display_fail']=='0'
        components=[x for x in opaque if int(x['frame'])==frame]
        assert len(components)==1
        c=components[0];assert c['slot']=='1' and int(c['id'])==ident
        observed_sources.add(c['source'])
        assert int(c['opaque'])==int(r['slot1'])==int(r['points'])>0 and r['slot2']=='0'
        assert 0<=int(r['offscreen'])<=int(r['points'])
        total+=int(r['points']);cropped+=int(r['offscreen'])
    assert observed_sources==sources
    return dict(nativeDrawFields=116,opaqueHeadComponentPixels=total,visibleHeadComponentPixels=total-cropped,
        croppedHeadComponentPixels=cropped,firstSourceAge=59,lastSourceAge=174,allSevenSourcesObserved=True)

def main():
    out=sync.ROOT/'audit_bounded_stock_head_effect_pixels_checked';assert not out.exists()
    prior=json.loads((sync.ROOT/'audit_bounded_stock_head_effect_census_checked/report.json').read_text())
    baseline_proof=json.loads((sync.ROOT/'audit_bounded_stock_head_finisher_scope_checked/report.json').read_text())
    assert prior['passed'] and baseline_proof['passed'];results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_stock_head_effect_pixels_runtime'
        baseline=sync.ROOT/f'audit_bounded_{fighter}_stock_head_finisher_runtime'
        assert sync.sha(baseline/'run.log')==baseline_proof['results'][fighter]['logSha256']
        census=sync.ROOT/f'audit_bounded_{fighter}_stock_head_effect_census_runtime'
        assert sync.sha(census/'run.log')==prior['results'][fighter]['logSha256']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=driver.driver_states(folder,fighter);assert rows==driver.driver_states(baseline,fighter)
        control=driver.scoped.original.state_gate(rows,fighter,ident)
        actors=prior['results'][fighter]['candidateNonBodyActors'];assert len(actors)==1
        sources=set(next(iter(actors.values()))['sources'])
        groups=summaries_at(folder);coverage=gate(groups,control['nativeActionFrame'],ident,sources)
        faults=[]
        for fault in ('source','display','missing_field','count'):
            bad=copy.deepcopy(groups);r=bad['COMPLETE_FOOTPRINT'][0]
            if fault in ('source','display'):r[fault+'_fail']='1'
            elif fault=='missing_field':bad['COMPLETE_FOOTPRINT'].pop()
            else:r['points']=str(int(r['points'])+1)
            try:gate(bad,control['nativeActionFrame'],ident,sources)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Fault accepted '+fault)
        results[fighter]=dict(**coverage,rejectedFaults=faults,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        intendedArtVisualReviewAccepted=False,allGoreEffectsAccepted=False,fullFinisherAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
