"""Bind seven native stage effects immediately after actual draw instruction."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def check_draw(r,point):
    assert r['source']=='05735161' and r['pc']=='FF804640' and r['after_fetch_pc']=='FF804650'
    assert r['raw_data']==r['merged_command']=='D082' and r['mask']=='FFFF'
    assert r['palette']=='1C1C' and r['skip']=='0000' and r['scaleX']==r['scaleY']=='256'
    assert tuple(int(r[k]) for k in ('origin_x','origin_y','width','height'))==(243,158,12,81)
    assert tuple(int(r[k]) for k in ('top','bottom','left','right'))==(0,253,0,511)
    assert r['before']=='15' and r['after']==point['source_vram']==point['display_vram']
    assert r['candidate']=='1' and int(r['changed'])==int(r['before']!=r['after'])
    assert (r['query_frame'],r['x'],r['y'])==(point['source_frame'],point['dma_x'],point['dma_y'])

def main():
    root=sync.ROOT;original=root/'audit_bounded_aerial_all_query_checked/report.json'
    old=json.loads(original.read_text());results={};faults=[];count=changed=0
    for fighter in ('sonya','kano'):
        case=root/f'audit_bounded_{fighter}_stage_query_post_fetch_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        commands=[];present=[]
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_STAGE_QUERY_COMMAND ' in line:commands.append(r)
            if '_IDLE_VRAM_POINT ' in line:
                assert r['source_vram']==r['display_vram'] and r['vram_rgb']==r['actual'] and r['display_matches']=='1';present.append(r)
        bound=[]
        for point in old['results'][fighter]['unresolvedStageDrawPredictions']:
            matches=[r for r in commands if r['source']=='05735161' and (r['query_frame'],r['x'],r['y'])==(point['source_frame'],point['dma_x'],point['dma_y'])]
            assert len(matches)==1;check_draw(matches[0],point);bound.append(matches[0]);count+=1;changed+=int(matches[0]['changed'])
            displayed=[r for r in present if all(r[k]==point[k] for k in ('kind','source_frame','slot','id','dma_x','dma_y'))]
            assert len(displayed)==1 and displayed[0]['source_vram']==matches[0]['after']
        for key,value in [('source','00000000'),('after_fetch_pc','FF804640'),('after','999'),('mask','00FF')]:
            mutant=dict(bound[0]);mutant[key]=value
            try:check_draw(mutant,old['results'][fighter]['unresolvedStageDrawPredictions'][0])
            except AssertionError:faults.append(fighter+'_'+key)
            else:raise AssertionError('Ineffective stage fault')
        results[fighter]=dict(immediateNativeStageEffects=bound,exactPresentationVRAMPoints=len(present),terminal=terminal,logSha=sync.sha(case/'run.log'))
    assert count==7 and changed==6
    out=root/'audit_bounded_stage_query_post_fetch_checked';out.mkdir(exist_ok=False)
    report=dict(passed=True,results=results,resolvedNativeStageEffects=7,overwrittenShadowPoints=6,unchangedShadowPoints=1,
        rejectedFaults=faults,priorStagePixelDecoderStillIncomplete=True,wholeArtAcceptance=False,fullGoalComplete=False,
        sourceSync=sync.verify(),originalQueryReportSha=sync.sha(original),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,resolvedStageEffects=7,overwrites=6,unchanged=1,rejectedFaults=len(faults))))

if __name__=='__main__':main()
