"""Controller digest/preserved route and native wins under slimmer text observer."""
import json,inspect
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_reptile_leg_spacing_runtime'
case=sync.ROOT/'audit_current_sonya_p2_reptile_slim_observation_runtime'
out=sync.ROOT/'audit_current_sonya_p2_reptile_slim_observation_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert (terminal['exitCode'],terminal['limitReason']) in [(0,None),(-1,'wall_limit')]
assert terminal['elapsedSeconds']<92 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert not (case/'stderr.log').read_bytes()
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_p2_reptile_slim_observation_preparation/campaign.lua')
rows,old=chronology.load(case/'run.log'),chronology.load(base/'run.log')
last=min(max(int(r['frame']) for g in rows.values() for r in g),46050)
for tag in set(rows)|set(old):
    if tag not in ('HEALTH','LIVE','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<last]==[r for r in old.get(tag,[]) if int(r['frame'])<last],tag
assert all(r['human']=='18:18' for r in rows['FIGHT']+rows['LIVE'])
assert all(r['writes']=='0' and r['assistance']=='none' for g in rows.values() for r in g)
code=inspect.getsource(chronology.check).replace('health[side - 1] > 0 and health[2 - side] == 0','health[side - 1] > health[2 - side] >= 0')
context={};exec(compile(code,__file__+'::higher_hp','exec'),context)
stages=context['check'](rows,2,18,list(range(13))+[14,15,16])
assert stages[:6]==[0,1,2,3,4,5]
entries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='5' and r['move']=='leg']
assert all(r['id']=='18' and r['roster']=='18' and r['a8']==r['actor'] and r['a13']==r['main'] for r in entries)
report=dict(passedFiniteChecks=True,unchangedControlDigestsAndNativeEventsThrough=last-1,earnedStages=stages,nativeReptileLegEntries=len(entries),ownReptileRounds=[r for r in rows['WIN'] if r['stage']=='5' and r['slot']=='2'],terminal=terminal,lastLoggedField=max(int(r['frame']) for g in rows.values() for r in g),strictAdvanceProofNeeded=6 in stages,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
