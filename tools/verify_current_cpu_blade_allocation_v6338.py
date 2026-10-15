"""Unchanged full allocator gate, actual successful collector successor path."""
import inspect,json
from pathlib import Path
import verify_current_cpu_blade_allocation_v6333 as prior
ROOT,need=prior.ROOT,prior.need
OUT=ROOT/'audit_v6339_current_cpu_blade_allocation_checked'


def main():
 scope=dict(prior.__dict__,__file__=__file__,CASE=ROOT/'audit_v6337_current_cpu_blade_allocation_ram',OUT=OUT)
 source=inspect.getsource(prior.main)
 before='for path in(PARENT,baseline,'
 need(source.count(before)==1,'Retain executed original gate source and prelaunch failure')
 source=source.replace(before,"for path in(ROOT/'tools/verify_current_cpu_blade_allocation_v6333.py',ROOT/'tools/capture_current_cpu_blade_allocation_v6336.py',ROOT/'audit_v6335_current_cpu_blade_allocator_prelaunch/failure.json',PARENT,baseline,",1)
 exec(compile(source,__file__+'::whole_original_gate_actual_terminal_path','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
