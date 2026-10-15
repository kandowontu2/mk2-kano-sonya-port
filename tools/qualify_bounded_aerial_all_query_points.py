"""Bind actual fighter-over-stock-foot overdraw; leave stage replay gaps open."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def bind_cover(q,bodies):
    assert q['match']=='1' and q['final']==q['actual'] and q['pc']=='FF804640'
    candidates=[b for b in bodies if b['frame']==q['source_frame'] and b['source']==q['source'] and b['command']==q['command']]
    assert len(candidates)==1;b=candidates[0]
    assert b['id']=='17' and b['slot']=='1'
    sx,sy,c=int(q['source_x']),int(q['source_y']),int(q['command'],16)
    assert 0<=sx<int(b['width']) and 0<=sy<int(b['height'])
    assert int(q['dma_x'])==(int(b['x'])+(-sx if c&16 else sx))&1023
    assert int(q['dma_y'])==(int(b['y'])+(-sy if c&32 else sy))&511
    assert int(q['index'])&0x7f00==0x0200

def main():
    root=sync.ROOT;results={};faults=[]
    for fighter,id in (('sonya',18),('kano',17)):
        case=root/f'audit_bounded_{fighter}_aerial_all_query_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        points=[];finals=[];bodies=[]
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_IDLE_VRAM_POINT ' in line:
                assert r['id']=={'1':str(id),'2':'4'}[r['slot']]
                assert int(r['frame'])==int(r['source_frame'])+1
                assert r['source_vram']==r['display_vram'] and r['vram_rgb']==r['actual'] and r['display_matches']=='1'
                assert int(r['source_matches'])==int(r['predicted']==r['source_vram']);points.append(r)
            if '_IDLE_ALL_DRAW_FINAL ' in line:finals.append(r)
            if '_IDLE_OPAQUE ' in line:bodies.append(r)
        bodypoints=[r for r in points if r['kind']=='body']
        assert len(bodypoints)==87 and all(r['source_matches']=='1' for r in bodypoints)
        unresolved=[r for r in points if r['source_matches']=='0'];assert len(unresolved)=={'sonya':3,'kano':4}[fighter]
        covers=[]
        if fighter=='kano':
            old=json.loads((root/'audit_bounded_aerial_motion_points_checked/report.json').read_text())['results']['kano']['unresolvedBodyRGBPoints']
            assert len(old)==8
            for r in old:
                found=[q for q in finals if q['kind']=='body' and all(q[k]==r[k] for k in ('source_frame','slot','id','dma_x','dma_y'))]
                assert len(found)==1;bind_cover(found[0],bodies);covers.append(found[0])
            for key,value in [('source','00000000'),('actual','FFFFFF'),('source_x','999'),('dma_x','999')]:
                mutant=dict(covers[0]);mutant[key]=value
                try:bind_cover(mutant,bodies)
                except AssertionError:faults.append(key)
                else:raise AssertionError('Ineffective cover fault')
            for q in covers:bind_cover(q,bodies)
        results[fighter]=dict(exactPresentedVRAMQueryPoints=len(points),exactBodyFinalDrawPoints=87,
            previouslyUnmatchedStockFootPointsBound=len(covers),coveringDraws=covers,
            unresolvedStageDrawPredictions=unresolved,terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_aerial_all_query_checked';out.mkdir(exist_ok=False)
    result=dict(passedBodyOverlapBinding=True,results=results,rejectedCoverFaults=faults,
        completeLayerReplayProven=False,wholeShadowAcceptance=False,fullGoalComplete=False,
        sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(exactPresentationPoints=sum(v['exactPresentedVRAMQueryPoints'] for v in results.values()),stockFootOverlapsBound=8,stagePredictionGaps=7)))

if __name__=='__main__':main()
