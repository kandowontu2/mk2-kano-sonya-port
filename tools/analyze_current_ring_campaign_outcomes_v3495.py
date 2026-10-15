"""Actual native Ring entries and ordered damage; never infer child ownership."""
import json,subprocess
from collections import Counter,defaultdict
from pathlib import Path
import verify_current_campaign_shao_ring_retreat_v3491 as native
import diagnose_current_boss_damage_action_order_v2385 as ordered
ROOT=native.ROOT;need=native.need;sha=native.sha
CASE=ROOT/'audit_v3490_current_sonya_natural_ring_retreat_campaign'
PROOF=ROOT/'audit_v3494_current_sonya_ring_campaign_checked/report.json'
OUT=ROOT/'audit_v3496_current_ring_campaign_outcomes'
def main():
    need(not OUT.exists(),'Immutable Ring outcome evidence')
    proof=json.loads(PROOF.read_text())
    need(proof['passed'] and proof['current3172WholeGuestAndCampaignAccepted'] and not proof['fullPortAcceptance'],
       'Whole actual source/input/native campaign proof first')
    logpath=CASE/'run.log';need(sha(logpath)==proof['inputHashes'][str(logpath)],'Accepted actual terminal log unchanged')
    rows=native.old.parse(logpath.read_text(encoding='utf-8-sig'),1,'sonya')
    fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD' and r['stage']==16}
    need(fields,'Actual natural Shao reached')
    entries=[r for r in rows if r['tag']=='SPECIAL' and r['stage']==16]
    for r in entries:
        need(r['move']=='ring' and r['entry']==0xffffb400 and r['at']==0xffffb410 and r['pc']==0xffffb420
           and r['id']==r['roster']==18 and r['actor']==r['a8'] and r['main']==r['a13'],
           'Actual dedicated true18 Ring instruction and human actor/Main registers, not a command plan')
    hits=[r for r in ordered.classify(rows,1)if r['stage']==16]
    grouped=defaultdict(lambda:dict(stores=0,damage=0))
    for r in hits:
        g=grouped[f"{r['actualDamageWriterAction']:04X}"];g['stores']+=1;g['damage']+=r['damage']
    # Every original opponent collision store is counted, but only the ordered
    # human-actor/Main subset is attributable from this observer. Child A8/A13
    # pointers alone cannot establish a Ring parent or native guard branch.
    all_damage=[r for r in rows if r['tag']=='HEALTH' and r['frame']in fields and r['slot']==2
        and r['pc']==0xff836700 and r['after']<r['before']]
    owned_events={r['event']for r in hits}
    unclassified=[dict(frame=r['frame'],event=r['event'],a8=r['a8'],a13=r['a13'],damage=r['before']-r['after'])
       for r in all_damage if r['event']not in owned_events]
    plans=[r for r in rows if r['tag']=='BOSS_PLAN' and r['stage']==16]
    commandplans=[r for r in plans if r['move']=='shao_ring_command_attempt']
    jumpplans=[r for r in plans if r['move']=='shao_ring_retreat_jump_attempt']
    transition=next(r for r in rows if r['tag']=='STAGE' and r['stage']==16)
    lower=max([r['event']for r in rows if r['tag']=='LOSS' and r['stage']==15 and r['event']<transition['event']]+[-1])
    kintaro=[r for r in rows if r['tag']=='WIN' and r['stage']==15 and r['slot']==1 and lower<r['event']<transition['event']]
    need(len(kintaro)==2 and all(r['id']==18 and r['pc']==0xff8296b0 for r in kintaro),'Two real native Kintaro wins in one successful attempt')
    wins=[r for r in rows if r['tag']=='WIN' and r['stage']==16 and r['slot']==1]
    endings=[r for r in rows if r['tag']in('ENDING_START','ENDING_COMPLETED')]
    earned_match=[]
    if proof['unassisted_clear_proven']:
        start=next(r for r in endings if r['tag']=='ENDING_START')
        last_loss=max([r['event']for r in rows if r['tag']=='LOSS' and r['stage']==16 and r['event']<start['event']]+[-1])
        earned_match=[r for r in wins if last_loss<r['event']<start['event']]
        need(len(earned_match)==2 and all(r['id']==18 and r['pc']==0xff8296b0 for r in earned_match),
           'Exactly two earned own Shao wins in one successful attempt before native ending; never combine paid losses')
    pins={str(p.resolve()):sha(p)for p in(PROOF,logpath,CASE/'guest_maincpu.bin',Path(__file__),Path(native.__file__),Path(ordered.__file__))}
    value=dict(passed=True,candidate='diagnostic_v3172_native_morph_shadow',fighter='sonya',humanSlot=1,cpuSlot=2,
       actualCurrentKintaroMatchClear=dict(ownWinFrames=[r['frame']for r in kintaro],nativeStage16Frame=transition['frame']),
       actualShaoFields=len(fields),actualPhysicalRingCommandPlans=len(commandplans),actualPhysicalRetreatJumpPlans=len(jumpplans),
       actualNativeOwnedShaoRingEntries=len(entries),actualNativeOwnedShaoRingEntryFrames=[r['frame']for r in entries],
       actualShaoDamageByOrderedHumanWriterAction=dict(grouped),
       actualOpponentCollisionStores=len(all_damage),actualOpponentCollisionDamage=sum(r['before']-r['after']for r in all_damage),
       humanAttributedCollisionStores=len(hits),humanAttributedCollisionDamage=sum(r['damage']for r in hits),
       unclassifiedCollisionStores=unclassified,unclassifiedCollisionDamage=sum(r['damage']for r in unclassified),
       actualShaoRoundWins=len(wins),actualShaoOwnWinFrames=[r['frame']for r in wins],actualEndingEvents=len(endings),
       actualSuccessfulShaoMatchWinFrames=[r['frame']for r in earned_match],
       nativeShaoMatchNeverInferredFromOneRoundOrAccumulatedContinues=True,
       nativeCampaignClearProven=proof['unassisted_clear_proven'],
       commandPlansNotAssumedActivations=True,entryNotAssumedChildCollisionOwnershipOrGuard=True,
       childParentGuardBranchAndFullRingRuntimeContactProven=False,
       observedNativeDamageHistogram=dict(Counter(r['before']-r['after']for r in all_damage)),
       controllerImprovementAccepted=False,characterGameplayDefectInferredFromControllerFailure=False,
       rawAudioFilesWritten=0,newBuildsOrROMCopies=0,fullPortAcceptance=False,inputHashes=pins,
       nextAction='Use actual Ring activation and observed original collision damage/wins/ending outcome. If child A8/Main cannot be attributed, a fresh read-only child/parent/guard/native damage trace is required; do not infer hit ownership from temporal proximity or change game power/AI/difficulty.')
    for file,digest in pins.items():need(sha(file)==digest,'Actual accepted diagnostic inputs unchanged')
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless Ring outcome evidence')
    print(json.dumps({k:v for k,v in value.items()if k not in('inputHashes','unclassifiedCollisionStores','actualNativeOwnedShaoRingEntryFrames')},indent=2),flush=True)
if __name__=='__main__':main()
