"""Continuous native footprint coverage with explicit actual viewport crop."""
import argparse,copy,json,re
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace,point_gate
from qualify_bounded_queued_throw_footprints import gate

def summaries_at(folder):
    groups={tag:[] for tag in ('COMPLETE_FOOTPRINT','IDLE_OPAQUE','IDLE_FIFO')}
    with (folder/'run.log').open() as stream:
        for line in stream:
            for tag in groups:
                if '_'+tag+' ' in line:groups[tag].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return groups

def main():
    parser=argparse.ArgumentParser();parser.add_argument('fighter',choices=['sonya','kano'])
    parser.add_argument('phase',choices=['opening','landing']);args=parser.parse_args()
    fighter,phase=args.fighter,args.phase;lo,hi={'opening':(114,144),'landing':(145,176)}[phase]
    folder=sync.ROOT/f'audit_bounded_{fighter}_viewport_throw_{phase}_runtime'
    out=sync.ROOT/f'audit_bounded_{fighter}_viewport_throw_{phase}_checked';assert not out.exists()
    prior=sync.ROOT/'audit_bounded_complete_throw_footprint_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed']
    old=sync.ROOT/f'audit_bounded_{fighter}_complete_throw_footprint_runtime'
    assert sync.sha(old/'run.log')==proof['results'][fighter]['logSha256']
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    fields,hits,points=trace(folder);oldfields,oldhits,_=trace(old)
    assert fields==oldfields and hits==oldhits
    point_gate(points);assert all(r['source_matches']=='1' for r in points)
    ready=min(int(r['frame']) for r in fields)
    groups=summaries_at(folder);summaries=groups['COMPLETE_FOOTPRINT']
    coverage=gate(summaries,groups['IDLE_OPAQUE'],groups['IDLE_FIFO'],ready,lo,hi)
    assert all(0<=int(r['offscreen'])<int(r['points']) and 0<=int(r['column'])<512
               and int(r['row']) in (0,256) for r in summaries)
    prior_queue=sync.ROOT/f'audit_bounded_{fighter}_queued_throw_{phase}_runtime'
    cropped_explains_prior=None
    if prior_queue.exists():
        previous=summaries_at(prior_queue)['COMPLETE_FOOTPRINT']
        assert len(previous)==len(summaries)
        assert all(a['source_age']==b['source_age'] and a['points']==b['points']
                   and a['display_fail']==b['offscreen'] for a,b in zip(previous,summaries))
        cropped_explains_prior=True
    bad=copy.deepcopy(summaries);bad[0]['display_fail']='1'
    try:gate(bad,groups['IDLE_OPAQUE'],groups['IDLE_FIFO'],ready,lo,hi)
    except AssertionError:pass
    else:raise AssertionError('Visible mismatch waived')
    cropped=sum(int(r['offscreen']) for r in summaries)
    report=dict(passed=True,fighter=fighter,phase=phase,**coverage,
        opaquePixelsOutsideActualViewport=cropped,visiblePixels=coverage['opaquePixels']-cropped,
        cameraColumns=sorted({int(r['column']) for r in summaries}),
        cameraCropExplainsPriorCounters=cropped_explains_prior,visibleMismatchRejected=True,
        terminal=terminal,identicalQualifiedGameplay=True,bothVideoBuffersCovered=True,
        exactSparsePoints=len(points),logSha256=sync.sha(folder/'run.log'),sourceSync=sync.verify(),
        checkerSha256=sync.sha(Path(__file__)),entireThrowChoreographyAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','fighter','phase','nativeDrawFields','opaquePixels','visiblePixels','opaquePixelsOutsideActualViewport','cameraColumns')}))

if __name__=='__main__':main()
