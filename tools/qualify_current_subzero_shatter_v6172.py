"""Whole inter-round AND next CPU refill for the same four native terminals.

Retain6166/6170 failed test assumptions and every original shatter predicate.
These captures continue beyond victim retirement into the next CPU game, so
two original81-store physical-slot refills occur, not one. Prove both chains
and account for every global sentinel; do not omit the second from records.
"""
import copy,json,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_current_kitana_scene_v6116 as refill_source
ROOT,need,sha=current.ROOT,current.need,current.sha
prior=Path(__file__).with_name('qualify_current_subzero_shatter_v6166.py')
repair=Path(__file__).with_name('qualify_current_subzero_shatter_v6170.py')

def full_refills(rs,side,guest):
 origin=int(next(r for r in rs if r['tag']=='ACTION')['frame'])
 # The complete existing earned two-KO interval, with no rows dropped inside it.
 inter=refill_source.refill([r for r in rs if int(r['frame'])<=origin],side,guest)
 h=[r for r in rs if r['tag']=='HEALTH'];startpc='FF9DECE0'if side==1 else'FF9DED10';steppc='FF9DEF40'if side==1 else'FF9DEF70'
 starts=[(i,r)for i,r in enumerate(h)if r['pc']==startpc]
 need(len(starts)==2,'Exactly two actual source-native refills in this complete next-match recording')
 consumed=set();sequences=[];values=list(range(4,161,2))+[161]
 for index,(i,r)in enumerate(starts):
  at=int(r['frame']);need(r['before']=='161'and r['after']=='65535','Each genuine161-to-FFFF sentinel')
  previous=65535;consumed.add(i)
  for age,value in enumerate(values):
   need(i+age+1<len(h),'All81 original refill stores retained')
   step=h[i+age+1]
   need(step['pc']==steppc and int(step['frame'])==at+age and int(step['before'])==previous and int(step['after'])==value,
        'Both complete native physical-slot refill writer/value/previous-health/field chains')
   consumed.add(i+age+1);previous=value
  need((at==inter['startFrame']and at+79==inter['endFrame'])if index==0 else at>origin,
       'First earned inter-round refill and separate subsequent CPU-match refill')
  sequences.append(dict(startFrame=at,endFrame=at+79,actualStores=81,physicalSlot=side,
                        interval='earned inter-round'if index==0 else'next CPU match',registerOwnershipNotRecordedOrClaimed=True))
 need(all(i in consumed or 0<=int(r['before'])<=161 and 0<=int(r['after'])<=161 for i,r in enumerate(h)),
      'Every invalid global health value accounted for across the entire original recording')
 return dict(inter,startFrame=inter['startFrame'],sequences=sequences,totalActualRefillStores=162,
             completeNextCPURefillAccepted=True,allActualGlobalHealthStoresAccountedFor=True)

source=prior.read_text()
before="replace('audit_v5003_subzero_','audit_v6165_current_subzero_')"
after="replace(\"observed=ROOT/f'audit_v5003_subzero_{fighter}_p{side}_lifecycle_observed/report.json'\",\"observed=ROOT/f'audit_v6165_current_subzero_{fighter}_p{side}_observed/report.json'\")"
need(source.count(before)==1,'Exact actual current report path')
source=source.replace(before,after,1).replace('audit_v6167_current_subzero_shatter_checked','audit_v6173_current_subzero_shatter_checked')
need(source.count('refill_source.refill(')==3,'All three complete positive/refill-fault calls retained')
source=source.replace('refill_source.refill(','full_refills(')
before='Path(__file__),Path(original.__file__),Path(refill_source.__file__)'
need(source.count(before)==1,'Keep every executed repair source pinned')
source=source.replace(before,'prior,repair,Path(__file__),Path(original.__file__),Path(refill_source.__file__)',1)
source=source.replace('actualNativeRefillStores=324','actualNativeRefillStores=648')
# Corrupt a real store in the newly covered second refill and actually run the
# whole grammar. These are additional faults, not replacements for old checks.
before="  need(full_refills(health,side,guest)==positive['nativeInterRoundRefill'],'Complete original refill positive restored')"
after=before+"\n  second=positive['nativeInterRoundRefill']['sequences'][1]['startFrame']\n  for label,age,value in [('wrong_next_cpu_refill_sentinel',0,'65534'),('wrong_next_cpu_refill_step',1,'7')]:\n   changed=copy.deepcopy(health)\n   target=next(r for r in changed if r['tag']=='HEALTH'and int(r['frame'])==second+age and r['after']==('65535'if age==0 else'6'));target['after']=value\n   try:full_refills(changed,side,guest)\n   except ValueError as e:extra_faults.append(dict(case=f'{fighter}_p{side}',fault=label,rejectedBy=str(e)))\n   else:raise ValueError('Accepted next CPU global refill corruption')"
need(source.count(before)==1,'Exact whole second-refill corruption checks')
source=source.replace(before,after,1).replace('len(extra_faults)==28','len(extra_faults)==36').replace('actualSemanticFaultsRejected=80','actualSemanticFaultsRejected=88')
scope=dict(globals(),__name__='complete_current_shatter_and_nextmatch')
exec(compile(source,__file__+'::whole_two_refill_current_matrix','exec'),scope)
if __name__=='__main__':
 out=ROOT/'audit_v6173_current_subzero_shatter_checked';need(not out.exists(),'Fresh complete second-refill successor')
 try:scope['run']()
 except Exception as error:
  need(not out.exists(),'Never overwrite an executed matrix report')
  out.mkdir();(out/'report.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),inputHashes={str(prior.resolve()):sha(prior),str(repair.resolve()):sha(repair),str(Path(__file__).resolve()):sha(__file__)},fullPortAcceptance=False),indent=2)+'\n')
  raise
