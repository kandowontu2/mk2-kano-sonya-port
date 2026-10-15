"""Owned native jump-entry matching; physical intent is not activation."""
import json
from collections import Counter
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_approved_180s_runtime'
out=root/'audit_current_kano_p2_shao_escape_activation_checked'
assert not out.exists()
proof=json.loads((root/'audit_current_kano_p2_kintaro_advance_checked/report.json').read_text())
assert proof['passedFiniteChecks'] and proof['logSHA256']==sync.sha(case/'run.log')
rows=load(case/'run.log')
plans=[r for r in rows.get('BOSS_PLAN',[]) if r['stage']=='16' and r['move']=='shao_knife_retreat_jump_attempt']
entries=[r for r in rows.get('BOSS_ACTION',[]) if r['stage']=='16' and r['after']=='776' and r['pc']=='FF831360']
assert plans and entries
assert all(r['id']==r['roster']=='17' and r['actor']==r['owner']==r['a8'] and r['main']==r['a13'] and int(r['at'],16)==int(r['main'],16)+0x1f0 for r in entries)
transactions=[]
for plan in plans:
    start=int(plan['frame']);stop=start+4
    hits=[r for r in entries if start<=int(r['frame'])<=stop and r['actor']==plan['human_actor'] and r['main']==plan['human_main']]
    ends=[r for r in rows['WIN'] if r['stage']=='16' and start<=int(r['frame'])<=stop]
    transactions.append(dict(start=start,plannedAction=int(plan['human_action']),plannedFlags=plan['flags'],plannedBody=plan['body'],gap=int(plan['gap']),direction=plan['direction'],actualJumpEntryFrames=[int(r['frame']) for r in hits],roundEndedWithinWindow=bool(ends)))
assert all(sum(t['start']<=int(r['frame'])<=t['start']+4 for t in transactions)==1 for r in entries)
missing=[t for t in transactions if not t['actualJumpEntryFrames'] and not t['roundEndedWithinWindow']]
report=dict(passedFiniteActivationChecks=True,physicalEscapeJumpPlans=len(plans),actualOwnedNativeJumpEntries=len(entries),completeInputWindowsWithoutJumpEntry=len(missing),missingPlanActionContexts=dict(Counter(t['plannedAction'] for t in missing)),missingPlanFlagContexts=dict(Counter(t['plannedFlags'] for t in missing)),transactions=transactions,upPressNotActivationProof=True,controllerFailureNotAutomaticallyCharacterBug=True,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='transactions'}))
