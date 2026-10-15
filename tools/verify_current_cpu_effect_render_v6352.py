"""Retain early-host-read failure; same captured scene once report is published."""
import inspect,json
from pathlib import Path
import verify_current_cpu_effect_render_v6350 as prior
ROOT,need=prior.ROOT,prior.need
OUT=ROOT/'audit_v6353_current_cpu_effect_render_checked'


def main():
 failure=ROOT/'audit_v6351_current_cpu_effect_render_checked/failure.json'
 record=json.loads(failure.read_text())
 need(not record['passed']and record['error'].startswith('FileNotFoundError'),
      'Actual premature result-read rejection retained, never rewrite captured evidence')
 need((prior.CASE/'result.json').exists(),'Same native capture final report actually published before successor')
 source=inspect.getsource(prior.main)
 before='for path in(PARENT,Path(__file__),'
 need(source.count(before)==1,'Preserve complete original checker plus failed execution pins')
 source=source.replace(before,"for path in(ROOT/'tools/verify_current_cpu_effect_render_v6350.py',ROOT/'audit_v6351_current_cpu_effect_render_checked/failure.json',PARENT,Path(__file__),",1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT)
 exec(compile(source,__file__+'::whole_original_effect_checker_after_actual_capture_publication','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
