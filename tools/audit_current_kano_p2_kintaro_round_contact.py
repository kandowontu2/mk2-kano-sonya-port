"""Chronological actor-owned action/HP evidence for one earned Kintaro round."""
import json,re
from collections import Counter
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_changed_health_only_runtime'
out=root/'audit_current_kano_p2_kintaro_round_contact_checked'
assert not out.exists()
proof=json.loads((root/'audit_current_kano_p2_shang_advance_checked/report.json').read_text())
assert proof['passedFiniteChecks'] and proof['logSHA256']==sync.sha(case/'run.log')
field=None;action=None;damage=[];entries=[];fields=0
with (case/'run.log').open() as stream:
    for line in stream:
        if not line.startswith('MK2_NAT_CAMPAIGN_'):continue
        tag=line.split()[0][17:];r=dict(re.findall(r'(\w+)=([^\s]+)',line))
        f=int(r['frame'])
        if not 63589<=f<=65340:continue
        if tag=='BOSS_FIELD':
            assert r['stage']=='15' and r['human_id']=='17' and r['cpu_id']=='12'
            field=r;fields+=1
        elif tag=='BOSS_ACTION':
            assert r['id']==r['roster']=='17' and r['owner']==r['actor'] and r['state']=='1'
            assert int(r['at'],16)==int(r['main'],16)+0x1f0
            if r['before']!=r['after']:entries.append(dict(frame=f,action=int(r['after']),pc=r['pc'],actor=r['actor'],main=r['main']))
            action=r
        elif tag=='HEALTH' and r['pc']=='FF836700' and int(r['after'])<int(r['before'])<=161:
            assert field is not None
            damage.append(dict(frame=f,victimSlot=int(r['slot']),damage=int(r['before'])-int(r['after']),a8=r['a8'],a13=r['a13'],cpuActor=field['cpu_actor'],humanMain=field['human_main'],cpuMain=field['cpu_main'],latestOwnedAction=int(action['after']) if action else None,latestActionFrame=int(action['frame']) if action else None,directHumanMainCaller=r['a13']==field['human_main'],directCpuMainCaller=r['a13']==field['cpu_main']))
assert fields and entries and damage
outgoing=[r for r in damage if r['victimSlot']==1]
incoming=[r for r in damage if r['victimSlot']==2]
assert sum(r['damage'] for r in outgoing)==161
assert all(r['a8']==r['cpuActor'] for r in outgoing)
direct=[r for r in outgoing if r['directHumanMainCaller']]
assert direct
report=dict(passedFiniteContactChecks=True,winningRoundWindow=[63589,65340],trueKanoAndKintaroFields=fields,actualOwnedStateTransitions=dict(Counter(r['action'] for r in entries)),nativeOutgoingDamage=sum(r['damage'] for r in outgoing),nativeIncomingDamage=sum(r['damage'] for r in incoming),directKanoMainOutgoingDamage=sum(r['damage'] for r in direct),actualHpRecords=damage,latestActionIsChronologicalContextNotExactHitboxProof=True,kintaroFullMatchAccepted=False,visualAudioAllContextsAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='actualHpRecords'}))
