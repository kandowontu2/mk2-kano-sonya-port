"""Bind final blade publication to its actual intra-field retirement order.

Native field1909 publishes its final trail before running original retirement;
that committed field displays at1910. All source retirement/pool contracts
remain, and no publication after the actual retirement event is admitted.
Keep6355's overstrict frame-only rejection, same actual capture, no rerun.
"""
import gzip,inspect,json,re
from pathlib import Path
import verify_current_cpu_effect_render_v6354 as bridge
prior=bridge.prior
ROOT,need=bridge.ROOT,bridge.need
OUT=ROOT/'audit_v6357_current_cpu_effect_render_checked'


def source_gate():
 source=inspect.getsource(prior.gate)
 changes={
  "1871<=q['frame']<1909":"1872<=q['frame']<=1909",
  "q['frame']>=1909":"q['frame']>1909",
 }
 for before,after in changes.items():
  need(source.count(before)==(2 if before.startswith('1871')else 1),'Exact final original publication-field boundary')
  source=source.replace(before,after)
 scope=dict(prior.gate.__globals__)
 exec(compile(source,__file__+'::whole_original_scene_gate_committed_final_field','exec'),scope)
 return scope['gate']


def order_contract(text,sources):
 lines=text.splitlines()
 cuts=[i for i,s in enumerate(lines)if s.startswith('MK2_BLADE_ALLOC_RETIRE ')and'frame=1909 'in s and'object=01031B00 'in s]
 need(len(cuts)==1,'One exact actual original blade retirement in full log order')
 published=[]
 for i,line in enumerate(lines):
  if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE '):continue
  values=dict(re.findall(r'(\w+)=([^\s]+)',line))
  if int(values['source'],16)in sources:
   need(i<cuts[0] and values['actor']=='01031B00','No blade-source publication after actual native retirement event, even in same field')
   published.append(dict(frame=int(values['frame']),source=int(values['source'],16),lineIndex=i))
 need([r['frame']for r in published]==list(range(1872,1910)), 'Every exact actual committed blade draw field through final pre-retirement publication')
 return dict(actualRetirementField=1909,retirementLineIndex=cuts[0],lastPublication=published[-1],
             committedDrawFields=38,lastDisplayedField=1910,firstEmptyEffectField=1911,noPublicationAfterActualRetirement=True)


def main():
 failure=ROOT/'audit_v6355_current_cpu_effect_render_checked/failure.json'
 need(json.loads(failure.read_text())['error']=="ValueError('No blade art still published after native retirement')", 'Original frame-only rejection preserved')
 source=inspect.getsource(bridge.main)
 before="'for path in(PARENT,Path(__file__),':"
 need(source.count(before)==1,'Retain earlier exact serialization bridge and every source/failure')
 after="'for path in(PARENT,Path(__file__),':"
 source=source.replace("\"for path in(ROOT/'tools/verify_current_cpu_effect_render_v6350.py',", "\"for path in(ROOT/'tools/verify_current_cpu_effect_render_v6354.py',ROOT/'audit_v6355_current_cpu_effect_render_checked/failure.json',ROOT/'tools/verify_current_cpu_effect_render_v6350.py',",1)
 gate=source_gate()
 with gzip.open(prior.CASE/'run.log.gz','rt',encoding='utf-8')as file:actual_text=file.read()
 def bound(g,records,guest,payload,seq,blade_sources):
  proof=gate(g,records,guest,payload,seq,blade_sources)
  proof['actualIntraFieldRetirementOrder']=order_contract(actual_text,blade_sources)
  return proof
 # bridge creates its nested scope from prior.__dict__, so supply a shallow
 # module-like namespace with the one strengthened original gate override.
 from types import SimpleNamespace
 adapted=SimpleNamespace(**dict(prior.__dict__,gate=bound))
 scope=dict(bridge.__dict__,__file__=__file__,OUT=OUT,prior=adapted)
 exec(compile(source,__file__+'::complete_original_effect_gate_with_actual_retirement_order','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
