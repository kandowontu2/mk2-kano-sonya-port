"""Strict same-attempt native KungLao clear into true Sonya versus LiuKang."""
import json,re
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_sonya_p2_kunglao_leg_spacing_runtime'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_match_advance_checked'
assert not out.exists()
rows=[]
for line in (case/'run.log').read_text().splitlines():
    m=re.match(r'MK2_NAT_CAMPAIGN_(\S+) (.*)',line)
    if m:
        r=dict(re.findall(r'(\w+)=([^ ]+)',m[2]));r['kind']=m[1];rows.append(r)
def check(events):
    start=next(r for r in events if r['kind']=='FIGHT' and r['frame']=='23056')
    advance=next(r for r in events if r['kind']=='FIGHT' and r['frame']=='26394')
    assert start['stage']=='3' and start['human']=='18:18' and start['cpu']=='0:0'
    assert advance['stage']=='4' and advance['human']=='18:18' and advance['cpu']=='1:1'
    between=[r for r in events if 23056<int(r['frame'])<26394]
    assert not any(r['kind']=='LOSS' for r in between)
    wins=[r for r in between if r['kind']=='WIN' and r['slot']=='2']
    assert [r['frame'] for r in wins]==['24150','25870']
    assert all(r['stage']=='3' and r['id']=='18' and r['entry']=='FFFEFA40' and r['pc']=='FF8296B0' and int(r['health'].split(',')[0])==0 and int(r['health'].split(',')[1])>0 for r in wins)
    return wins,advance
wins,advance=check(rows)
faults=[]
for label in ('wrong_winner','intervening_paid_loss'):
    changed=[dict(r) for r in rows]
    if label=='wrong_winner':next(r for r in changed if r['kind']=='WIN' and r['frame']=='24150')['id']='1'
    else:changed.append(dict(kind='LOSS',frame='25000'))
    try:check(changed)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Fault accepted: '+label)
out.mkdir();report=dict(passed=True,sameAttemptKungLaoCleared=True,nextNativeLiuKangFight=advance,wins=wins,rejectedFaults=faults,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
