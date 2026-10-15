"""Two owned round wins in one attempt then actual next opponent, no proxy."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_p2_sonya_standing_counter_runtime'
out=sync.ROOT/'audit_current_kano_p2_sonya_match_advance_checked'
assert not out.exists()
finite=json.loads((sync.ROOT/'audit_current_kano_p2_sonya_standing_counter_checked/report.json').read_text())
assert finite['finiteObservationPassed'] and finite['proof']['openingMatchCleared']
rows=chronology.load(folder/'run.log')
opening=next(r for r in rows['FIGHT'] if r['stage']=='0')
arrival=next(r for r in rows['STAGE'] if r['stage']=='1')
next_fight=next(r for r in rows['FIGHT'] if r['stage']=='1')
wins=[r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='0' and int(r['frame'])<int(arrival['frame'])]
assert len(wins)==2 and opening['human']=='17:17' and opening['cpu']=='18:18'
assert all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in wins)
assert not any(int(opening['frame'])<=int(r['frame'])<=int(arrival['frame']) for r in rows.get('LOSS',[]))
assert int(wins[-1]['frame'])<int(arrival['frame'])<=int(next_fight['frame'])
assert next_fight['human']=='17:17' and next_fight['cpu']=='8:8'
out.mkdir();report=dict(earnedOpeningSonyaMatchAdvancePassed=True,twoWinsSameAttempt=True,
    opening=opening,wins=wins,arrival=arrival,nextFight=next_fight,logSHA256=sync.sha(folder/'run.log'),
    fullCampaignAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(dict(passed=True,nextFight=next_fight['frame'],opponent=next_fight['cpu'])))
