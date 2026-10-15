"""Sonya remaining stock-effect footprints; native victim trace unchanged."""
import collections,json,re
from pathlib import Path
import qualify_bounded_stock_head_body_footprints_driver as driver
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_sonya_stock_head_stock_effect_pixels_checked';assert not out.exists()
    folder=sync.ROOT/'audit_bounded_sonya_stock_head_stock_effect_pixels_runtime'
    baseline=sync.ROOT/'audit_bounded_sonya_stock_head_finisher_runtime'
    prior=json.loads((sync.ROOT/'audit_bounded_stock_head_finisher_scope_checked/report.json').read_text())
    assert prior['passed'] and sync.sha(baseline/'run.log')==prior['results']['sonya']['logSha256']
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    rows=driver.driver_states(folder,'sonya');assert rows==driver.driver_states(baseline,'sonya')
    control=driver.scoped.original.state_gate(rows,'sonya',18);ready=control['nativeActionFrame']
    proof=json.loads((sync.ROOT/'audit_bounded_stock_head_remaining_effects_classified/report.json').read_text())
    assert proof['passed'];sources=set(proof['results']['sonya']['stockEffectSources'])
    census=sync.ROOT/'audit_bounded_sonya_stock_head_effect_census_runtime/run.log'
    assert sync.sha(census)==proof['results']['sonya']['sourceLogSha256']
    expected=collections.Counter()
    with census.open() as stream:
        for line in stream:
            if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if r['physical']=='0' and r['source'] in sources:expected[(int(r['frame']),r['source'])]+=1
    groups=summaries_at(folder);opaque=groups['IDLE_OPAQUE'];summaries=groups['COMPLETE_FOOTPRINT']
    actual=collections.Counter((int(r['frame']),r['source']) for r in opaque)
    assert actual==expected and sum(actual.values())==440
    assert len(summaries)==116 and {int(r['frame'])-1-ready for r in summaries}==set(range(59,175))
    total=cropped=0
    for r in summaries:
        frame=int(r['frame'])-1;components=[x for x in opaque if int(x['frame'])==frame]
        assert int(r['source_age'])==frame-ready and r['source_fail']==r['display_fail']=='0'
        assert sum(int(x['opaque']) for x in components)==int(r['points'])==int(r['slot1'])>0 and r['slot2']=='0'
        assert all(x['source'] in sources for x in components)
        assert 0<=int(r['offscreen'])<=int(r['points'])
        total+=int(r['points']);cropped+=int(r['offscreen'])
    report=dict(passed=True,nativeDrawFields=116,nativeEffectDraws=440,opaqueComponentPixels=total,
        visibleComponentPixels=total-cropped,croppedComponentPixels=cropped,terminal=terminal,
        logSha256=sync.sha(folder/'run.log'),sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        intendedArtVisualReviewAccepted=False,allFinisherAudioAccepted=False,kanoStockEffectsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','nativeDrawFields','nativeEffectDraws','opaqueComponentPixels','visibleComponentPixels','croppedComponentPixels')}))

if __name__=='__main__':main()
