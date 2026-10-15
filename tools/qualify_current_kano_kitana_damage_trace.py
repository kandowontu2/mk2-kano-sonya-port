"""Whole observer-neutrality gate and actual hit-time action classification."""
import json
from collections import Counter
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_kitana_damage_trace_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_kitana_damage_trace_preparation/campaign.lua')
rows=chronology.load(folder/'run.log');old=chronology.load(sync.ROOT/'audit_current_kano_kitana_ground_spacing_runtime/run.log')
for tag in set(rows)|set(old):
    if tag=='KITANA_DAMAGE_DETAIL':continue
    assert rows.get(tag,[])==old.get(tag,[]),tag
hits=rows['KITANA_DAMAGE_DETAIL'];assert hits and all(r['ids']=='17,4' for r in hits)
incoming=[r for r in hits if r['victim_slot']=='1']
classes=Counter((r['actions'].split(',')[1],int(r['before'])-int(r['after'])) for r in incoming)
out=sync.ROOT/'audit_current_kano_kitana_damage_trace_checked'
assert not out.exists();out.mkdir()
report=dict(passedNeutrality=True,hits=hits,incomingActionDamageCounts=[dict(action=k[0],damage=k[1],count=v) for k,v in classes.items()],
 exactNativeDamageWriterObserved=True,universalSourceAttribution=False,fullPortAccepted=False,logSHA256=sync.sha(folder/'run.log'))
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report['incomingActionDamageCounts'],indent=2))
