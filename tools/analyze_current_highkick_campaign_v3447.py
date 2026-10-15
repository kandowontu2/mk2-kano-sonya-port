"""Ordered current-campaign outcomes; never equate a kick plan with activation."""
import json
import subprocess
from collections import Counter,defaultdict
from pathlib import Path
import verify_current_campaign_shao_highkick_v3440 as native
import diagnose_current_boss_damage_action_order_v2385 as ordered

ROOT=native.ROOT;need=native.need;sha=native.sha
CAPTURE=ROOT/'audit_v3426_current_sonya_natural_defensive_leg_highkick_campaign'
PROOF=ROOT/'audit_v3446_current_sonya_defensive_leg_campaign_checked/report.json'
OUT=ROOT/'audit_v3448_current_sonya_highkick_campaign_outcomes'

def run():
    need(not OUT.exists(),'Immutable campaign diagnostic')
    proof=json.loads(PROOF.read_text())
    need(proof['passed'] and proof['bounded_campaign_evidence_proven'] and
         proof['current3172WholeGuestAndCampaignAccepted'] and not proof['fullPortAcceptance'],
         'Whole terminal native source/campaign/input proof first')
    logpath=CAPTURE/'run.log';key=str(logpath)
    need(proof['inputHashes'][key]==sha(logpath),'Actual accepted log bytes unchanged')
    rows=native.old.parse(logpath.read_text(encoding='utf-8-sig'),1,'sonya')
    fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
    shao={f:r for f,r in fields.items()if r['stage']==16}
    actions=[r for r in rows if r['tag']=='BOSS_ACTION'and r['stage']==16]
    # Track every action store in original event order, so a same-field update
    # is not incorrectly classified from the frame's earlier action snapshot.
    hits=[r for r in ordered.classify(rows,1)if r['stage']==16]
    grouped=defaultdict(lambda:dict(stores=0,damage=0))
    for hit in hits:
        group=grouped[f"{hit['actualDamageWriterAction']:04X}"]
        group['stores']+=1;group['damage']+=hit['damage']
    plans=[r for r in rows if r['tag']=='BOSS_PLAN'and r['stage']==16]
    inputby=defaultdict(set)
    for row in rows:
        if row['tag']=='INPUT'and row['frame']in shao:inputby[row['frame']].add(row['button'])
    activation=[r for r in actions if r['after']==0x113]
    guest=(CAPTURE/'guest_maincpu.bin').read_bytes()
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    at=(0xff83c330-0xff800000)//8
    need(guest[at:at+4]==original[at:at+4],'Original common native action-store instruction unchanged')
    for row in activation:
        need(row['pc']==0xff83c340 and row['mask']==65535 and row['a1']&65535==0x113 and
             row['a8']==row['actor']and row['a13']==row['main'],
             'Actual native0113 assignment, not a planned or assumed move')
    # A real match clear requires two own wins since the latest loss, followed
    # by native transition. Earlier single wins across paid continues do not sum.
    transition=next((r for r in rows if r['tag']=='STAGE'and r['stage']==16),None)
    need(transition is not None,'Current natural route reaches Shao')
    preceding=[r for r in rows if r['tag']=='LOSS'and r['stage']==15 and r['event']<transition['event']]
    lower=preceding[-1]['event']if preceding else -1
    kintaro=[r for r in rows if r['tag']=='WIN'and r['stage']==15 and r['slot']==1 and lower<r['event']<transition['event']]
    need(len(kintaro)==2 and all(r['id']==18 and r['pc']==0xff8296b0 for r in kintaro),'Two earned current Sonya Kintaro wins in one successful attempt')
    endings=[r for r in rows if r['tag']in('ENDING_START','ENDING_COMPLETED')]
    shao_wins=[r for r in rows if r['tag']=='WIN'and r['stage']==16 and r['slot']==1]
    pins={str(PROOF):sha(PROOF),key:sha(logpath),str(CAPTURE/'guest_maincpu.bin'):sha(CAPTURE/'guest_maincpu.bin'),
          str(ROOT/'mk2/mk2-maincpu.bin'):sha(ROOT/'mk2/mk2-maincpu.bin'),str(Path(__file__).resolve()):sha(__file__),
          str(Path(ordered.__file__).resolve()):sha(ordered.__file__),str(Path(native.__file__).resolve()):sha(native.__file__)}
    return dict(passed=True,candidate='diagnostic_v3172_native_morph_shadow',fighter='sonya',humanSlot=1,cpuSlot=2,
        terminalFrame=next(r['frame']for r in rows if r['tag']=='RESULT'),
        actualCurrentKintaroMatchClear=dict(ownWinFrames=[r['frame']for r in kintaro],nativeStage16Frame=transition['frame']),
        actualShaoRoundWins=len(shao_wins),actualEndingEvents=len(endings),
        actualShaoFields=len(shao),actualPhysicalHighKickPlans=len(plans),actualNative0113Assignments=len(activation),
        plannedMoveNeverAssumedActivated=True,actualShaoDamageByOrderedWriterAction=dict(grouped),
        actualShao0113Damage=sum(r['damage']for r in hits if r['actualDamageWriterAction']==0x113),
        actualShaoPreInputActionDistribution={f'{a:04X}':n for a,n in Counter(r['human_action']for r in shao.values()).items()},
        actualPhysicalKickFields=len([f for f in shao if 'High_Kick'in inputby[f]]),
        actualPhysicalGuardFields=len([f for f in shao if 'Block'in inputby[f]]),
        actualGapRange=[min(r['gap']for r in shao.values()),max(r['gap']for r in shao.values())],
        fullNativeCampaignAndEndingAccepted=proof['unassisted_clear_proven'],
        controllerImprovementAccepted=False,characterGameplayDefectInferredFromControllerFailure=False,
        rawAudioFilesWritten=0,newBuildsOrROMCopies=0,fullPortAcceptance=False,inputHashes=pins,
        nextAction='Use measured activation/range/native block and hurt exposure before designing any successor input policy. Do not change character gameplay or native boss difficulty merely because this controller loses.')

if __name__=='__main__':
    value=run()
    for file,digest in value['inputHashes'].items():need(sha(file)==digest,'Actual diagnostic input unchanged')
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless diagnostic compression')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)
