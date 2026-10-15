"""Every native opaque component draw in a continuous throw window."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace,point_gate

def gate(summaries,opaque,fifo,ready):
    expected={int(r['frame']) for r in fifo if 114<=int(r['frame'])-ready<=176}
    assert expected and len(expected)>=30
    observed=[int(r['frame'])-1 for r in summaries]
    assert len(observed)==len(set(observed)) and set(observed)==expected
    total=0
    for r in summaries:
        frame=int(r['frame'])-1
        assert int(r['source_age'])==frame-ready and r['source_fail']==r['display_fail']=='0'
        components=[x for x in opaque if int(x['frame'])==frame]
        assert components
        totals={slot:sum(int(x['opaque']) for x in components if x['slot']==str(slot)) for slot in (1,2)}
        assert all(totals[slot]==int(r['slot'+str(slot)])>0 for slot in (1,2))
        assert sum(totals.values())==int(r['points'])
        total+=int(r['points'])
    return dict(nativeDrawFields=len(expected),opaquePixels=total,
                firstSourceAge=min(expected)-ready,lastSourceAge=max(expected)-ready,
                everyNativeBodyDrawInWindowCovered=True)

def main():
    out=sync.ROOT/'audit_bounded_throw_window_footprints_checked';assert not out.exists()
    prior=sync.ROOT/'audit_bounded_complete_throw_footprint_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed']
    results={}
    for fighter in ('sonya','kano'):
        old=sync.ROOT/f'audit_bounded_{fighter}_complete_throw_footprint_runtime'
        assert sync.sha(old/'run.log')==proof['results'][fighter]['logSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_throw_window_footprint_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,points=trace(folder);oldfields,oldhits,_=trace(old)
        assert fields==oldfields and hits==oldhits
        point_gate(points);assert all(r['source_matches']=='1' for r in points)
        ready=min(int(r['frame']) for r in fields)
        summaries=[];opaque=[];fifo=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if '_COMPLETE_FOOTPRINT ' in line:summaries.append(r)
                elif '_IDLE_OPAQUE ' in line:opaque.append(r)
                elif '_IDLE_FIFO ' in line:fifo.append(r)
        coverage=gate(summaries,opaque,fifo,ready);faults=[]
        for name in ('wrong_display','missing_field','wrong_pixel_count'):
            bad=copy.deepcopy(summaries)
            if name=='wrong_display':bad[0]['display_fail']='1'
            elif name=='missing_field':bad.pop()
            else:bad[0]['points']=str(int(bad[0]['points'])+1)
            try:gate(bad,opaque,fifo,ready)
            except AssertionError:faults.append(name)
            else:raise AssertionError('Fault accepted '+name)
        results[fighter]=dict(**coverage,rejectedFaults=faults,
            identicalPreviouslyQualifiedGameplay=True,terminal=terminal,
            logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        scope='Every opaque body-component pixel at every native body draw in readyages114..176, not entire match/framebuffer',
        entireThrowChoreographyAccepted=False,allContextsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
