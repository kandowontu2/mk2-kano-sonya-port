"""CPU action771 does not by itself classify active attack ownership."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_mirror_neutral_recovery_runtime'
out=sync.ROOT/'audit_current_sonya_mirror_stance_damage_owners'
assert not out.exists()
rows=chronology.load(folder/'run.log')
classified={};selected=[]
for r in rows['MIRROR_STANDING_DAMAGE']:
    if r['victim_slot']!='1' or r['actions'].split(',')[1]!='771':continue
    if r['a8']==r['p2_actor'] and r['a13']==r['p2_main']:kind='physical_cpu_actor_main'
    elif r['a8']==r['p1_actor'] and r['a13']==r['p1_main']:kind='physical_human_actor_main'
    else:kind='other_helper_context_not_attributed'
    item=classified.setdefault(kind,dict(callbacks=0,damage=0));item['callbacks']+=1;item['damage']+=int(r['before'])-int(r['after'])
    selected.append(dict(kind=kind,row=r))
assert sum(r['callbacks'] for r in classified.values())==33
out.mkdir();(out/'report.json').write_text(json.dumps(dict(observationCompleted=True,groups=classified,callbacks=selected,logSHA256=sync.sha(folder/'run.log'),exactAttackSubtypeProven=False,fullPortAccepted=False),indent=2))
print(json.dumps(classified))
