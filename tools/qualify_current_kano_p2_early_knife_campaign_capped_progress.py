"""Qualify earned match progress before actual wall cap; never full-run acceptance."""
import copy,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_early_knife_campaign_40000_runtime'
out=sync.ROOT/'audit_current_kano_p2_early_knife_campaign_capped_progress_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['limitReason']=='wall_limit' and terminal['exitCode']==-1
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_p2_early_knife_campaign_40000_preparation/campaign.lua')
assert not (case/'stderr.log').read_text().strip()
rows=chronology.load(case/'run.log');old=chronology.load(sync.ROOT/'audit_current_kano_p2_scorpion_early_knife_runtime/run.log')
for tag in set(rows)|set(old):
    if tag not in ('RESULT','HOST_BOUND'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<32000]==[r for r in old.get(tag,[]) if int(r['frame'])<32000],tag
def gate(records):
    assert all(r['human']=='17:17' for r in records['LIVE']+records['FIGHT'])
    assert all(r['writes']=='0' and r['assistance']=='none' for group in records.values() for r in group)
    for stage,wins,next_frame,next_cpu in [('7',['31012','32285'],'32806','11:11'),('8',['33372','34420'],'34953','4:4')]:
        own=[r for r in records['WIN'] if r['stage']==stage and r['slot']=='2']
        assert [r['frame'] for r in own]==wins
        assert all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' for r in own)
        assert not any(int(wins[0])<int(r['frame'])<int(next_frame) for r in records['LOSS'])
        fight=next(r for r in records['FIGHT'] if r['frame']==next_frame)
        assert fight['stage']==str(int(stage)+1) and fight['human']=='17:17' and fight['cpu']==next_cpu
    mirror=[r for r in records['LIVE'] if r['stage']=='7'];assert mirror
    assert all(r['cpu']=='17:17' and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in mirror)
    return dict(nativeMirrorCleared=True,nativeJaxCleared=True,nextKitanaFight=34953,mirrorDistinctFields=len(mirror))
proof=gate(rows)
bad=copy.deepcopy(rows);next(r for r in bad['WIN'] if r['frame']=='32285')['slot']='1'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Wrong winner accepted')
out.mkdir();(out/'report.json').write_text(json.dumps(dict(earnedPartialProgressVerified=True,proof=proof,terminal=terminal,
    priorPrefixUnchangedThrough=31999,lastLoggedField=max(int(r['frame']) for group in rows.values() for r in group),
    wrongWinnerFaultRejected=True,completed40000FieldRun=False,fullCampaignAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log')),indent=2))
print(json.dumps(proof))
