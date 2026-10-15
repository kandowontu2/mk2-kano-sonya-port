"""Native two-way contact and recovery with finite actual presentation checks."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify

def main():
    root=sync.ROOT;results={};payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes()
    for fighter,id,mainroot in (('sonya',18,0xff020000),('kano',17,0xff000000)):
        case=root/f'audit_bounded_{fighter}_contact_reapproach_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        assert 'IDLE_TERMINAL frame=1544' in text
        fields=[];health=[];points=[];inputs=[];poses=set();gaps=[]
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_FIELD ' in line:
                assert r['id']=={'1':str(id),'2':'4'}[r['slot']] and r['roster']==r['id']
                assert r['state']=='1' and r['owner']==r['actor'] and int(r['hp'])>0
                fields.append(r)
                if r['slot']=='1':poses.add(r['pose'])
            if '_CONTACT_HEALTH ' in line:
                assert r['pc']=='FF836700' and r['mask']=='FFFF' and int(r['after'])<int(r['before']);health.append(r)
            if '_IDLE_VRAM_POINT ' in line:
                assert r['source_vram']==r['display_vram'] and r['vram_rgb']==r['actual'] and r['display_matches']=='1'
                assert int(r['frame'])==int(r['source_frame'])+1;points.append(r)
                if r['source_matches']=='0':gaps.append(r)
            if '_INPUT ' in line and int(r['frame'])>=1304:inputs.append(r)
        assert len(fields)==480 and len({(r['frame'],r['slot']) for r in fields})==480
        assert len(health)==2 and [r['slot'] for r in health]==['1','2']
        assert all(r['before']=='161' for r in health)
        first,second=int(health[0]['frame']),int(health[1]['frame']);assert first<second
        own=[r for r in fields if r['slot']=='1'];victim=[r for r in fields if r['slot']=='2']
        assert own[-1]['hp']==health[0]['after'] and victim[-1]['hp']==health[1]['after']
        for actors in (own,victim):
            assert all(r['y']==r['floor'] and int(r['vy'],16)==int(r['gravity'],16)==0 for r in actors[-3:])
        highpunch=[r for r in inputs if r['button']=='High_Punch']
        assert [(int(r['frame']),r['slot']) for r in highpunch]==[(1304+a,'2') for a in range(112,116)]+[(1304+a,'1') for a in range(200,204)]
        assert all(r['button'] in ('Right','Left','High_Punch') for r in inputs)
        census=classify(payload,0xfe800000,mainroot,sorted(poses));animations=sorted({a for refs in census.values() for a in refs})
        assert 0 in animations and 1 in animations and ({15,16,17}&set(animations)) and ({19,20,35}&set(animations)),animations
        reactions=[r for r in own if first<=int(r['frame'])<first+32 and ({15,16,17}&set(census[r['pose']]))]
        assert reactions and len(points)>3000
        results[fighter]=dict(nativeDamageWrites=health,ownedActorFields=480,exactPresentedVRAMPoints=len(points),
            observedMainAnimationReferences=animations,actualReactionFields=len(reactions),
            unresolvedAllDrawPredictionPoints=gaps,terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_contact_reapproach_checked';out.mkdir(exist_ok=False)
    result=dict(passedTwoWayContactOwnershipAndPresentation=True,results=results,
        entireArtLayerReplayProven=False,allReactionsArenasMovesProven=False,fullGoalComplete=False,
        sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:dict(health=v['nativeDamageWrites'],presentationPoints=v['exactPresentedVRAMPoints'],animations=v['observedMainAnimationReferences'],unresolved=len(v['unresolvedAllDrawPredictionPoints'])) for k,v in results.items()}))

if __name__=='__main__':main()
