"""Actual native Ring entries and ordered damage; never infer child ownership."""
import json,subprocess
from collections import Counter,defaultdict
from pathlib import Path
import verify_current_campaign_shao_ring_retreat_v3491 as native
import diagnose_current_boss_damage_action_order_v2385 as ordered
ROOT=native.ROOT;need=native.need;sha=native.sha
CASE=ROOT/'audit_v3490_current_sonya_natural_ring_retreat_campaign'
PROOF=ROOT/'audit_v3494_current_sonya_ring_campaign_checked/report.json'
OUT=ROOT/'audit_v3503_current_ring_deciding_route_outcomes'
def final_contract(rows):
    start=next(r for r in rows if r['tag']=='ENDING_START')
    last_loss=max([r['event']for r in rows if r['tag']=='LOSS' and r['stage']==16 and r['event']<start['event']]+[-1])
    attempt=[r for r in rows if last_loss<r['event']<start['event']]
    fields={r['frame']:r for r in attempt if r['tag']=='BOSS_FIELD' and r['stage']==16}
    kos=[r for r in attempt if r['tag']=='HEALTH' and r['slot']==2 and r['frame']in fields
        and r['pc']==0xff836700 and r['before']>0 and r['after']==0]
    need(len(kos)==2,'Exactly two real original-collision Shao KOs since latest paid loss')
    for ko in kos:
        f=fields[ko['frame']]
        need(f['human_id']==18 and f['cpu_id']==13 and int(f['health'].split(',')[0])>0,
             'Each actual boss KO belongs to live true Sonya versus scheduled Shao')
    ordinary=[r for r in attempt if r['tag']=='WIN' and r['slot']==1 and r['stage']==16]
    first_transition=next(r for r in attempt if r['tag']=='STATE' and r['frame']>kos[0]['frame'])
    need(len(ordinary)==1 and ordinary[0]['frame']==first_transition['frame'] and ordinary[0]['id']==18
       and ordinary[0]['pc']==0xff8296b0 and first_transition['mode']==5 and first_transition['winner']==1
       and first_transition['health']==ordinary[0]['health'],
       'First real Shao KO has own winner-table call at next native round-result transition, not collision field')
    final=kos[-1]
    transition=next(r for r in attempt if r['tag']=='STATE' and r['frame']>final['frame'])
    need(transition['mode']==11 and transition['winner']==1 and transition['roster']=='18,13'
       and transition['health'].endswith(',0') and int(transition['health'].split(',')[0])>0,
       'Deciding native collision KO followed by owned boss-death mode11, never an assumed normal WIN-table call')
    need(start['winner']==1 and start['roster']==18 and start['actors']=='00000000,00000000'
       and start['health']==transition['health'],'Same final native health and owned retirement enter own ending')
    return dict(actualSuccessfulShaoMatchKOFrames=[r['frame']for r in kos],
       firstRoundOwnWinnerTableFrame=ordinary[0]['frame'],decidingKOHasNoOrdinaryWinnerTableCall=True,
       firstRoundNativeResultTransitionFrame=first_transition['frame'],
       finalNativeBossDeathTransitionFrame=transition['frame'],finalNativeEndingRetirementFrame=start['frame'],
       finalNativeHealth=start['health'])
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
    earned_match={};faults=[]
    if proof['unassisted_clear_proven']:
        earned_match=final_contract(rows)
        final_frame=earned_match['actualSuccessfulShaoMatchKOFrames'][-1]
        native_transition=earned_match['finalNativeBossDeathTransitionFrame']
        variants=[]
        variants.append(('missing_actual_deciding_collision_KO',[r for r in rows if not(r['tag']=='HEALTH' and r['frame']==final_frame and r['slot']==2 and r['after']==0)],'Exactly two real original-collision Shao KOs'))
        changed=[dict(r)for r in rows]
        next(r for r in changed if r['tag']=='STATE' and r['frame']==native_transition)['winner']=2
        variants.append(('wrong_actual_boss_death_winner',changed,'Deciding native collision KO followed by owned boss-death'))
        changed=[dict(r)for r in rows]
        next(r for r in changed if r['tag']=='BOSS_FIELD' and r['frame']==final_frame)['human_id']=1
        variants.append(('wrong_actual_deciding_own_identity',changed,'Each actual boss KO belongs to live true Sonya'))
        for name,changed,message in variants:
            need(changed!=rows,'Non-vacuous actual deciding-route fault')
            try:final_contract(changed)
            except ValueError as error:
                need(message in str(error),'Specific actual native deciding-KO invariant');faults.append(name)
            else:raise ValueError('Corrupted actual deciding route accepted')
        need(final_contract(rows)==earned_match,'Same-path original deciding-route positive')
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
       actualSuccessfulShaoMatch=earned_match,
       nativeShaoMatchNeverInferredFromOneRoundOrAccumulatedContinues=True,
       actualDecidingRouteQualifiedFaults=faults,samePathDecidingRoutePositiveAccepted=True,
       failed3495TwoWinnerCallsAssumptionSuperseded=True,
       failed3500SameCollisionAndWinnerFieldAssumptionSuperseded=True,
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
