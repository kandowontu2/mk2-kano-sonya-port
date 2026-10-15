"""Verify observation neutrality and direct native action270 hit linkage."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_mirror_air_contact_trace_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_mirror_air_contact_trace_preparation/campaign.lua')
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_current_mirror_confirmed_jump_runtime/run.log')
assert rows['RESULT'][0]['frame']=='18500'
for tag in set(rows)|set(old):
    if tag in ('AIR_NATIVE_ENTRY','AIR_NATIVE_DAMAGE','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<18500]==[r for r in old.get(tag,[]) if int(r['frame'])<18500],tag
entries=rows.get('AIR_NATIVE_ENTRY',[])
assert entries,'Native entry observer never triggered'
contacts=[r for r in rows.get('AIR_NATIVE_DAMAGE',[]) if r['victim_slot']=='2' and r['a8']==r['p1_actor'] and r['a13']==r['p1_main'] and r['actions'].split(',')[0]=='270']
report=dict(passedNeutrality=True,unchangedInputsThrough=18499,nativeEntries=entries,
 directOwnAction270Contacts=contacts,allNativeDamage=rows.get('AIR_NATIVE_DAMAGE',[]),
 fullPortAccepted=False,campaignClear=False,logSHA256=sync.sha(folder/'run.log'))
out=sync.ROOT/'audit_current_mirror_air_contact_trace_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(passed=True,entryCount=len(entries),directContacts=len(contacts),damageCount=len(rows.get('AIR_NATIVE_DAMAGE',[])))))
