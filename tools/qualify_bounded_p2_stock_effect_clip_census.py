"""Raw artwork, native clip eligibility and actual viewport kept separate."""
import collections,copy,json,re
from pathlib import Path
from qualify_bounded_p2_stock_effect_pixels import fifo_at
from qualify_bounded_p2_stock_head_body_pixels import driver
from qualify_bounded_stock_head_finisher import gate as control_gate
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def coverage_gate(groups,ready,expected):
    opaque=[r for r in groups['IDLE_OPAQUE'] if 1<=int(r['frame'])-ready<=174]
    actual=collections.Counter((int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16)) for r in opaque)
    assert actual==expected
    assert all(0<=int(r['eligible'])<=int(r['opaque']) and int(r['eligible'])+int(r['native_clipped'])==int(r['opaque']) for r in opaque)
    summaries=groups['COMPLETE_FOOTPRINT'];frames={key[0] for key in expected}
    assert len(summaries)==len(frames)==115 and {int(r['frame'])-1 for r in summaries}==frames
    for r in summaries:
        frame=int(r['frame'])-1
        assert r['source_fail']==r['display_fail']=='0' and int(r['source_age'])==frame-ready
        assert int(r['points'])==int(r['slot1'])==sum(int(x['eligible']) for x in opaque if int(x['frame'])==frame)>0 and r['slot2']=='0'
        assert 0<=int(r['offscreen'])<=int(r['points'])
    total=sum(int(r['points']) for r in summaries);cropped=sum(int(r['offscreen']) for r in summaries)
    return dict(nativeDrawFields=115,nativeEffectDraws=sum(actual.values()),rawOpaqueComponentPixels=sum(int(r['opaque']) for r in opaque),
        nativeClippedComponentPixels=sum(int(r['native_clipped']) for r in opaque),eligibleComponentPixels=total,
        viewportCroppedComponentPixels=cropped,visibleComponentPixels=total-cropped)

def main():
    out=sync.ROOT/'audit_bounded_p2_stock_effect_clip_census_checked';assert not out.exists();results={}
    proof=json.loads((sync.ROOT/'audit_bounded_p2_stock_head_native_census_checked/report.json').read_text())
    source_proof=json.loads((sync.ROOT/'audit_bounded_stock_head_remaining_effects_classified/report.json').read_text())
    assert proof['passed'] and source_proof['passed']
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_effect_clip_census_syntax_runtime'
        census=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_effect_census_runtime'
        assert sync.sha(census/'run.log')==proof['results'][fighter]['logHashes']['effect_census']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
        states=driver(folder,fighter);assert states==driver(census,fighter)
        control=control_gate(states,fighter,ident);ready=control['nativeActionFrame']
        sources=set(source_proof['results'][fighter]['stockEffectSources']);expected=fifo_at(census,sources)
        assert fifo_at(folder,sources)==expected and sum(expected.values())==438
        dma=collections.Counter()
        with (folder/'run.log').open() as stream:
            for line in stream:
                if not line.startswith('MK2_EFFECT_MAPPING_DMA '):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['pc']=='FF804640'
                dma[(int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16))]+=1
        assert dma==expected
        groups=summaries_at(folder);coverage=coverage_gate(groups,ready,expected);faults=[]
        for fault in ('visible_mismatch','wrong_eligible','wrong_clipped','missing_draw'):
            bad=copy.deepcopy(groups)
            if fault=='visible_mismatch':bad['COMPLETE_FOOTPRINT'][0]['display_fail']='1'
            elif fault=='wrong_eligible':bad['IDLE_OPAQUE'][0]['eligible']=str(int(bad['IDLE_OPAQUE'][0]['eligible'])+1)
            elif fault=='wrong_clipped':bad['IDLE_OPAQUE'][0]['native_clipped']='9999'
            else:bad['IDLE_OPAQUE'].pop(0)
            try:coverage_gate(bad,ready,expected)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Fault accepted '+fault)
        results[fighter]=dict(**coverage,rejectedFaults=faults,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        subjectiveArtAccepted=False,heardAudioAccepted=False,allFinishersAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
