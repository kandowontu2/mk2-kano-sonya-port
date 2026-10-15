"""Actual uppercut entry art, native damage/flight/get-up and presentation."""
import json,re,struct
from pathlib import Path
import verify_native_source_sync as sync
from classify_observed_native_pose_sequences import classify

def main():
    root=sync.ROOT;results={};payload=(sync.BUILD/'roms/mk2ks/mk2ks.mdata').read_bytes()
    stock=(root/'mk2/mk2-maincpu.bin').read_bytes();stockroot=struct.unpack_from('<I',stock,0x020c2a+4*4)[0]
    for fighter,id,mainroot in (('sonya',18,0xff020000),('kano',17,0xff000000)):
        case=root/f'audit_bounded_{fighter}_settled_uppercut_recovery_runtime'
        terminal=json.loads((case/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<320*1024*1024
        text=(case/'run.log').read_text();assert '[LUA ERROR]' not in text and '_FAILED ' not in text
        assert 'IDLE_TERMINAL frame=1544' in text
        own=[];victim=[];health=[];points=[];inputs=[];gaps=[]
        for line in text.splitlines():
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if '_FIELD ' in line:
                assert r['id']=={'1':str(id),'2':'4'}[r['slot']] and r['roster']==r['id']
                assert r['state']=='1' and r['owner']==r['actor'] and int(r['hp'])>0
                (own if r['slot']=='1' else victim).append(r)
            if '_CONTACT_HEALTH ' in line:health.append(r)
            if '_IDLE_VRAM_POINT ' in line:
                assert r['source_vram']==r['display_vram'] and r['vram_rgb']==r['actual'] and r['display_matches']=='1'
                assert int(r['frame'])==int(r['source_frame'])+1;points.append(r)
                if r['source_matches']=='0':gaps.append(r)
            if '_INPUT ' in line and int(r['frame'])>=1304:inputs.append(r)
        assert len(own)==len(victim)==240 and len(health)==1
        event=health[0];assert event['slot']=='1' and event['before']=='161' and event['after']=='121' and event['pc']=='FF836700' and event['mask']=='FFFF'
        strike=int(event['frame']);assert strike==1424
        punches=[r for r in inputs if r['button']=='High_Punch'];downs=[r for r in inputs if r['button']=='Down']
        assert [(int(r['frame']),r['slot']) for r in punches]==[(1304+a,'2') for a in range(112,116)]
        assert [(int(r['frame']),r['slot']) for r in downs]==[(1304+a,'2') for a in range(96,124)]
        assert {r['floor'] for r in own}=={own[0]['floor']}
        airborne=[r for r in own if int(r['frame'])>strike and int(r['y'])<int(r['floor']) and int(r['vy'],16)!=0]
        assert len(airborne)>20
        assert all(r['y']==r['floor'] and int(r['vx'],16)==int(r['vy'],16)==int(r['gravity'],16)==0 and r['hp']=='121' for r in own[-20:])
        assert all(r['hp']=='161' for r in victim)
        census=classify(payload,0xfe800000,mainroot,sorted({r['pose'] for r in own}))
        stockcensus=classify(stock,0xff800000,stockroot,sorted({r['pose'] for r in victim}))
        animations=sorted({a for refs in census.values() for a in refs});stockanimations=sorted({a for refs in stockcensus.values() for a in refs})
        assert {0,15,18}.issubset(animations),animations
        assert 28 in stockanimations,stockanimations
        assert len(points)>3000
        results[fighter]=dict(damage=event,nativeAirborneFields=len(airborne),finalRecoveredFields=20,
            unchangedFloor=int(own[0]['floor']),exactPresentedVRAMPoints=len(points),
            addedAnimationReferences=animations,stockAnimationReferences=stockanimations,
            unresolvedAllDrawPredictionPoints=gaps,terminal=terminal,logSha=sync.sha(case/'run.log'))
    out=root/'audit_bounded_settled_uppercut_recovery_checked';out.mkdir(exist_ok=False)
    report=dict(passedFiniteUppercutKnockdownRecovery=True,results=results,
        entireArtLayerReplayProven=False,allReactionStatesArenasProven=False,fullGoalComplete=False,
        sourceSync=sync.verify(),checkerSha=sync.sha(Path(__file__)))
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:dict(airborne=v['nativeAirborneFields'],floor=v['unchangedFloor'],presentationPoints=v['exactPresentedVRAMPoints'],animations=v['addedAnimationReferences'],unresolved=len(v['unresolvedAllDrawPredictionPoints'])) for k,v in results.items()}))

if __name__=='__main__':main()
