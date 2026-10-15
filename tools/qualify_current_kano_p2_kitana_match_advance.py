"""Explicit same-attempt Kitana clear and true native next Mileena opponent."""
import copy,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_kitana_campaign_43000_runtime'
out=sync.ROOT/'audit_current_kano_p2_kitana_match_advance_checked'
assert not out.exists()
prior=json.loads((sync.ROOT/'audit_current_kano_p2_kitana_campaign_43000_checked/report.json').read_text())
assert prior['finiteEvidenceVerified'] and prior['completed43000FieldRun'] and prior['logSHA256']==sync.sha(case/'run.log')
rows=chronology.load(case/'run.log')
def gate(records):
    start=next(r for r in records['FIGHT'] if r['frame']=='38531')
    assert start['stage']=='9' and start['human']=='17:17' and start['cpu']=='4:4'
    wins=[r for r in records['WIN'] if r['stage']=='9' and r['slot']=='2' and 38531<int(r['frame'])<41944]
    assert [r['frame'] for r in wins]==['39556','41435']
    assert all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' for r in wins)
    assert not any(38531<int(r['frame'])<41944 for r in records['LOSS'])
    fight=next(r for r in records['FIGHT'] if r['frame']=='41944')
    assert fight['stage']=='10' and fight['human']=='17:17' and fight['cpu']=='5:5'
    fields=[r for r in records['LIVE'] if r['stage']=='10'];assert fields
    assert all(r['human']=='17:17' and r['cpu']=='5:5' and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in fields)
    return dict(sameAttemptKitanaCleared=True,ownWins=wins,nextNativeMileenaFight=fight,distinctNativePairFields=len(fields))
proof=gate(rows)
bad=copy.deepcopy(rows);next(r for r in bad['WIN'] if r['frame']=='41435')['slot']='1'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Opponent victory counted as own clear')
out.mkdir();(out/'report.json').write_text(json.dumps(dict(passed=True,proof=proof,wrongWinnerFaultRejected=True,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False),indent=2));print(json.dumps(proof))
