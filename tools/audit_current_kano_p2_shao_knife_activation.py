"""Actual owned knife entries vs physical plans in retained Shao trace."""
import json
from collections import Counter
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_approved_180s_runtime'
out=root/'audit_current_kano_p2_shao_knife_activation_checked'
assert not out.exists()
proof=json.loads((root/'audit_current_kano_p2_kintaro_advance_checked/report.json').read_text())
assert proof['passedFiniteChecks'] and proof['logSHA256']==sync.sha(case/'run.log')
rows=load(case/'run.log')
plans=[r for r in rows.get('BOSS_PLAN',[]) if r['stage']=='16' and r['move']=='shao_knife_command_attempt']
entries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='16' and r['move']=='knife']
assert plans and entries
assert all(r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] and r['entry']=='FFFFB000' for r in entries)
transactions=[]
for plan in plans:
    start=int(plan['frame']);stop=start+63
    hits=[r for r in entries if start<int(r['frame'])<=stop]
    ends=[r for r in rows['WIN'] if r['stage']=='16' and start<int(r['frame'])<=stop]
    transactions.append(dict(start=start,plannedAction=int(plan['human_action']),plannedFlags=plan['flags'],plannedHeight=int(plan['height']),ownedNativeEntryFrames=[int(r['frame']) for r in hits],roundEndedWithinWindow=bool(ends)))
assert all(sum(t['start']<int(r['frame'])<=t['start']+63 for t in transactions)==1 for r in entries)
missing=[t for t in transactions if not t['ownedNativeEntryFrames'] and not t['roundEndedWithinWindow']]
report=dict(passedFiniteActivationChecks=True,physicalKnifePlans=len(plans),actualOwnedNativeKnifeEntries=len(entries),completeWindowPlansWithoutEntry=len(missing),missingPlanActionContexts=dict(Counter(t['plannedAction'] for t in missing)),missingPlanFlagContexts=dict(Counter(t['plannedFlags'] for t in missing)),transactions=transactions,plannedButtonsNotActivationProof=True,missingEntriesAreNotAutomaticallyGameBug=True,knifeContactDamageProvenByThisCheck=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='transactions'}))
