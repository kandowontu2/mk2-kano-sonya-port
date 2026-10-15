"""Bind actual fault rows to Sub-Zero7, not earlier Kitana/Jax Ring fields.

Preserve5675's combined physical proof; qualify this new target specifically.
The actual completed match was lost. No natural advancement is credited.
"""
import inspect,json,re,traceback
from pathlib import Path
import verify_sonya_p2_subzero_ring_probe_v5674 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5677_sonya_p2_subzero_ring_bound_checked'


def run():
 source=inspect.getsource(previous.run)
 before=' scope=dict(vars(original),__file__=__file__,capture=capture,OUT=OUT,'
 need(source.count(before)==1,'One ordinary complete verifier binding site')
 addition=""" before="fields=[r for r in rows if r['tag']=='RANGE_FIELD'];f=fields[0];faults=[]"
 after="fields=[r for r in rows if r['tag']=='RANGE_FIELD'and r['stage']=='7'];f=fields[0];faults=[]"
 need(source.count(before)==1,'Every actual input/state fault must target native Sub-Zero fields')
 source=source.replace(before,after,1)
"""
 source=source.replace(before,addition+before,1)
 scope=dict(vars(previous),__file__=__file__,OUT=OUT)
 exec(compile(source,__file__+'::entire_completed_encounter_faults_bound_to_SubZero7','exec'),scope)
 report=scope['run']()
 import gzip
 text=gzip.open(previous.capture.OUT/'run.log.gz','rt',encoding='utf-8').read().replace('\r\n','\n')
 rows=previous.original.original.parse(text)
 rings=[r for r in rows if r['tag']=='SPECIAL'and r['stage']=='7'and r['move']=='ring']
 fields=[r for r in rows if r['tag']=='RANGE_FIELD'and r['stage']=='7']
 need(rings and fields,'Real owned Sub-Zero encounter Ring tasks and complete per-field provenance')
 replay=previous.make_replay();positive=replay(text)
 native=previous.native_gate(text,previous.capture.native.expected())
 need(positive==report['actualFullRingSpacingReplay']and native==report['native'],
  'Entire actual physical and native positive, no substituted match')
 faults=[]
 ring=rings[0]
 line=next(s for s in text.splitlines()if s.startswith('MK2_NAT_CAMPAIGN_SPECIAL frame='+str(ring['frame'])+' ')
  and ' stage=7 'in s and ' move=ring 'in s)
 for key,value in [('id','1'),('a8','01000000'),('entry','FFF00000'),('pc','FFF00000')]:
  damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and damaged!=line,'Nonvacuous actual context8 Ring task fault '+key)
  try:replay(text.replace(line,damaged,1))
  except ValueError as error:faults.append(dict(tag='SPECIAL',stage=7,key=key,rejectedBy=str(error)))
  else:raise ValueError('Actual native context8 owned Ring task fault admitted '+key)
 action=next(r for r in rows if r['tag']=='RANGE_ACTION'and r['stage']=='7')
 line=next(s for s in text.splitlines()if s.startswith('MK2_NAT_CAMPAIGN_RANGE_ACTION frame='+str(action['frame'])+' ')
  and ' stage=7 'in s and ' actor='+action['actor']+' 'in s and ' after='+action['after']+' 'in s)
 for key,value in [('owner','01000000'),('at','01000000'),('mask','00FF'),('a8','01000000')]:
  damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and damaged!=line,'Nonvacuous real context8 native action fault '+key)
  try:replay(text.replace(line,damaged,1))
  except ValueError as error:faults.append(dict(tag='RANGE_ACTION',stage=7,key=key,rejectedBy=str(error)))
  else:raise ValueError('Actual context8 native action fault admitted '+key)
 need(replay(text)==positive,'Entire native physical positive restored')
 prior=previous.OUT/'report.json';old=json.loads(prior.read_text())
 need(old['passed']and not native['actualSubZeroEncounterWon'],
  'Original combined proof preserved; actual lost encounter never a fabricated clear')
 for p in [Path(previous.__file__),prior,Path(__file__)]:
  report['inputHashes'][str(p.resolve())]=sha(p)
 report.update(actualContext8RingTasks=len(rings),actualContext8PhysicalFields=len(fields),
  allElevenStateInputWinnerFaultsTargetActualSubZero=True,
  actualContext8TaskAndActionFaultsRejected=faults,
  priorCombinedProof=str(prior),actualSubZeroAdvanceAccepted=False,
  scope='Every actual field/input/reset/owner/action across Kitana,Jax,Sub-Zero plus11actual Sub-Zero state/input/winner faults and8actual Sub-Zero Ring/task action faults. One own round, two CPU rounds, genuine first match loss. No tower/full art/shadow/audio/port acceptance.')
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Actual source/evidence bytes intact')
 return report


if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable context-bound native proof');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
