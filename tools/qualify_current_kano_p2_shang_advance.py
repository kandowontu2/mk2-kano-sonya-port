"""Same-attempt Shang clear and separate later Kintaro round, not boss clear."""
import copy,json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_changed_health_only_runtime'
out=root/'audit_current_kano_p2_shang_advance_checked'
assert not out.exists()
prior=json.loads((root/'audit_current_kano_p2_changed_health_only_checked/report.json').read_text())
assert prior['passedFinitePrefixChecks'] and prior['logSHA256']==sync.sha(case/'run.log')
rows=load(case/'run.log')
def gate(records):
    start=next(r for r in records['FIGHT'] if r['frame']=='56386')
    assert start['stage']=='14' and start['human']=='17:17' and start['cpu']=='6:6'
    nxt=next(r for r in records['FIGHT'] if r['frame']=='59523')
    assert nxt['stage']=='15' and nxt['human']=='17:17' and nxt['cpu']=='12:12' and nxt['schedule']=='FFFA3180'
    wins=[r for r in records['WIN'] if r['stage']=='14' and r['slot']=='2' and 56386<int(r['frame'])<59523]
    assert [r['frame'] for r in wins]==['57066','58979']
    assert all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in wins)
    assert not any(56386<int(r['frame'])<59523 for r in records['LOSS'])
    loss=next(r for r in records['LOSS'] if r['frame']=='62730')
    assert loss['stage']=='15'
    fresh=next(r for r in records['FIGHT'] if r['frame']=='63589')
    assert fresh['stage']=='15' and fresh['human']=='17:17' and fresh['cpu']=='12:12'
    roundwin=next(r for r in records['WIN'] if r['frame']=='65340')
    assert roundwin['stage']=='15' and roundwin['slot']=='2' and roundwin['id']=='17' and roundwin['entry']=='FFFEFA20' and roundwin['pc']=='FF8296B0' and roundwin['health']=='0,81'
    assert not any(63589<int(r['frame'])<=65340 for r in records['LOSS'])
    assert not any(r['stage']=='16' for r in records['STAGE'])
    return dict(shangAttempt=start,shangOwnedWins=wins,nextKintaroFight=nxt,kintaroFailedAttemptLoss=loss,kintaroFreshAttempt=fresh,kintaroSingleOwnedRound=roundwin)
proof=gate(rows);faults=[]
for label in ['wrong_winner','intervening_paid_loss','wrong_next_actor','wrong_boss_round_attempt']:
    bad=copy.deepcopy(rows)
    if label=='wrong_winner':next(r for r in bad['WIN'] if r['frame']=='58979')['slot']='1'
    elif label=='intervening_paid_loss':bad['LOSS'].append(dict(frame='58000',stage='14'))
    elif label=='wrong_next_actor':next(r for r in bad['FIGHT'] if r['frame']=='59523')['human']='1:1'
    else:bad['LOSS'].append(dict(frame='64000',stage='15'))
    try:gate(bad)
    except (AssertionError,StopIteration):faults.append(label)
    else:raise AssertionError('False clear accepted '+label)
report=dict(passedFiniteChecks=True,shangTsungCurrentMatchCleared=True,kintaroSingleRoundWon=True,kintaroMatchCleared=False,proof=proof,rejectedFaults=faults,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
