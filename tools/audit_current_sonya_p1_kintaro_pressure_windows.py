"""Passive HP/physical jump-plan windows; not an exact attack ownership classifier."""
import collections,json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
path=sync.ROOT/'audit_current_sonya_p1_boss_light_runtime/run.log'
out=sync.ROOT/'audit_current_sonya_p1_kintaro_pressure_windows_checked'
assert not out.exists()
rows=load(path)
plans=[r for r in rows['BOSS_PLAN'] if r['stage']=='15' and r['move']=='close_pressure_jumpkick_attempt']
damage=[r for r in rows['HEALTH'] if int(r['frame'])>=107554 and r['pc']=='FF836700' and int(r['before'])<=161 and int(r['before'])>int(r['after'])]
hist={str(side):dict(collections.Counter(int(r['before'])-int(r['after']) for r in damage if r['slot']==str(side))) for side in (1,2)}
windows=[]
for r in damage:
 if r['slot']!='1' or int(r['before'])-int(r['after'])!=40:continue
 matches=[p for p in plans if 0<=int(r['frame'])-int(p['frame'])<=60]
 if matches:
  plan=matches[-1]
  windows.append(dict(plan=plan,healthWrite=r,fieldsAfterPlan=int(r['frame'])-int(plan['frame']),qualification='40HP loss after physical jump plan; not exact attack causality/ownership'))
report=dict(stage15PhysicalJumpPlans=len(plans),stage15ActualDamageHistograms=hist,
 human40HPLossWithin60FieldsAfterJumpPlan=windows,
 closeGapUnder95PairedWindows=sum(int(r['plan']['gap'])<95 for r in windows),
 strategyHypothesis='Backjump only at gap<95 to avoid close-range pressure while retaining forward jumps at wider gaps; not asserted to win',
 exactAttackCausalityAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(path))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(plans=len(plans),damageHistograms=hist,paired40HPWindows=len(windows),closeGapUnder95PairedWindows=report['closeGapUnder95PairedWindows'])))
