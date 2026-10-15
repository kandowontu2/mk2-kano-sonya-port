"""Attribute native damage timing to planned attack windows, not guessed subtype."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_sonya_mirror_recovery_damage'
assert not out.exists()
cases=[]
for name in ('neutral_recovery','active_flag_guard','standing_ready'):
    folder=sync.ROOT/f'audit_current_sonya_mirror_{name}_runtime'
    rows=chronology.load(folder/'run.log')
    requests=rows.get('MIRROR_STANDING_COUNTER',[])
    groups={};selected=[]
    for r in rows['MIRROR_STANDING_DAMAGE']:
        if r['victim_slot']!='1':continue
        frame=int(r['frame'])
        preceding=[q for q in requests if int(q['frame'])<=frame]
        age=frame-int(preceding[-1]['frame']) if preceding else None
        phase='planned_counter_window' if age is not None and age<32 else 'outside_counter_window'
        cpu_action=r['actions'].split(',')[1];human_action=r['actions'].split(',')[0]
        key=f'{phase}:cpu{cpu_action}:human{human_action}'
        group=groups.setdefault(key,dict(callbacks=0,damage=0))
        group['callbacks']+=1;group['damage']+=int(r['before'])-int(r['after'])
        selected.append(dict(phase=phase,fieldsSinceRequest=age,row=r))
    cases.append(dict(case=name,groups=groups,hits=selected,logSHA256=sync.sha(folder/'run.log')))
out.mkdir();(out/'report.json').write_text(json.dumps(dict(cases=cases,fullPortAccepted=False,
    note='Windows classify requested controller timing, not proof that commands stayed active or native attack subtype.'),indent=2))
print(json.dumps([dict(case=c['case'],groups=c['groups']) for c in cases]))
