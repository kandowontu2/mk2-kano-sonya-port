"""Host-render optimization is valid only with identical complete guest prefix."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_runtime'
oldcase=sync.ROOT/'audit_current_kano_p2_mileena_choke_counter_runtime'
out=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_checked'
assert not out.exists()
lua=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_preparation/campaign.lua'
priorlua=sync.ROOT/'audit_current_kano_p2_mileena_choke_counter_preparation/campaign.lua'
marker="if frame>=80000 then log('HOST_BOUND','maximum_fields=80000 full_campaign_acceptance=false')"
source=lua.read_text()
assert source.count(marker)==1
assert source.replace(marker,marker.replace('80000','60000'))==priorlua.read_text()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert (terminal['exitCode'],terminal['limitReason']) in [(0,None),(-1,'wall_limit')]
assert terminal['elapsedSeconds']<92 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(lua)
assert not (case/'stderr.log').read_bytes()
rows=chronology.load(case/'run.log');old=chronology.load(oldcase/'run.log')
last=lambda data:max(int(r['frame']) for group in data.values() for r in group)
cutoff=min(last(rows),last(old))
for tag in set(rows)|set(old):
    if tag not in ('RESULT','HOST_BOUND'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in old.get(tag,[]) if int(r['frame'])<cutoff], 'Guest prefix diverged: '+tag
assert all(r['human']=='17:17' for r in rows['LIVE']+rows['FIGHT'])
assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
stages=chronology.check(rows,2,17,list(range(13))+[14,15,16])
assert stages[:12]==list(range(12))
report=dict(finiteEvidenceVerified=True,physicalControllerUnchanged=True,
            completeGuestPrefixIdenticalBefore=cutoff,earnedStages=stages,
            ownWinsAfterMileena=[r for r in rows['WIN'] if int(r['stage'])>=11 and r['slot']=='2'],
            lastLoggedField=last(rows),endingCompleted=rows.get('ENDING_COMPLETED',[]),
            terminal=terminal,logSHA256=sync.sha(case/'run.log'),
            fullCampaignAccepted=False,fullPortAccepted=False,
            visualAcceptance=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
