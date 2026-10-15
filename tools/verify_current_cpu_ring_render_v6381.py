"""Keep the complete Ring proof; bind every DMA to its passive register tap.

The preserved6379 negative test exposed an unowned-DMA source discrepancy
outside its body/child FIFO gate. Check the independent actual source and
command observations for every event, including background and shadow draws.
No native rerun, record removal, game change or weakened counterexample.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import verify_current_cpu_ring_render_v6379 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v6382_current_cpu_ring_render_checked'


def native_gate(groups,*args):
 registers={r['event']:r for r in groups['FLOOR_DMA_REGS']}
 dmas={r['event']:r for r in groups['FLOOR_DMA']}
 need(len(registers)==len(groups['FLOOR_DMA_REGS']) and
      len(dmas)==len(groups['FLOOR_DMA']) and set(registers)==set(dmas),
      'Every actual DMA has one independent passive register observation')
 for event,row in dmas.items():
  register=registers[event]
  need(all(register[k]==row[k] for k in ('frame','source','command')),
       'Every owned and unowned DMA source/command matches actual registers')
 result=original.native_gate(groups,*args)
 return {**result,'allNativeDMARegisterBindings':len(dmas)}


def main(preflight=False):
 source=inspect.getsource(original.main)
 before='Path(__file__),Path(original.__file__),Path(shadows.__file__)'
 need(source.count(before)==1,'Pin the preserved original checker and successor')
 source=source.replace(before,'Path(__file__),Path(prior.__file__),Path(original.__file__),Path(shadows.__file__)',1)
 scope=dict(original.__dict__,OUT=OUT,__file__=__file__,prior=original,native_gate=native_gate)
 exec(compile(source,__file__+'::whole6379_plus_complete_DMA_register_binding','exec'),scope)
 return scope['main'](preflight)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if not args.preflight:OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
