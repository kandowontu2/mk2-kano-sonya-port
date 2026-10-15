"""Same paid attempt must earn both Sub-Zero rounds before native Cage fight."""
import copy,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_sonya_p2_subzero_close_retreat_runtime'
out=sync.ROOT/'audit_current_sonya_p2_subzero_match_advance_checked'
assert not out.exists()
prior=json.loads((sync.ROOT/'audit_current_sonya_p2_subzero_close_retreat_checked/report.json').read_text())
assert prior['finiteEvidenceVerified'] and prior['logSHA256']==sync.sha(case/'run.log')
rows=chronology.load(case/'run.log')
def gate(records):
    start=next(r for r in records['FIGHT'] if r['frame']=='14594')
    assert start['stage']=='1' and start['human']=='18:18' and start['cpu']=='8:8'
    wins=[r for r in records['WIN'] if r['stage']=='1' and r['slot']=='2' and 14594<int(r['frame'])<17315]
    assert [r['frame'] for r in wins]==['15397','16802']
    assert all(r['id']=='18' and r['entry']=='FFFEFA40' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in wins)
    assert not any(14594<int(r['frame'])<17315 for r in records['LOSS'])
    fight=next(r for r in records['FIGHT'] if r['frame']=='17315')
    assert fight['stage']=='2' and fight['human']=='18:18' and fight['cpu']=='2:2'
    fields=[r for r in records['LIVE'] if r['stage']=='2'];assert fields
    assert all(r['human']=='18:18' and r['cpu']=='2:2' and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in fields)
    return dict(sameAttemptSubzeroCleared=True,ownWins=wins,nextNativeCageFight=fight,distinctNativePairFields=len(fields))
proof=gate(rows)
bad_winner=copy.deepcopy(rows);next(r for r in bad_winner['WIN'] if r['frame']=='16802')['slot']='1'
bad_loss=copy.deepcopy(rows);bad_loss['LOSS'].append(dict(frame='16000',stage='1'))
for fault in (bad_winner,bad_loss):
    try:gate(fault)
    except AssertionError:pass
    else:raise AssertionError('Invalid same-attempt clear accepted')
out.mkdir();(out/'report.json').write_text(json.dumps(dict(passed=True,proof=proof,wrongWinnerFaultRejected=True,interveningPaidLossFaultRejected=True,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False),indent=2)+'\n');print(json.dumps(proof))
