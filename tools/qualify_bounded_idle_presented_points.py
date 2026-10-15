"""Actual presentation target RGB, with source VRAM and ownership binding."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_idle_scanout_points import check as check_body

def check_point(r,fighter):
    assert r['id']=={'1':str(fighter),'2':'4'}[r['slot']]
    assert int(r['frame'])==int(r['source_frame'])+1
    assert r['predicted']==r['source_vram']==r['display_vram']
    assert r['vram_rgb']==r['actual'] and r['source_matches']==r['display_matches']=='1'

def main():
    root=sync.ROOT;results={};faults=[]
    observer=root/'audit_bounded_idle_presented_points_preparation/prepared_observer.lua'
    lua=observer.read_text();assert 'screen:pixels()' not in lua
    assert 'manager.machine.video:snapshot_pixels()' in lua and ':snapshot(' not in lua
    for fighter,id in (('sonya',18),('kano',17)):
        case=root/f'audit_bounded_{fighter}_idle_presented_points_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        assert terminal['observerSha256']==sync.sha(observer)
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        points=[];body=[];finals=[]
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_IDLE_VRAM_POINT ' in line:check_point(r,id);points.append(r)
            if '_IDLE_ALL_DRAW_FINAL ' in line:assert r['match']=='1' and r['final']==r['actual'];finals.append(r)
            if '_IDLE_SCANPOINT ' in line and r['kind']=='body':check_body(r,id);body.append(r)
        assert len(points)==len(finals)=={'sonya':1938,'kano':1958}[fighter] and len(body)==60
        assert len({(r['source_frame'],r['slot']) for r in points})==30
        for key,value in [('actual','FFFFFF'),('source_vram','999'),('frame','9999'),('id','1')]:
            mutant=dict(points[0]);mutant[key]=value
            try:check_point(mutant,id)
            except AssertionError:faults.append(fighter+'_'+key)
            else:raise AssertionError('Ineffective mutation')
        for r in points:check_point(r,id)
        results[fighter]=dict(presentationShadowQueryPoints=len(points),bodyBottomPoints=60,
            unresolvedPresentationPoints=0,terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_idle_presented_points_checked';out.mkdir(exist_ok=False)
    report=dict(passed=True,results=results,rejectedFaults=faults,
        priorScreenPixelsReportsAreCurrentDrawBitmapNotPresentation=True,
        finiteIdleQueryPresentationProven=True,entireShadowRasterProven=False,
        allAnimationArenaCoverageProven=False,fullGoalComplete=False,sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)),
        sourceHashes={str(root/p):sync.sha(root/p) for p in ('mame-mkp/src/emu/screen.cpp','mame-mkp/src/emu/video.cpp','mame-mkp/src/frontend/mame/luaengine.cpp')})
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,presentationShadowPoints=3896,bodyBottomPoints=120,unresolved=0,faults=len(faults))))

if __name__=='__main__':main()
