"""Native higher-health winners, exact mirror prefix, genuine Sonya identity."""
import inspect,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_sonya_p2_subzero_hk_ring_runtime'
out=sync.ROOT/'audit_current_sonya_p2_subzero_hk_ring_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert (terminal['exitCode'],terminal['limitReason']) in [(0,None),(-1,'wall_limit')]
assert terminal['elapsedSeconds']<92 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_p2_subzero_hk_ring_preparation/campaign.lua')
assert not (case/'stderr.log').read_bytes()
rows=chronology.load(case/'run.log');old=chronology.load(sync.ROOT/'audit_current_sonya_p2_mirror_guard_runtime/run.log')
for tag in set(rows)|set(old):
    if tag not in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<6684]==[r for r in old.get(tag,[]) if int(r['frame'])<6684],tag
assert all(r['human']=='18:18' for r in rows['LIVE']+rows['FIGHT'])
assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
code=inspect.getsource(chronology.check).replace('health[side - 1] > 0 and health[2 - side] == 0','health[side - 1] > health[2 - side] >= 0')
context={};exec(compile(code,__file__+'::native_higher_health','exec'),context)
stages=context['check'](rows,2,18,list(range(13))+[14,15,16])
assert stages[:2]==[0,1]
wins=[r for r in rows['WIN'] if r['stage']=='1' and r['slot']=='2']
assert all(r['entry']=='FFFEFA40' for r in wins)
report=dict(finiteEvidenceVerified=True,mirrorPrefixIdenticalThrough=6683,earnedStages=stages,
            subzeroOwnWins=wins,subzeroMatchCleared=2 in stages,
            sampledNativeHKStates=len([r for r in rows['LIVE'] if r['stage']=='1' and r['actions'].split(',')[0]=='259']),
            nativeRingEntries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='1' and r['move']=='ring'],
            terminal=terminal,lastLoggedField=max(int(r['frame']) for group in rows.values() for r in group),
            timerDirectlyObserved=False,fullCampaignAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
