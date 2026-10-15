"""Native chronology and earlier prefix; don't conflate wins across retries."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_baraka_choke_route_runtime'
out=sync.ROOT/'audit_current_kano_p2_baraka_choke_route_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert (terminal['exitCode'],terminal['limitReason']) in [(0,None),(-1,'wall_limit')]
assert terminal['elapsedSeconds']<92 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_p2_baraka_choke_route_preparation/campaign.lua')
assert not (case/'stderr.log').read_bytes()
rows=chronology.load(case/'run.log');old=chronology.load(sync.ROOT/'audit_current_kano_p2_campaign_slim_health_runtime/run.log')
for tag in set(rows)|set(old):
    if tag not in ('RESULT','HOST_BOUND'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<21977]==[r for r in old.get(tag,[]) if int(r['frame'])<21977],tag
assert all(r['human']=='17:17' for r in rows['LIVE']+rows['FIGHT'])
assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
stages=chronology.check(rows,2,17,list(range(13))+[14,15,16])
entries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='6' and r['move']=='choke']
assert all(r['id']==r['roster']=='17' and r['a8']==r['actor'] and r['a13']==r['main'] for r in entries)
report=dict(finiteEvidenceVerified=True,priorPrefixUnchangedThrough=21976,earnedStages=stages,
    barakaNativeChokeEntries=len(entries),barakaLPInputFields=len(rows.get('BARAKA_CHOKE_LP_INPUT',[])),
    barakaOwnWins=[r for r in rows['WIN'] if r['stage']=='6' and r['slot']=='2'],
    paidLosses=rows.get('LOSS',[]),lastLoggedField=max(int(r['frame']) for group in rows.values() for r in group),
    endingCompleted=rows.get('ENDING_COMPLETED',[]),terminal=terminal,
    fullCampaignAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
