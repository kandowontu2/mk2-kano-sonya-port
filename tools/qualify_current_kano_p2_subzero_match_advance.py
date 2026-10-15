"""Actual same-attempt native SubZero clear, real Kano17 versus next Liu2."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_p2_subzero_low_knife_runtime'
out=sync.ROOT/'audit_current_kano_p2_subzero_match_advance_checked'
assert not out.exists()
prior=json.loads((sync.ROOT/'audit_current_kano_p2_subzero_low_knife_checked/report.json').read_text())
assert prior['finiteObservationPassed'] and prior['proof']['subZeroMatchCleared']
rows=chronology.load(folder/'run.log')
start=next(r for r in rows['FIGHT'] if r['stage']=='1')
arrival=next(r for r in rows['STAGE'] if r['stage']=='2')
next_fight=next(r for r in rows['FIGHT'] if r['stage']=='2')
wins=[r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='1' and int(r['frame'])<int(arrival['frame'])]
assert len(wins)==2 and start['human']=='17:17' and start['cpu']=='8:8'
assert all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in wins)
assert not any(int(start['frame'])<=int(r['frame'])<=int(arrival['frame']) for r in rows.get('LOSS',[]))
assert int(wins[-1]['frame'])<int(arrival['frame'])<=int(next_fight['frame'])
assert next_fight['human']=='17:17' and next_fight['cpu']=='2:2'
entries=rows.get('KANO_P2_SUBZERO_KNIFE_ENTRY',[])
assert entries and all(r['a8']==r['own']==r['owner'] and r['a13']==r['main'] for r in entries)
out.mkdir()
(out/'report.json').write_text(json.dumps(dict(earnedCurrentKanoP2SubZeroAdvancePassed=True,
    twoWinsSameAttempt=True,start=start,wins=wins,arrival=arrival,nextFight=next_fight,
    actualOwnedKnifeRoutineEntries=len(entries),knifeDamageExhaustivelyAttributed=False,
    logSHA256=sync.sha(folder/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False),indent=2))
print(json.dumps(dict(passed=True,wins=[r['frame'] for r in wins],nextFight=next_fight['frame'],opponent=next_fight['cpu'])))
