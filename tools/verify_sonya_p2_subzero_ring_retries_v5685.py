"""Independent entire real input/native gate;3losses or true stage8 advance.

No first-round win or observer timeout is credited as a match/tower clear.
Native PC/ID/HP winner checks and all19actual Sub-Zero fault gates retained.
"""
import inspect,json,re,traceback
from pathlib import Path
import verify_sonya_p2_subzero_ring_record_bound_v5678 as previous
import verify_sonya_p2_subzero_ring_bound_v5676 as bound
import verify_sonya_p2_subzero_ring_probe_v5674 as context
import run_sonya_p2_subzero_ring_retries_v5683 as capture
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5686_sonya_p2_subzero_ring_retries_checked'


def native_gate(text,guest):
 source=inspect.getsource(context.original.native_gate)
 changes=[("r['stage']=='2'","r['stage']=='7'"),('18 if side==2 else 4','18 if side==2 else 8'),
  ("end['stage']=='3'","end['stage']=='8'"),("end['stage']=='2'","end['stage']=='7'"),
  ('==[0,1,2,3]','==list(range(9))'),('==[0,1,2]','==list(range(8))'),
  ('and not losses and','and len(losses)<3 and'),('len(losses)==1','len(losses)==3')]
 for before,after in changes:
  need(source.count(before)==(2 if before=="r['stage']=='2'"else 1),'Whole native3encounter context adaptation '+before)
  source=source.replace(before,after)
 source=source.replace('Kitana','SubZero').replace('MK2_KITANA_RING_PROBE_BOUNDARY','MK2_SUBZERO_RING_RETRY_BOUNDARY')
 scope=dict(vars(context.original),__file__=__file__)
 exec(compile(source,__file__+'::whole_native_PC_ID_HP_winner_and_stage_gate','exec'),scope)
 positive=scope['native_gate'](text,guest)
 rows=context.original.original.parse(text)
 losses=[r for r in rows if r['tag']=='LOSS'and r['stage']=='7']
 counter=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()
  if s.startswith('MK2_SUBZERO_RING_RETRY_LOSS ')]
 need(len(losses)==len(counter)<=3 and [int(r['actual_losses'])for r in counter]==list(range(1,len(counter)+1))and
  [r['frame']for r in losses]==[int(r['frame'])for r in counter],
  'Exactly one actual native paid-loss row per read-only retry counter edge')
 selections=[r for r in rows if r['tag']=='SELECT_ID']
 need(len(selections)==2*(len(losses)+(1 if positive['actualSubZeroEncounterWon']else 0)),
  'Exactly two true-ID confirmation checkpoints for every real continued selection')
 last_selection=max(r['frame']for r in selections)
 final_wins=[r for r in rows if r['tag']=='WIN'and r['stage']=='7'and r['frame']>last_selection]
 own=sum(r['slot']=='2'for r in final_wins);cpu=sum(r['slot']=='1'for r in final_wins)
 need((positive['actualSubZeroEncounterWon']and own==2 and cpu<=1)or
  (not positive['actualSubZeroEncounterWon']and cpu==2 and own<=1),
  'Actual final match two native rounds by one side; previous lost-match round wins cannot fabricate advancement')
 need('MK2_SUBZERO_RING_RETRY_FRAME_LIMIT 'not in text,'No finite observer/frame deadline credited as a complete encounter')
 positive.update(actualContinuedLosses=len(losses),actualFinalMatchOwnRoundWins=own,
  actualFinalMatchCpuRoundWins=cpu,actualRetryCounterEdges=counter)
 return positive


def run():
 # Rebind the real capture/native gate in the ordinary complete proof carrier.
 #5685 never mutates the executed old gate or its sources/evidence.
 carrier=type('Context',(),{})()
 for name,value in vars(context).items():setattr(carrier,name,value)
 carrier.capture=capture;carrier.native_gate=native_gate
 bound_carrier=type('Bound',(),{})()
 for name,value in vars(bound).items():setattr(bound_carrier,name,value)
 bound_carrier.previous=carrier
 scope=dict(vars(previous),__file__=__file__,OUT=OUT,previous=bound_carrier)
 source=inspect.getsource(previous.run)
 # Previously this proof deliberately required a lost first match. Here the
 # entire retained native gate proves the actual finite outcome either way.
 target="need(old['passed']and not native['actualSubZeroEncounterWon'],"
 replacement="need(old['passed']and isinstance(native['actualSubZeroEncounterWon'],bool),"
 need(source.count("source=inspect.getsource(previous.run)")==1,'One ordinary whole bound-proof source assembly')
 addition=f" source=source.replace({target!r},{replacement!r},1)\n"
 site=' scope=dict(vars(previous),__file__=__file__,OUT=OUT)'
 need(source.count(site)==1,'One original complete fault-proof binding')
 source=source.replace(site,addition+site,1)
 exec(compile(source,__file__+'::whole19actual_faults_with_native_retry_outcome','exec'),scope)
 report=scope['run']()
 report.update(actualSubZeroAdvanceAccepted=report['native']['actualSubZeroEncounterWon'],
  actualRetryBound=3,fullTowerAccepted=False,
  scope='Whole real finite3loss comparison: every actual Kitana/Jax/Sub-Zero physical field,19actual target-state/input/task/action/native-winner faults, independently counted genuine continued selections and final-match two-round winner, actual source-exact initialized guest. Genuine stage8 advance or actual third lost match only; never a whole tower/art/audio/port pass.')
 for p in [Path(__file__),Path(capture.__file__),Path(context.__file__),Path(bound.__file__),Path(previous.__file__)]:
  report['inputHashes'][str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All actual source/proof/failure bytes preserved')
 return report


if __name__=='__main__':
 need((capture.OUT/'result.json').is_file(),'Await actual terminal, never duplicate a live capture')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable real retry proof');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
