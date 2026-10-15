"""Whole actual first P2 Sub-Zero encounter, not a tower or planned-move pass.

Retain the complete5632 guest/source/state/input/reset/fault gate, dispatch the
ordinary5188 independent Sub-Zero factory with slot2, and fault real native
action rows. Never credit an unexecuted HUMAN107 branch or a natural clear.
"""
import collections,inspect,json,re,traceback
from pathlib import Path
from types import SimpleNamespace
import verify_current_sonya_p2_kitana_prefix_v5632 as previous
import verify_current_sonya_p2_campaign_v5630 as original
import verify_tested_prime_prefix_v5188 as subzero
import run_verified_kitana_jax_sonya_p2_campaign_v5663 as capture
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5670_current_sonya_p2_subzero_prefix_checked'


def run():
 source=inspect.getsource(previous.run)
 for before,after in [('whole.original.supplemental.kitana','whole.subzero'),
  (' stage=2',' stage=7'),(' stage=3 ',' stage=8 '),('cpuIdentity=4','cpuIdentity=8')]:
  need(source.count(before)==1,'One whole actual encounter context adaptation '+before)
  source=source.replace(before,after,1)
 source=source.replace('KITANA_FIELD','SUBZERO_FIELD').replace('KITANA_DECISION','SUBZERO_DECISION')
 # Bind both real module provenance and the ordinary parser namespace.5188's
 # make_replay globals contain kitana.original, not a direct original alias.
 parser_carrier=SimpleNamespace(**vars(subzero))
 parser_carrier.original=subzero.kitana.original
 carrier=SimpleNamespace(__file__=original.__file__,capture=capture,
  subzero=parser_carrier,p2_factory=original.p2_factory)
 scope=dict(vars(previous),__file__=__file__,OUT=OUT,whole=carrier)
 exec(compile(source,__file__+'::entire_completed_SubZero_P2_encounter','exec'),scope)
 report=scope['run']()
 # Read the same bounded, complete native encounter again; no growing-log
 # hash, no synthetic rows and no mutation of the executed input sources.
 lines=[];seen=False;count=0
 import gzip
 with gzip.open(capture.OUT/'run.log.gz','rt',encoding='utf-8',newline='')as reader:
  for line in reader:
   need(line.endswith('\n'),'Only complete real native encounter records')
   count+=len(line.encode());need(count<=128*1024*1024,'Same bounded actual first encounter')
   lines.append(line)
   if line.startswith('MK2_NAT_CAMPAIGN_SUBZERO_FIELD '):seen=True
   if seen and ((line.startswith('MK2_NAT_CAMPAIGN_LOSS ')and ' stage=7'in line)or
    (line.startswith('MK2_NAT_CAMPAIGN_STAGE ')and ' stage=8 'in line)):break
  else:raise ValueError('Actual completed Sub-Zero boundary unavailable; never restart the live job')
 text=''.join(lines)
 need(report['actualNativePrefixSHA256']==__import__('hashlib').sha256(text.encode()).hexdigest().upper(),
  'Exactly the same already-qualified complete native encounter')
 replay=original.p2_factory(subzero.make_replay,subzero)()
 positive=replay(text);rows=subzero.kitana.original.parse(text)
 actions=[r for r in rows if r['tag']=='SUBZERO_ACTION']
 need(actions and positive['actualNativeLegActivations']>0,
  'Actual owned native action and leg task entry, never planned inputs credited')
 action=actions[0]
 line=next(s for s in lines if s.startswith('MK2_NAT_CAMPAIGN_SUBZERO_ACTION frame='+str(action['frame'])+' ')
  and ' actor='+action['actor']+' 'in s and ' after='+action['after']+' 'in s)
 faults=[]
 for key,value in [('owner','01000000'),('at','01000000'),('a8','01000000'),('mask','00FF')]:
  damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and damaged!=line,'Nonvacuous real native action fault '+key)
  try:replay(text.replace(line,damaged,1))
  except ValueError as error:faults.append(dict(tag='SUBZERO_ACTION',key=key,rejectedBy=str(error)))
  else:raise ValueError('Real native owned action fault admitted '+key)
 uppercuts=[r for r in actions if int(r['after'])==0x107]
 if uppercuts:
  action=uppercuts[0]
  line=next(s for s in lines if s.startswith('MK2_NAT_CAMPAIGN_SUBZERO_ACTION frame='+str(action['frame'])+' ')
   and ' actor='+action['actor']+' 'in s and ' after=263 'in s)
  for key,value in [('pc','FFF00000'),('a1','00000106')]:
   damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
   need(n==1 and damaged!=line,'Nonvacuous executed HUMAN107 store fault')
   try:replay(text.replace(line,damaged,1))
   except ValueError as error:faults.append(dict(tag='SUBZERO_ACTION',key=key,rejectedBy=str(error)))
   else:raise ValueError('Actual HUMAN107 uppercut instruction fault admitted '+key)
 need(replay(text)==positive==report['actualCompletePhysicalReplay'],'Whole actual native positive restored')
 for path in [Path(subzero.__file__),Path(subzero.kitana.original.__file__)]:
  report['inputHashes'][str(path.resolve())]=sha(path)
 fields=[r for r in rows if r['tag']=='SUBZERO_FIELD']
 report.update(actualOwnedActionFaultsRejected=faults,
  actualCPUActionHistogram=dict(collections.Counter(int(r['cpu_action'])for r in fields)),
  executedNativeHuman107InstructionGateAccepted=bool(uppercuts),
  actualHuman107Stores=len(uppercuts),
  scope='Complete actual first Sub-Zero P2 input/state/reset/ownership/action replay and every-byte initialized current guest. Executed HUMAN107 instruction coverage is reported separately, never assumed from intended commands. No tower, full art/shadow/audio or port acceptance.')
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every immutable actual source/proof unchanged')
 return report


if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable actual Sub-Zero encounter proof');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
