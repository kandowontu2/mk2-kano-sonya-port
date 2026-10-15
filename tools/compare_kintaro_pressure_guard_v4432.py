"""Independently replay actual Kintaro guard/release; native outcomes only."""
import collections,json,subprocess
from pathlib import Path
import verify_kintaro_pressure_guard_whole_campaign_v4430 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OLD=ROOT/'audit_v4304_sonya_shang_jump_retry_p2_campaign'
NEW=current.FOLDER
OUT=ROOT/'audit_v4433_kintaro_pressure_guard_native_comparison'

def controls(text):
    rows=current.spacing.parse(text)
    fields=[r for r in rows if r['tag']=='BOSS_FIELD' and r['stage']=='15']
    inputs=collections.defaultdict(list);plans={}
    for r in rows:
        if r['tag']=='INPUT':inputs[r['frame']].append(r['button'])
        if r['tag']=='BOSS_PLAN' and r['stage']=='15':plans[r['frame']]=r
    last=None;command=previous=jump=-1000;direction=None;down=None
    wait=[];guard_jumps=[];facing=[]
    for f in fields:
        frame=f['frame'];need(f['human_id']=='18' and f['cpu_id']=='12' and
          f['writes']=='0' and f['assistance']=='none','Actual native Sonya18/Kintaro12, no input intent credited')
        if last is None or frame-last!=1:command=previous=jump=-1000;direction=None;down=None
        last=frame;h=int(f['height']);a=int(f['human_action']);ca=int(f['cpu_action'])
        flags=int(f['flags'],16);body=int(f['body'],16);gap=int(f['gap']);ch=int(f['cpu_height'])
        stance=h==0 and flags&0x0c==0 and body&0x0c==0 and a in (0x303,0x302,0x304)
        forward='Right' if int(f['h_x'])<int(f['c_x']) else 'Left'
        expected=[];planned=None
        if frame-command<36:
            age=frame-command
            if a!=0x107 and not stance:expected=['Down','Block'];command=-1000;down=None
            else:
                if down is None:down=frame
                expected=['Down']
                if age<=2:expected.append('High_Punch')
        elif frame-jump<16:down=None;expected=['Up',direction]
        elif h>8:
            down=None
            if frame-jump<48:expected.append(direction)
            if int(f['human_vy'],16)<0x80000000 and frame%6<3:expected.append('High_Kick')
        elif ca==0x407:
            if down is None:down=frame
            expected=['Down']
            if (stance and gap<95 and frame-down>=12 and frame-previous>=30 and
              0<int(f['cpu_vy'],16)<0x80000000 and 160<ch<=240):
                planned='descending_stomp_uppercut_attempt';command=previous=frame;expected.append('High_Punch')
        elif gap<170:
            if down is None:down=frame
            ready=stance or(h==0 and flags&0x0c==0 and body&0x0c==0 and a in (0x700,0x701))
            expected=['Down','Block']
            if ready and frame-down>=12 and gap<145 and ch<20 and frame-jump>=60:
                planned='close_pressure_jumpkick_attempt';jump=frame;direction=forward;down=None;expected=['Up',direction]
                if a in (0x700,0x701):guard_jumps.append(frame)
                facing.append(frame)
            else:wait.append(frame)
        else:expected=['Down','Block'];down=None
        need(inputs[frame]==expected,'Every actual Kintaro guard/release/stomp/late-kick input independently replayed at '+str(frame))
        need((frame in plans)==(planned is not None),'Actual pressure/stomp plan exists exactly when native state permits an input attempt')
        if planned:
            need(plans[frame]['move']==planned and plans[frame]['direction']==(direction if planned=='close_pressure_jumpkick_attempt' else 'none'),
              'Actual plan label and forward direction agree with independent native state')
    need(wait and guard_jumps and facing,'Real pressure waiting and actual native block-to-jump input attempts required')
    moves=[r for r in rows if r['tag']=='BOSS_ACTION' and r['stage']=='15' and int(r['after']) in (0x308,0x200)]
    for r in moves:
        need(r['id']==r['roster']=='18' and r['actor']==r['owner']==r['a8'] and r['main']==r['a13'] and
          int(r['at'],16)==int(r['main'],16)+0x1f0 and r['mask']=='FFFF' and
          r['pc']==('FF831360' if int(r['after'])==0x308 else 'FF871F50'),
          'Actual original native jump/airkick setter and owned task, not sampled hurt/throw motion')
    need(any(int(r['after'])==0x308 for r in moves) and any(int(r['after'])==0x200 for r in moves),
      'Genuine native jump and airkick writers, not planned input counts')
    return dict(pressureGuardWaitFields=len(wait),firstPressureGuardWaitFrame=wait[0],
      actualGuardToJumpInputPlans=len(guard_jumps),firstGuardToJumpPlanFrame=guard_jumps[0],
      actualForwardPressurePlans=len(facing),actualNativeJumpWriters=sum(int(r['after'])==0x308 for r in moves),
      actualNativeAirKickWriters=sum(int(r['after'])==0x200 for r in moves),
      plansNeverAssumedActivations=True,nonActorStoresNeverCreditedAsActivations=True)

