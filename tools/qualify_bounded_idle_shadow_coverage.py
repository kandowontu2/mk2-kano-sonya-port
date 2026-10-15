"""Account for actual body coverage without waiving unresolved source points."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;results={}
    for fighter,id in (('sonya',18),('kano',17)):
        case=root/f'audit_bounded_{fighter}_idle_shadow_coverage_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        rows=[];body=[]
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_IDLE_OPAQUE ' in line:body.append(r)
            if '_IDLE_SHADOW_COVER ' in line:rows.append(r)
        assert len(body)==60 and len(rows)>1900
        covered=visible=unresolved=0
        for r in rows:
            assert int(r['frame'])==int(r['source_frame'])+1
            assert r['id']=={'1':str(id),'2':'4'}[r['slot']]
            assert int(r['match'])==int(r['final']==r['actual'])
            if r['covered']=='1':
                assert r['match']=='1' and r['cover_pc']=='FF804640'
                assert r['cover_id']=={'1':str(id),'2':'4'}[r['cover_slot']]
                candidates=[b for b in body if b['frame']==r['source_frame'] and b['slot']==r['cover_slot'] and b['source']==r['cover_source'] and b['command']==r['cover_command']]
                assert len(candidates)==1;b=candidates[0]
                sx,sy=int(r['cover_sx']),int(r['cover_sy']);c=int(r['cover_command'],16)
                assert 0<=sx<int(b['width']) and 0<=sy<int(b['height']) and int(r['cover_pixel'])>0
                assert int(r['dma_x'])==(int(b['x'])+(-sx if c&16 else sx))&1023
                assert int(r['dma_y'])==(int(b['y'])+(-sy if c&32 else sy))&511
                assert int(r['index'])&255==int(r['cover_pixel'])
                covered+=1
            elif r['match']=='1':
                assert r['index']=='15' and r['final']=='000000';visible+=1
            else:
                assert r['covered']=='0';unresolved+=1
        assert covered+visible+unresolved==len(rows) and covered>500 and unresolved>0
        results[fighter]=dict(points=len(rows),bodyCoverageProven=covered,visibleShadowPoints=visible,
            unresolvedSourcePoints=unresolved,allUnresolvedHaveNoObservedBodyCoverage=True,
            terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_idle_shadow_coverage_checked';out.mkdir(exist_ok=False)
    result=dict(completed=True,results=results,wholeShadowAcceptance=False,fullGoalComplete=False,
        nextEvidence='Actual DMA LRSKIP and banked clipping registers for remaining source points',
        sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a in ('points','bodyCoverageProven','visibleShadowPoints','unresolvedSourcePoints')} for k,v in results.items()}))

if __name__=='__main__':main()
