"""Native mirror contacts and earned advancement; no preset success outcome."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_mirror_active_flag_guard_runtime'
out=sync.ROOT/'audit_current_sonya_mirror_active_flag_guard_classified'
assert not out.exists()
rows=chronology.load(folder/'run.log')
gate=json.loads((sync.ROOT/'audit_current_sonya_mirror_active_flag_guard_checked/report.json').read_text())
assert gate['passedObservationChecks']
damage=rows.get('MIRROR_STANDING_DAMAGE',[])
assert all(r['ids']=='18,18' and r['p1_actor']!=r['p2_actor'] and r['p1_main']!=r['p2_main'] for r in damage)
contacts=[r for r in damage if r['victim_slot']=='2' and r['actions'].split(',')[0]=='259' and r['a8']==r['p1_actor'] and r['a13']==r['p1_main']]
incoming={}
for r in damage:
    if r['victim_slot']=='1':
        item=incoming.setdefault(r['actions'].split(',')[1],dict(callbacks=0,damage=0))
        item['callbacks']+=1;item['damage']+=int(r['before'])-int(r['after'])
wins=[r for r in rows.get('WIN',[]) if r['slot']=='1' and r['stage']=='5']
advanced=any(int(r['stage'])==6 for r in rows['STAGE'])
if advanced:assert len(wins)>=2
report=dict(observationPassed=True,completedRunAccepted=gate['completedRunAccepted'],
    ownKickContacts=len(contacts),outgoing=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),
    incomingByCpuActionAtCallback=incoming,ownMirrorRoundWins=wins,mirrorMatchCleared=advanced,
    fullCampaignClear=False,fullPortAccepted=False,logSHA256=sync.sha(folder/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
