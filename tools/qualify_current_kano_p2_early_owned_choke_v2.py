"""Direct prefix comparison; preserve v1 layered-path substitution failure."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_early_owned_choke_runtime'
out=root/'audit_current_kano_p2_early_owned_choke_v2_checked'
assert not out.exists()
rows=load(case/'run.log');prior=load(root/'audit_current_kano_p2_cage_owned_choke_runtime/run.log')
def prefix(records):
    return {tag:[r for r in items if int(r['frame'])<=14045] for tag,items in records.items() if tag!='HOST_BOUND' and any(int(r['frame'])<=14045 for r in items)}
assert prefix(rows)==prefix(prior)
win=next(r for r in rows['WIN'] if r['frame']=='20617')
assert win['stage']=='3' and win['slot']=='2' and win['id']=='17' and win['entry']=='FFFEFA20' and win['pc']=='FF8296B0' and win['health']=='0,161'
assert not any(r['stage']=='4' for r in rows['STAGE'])
loss=next(r for r in rows['LOSS'] if r['frame']=='21877');assert loss['stage']=='3'
entries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='3' and r['move']=='choke']
assert entries and all(r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] for r in entries)
report=dict(passedFiniteChecks=True,actualInputNativePrefixIdenticalThrough=14045,actualOwnedKungChokeEntries=len(entries),finitePerfectKungRound=win,laterAttemptLoss=loss,kungMatchClearObserved=False,liuBranchObserved=False,campaignStrategyAdopted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
