"""Actual earlier route retained; scope any resource cap explicitly as partial."""
import copy,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_kitana_counter_runtime'
out=sync.ROOT/'audit_current_kano_p2_kitana_counter_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert (terminal['exitCode'],terminal['limitReason']) in ((0,None),(-1,'wall_limit'))
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_p2_kitana_counter_preparation/campaign.lua')
assert not (case/'stderr.log').read_text().strip()
rows=chronology.load(case/'run.log');old=chronology.load(sync.ROOT/'audit_current_kano_p2_early_knife_campaign_40000_runtime/run.log')
for tag in set(rows)|set(old):
    if tag not in ('RESULT','HOST_BOUND'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<34953]==[r for r in old.get(tag,[]) if int(r['frame'])<34953],tag
def gate(records):
    assert all(r['human']=='17:17' for r in records['LIVE']+records['FIGHT'])
    assert all(r['writes']=='0' and r['assistance']=='none' for group in records.values() for r in group)
    stages=chronology.check(records,2,17,list(range(13))+[14,15,16])
    assert stages[:10]==list(range(10))
    fight=next(r for r in records['FIGHT'] if r['stage']=='9')
    assert fight['frame']=='34953' and fight['cpu']=='4:4'
    damage=records.get('KANO_P2_KITANA_DAMAGE',[])
    assert all(r['ids']=='4,17' and r['p1_actor']!=r['p2_actor'] and r['p1_main']!=r['p2_main'] for r in damage)
    kicks=[r for r in damage if r['victim_slot']=='1' and r['actions'].split(',')[1]=='259' and r['a8']==r['p2_actor'] and r['a13']==r['p2_main']]
    return dict(earnedStages=stages,kitanaOwnWins=[r for r in records['WIN'] if r['stage']=='9' and r['slot']=='2'],
        kitanaMatchCleared=10 in stages,ownedHKContacts=len(kicks),ownedHKDamage=sum(int(r['before'])-int(r['after']) for r in kicks),
        outgoing=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),
        incoming=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'))
proof=gate(rows)
bad=copy.deepcopy(rows);bad['LIVE'][0]['human']='17:1'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Proxy accepted')
completed=terminal['limitReason'] is None and rows.get('RESULT',[]) and rows['RESULT'][0]['frame']=='40000'
out.mkdir();(out/'report.json').write_text(json.dumps(dict(finiteEvidenceVerified=True,proof=proof,terminal=terminal,
    priorPrefixUnchangedThrough=34952,lastLoggedField=max(int(r['frame']) for group in rows.values() for r in group),
    completed40000FieldRun=bool(completed),proxyFaultRejected=True,fullCampaignAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log')),indent=2))
print(json.dumps(dict(proof=proof,completed40000=bool(completed),limitReason=terminal['limitReason'])))
