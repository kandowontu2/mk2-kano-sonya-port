"""Actual unassisted CPU Sonya ordinary throws use living Kano's own ROM poses."""
import json,re
from pathlib import Path
import verify_native_ground_throw_campaign_v1612 as campaign
import verify_native_ground_throw_humans_v1606 as human
import verify_native_ground_throw_source_v1598 as source
ROOT=source.ROOT
OUT=ROOT/'audit_v1615_native_cpu_ground_throw_checked'
def verify():
    folder=ROOT/'audit_v1604_kano_p2_throw_cpu_campaign';pins={}
    campaign.matched(folder,pins)
    path=ROOT/'audit_v1612_ground_throw_campaign_checked/report.json'
    bounded=json.loads(path.read_text());assert bounded['passed'] and not bounded['unassisted_clear_proven']
    pins[str(path.resolve())]=campaign.digest(path)
    guest,_,payload=source.expected()
    log=folder/'run.log';before=campaign.digest(log)
    text=log.read_text(encoding='utf-8-sig');rows=campaign.parse(text,2,'kano')
    live=[r for r in rows if r['tag']=='LIVE' and r['stage']==3 and r['cpu']=='18:18']
    assert live and all(r['human']=='17:17' for r in live)
    held=[r for r in live if r['actions']=='0,1287']
    assert len(held)>=2
    main43={0xff0126e0,0xff012720,0xff012760,0xff0127c0}
    evidence=[]
    for r in held:
        poses=tuple(int(v,16) for v in r['poses'].split(','))
        hp=tuple(int(v)for v in r['health'].split(','))
        assert hp[0]>0 and r['human_actor']==0x01033e10 and r['cpu_actor']==0x01033c00
        assert not(int(r['flags'].split(',')[0],16)&4)==False
        parts=human.pose_sources(poses[0],payload,guest)
        assert all(not(0x1ec0000*8<=p['source']<0x1ee0000*8)for p in parts)
        evidence.append(dict(frame=r['frame'],humanID=17,cpuID=18,positiveHumanHealth=hp[0],
          actualKanoPose=hex(poses[0]),actualCPUAction=0x507,
          insideNativeMain43HeldPhase=poses[0] in main43,
          nativeFloor=r['hfloor'],physicalPosition=r['hpos'],sources=[hex(p['source'])for p in parts]))
    assert sum(r['insideNativeMain43HeldPhase']for r in evidence)>=2
    damage=[r for r in rows if r['tag']=='HEALTH' and 8895<=r['frame']<=10881 and r['slot']==2 and
            r['before']-r['after']==32 and r['pc']==0xff836700 and r['a8']==0x01033e10]
    assert len(damage)>=2
    for r in live:
        pose=int(r['poses'].split(',')[0],16)
        assert all(not(0x1ec0000*8<=p['source']<0x1ee0000*8)for p in human.pose_sources(pose,payload,guest))
    assert campaign.digest(log)==before;pins[str(log.resolve())]=before
    for module in(campaign,human,source):pins[str(Path(module.__file__).resolve())]=campaign.digest(Path(module.__file__))
    pins[str(Path(__file__).resolve())]=campaign.digest(Path(__file__))
    return dict(passed=True,candidate=source.NAME,trueCPU18ThrowsTrueHuman17=True,
       actualHeldAndRecoveryObservations=evidence,actualNative32PointThrowContacts=len(damage),
       noHeadlessGraphicsInObservedLivingKanoPoses=True,nativeOwnStage3RoundWins=2,
       inputOnly=True,capturedEvidenceChanged=False,inputHashes=pins,
       completeCPUHeldRasterChoreographyProven=False,fullPortAcceptance=False,
       scope='Real CPU throw state/ROM pose/damage proof, not every held field or whole-port fidelity')
if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
