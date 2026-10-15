"""Current Jax clap physical body FIFO/clip/source/display footprint proof."""
import collections,copy,json,re
from pathlib import Path
from qualify_bounded_jax_clap_draw_census import state_at
from qualify_bounded_jax_clap_finisher import gate as control_gate
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def coverage_gate(groups,ready,expected):
    opaque=[r for r in groups['IDLE_OPAQUE'] if 1<=int(r['frame'])-ready<=188]
    actual=collections.Counter((int(r['frame']),r['slot'],r['id'],r['pose'],r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16)) for r in opaque)
    assert actual==expected
    assert all(0<=int(r['eligible'])<=int(r['opaque']) and int(r['eligible'])+int(r['native_clipped'])==int(r['opaque']) for r in opaque)
    summaries=groups['COMPLETE_FOOTPRINT'];assert len(summaries)==188
    assert {int(r['frame'])-1-ready for r in summaries}==set(range(1,189))
    for r in summaries:
        frame=int(r['frame'])-1
        assert r['source_fail']==r['display_fail']=='0' and int(r['source_age'])==frame-ready
        totals={slot:sum(int(x['eligible']) for x in opaque if int(x['frame'])==frame and x['slot']==str(slot)) for slot in (1,2)}
        assert all(totals[slot]==int(r['slot'+str(slot)])>0 for slot in (1,2))
        assert sum(totals.values())==int(r['points']) and 0<=int(r['offscreen'])<=int(r['points'])
    total=sum(int(r['points']) for r in summaries);cropped=sum(int(r['offscreen']) for r in summaries)
    return dict(nativeDrawFields=188,nativeBodyDraws=sum(actual.values()),eligibleComponentPixels=total,
        rawOpaqueComponentPixels=sum(int(r['opaque']) for r in opaque),nativeClippedComponentPixels=sum(int(r['native_clipped']) for r in opaque),
        visibleComponentPixels=total-cropped,viewportCroppedComponentPixels=cropped)

def main():
    out=sync.ROOT/'audit_bounded_jax_clap_body_pixels_checked';assert not out.exists();results={}
    proof=json.loads((sync.ROOT/'audit_bounded_jax_clap_draw_census_checked/report.json').read_text());assert proof['passed']
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_jax_clap_body_pixels_runtime'
        census=sync.ROOT/f'audit_bounded_{fighter}_jax_clap_draw_census_runtime'
        assert sync.sha(census/'run.log')==proof['results'][fighter]['logSha256']
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        old=state_at(census,fighter);tags={tag for tag,r in old}
        current=[row for row in state_at(folder,fighter) if row[0] in tags];assert current==old
        control=control_gate(current,ident);ready=control['nativeActionFrame'];expected=collections.Counter()
        with (census/'run.log').open() as stream:
            for line in stream:
                if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if r['physical']=='0':continue
                size=int(r['size'],16);xy=int(r['xy'],16)
                expected[(int(r['frame']),r['physical'],r['id'],r['pose'],r['source'],size&1023,(size>>16)&1023,xy&1023,(xy>>16)&511,(int(r['command'],16)>>16)&65535)]+=1
        groups=summaries_at(folder);coverage=coverage_gate(groups,ready,expected);faults=[]
        for fault in ('visible_mismatch','missing_draw','wrong_clip'):
            bad=copy.deepcopy(groups)
            if fault=='visible_mismatch':bad['COMPLETE_FOOTPRINT'][0]['display_fail']='1'
            elif fault=='missing_draw':bad['IDLE_OPAQUE'].pop(0)
            else:bad['IDLE_OPAQUE'][0]['native_clipped']='9999'
            try:coverage_gate(bad,ready,expected)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Fault accepted '+fault)
        results[fighter]=dict(**coverage,rejectedFaults=faults,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        nonphysicalEffectsAccepted=False,allSubjectiveArtAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
