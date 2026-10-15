"""Retain actual retirement-frame queued-but-undrawn parts, without inventing DMA.

Own source/cache/projection proof covers the entire observed transition. The
underlying queue-discard mechanism is explicitly not accepted by this evidence.
"""
import inspect,json,traceback
from pathlib import Path
import verify_current_ko_round_body_shadow_v5390 as base
ROOT,need,sha=base.ROOT,base.need,base.sha
OUT=ROOT/'audit_v5393_current_ko_round_body_shadow_checked'

def run():
 failure=ROOT/'audit_v5391_current_ko_round_body_shadow_checked/report.json'
 failed=json.loads(failure.read_text())
 need(not failed['passed']and failed['error']=="ValueError('Every actual whole native fighter FIFO publication reaches source-qualified scene DMA')",'Preserve actual too-strong original body-publication-to-hardware assumption')
 source=inspect.getsource(base.check_context)
 before=" need(all(hardware[k]>=v for k,v in published.items()),'Every actual whole native fighter FIFO publication reaches source-qualified scene DMA')"
 after=""" missing=published-hardware
 retired={f for f in range(FIRST,LAST+1)if all(by[f,s]['valid']and not by[f+1,s]['valid']for s in(1,2))}
 need(retired=={3208},'Exactly actual native both-actor retirement boundary')
 expected_missing=Counter()
 for t in rows['MK2_HPHASE_QUEUE']:
  if num(t,'frame')in retired:
   xy=num(t,'xy');size=num(t,'size')
   expected_missing[(num(t,'frame'),num(t,'source'),num(t,'command')>>16,xy&1023,(xy>>16)&511,size&65535,size>>16,0xff804640)]+=1
 need(missing==expected_missing and sum(missing.values())==3 and
  all(hardware[k]==0 for k in missing),'All and only three genuine pre-retirement queued parts absent from actual native DMA')
 need(all(hardware[k]>=v for k,v in (published-missing).items()),'Every other actual fighter FIFO part reaches source-qualified hardware')
 need(by[3208,1]['hp']==0 and by[3208,2]['hp']==161 and by[3209,1]['mode']==by[3209,2]['mode']==6,
  'Absent queued parts belong to actual earned-KO winner/loser retirement, not ordinary gameplay')"""
 need(source.count(before)==1,'Replace only disproven every-publication-draw assumption')
 source=source.replace(before,after,1)
 before='everyPublishedBodyBoundToWholeSceneDMA=True,entireShadowHardwareStreamBoundToWholeScene=True,'
 after="""everyPublishedBodyBoundToWholeSceneDMA=False,entireShadowHardwareStreamBoundToWholeScene=True,
  everyNonretirementPublishedBodyBoundToWholeSceneDMA=True,
  actualPreRetirementQueuedButNotDrawnBodyParts=sum(missing.values()),
  actualUndrawnQueueParts=[dict(frame=k[0],source=f'{k[1]:08X}',command=f'{k[2]:04X}',x=k[3],y=k[4],width=k[5],height=k[6],count=v)for k,v in missing.items()],
  retirementQueueDiscardMechanismSourceProven=False,"""
 need(source.count(before)==1,'Do not claim the three observed undrawn publications reached hardware')
 source=source.replace(before,after,1)
 ns=dict(base.check_context.__globals__)
 exec(compile(source,__file__+'::actual_observed_retirement_queue_nonpublication','exec'),ns)
 run_source=inspect.getsource(base.run)
 ns['check_context']=ns['check_context']
 exec(compile(run_source,__file__+'::entire_original_transition_source_scope','exec'),ns)
 report=ns['run']()
 report.update(preservedOriginalFailure=str(failure),scope=__doc__)
 for p in(failure,Path(__file__),Path(base.__file__)):
  report['inputHashes'][str(p.resolve())]=sha(p)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable observed retirement/source proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualFaultsRejected','wholeNativeHealth','wholeNativeState')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
