"""Measure native knife entry/recovery exit; no timing edits or replay."""
import json
from collections import Counter
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_shao_close_knife_runtime'
out=root/'audit_current_shao_close_knife_recovery_checked';assert not out.exists()
rows=load(case/'run.log')
entries=[r for r in rows['SPECIAL'] if r['stage']=='16' and r['move']=='knife']
actions=[r for r in rows['BOSS_ACTION'] if r['stage']=='16']
plans=[r for r in rows['BOSS_PLAN'] if r['move']=='shao_close_knife_command_attempt']
chains=[]
for e in entries:
    assert e['id']==e['roster']=='17' and e['actor']==e['a8'] and e['main']==e['a13']
    f=int(e['frame'])
    same=[r for r in actions if r['actor']==e['actor'] and r['main']==e['main'] and f<=int(r['frame'])<f+96]
    start=next((r for r in same if r['after']=='4'),None)
    if not start:continue
    recovery=next((r for r in same if int(r['frame'])>=int(start['frame']) and r['before']=='4' and r['after']=='1540'),None)
    if not recovery:continue
    end=next((r for r in same if int(r['frame'])>=int(recovery['frame']) and r['before']=='1540' and r['after']!='1540'),None)
    if not end:continue
    prior=[r for r in plans if r['human_main']==e['main'] and 0<=f-int(r['frame'])<64]
    plan=max(prior,key=lambda r:int(r['frame'])) if prior else None
    chains.append(dict(entry=f,recovery=int(recovery['frame']),exit=int(end['frame']),exitAction=int(end['after']),
        entryToExit=int(end['frame'])-f,planToExit=int(end['frame'])-int(plan['frame']) if plan else None,
        exitPC=end['pc']))
assert chains
report=dict(actualKnifeEntries=len(entries),observedRecoveryChains=len(chains),
    entryToExitFields=dict(Counter(r['entryToExit'] for r in chains)),
    planToExitFields=dict(Counter(r['planToExit'] for r in chains)),exitActions=dict(Counter(r['exitAction'] for r in chains)),
    chains=chains,logSHA256=sync.sha(case/'run.log'),
    caveat='Recovery exit may include interruption; no dense incoming-damage coverage claimed. Do not infer shortened move timing or a winning controller.',fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='chains'}))
