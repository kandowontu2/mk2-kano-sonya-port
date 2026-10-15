"""All opaque source pixels in one native body field, with coverage census."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace,point_gate

def main():
    out=sync.ROOT/'audit_bounded_complete_throw_footprint_checked';assert not out.exists()
    prior=sync.ROOT/'audit_bounded_large_rom_cross_throw_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed']
    results={}
    for fighter in ('sonya','kano'):
        old=sync.ROOT/f'audit_bounded_{fighter}_large_rom_cross_throw_runtime'
        assert sync.sha(old/'run.log')==proof['results'][fighter]['logSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_complete_throw_footprint_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes']<320*1024*1024
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,points=trace(folder);oldfields,oldhits,oldpoints=trace(old)
        assert fields==oldfields and hits==oldhits and points==oldpoints
        point_gate(points);assert all(r['source_matches']=='1' for r in points)
        summaries=[];opaque=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                if '_COMPLETE_FOOTPRINT ' in line:summaries.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
                elif '_IDLE_OPAQUE ' in line:opaque.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        assert len(summaries)==1
        summary=summaries[0]
        assert summary['source_age']=='128' and summary['source_fail']==summary['display_fail']=='0'
        sourceframe=int(summary['frame'])-1
        components=[r for r in opaque if int(r['frame'])==sourceframe]
        assert components
        totals={slot:sum(int(r['opaque']) for r in components if r['slot']==str(slot)) for slot in (1,2)}
        assert all(totals[slot]==int(summary['slot'+str(slot)])>1000 for slot in (1,2))
        assert sum(totals.values())==int(summary['points'])
        results[fighter]=dict(sourceFrame=sourceframe,completeOpaquePixelsPerSlot=totals,
            bodyComponents=len(components),sourceAndDisplayedFailures=0,
            matchingPreviouslyQualifiedGameplay=True,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        scope='One field per throw direction; every opaque body-component source pixel, not entire animation or framebuffer',
        fullThrowAnimationAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
