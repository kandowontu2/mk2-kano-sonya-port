"""Actual native paid-loss/field costs and Kung Lao guard-state rejection witnesses."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify();root=sync.ROOT
out=root/'audit_current_sonya_p1_early_ladder_cost_checked';assert not out.exists()
path=root/'audit_current_sonya_p1_boss_light_runtime/run.log';rows=load(path)
stages=rows['STAGE'];costs=[]
for i,r in enumerate(stages[:-1]):
 stage=r['stage']
 if int(stage)>=15:continue
 fights=[f for f in rows['FIGHT'] if f['stage']==stage]
 assert fights and all(f['human']=='18:18' and f['writes']=='0' and f['assistance']=='none' for f in fights)
 costs.append(dict(stage=int(stage),cpuIdentities=sorted(set(f['cpu'] for f in fights)),firstFight=int(r['frame']),fieldsUntilNextStage=int(stages[i+1]['frame'])-int(r['frame']),paidLosses=sum(x['stage']==stage for x in rows['LOSS']),paidSelections=len(set(f['selection'] for f in fights))))
kung_live=[r for r in rows['LIVE'] if r['stage']=='4']
def rejected_guard(r):
 assert r['human']=='18:18' and r['cpu']=='0:0'
 flag=int(r['flags'].split(',')[0],16);action=r['actions'].split(',')[0]
 return action in ('1792','1793') and flag&0x1c!=0 and flag&0x18==0
witness=[r for r in kung_live if rejected_guard(r)]
assert witness
faults=[]
positive=witness[0]
for name,bad in (
 ('not_native_guard_action',dict(positive,actions='512,771')),
 ('attack_or_air_flags_not_recovery',dict(positive,flags='0015,0000')),
 ('no_rejected_flag_bit',dict(positive,flags='0001,0000')),
):
 assert not rejected_guard(bad);faults.append(name)
plans=[r for r in rows.get('KUNGLAO_GUARD_ATTEMPT',[]) if r['stage']=='4']
legs=[r for r in rows.get('SPECIAL',[]) if r['stage']=='4' and r['move']=='leg']
assert all(r['id']==r['roster']=='18' and r['actor']==r['a8'] and r['main']==r['a13'] for r in legs)
report=dict(stageFieldCosts=costs,descendingCostStages=sorted(costs,key=lambda r:r['fieldsUntilNextStage'],reverse=True),
 kungPhysicalLegPlans=len(plans),kungOwnedNativeLegEntries=len(legs),kungLiveSamples=len(kung_live),
 kungNativeBlockSamples=sum(r['actions'].split(',')[0] in ('1792','1793') for r in kung_live),
 kungGuardFlagRejectWitnesses=witness,rejectedClassificationFaults=faults,
 heightBodyVelocityReadinessFullyObserved=False,allWitnessesWouldActivateLegAccepted=False,
 proposedVariant='stage4 Kung only: permit nativeguard1792/1793 with no flags18, preservefloor/VY/body/CPU-safe/range110/Down7LPBlock3..7/retry32',
 logSHA256=sync.sha(path),fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(topCosts=report['descendingCostStages'][:5],plans=len(plans),entries=len(legs),guardRejectWitnesses=len(witness),faults=faults)))
