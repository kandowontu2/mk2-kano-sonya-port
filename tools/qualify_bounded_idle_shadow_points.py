"""Finite owned shadow submission and visible points, with occlusions unwaived."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_idle_scanout_points import check as check_body

def main():
    root=sync.ROOT;results={}
    for fighter,id in (('sonya',18),('kano',17)):
        case=root/f'audit_bounded_{fighter}_idle_shadow_points_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        rows=[];points=[];body=[]
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_IDLE_SHADOW_DMA ' in line:
                assert r['id']=={'1':str(id),'2':'4'}[r['slot']] and r['actor']==r['owner']
                assert r['pc'] in ('FF8015A0','FF801610')
                assert r['height']=='1' and int(r['command'],16)&15==8
                assert r['scaleX']==r['scaleY']=='256';rows.append(r)
            if '_IDLE_SCANPOINT ' in line:
                if r['kind']=='body':check_body(r,id);body.append(r)
                else:points.append(r)
        assert len(body)==60 and len(points)==sum(int(r['opaque'])>0 for r in rows)
        assert len(points)>1000
        visible={};mismatched=[]
        for r in points:
            assert r['palette_index']=='15' and r['expected']=='000000'
            assert int(r['frame'])==int(r['source_frame'])+1
            assert r['id']=={'1':str(id),'2':'4'}[r['slot']]
            assert int(r['display_y'])==int(r['dma_y'])-int(r['row'])
            assert int(r['display_x'])==int(r['dma_x'])-int(r['column'])
            assert 0<=int(r['display_x'])<400 and 0<=int(r['display_y'])<254
            assert int(r['match'])==int(r['actual']==r['expected'])
            matches=[s for s in rows if s['frame']==r['source_frame'] and s['slot']==r['slot'] and s['y']==r['dma_y'] and int(s['opaque'])>0]
            assert matches
            key=(int(r['source_frame']),int(r['slot']))
            if r['match']=='1':visible[key]=visible.get(key,0)+1
            else:mismatched.append(r)
        assert len(visible)==30 and min(visible.values())>0
        results[fighter]=dict(nativeShadowRows=len(rows),sourceShadowPoints=len(points),
            exactVisibleBlackPoints=len(points)-len(mismatched),unresolvedCoveredOrMismatchedPoints=len(mismatched),
            fieldsWithVisibleShadowBySlot={str(k):v for k,v in visible.items()},
            allOcclusionsExplained=False,terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_idle_shadow_points_checked';out.mkdir(exist_ok=False)
    report=dict(passedFiniteVisibleShadowPresence=True,results=results,wholeShadowRasterAccepted=False,
        allAnimationShadowAcceptance=False,fullGoalComplete=False,sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:{key:value for key,value in v.items() if key in ('nativeShadowRows','exactVisibleBlackPoints','unresolvedCoveredOrMismatchedPoints')} for k,v in results.items()}))

if __name__=='__main__':main()
