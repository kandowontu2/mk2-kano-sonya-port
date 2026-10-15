"""Same paid attempt clears real Scorpion; actual independent Kano mirror pair."""
import copy,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_scorpion_early_knife_runtime'
out=sync.ROOT/'audit_current_kano_p2_scorpion_match_advance_checked'
assert not out.exists()
prior=json.loads((sync.ROOT/'audit_current_kano_p2_scorpion_early_knife_checked/report.json').read_text())
assert prior['finiteObservationPassed'] and prior['logSHA256']==sync.sha(case/'run.log')
rows=chronology.load(case/'run.log')
def gate(records):
    start=next(r for r in records['FIGHT'] if r['frame']=='26080')
    assert start['stage']=='6' and start['human']=='17:17' and start['cpu']=='3:3'
    own=[r for r in records['WIN'] if r['stage']=='6' and r['slot']=='2' and 26080<int(r['frame'])<30320]
    assert [r['frame'] for r in own]==['26925','29810']
    assert all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' for r in own)
    assert not any(26080<int(r['frame'])<30320 for r in records['LOSS'])
    mirror=next(r for r in records['FIGHT'] if r['frame']=='30320')
    assert mirror['stage']=='7' and mirror['human']=='17:17' and mirror['cpu']=='17:17'
    fields=[r for r in records['LIVE'] if r['stage']=='7']
    assert fields
    assert all(r['human']=='17:17' and r['cpu']=='17:17' and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in fields)
    return dict(sameAttemptScorpionClear=True,ownWins=own,nativeMirrorFight=mirror,distinctNativeMirrorFields=len(fields))
proof=gate(rows)
bad=copy.deepcopy(rows);field=next(r for r in bad['LIVE'] if r['stage']=='7');field['cpu_actor']=field['human_actor']
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Aliased native mirror actors accepted')
out.mkdir();(out/'report.json').write_text(json.dumps(dict(passed=True,proof=proof,aliasedMirrorFaultRejected=True,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False),indent=2))
print(json.dumps(proof))
