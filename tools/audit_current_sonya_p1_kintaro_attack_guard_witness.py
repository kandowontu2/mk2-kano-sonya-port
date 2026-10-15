"""Observed branch conditions + immutable executed source, not raw hardware/activation proof."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_sonya_p1_kintaro_attack_guard_runtime'
out=root/'audit_current_sonya_p1_kintaro_attack_guard_witness_checked';assert not out.exists()
lua=root/'audit_current_sonya_p1_kintaro_attack_guard_preparation/campaign.lua'
assert sync.sha(lua)=='9AB6550B7A085D0953974AD1A7FC9260143F18BA8F74C8FE0457C536274CFCC0'
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['observerSha256']==sync.sha(lua) and terminal['limitReason'] in (None,'wall_limit')
rows=load(case/'run.log')
fields=[r for r in rows.get('BOSS_FIELD',[]) if r['stage']=='15']
plans=[r for r in rows.get('BOSS_PLAN',[]) if r['stage']=='15']
witness=[]
for r in fields:
 frame=int(r['frame'])
 if int(r['height'])>8 or r['cpu_action']=='1031' or not(int(r['cpu_flags'],16)&0x10):continue
 recent=[p for p in plans if int(p['frame'])<=frame]
 jump=[p for p in recent if p['move']=='close_pressure_jumpkick_attempt']
 upper=[p for p in recent if p['move']=='descending_stomp_uppercut_attempt']
 if jump and frame-int(jump[-1]['frame'])<16:continue
 if upper and frame-int(upper[-1]['frame'])<36:
  cancelled=any(c['stage']=='15' and c['start']==upper[-1]['frame'] and int(c['frame'])<=frame for c in rows.get('BOSS_CANCEL',[]))
  if not cancelled:continue
 assert r['human_id']=='18' and r['cpu_id']=='12' and r['writes']=='0' and r['assistance']=='none'
 witness.append(r)
stages=[int(r['stage']) for r in rows['STAGE']]
report=dict(changedStage15Reached=15 in stages,guardBranchConditionsSampled=len(witness),
 sampledConditionsWithActualBlockAction=sum(r['human_action'] in ('1792','1793') for r in witness),
 conditionSamples=witness,
 branchExecutionEvidence='immutable executed controller source plus observed priority conditions; raw per-field physical hardware was not logged',
 rawPerFieldHardwareAccepted=False,guardCollisionAccepted=False,
 physicalBossJumpPlans=len([p for p in plans if p['move']=='close_pressure_jumpkick_attempt']),
 physicalBossUpperPlans=len([p for p in plans if p['move']=='descending_stomp_uppercut_attempt']),
 actualAirborneObservations=[r for r in rows.get('BOSS_RESPONSE',[]) if r['stage']=='15'],
 ownedNativeJumpSetterAccepted=False,ownedNativeUpperSetterAccepted=False,
 actualOwnedBossSpecialEntries=[r for r in rows.get('SPECIAL',[]) if r['stage'] in ('15','16')],
 ownBossRoundWins=[r for r in rows['WIN'] if r['stage'] in ('15','16') and r['slot']=='1'],
 terminal=terminal,logSHA256=sync.sha(case/'run.log'),fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(changedStage15Reached=report['changedStage15Reached'],sampledGuardConditions=len(witness),sampledBlockActions=report['sampledConditionsWithActualBlockAction'],ownBossRoundWins=report['ownBossRoundWins'],logSHA256=report['logSHA256'])))
