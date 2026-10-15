"""Earned same-attempt Mileena clear, genuine native Baraka successor."""
import copy,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_mileena_choke_counter_runtime'
out=sync.ROOT/'audit_current_kano_p2_mileena_match_advance_checked'
assert not out.exists()
prior=json.loads((sync.ROOT/'audit_current_kano_p2_mileena_choke_counter_checked/report.json').read_text())
assert prior['finiteEvidenceVerified'] and prior['logSHA256']==sync.sha(case/'run.log')
rows=chronology.load(case/'run.log')
def gate(records):
    start=next(r for r in records['FIGHT'] if r['frame']=='47350')
    assert start['stage']=='10' and start['human']=='17:17' and start['cpu']=='5:5'
    wins=[r for r in records['WIN'] if r['stage']=='10' and r['slot']=='2' and 47350<int(r['frame'])<50932]
    assert [r['frame'] for r in wins]==['48447','50423']
    assert all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in wins)
    assert not any(47350<int(r['frame'])<50932 for r in records['LOSS'])
    fight=next(r for r in records['FIGHT'] if r['frame']=='50932')
    assert fight['stage']=='11' and fight['human']=='17:17' and fight['cpu']=='10:10'
    fields=[r for r in records['LIVE'] if r['stage']=='11']
    assert fields and all(r['human']=='17:17' and r['cpu']=='10:10' and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in fields)
    return dict(sameAttemptMileenaCleared=True,ownWins=wins,nextNativeBarakaFight=fight,distinctNativePairFields=len(fields))
proof=gate(rows)
for fault in ('winner','paid_loss'):
    bad=copy.deepcopy(rows)
    if fault=='winner': next(r for r in bad['WIN'] if r['frame']=='50423')['slot']='1'
    else: bad['LOSS'].append(dict(frame='49000'))
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('False clear accepted: '+fault)
out.mkdir()
(out/'report.json').write_text(json.dumps(dict(passed=True,proof=proof,wrongWinnerFaultRejected=True,interveningPaidLossFaultRejected=True,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False),indent=2)+'\n')
print(json.dumps(proof))
