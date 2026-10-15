"""Natural jump/landing and actual presentation; distinguish replay gaps."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify
from qualify_bounded_idle_scanout_points import check as check_body

def main():
    root=sync.ROOT;results={};payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes()
    for fighter,id,mainroot in (('sonya',18,0xff020000),('kano',17,0xff000000)):
        case=root/f'audit_bounded_{fighter}_aerial_motion_points_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        assert 'IDLE_TERMINAL frame=1484' in text
        points=[];body=[];fields=[];inputs=[];poses=set();unresolved=[]
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_IDLE_VRAM_POINT ' in line:
                assert r['id']=={'1':str(id),'2':'4'}[r['slot']]
                assert int(r['frame'])==int(r['source_frame'])+1
                assert r['source_vram']==r['display_vram'] and r['vram_rgb']==r['actual'] and r['display_matches']=='1'
                assert int(r['source_matches'])==int(r['predicted']==r['source_vram'])
                points.append(r)
                if r['source_matches']=='0':unresolved.append(r)
            if '_IDLE_SCANPOINT ' in line and r['kind']=='body':check_body(r,id);body.append(r)
            if '_FIELD ' in line:
                assert r['id']=={'1':str(id),'2':'4'}[r['slot']] and r['roster']==r['id']
                assert r['state']=='1' and r['owner']==r['actor'] and r['hp']=='161';fields.append(r)
                if r['slot']=='1':poses.add(r['pose'])
            if '_INPUT ' in line and int(r['frame'])>=1304:inputs.append(r)
        assert len(fields)==360
        expected=[(1304+a,b) for start,stop,buttons in ((8,12,['Up']),(72,76,['Up','Right'])) for a in range(start,stop) for b in buttons]
        assert [(int(r['frame']),r['button']) for r in inputs]==expected and all(r['slot']=='1' for r in inputs)
        own=[r for r in fields if r['slot']=='1']
        for low,high in ((1313,1367),(1377,1431)):
            episode=[r for r in own if low<=int(r['frame'])<=high]
            assert any(r['y']!=r['floor'] and int(r['vy'],16)!=0 for r in episode)
        assert all(r['y']==r['floor'] and int(r['vy'],16)==int(r['gravity'],16)==0 for r in own[-20:])
        census=classify(payload,0xfe800000,mainroot,sorted(poses));animations=sorted({a for refs in census.values() for a in refs})
        assert {0,6}.issubset(animations) and ({7,8}&set(animations)),animations
        assert len(points)>2000 and len(body)>=80
        results[fighter]=dict(ownedActorFields=360,physicalJumpInputs=12,nativeAirborneEpisodes=2,finalGroundedFields=20,
            exactPresentationVRAMPoints=len(points),bodyBottomPoints=len(body),unresolvedDMAPredictionPoints=unresolved,
            observedMainAnimationReferences=animations,terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_aerial_motion_points_checked';out.mkdir(exist_ok=False)
    report=dict(passedJumpLandingAndVRAMPresentation=True,results=results,entireDrawReplayProven=False,
        wholeShadowAcceptance=False,allStatesArenasProven=False,fullGoalComplete=False,
        sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:dict(presentationPoints=v['exactPresentationVRAMPoints'],bodyPoints=v['bodyBottomPoints'],unresolved=len(v['unresolvedDMAPredictionPoints']),animations=v['observedMainAnimationReferences']) for k,v in results.items()}))

if __name__=='__main__':main()
