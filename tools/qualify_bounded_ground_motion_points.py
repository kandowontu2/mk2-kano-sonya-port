"""Finite physical ground-motion source and actual presentation checks."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify
from qualify_bounded_idle_presented_points import check_point
from qualify_bounded_idle_scanout_points import check as check_body

def main():
    root=sync.ROOT;results={}
    payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes()
    for fighter,id,mainroot in (('sonya',18,0xff020000),('kano',17,0xff000000)):
        case=root/f'audit_bounded_{fighter}_ground_motion_points_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        assert 'IDLE_TERMINAL frame=1484' in text
        points=[];body=[];fields=[];inputs=[];poses=set()
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_IDLE_VRAM_POINT ' in line:check_point(r,id);points.append(r)
            if '_IDLE_SCANPOINT ' in line and r['kind']=='body':check_body(r,id);body.append(r)
            if '_FIELD ' in line:
                assert r['id']=={'1':str(id),'2':'4'}[r['slot']] and r['roster']==r['id']
                assert r['state']=='1' and r['owner']==r['actor'] and r['hp']=='161'
                fields.append(r)
                if r['slot']=='1':poses.add(r['pose'])
            if '_INPUT ' in line and int(r['frame'])>=1304:inputs.append(r)
        assert len(fields)==360 and len({(r['frame'],r['slot']) for r in fields})==360
        expected={}
        for start,stop,button in ((8,24,'Right'),(32,48,'Left'),(64,80,'Down'),(96,100,'High_Kick')):
            for age in range(start,stop):expected[1304+age]=button
        assert len(inputs)==len(expected)==52
        assert {int(r['frame']):r['button'] for r in inputs}==expected and all(r['slot']=='1' for r in inputs)
        census=classify(payload,0xfe800000,mainroot,sorted(poses))
        animations=sorted({a for refs in census.values() for a in refs})
        assert {0,1,3,5,13}.issubset(animations),animations
        assert len(points)>2000 and len(body)>=80
        results[fighter]=dict(ownedActorFields=360,physicalMotionInputs=52,presentedShadowQueryPoints=len(points),
            presentedBodyBottomPoints=len(body),observedMainAnimationReferences=animations,poseReferenceCensus=census,
            terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_ground_motion_points_checked';out.mkdir(exist_ok=False)
    report=dict(passed=True,results=results,finiteWalkCrouchKickPresentationProven=True,
        allMovesStatesArenasProven=False,fullGoalComplete=False,sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a in ('presentedShadowQueryPoints','presentedBodyBottomPoints','observedMainAnimationReferences')} for k,v in results.items()}))

if __name__=='__main__':main()
