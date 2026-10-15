"""Retain exact failed point evidence; no mismatch waiver or acceptance."""
import json
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace

def main():
    out=sync.ROOT/'audit_bounded_sweep_presentation_gaps';assert not out.exists()
    results={}
    for fighter in ('sonya','kano'):
        folder=sync.ROOT/f'audit_bounded_{fighter}_sweep_presentation_runtime'
        fields,hits,points=trace(folder)
        failures=[r for r in points if r['source_vram']!=r['display_vram'] or
            r['vram_rgb']!=r['actual'] or r['display_matches']!='1' or
            int(r['frame'])!=int(r['source_frame'])+1]
        results[fighter]=dict(pointCount=len(points),failedPoints=failures,
            failureCount=len(failures),failedSourceFrames=sorted({int(r['source_frame']) for r in failures}),
            logSha256=sync.sha(folder/'run.log'),acceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(dict(results=results,
        acceptance=False,fullGoalComplete=False),indent=2)+'\n')
    print(json.dumps({k:dict(count=v['failureCount'],frames=v['failedSourceFrames'],
        first=v['failedPoints'][:2]) for k,v in results.items()}))

if __name__=='__main__':main()
