"""Strict same-paid-attempt Cage clear; do not imply entire route improvement."""
import copy,json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_cage_owned_choke_runtime'
out=root/'audit_current_kano_p2_cage_choke_advance_checked'
assert not out.exists()
rows=load(case/'run.log')
def gate(records):
    fight=next(r for r in records['FIGHT'] if r['frame']=='10556')
    assert fight['human']=='17:17' and fight['cpu']=='2:2' and fight['stage']=='2'
    wins=[r for r in records['WIN'] if r['stage']=='2' and r['slot']=='2' and 10556<int(r['frame'])<14046]
    assert [r['frame'] for r in wins]==['12131','13533']
    assert all(r['id']=='17' and r['pc']=='FF8296B0' and r['entry']=='FFFEFA20' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in wins)
    assert not any(10556<int(r['frame'])<14046 for r in records['LOSS'])
    nxt=next(r for r in records['FIGHT'] if r['frame']=='14046')
    assert nxt['stage']=='3' and nxt['human']=='17:17' and nxt['cpu']=='0:0'
    return dict(fight=fight,ownedWins=wins,nextFight=nxt)
proof=gate(rows);faults=[]
for label in ('wrongwinner','paidloss'):
    bad=copy.deepcopy(rows)
    if label=='wrongwinner':next(r for r in bad['WIN'] if r['frame']=='13533')['slot']='1'
    else:bad['LOSS'].append(dict(frame='13000'))
    try:gate(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('False clear accepted')
chokes=[r for r in rows.get('SPECIAL',[]) if r['stage']=='2' and r['move']=='choke']
assert chokes and all(r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] for r in chokes)
report=dict(passedFiniteChecks=True,cageSameAttemptCleared=True,actualOwnedCageChokeEntries=len(chokes),proof=proof,rejectedFaults=faults,entireRouteFaster=False,campaignStrategyAdopted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
