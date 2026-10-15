"""Immutable executed lower-airkick controller + sampled native states; no invented entry PCs."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify();root=sync.ROOT;case=root/'audit_current_sonya_p1_kintaro_low_airkick_runtime'
out=root/'audit_current_sonya_p1_kintaro_low_airkick_witness_checked';assert not out.exists()
lua=root/'audit_current_sonya_p1_kintaro_low_airkick_preparation/campaign.lua'
assert sync.sha(lua)=='8830F9E2E7923869B3620A720B75B01814536F945D6D42E128B3A7A7FCA8417E'
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['observerSha256']==sync.sha(lua) and terminal['limitReason'] in (None,'wall_limit')
rows=load(case/'run.log');fields=[r for r in rows.get('BOSS_FIELD',[]) if r['stage']=='15' and 'human_vy' in r]
plans=[r for r in rows.get('BOSS_PLAN',[]) if r['stage']=='15']
conditions=[]
for r in fields:
 frame=int(r['frame']);height=int(r['height']);vy=int(r['human_vy'],16)
 if not (8<height<=60 and int(r['gap'])<=100 and 0<vy<0x80000000 and frame%6<3):continue
 recent=[p for p in plans if int(p['frame'])<=frame]
 jumps=[p for p in recent if p['move']=='close_pressure_jumpkick_attempt'];uppers=[p for p in recent if p['move']=='descending_stomp_uppercut_attempt']
 if jumps and frame-int(jumps[-1]['frame'])<16:continue
 if uppers and frame-int(uppers[-1]['frame'])<36:
  cancelled=any(c['stage']=='15' and c['start']==uppers[-1]['frame'] and int(c['frame'])<=frame for c in rows.get('BOSS_CANCEL',[]))
  if not cancelled:continue
 conditions.append(r)
native_kick_samples=[r for r in fields if r['human_action']=='512']
assert all(r['human_id']=='18' and r['cpu_id']=='12' and r['writes']=='0' and r['assistance']=='none' for r in fields)
report=dict(changedStage15Reached=any(r['stage']=='15' for r in rows['FIGHT']),
 sampledLowerPhysicalKickConditions=conditions,conditionEvidence='immutable executed source + sampled priority state, not raw hardware',
 sampledNativeAction512=native_kick_samples,nativeAction512EntryPCObserved=False,
 sampledAirborneTransitions=[r for r in rows.get('BOSS_RESPONSE',[]) if r['stage']=='15'],
 physicalJumpPlans=[p for p in plans if p['move']=='close_pressure_jumpkick_attempt'],
 ownKintaroRoundWins=[r for r in rows['WIN'] if r['stage']=='15' and r['slot']=='1'],
 nativeRecovery1549Samples=[r for r in fields if r['human_action']=='1549'],
 rawPerFieldHardwareAccepted=False,exactAttackContactBlockingAccepted=False,
 terminal=terminal,logSHA256=sync.sha(case/'run.log'),fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(changedStage15Reached=report['changedStage15Reached'],sampledLowerKickConditions=len(conditions),native512SampleCount=len(native_kick_samples),native512SampleHeights=[r['height'] for r in native_kick_samples],ownKintaroRoundWins=report['ownKintaroRoundWins'],logSHA256=report['logSHA256'])))
