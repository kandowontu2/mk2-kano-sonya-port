"""Bind the real mode7-to2 entry field, with complete mode2 knife callbacks.

This single first knife starts during the actual round-fill handoff, not in
the middle of round1. Preserve both failed host assumptions and native trace.
"""
import json
from pathlib import Path
import verify_current_kano_cpu_blade_knife_v6306 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6309_current_kano_cpu_blade_knife_checked'


def main():
 failure7=ROOT/'audit_v6307_current_kano_cpu_blade_knife_checked/failure.json'
 need(not json.loads(failure7.read_text())['passed'],'Retain original mode-assumption rejection')
 source=Path(prior.__file__).read_text()
 before='"native[\'mode\']==(2)",'
 need(source.count(before)==1,'Single current native entry-field correction')
 source=source.replace(before,'"native[\'mode\']==(7)",',1)
 source=source.replace('audit_v6307_current_kano_cpu_blade_knife_checked','audit_v6309_current_kano_cpu_blade_knife_checked')
 before="'for path in(failure,Path(prior.__file__),PARENT,Path(__file__),',"
 after="'for path in(failure7,ROOT/\'tools/verify_current_kano_cpu_blade_knife_v6306.py\',failure,Path(prior.__file__),PARENT,Path(__file__),',"
 need(source.count(before)==1,'Both executed corrections and failures pinned');source=source.replace(before,after,1)
 before='changes={'
 after="changes={\n  'shots=knife(text,guest)':\n   \"shots=knife(text,guest)\\n need(all(r['mode']==2 for r in model.knife.R.rows(text,'FIELD')if 2443<=r['frame']<=2495),'Every actual knife lifecycle callback is mode2 after the observed mode7 handoff')\","
 need(source.count(before)==1,'Complete knife live-callback mode check');source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__name__='native_round_entry_context',__file__=__file__,failure7=failure7)
 exec(compile(source,__file__+'::whole_existing_phase_and_fault_contract','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
