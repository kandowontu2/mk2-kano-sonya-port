"""Record evidence of mixed pending fields; never waive incomplete coverage."""
import json,re
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace

def main():
    out=sync.ROOT/'audit_bounded_throw_window_queue_gap';assert not out.exists()
    results={}
    for fighter in ('sonya','kano'):
        folder=sync.ROOT/f'audit_bounded_{fighter}_throw_window_footprint_runtime'
        fields,hits,points=trace(folder);ready=min(int(r['frame']) for r in fields)
        summaries=[];fifo=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if '_COMPLETE_FOOTPRINT ' in line:summaries.append(r)
                elif '_IDLE_FIFO ' in line and 114<=int(r['frame'])-ready<=176:fifo.append(r)
        samefield=[r for r in points if r['frame']==r['source_frame']]
        missing=sorted({int(r['frame']) for r in fifo}-{int(r['frame'])-1 for r in summaries})
        assert samefield and missing
        assert all(r['source_vram']=='-1' for r in samefield)
        results[fighter]=dict(terminal=json.loads((folder/'terminal.json').read_text()),
            actualBodyFIFOFields=len({r['frame'] for r in fifo}),
            completeFootprintSummaryFields=len(summaries),missingSourceFrames=missing,
            prematureSameFieldQueries=len(samefield),firstPrematureQueries=samefield[:4],
            footprintCounterFailures=sum(int(r['source_fail'])+int(r['display_fail']) for r in summaries),
            logSha256=sync.sha(folder/'run.log'),acceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(dict(results=results,
        acceptance=False,fullGoalComplete=False),indent=2)+'\n')
    print(json.dumps({k:dict(bodyFIFOFields=v['actualBodyFIFOFields'],
        footprintFields=v['completeFootprintSummaryFields'],prematureQueries=v['prematureSameFieldQueries'],
        missingFields=len(v['missingSourceFrames'])) for k,v in results.items()}))

if __name__=='__main__':main()
