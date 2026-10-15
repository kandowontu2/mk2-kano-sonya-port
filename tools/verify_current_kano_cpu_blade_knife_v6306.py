"""Keep unrelated post-KO floor changes outside the complete knife window.

The all-mode HP/state/native-choice inventory remains whole-match. Only the
old knife model's allfields extent is scoped to its actual entry through both
own recovery and child retirement; every phase/guard/damage rule is unchanged.
The original6305 executed failure is preserved, not called a gameplay fix.
"""
import json
from pathlib import Path
import verify_current_kano_cpu_blade_knife_v6304 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6307_current_kano_cpu_blade_knife_checked'


def main():
 failure=ROOT/'audit_v6305_current_kano_cpu_blade_knife_checked/failure.json'
 need(not json.loads(failure.read_text())['passed'],'Retain actual old whole-match-floor rejection')
 source=Path(prior.__file__).read_text()
 changes={
  "'assert len(actions)==len(births)==2':'assert len(actions)==len(births)==1',":
   "'assert len(actions)==len(births)==2':'assert len(actions)==len(births)==1',\n"
   " \"allfields=rows(log,'FIELD');by={(r['frame'],r['slot']):r for r in allfields}\":\n"
   "  \"allfields=[r for r in rows(log,'FIELD')if actions[0]['frame']<r['frame']<=max(actions[0]['frame']+50,max(q['frame']for q in overlap.rows(log,'RETIRE')))];by={(r['frame'],r['slot']):r for r in allfields}\",",
  '"native[\'mode\']==2",':'"native[\'mode\']==(2)",',
  "OUT=ROOT/'audit_v6305_current_kano_cpu_blade_knife_checked'":"OUT=ROOT/'audit_v6307_current_kano_cpu_blade_knife_checked'",
  'for path in(PARENT,Path(__file__),':'for path in(failure,Path(prior.__file__),PARENT,Path(__file__),',
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Exact scoped knife context correction');source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,__name__='current_complete_knife_window',failure=failure,prior=prior)
 exec(compile(source,__file__+'::whole_prior_phase_and_fault_contract','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
