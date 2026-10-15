"""Require two own Kitana wins in one selection, then native stage4/FIGHT."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_standing_counter_long_runtime'
out=sync.ROOT/'audit_current_kano_kitana_match_advance_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
stages=chronology.check(rows,1,17,list(range(17)))
assert 4 in stages
arrival=next(r for r in rows['STAGE'] if r['stage']=='4')
fight=next(r for r in rows['FIGHT'] if r['stage']=='4')
wins=[r for r in rows['WIN'] if r['stage']=='3' and r['slot']=='1' and int(r['frame'])<int(arrival['frame'])]
assert len(wins)==2
assert not any(int(wins[0]['frame'])<int(r['frame'])<int(arrival['frame']) for r in rows.get('LOSS',[])+rows.get('SELECT',[]))
assert all(r['id']=='17' and r['entry']=='FFFEFA20' for r in wins)
assert all(r['human']=='17:17' for r in rows['LIVE'])
assert all(r['actor']==r['owner'] and r['id']=='17' for r in rows.get('KANO_STANDING_ACTION',[]))
highkicks=[r for r in rows.get('KANO_STANDING_ACTION',[]) if r['action']=='259']
assert highkicks
assert int(arrival['frame'])<int(fight['frame'])
report=dict(passed=True,observedStages=stages,kitanaOwnWinsSameAttempt=wins,nextStage=arrival,nextFight=fight,nativeStandingHighKickEntries=len(highkicks),allSampledHumanIdentitiesTrue17=True,logSHA256=sync.sha(folder/'run.log'),terminal=terminal,gameCodeChanged=False,fullCampaignClear=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(passed=True,kitanaMatchCleared=True,nextStage=arrival,nextFight=fight)))
