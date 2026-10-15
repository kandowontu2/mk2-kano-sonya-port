"""Earned route, real Kano ownership, exact native HK contact; no assumed win."""
import copy,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_p2_sonya_standing_counter_runtime'
out=sync.ROOT/'audit_current_kano_p2_sonya_standing_counter_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_bounded_campaign_progress_core_kano_p2_runtime/run.log')
for tag in set(rows)|set(old):
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<1690]==[r for r in old.get(tag,[]) if int(r['frame'])<1690],tag
def gate(records):
    assert records['RESULT'][0]['frame']=='20000'
    assert all(r['writes']=='0' and r['assistance']=='none' for group in records.values() for r in group)
    assert all(r['human']=='17:17' for r in records['LIVE']+records['FIGHT'])
    assert all(r['roster']=='17' for r in records['SELECT_ID'])
    stages=chronology.check(records,2,17,list(range(13))+[14,15,16])
    damage=records.get('KANO_P2_SONYA_DAMAGE',[])
    assert all(r['ids']=='18,17' and r['p1_actor']!=r['p2_actor'] and r['p1_main']!=r['p2_main'] for r in damage)
    contacts=[r for r in damage if r['victim_slot']=='1' and r['actions'].split(',')[1]=='259' and r['a8']==r['p2_actor'] and r['a13']==r['p2_main']]
    return dict(earnedStages=stages,ownKickContacts=len(contacts),
        outgoing=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),
        incoming=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),
        openingOwnRoundWins=[r for r in records.get('WIN',[]) if r['stage']=='0' and r['slot']=='2'],
        paidLosses=len(records.get('LOSS',[])),openingMatchCleared=1 in stages)
proof=gate(rows)
bad=copy.deepcopy(rows);bad['LIVE'][0]['human']='17:1'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Proxy player accepted')
out.mkdir();report=dict(finiteObservationPassed=True,priorColdPrefixUnchangedThrough=1689,
    proof=proof,proxyFaultRejected=True,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),
    fullCampaignAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(proof))