def main():
    need(not OUT.exists(),'Fresh immutable actual guard/release comparison')
    paths=[ROOT/'audit_v4309_shang_jump_retry_whole_campaign_checked/report.json',
      ROOT/'audit_v4431_kintaro_pressure_guard_whole_campaign_checked/report.json']
    proofs=[json.loads(p.read_text()) for p in paths]
    need(all(p['passed'] and p['case']['passed'] and p['case']['actualWholeCampaignGrammarRetained'] for p in proofs),
      'Both original full native campaigns and physical grammars qualified first')
    old=(OLD/'run.log').read_text();new=(NEW/'run.log').read_text();positive=controls(new)
    oldrows=current.spacing.parse(old);newrows=current.spacing.parse(new)
    original_inputs=collections.defaultdict(list);new_inputs=collections.defaultdict(list)
    for r in oldrows:
        if r['tag']=='INPUT':original_inputs[r['frame']].append(r['button'])
    for r in newrows:
        if r['tag']=='INPUT':new_inputs[r['frame']].append(r['button'])
    first=min(f for f in set(original_inputs)|set(new_inputs) if original_inputs[f]!=new_inputs[f])
    a=[r for r in oldrows if r['frame']<first];b=[r for r in newrows if r['frame']<first]
    need(a and a==b,'All actual native observations before first changed input identical')
    outcomes=[]
    for rows in (oldrows,newrows):
        wins=[r for r in rows if r['tag']=='WIN' and r['stage']=='15' and r['slot']=='2']
        outcomes.append(dict(actualOwnKintaroRoundWins=len(wins),
          actualKintaroPaidLosses=sum(r['tag']=='LOSS' and r['stage']=='15' for r in rows),
          actualOwnKintaroRoundResults=wins,actualShaoStageEntered=any(r['tag']=='STAGE' and r['stage']=='16' for r in rows),
          actualEndingStarts=sum(r['tag']=='ENDING_START' for r in rows),actualEndingCompletions=sum(r['tag']=='ENDING_COMPLETED' for r in rows)))
    faults=[]
    for tag,frame,key,value in [('INPUT',positive['firstPressureGuardWaitFrame'],'button','High_Punch'),
      ('BOSS_FIELD',positive['firstPressureGuardWaitFrame'],'human_id','0'),
      ('BOSS_FIELD',positive['firstGuardToJumpPlanFrame'],'human_action','0'),
      ('BOSS_PLAN',positive['firstGuardToJumpPlanFrame'],'direction','none')]:
        try:controls(current.physical.change(new,tag,frame,key,value))
        except Exception as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
        else:raise ValueError('Actual pressure guard/input/readiness/plan fault accepted')
    pins={}
    for proof in proofs:
        for p,h in proof['case']['inputHashes'].items():
            need(p not in pins or pins[p]==h,'Exact shared original inputs');pins[p]=h
    for p in (*paths,Path(__file__).resolve(),Path(current.__file__).resolve(),OLD/'run.log',NEW/'run.log'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual source/evidence/public input byte unchanged')
    return dict(passed=True,actualNativeControls=positive,firstChangedInputFrame=first,identicalNativePrefixRows=len(a),
      originalOutcome=outcomes[0],pressureGuardOutcome=outcomes[1],actualFaultsRejected=faults,inputHashes=pins,
      naturalTowerClearAccepted=proofs[1]['actualNaturalSonyaP2TowerClearAccepted'],
      pressureGuardPolicyPromoted=outcomes[1]['actualShaoStageEntered'],
      comparisonNotStatisticalAIDominance=True,nativeFloorShadowArtAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    report=main();OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
