"""Actual upper263/recovery1539/exit chains; distinguish interruption/censoring."""
import json
from collections import Counter
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_shao_upper_contact_bounded180_runtime'
out=root/'audit_current_kano_p2_shao_upper_recovery_chain_checked'
assert not out.exists()
rows=load(case/'run.log')
actions=[r for r in rows['BOSS_ACTION'] if r['stage']=='16']
damage=rows.get('SHAO_UPPER_DAMAGE',[]);chains=[]
for i,entry in enumerate(actions):
    if entry['after']!='263':continue
    frame=int(entry['frame']);end=frame+128
    same=[r for r in actions[i+1:] if r['actor']==entry['actor'] and r['main']==entry['main'] and frame<=int(r['frame'])<end]
    first=next((r for r in same if r['after']!='263'),None)
    if first is None:continue
    recovery=first['after']=='1539'
    last=next((r for r in same if recovery and int(r['frame'])>=int(first['frame']) and r['after'] not in ('263','1539')),None)
    stop=int(last['frame']) if last else int(first['frame'])
    incoming=[r for r in damage if r['victim_slot']=='2' and r['human_main']==entry['main'] and frame<=int(r['frame'])<=stop]
    chains.append(dict(entry=frame,firstTransition=int(first['frame']),firstAction=int(first['after']),recoveryExit=int(last['frame']) if last else None,recoveryExitAction=int(last['after']) if last else None,totalObservedFields=stop-frame,incomingHPWithinChain=sum(int(r['before'])-int(r['after']) for r in incoming),cleanRecoveryCompletion=recovery and last is not None and not incoming))
clean=[r for r in chains if r['cleanRecoveryCompletion']]
assert chains and clean
report=dict(passedFiniteStateChainChecks=True,observedChains=len(chains),firstTransitionActions=dict(Counter(r['firstAction'] for r in chains)),cleanRecoveryDurations=dict(Counter(r['totalObservedFields'] for r in clean)),chains=chains,upperStateExitIsNotFullRecovery=True,recovery1539IdentifiedByOriginalRoutine=True,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='chains'}))
