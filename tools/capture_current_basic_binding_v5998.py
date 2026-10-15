"""Whole5994 transport, corrected both-record stage-word Lua binding.

Retain the real5993 frame0 assertion failure. No game logic changes, file-copy
recovery trees, guest assistance or fallback to an older executable.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_basic_ground_v5994 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
LUA=ROOT/'mk2ks_basic_ground_binding_v5997.lua'

def run(fighter,side):
 failed=ROOT/'audit_v5996_basic_kano_p1_observed/report.json'
 error=json.loads(failed.read_text())
 need(not error['passed']and 'Actual successful terminal native boot'in error['error']and
      '5993.lua:13: assertion failed'in(ROOT/'audit_v5995_basic_kano_p1/stderr.log').read_text(),
      'Actual frame0 source-binding failure retained')
 source=inspect.getsource(earlier.run)
 before='audit_v5995_basic_{fighter}_p{side}'
 need(source.count(before)==1,'One fresh output folder');source=source.replace(before,'audit_v5999_basic_{fighter}_p{side}',1)
 scope=dict(earlier.run.__globals__,LUA=LUA,__file__=__file__)
 exec(compile(source,__file__+'::whole5994_corrected_two_record_Lua','exec'),scope)
 report=scope['run'](fighter,side)
 for p in(Path(earlier.__file__).resolve(),ROOT/'mk2ks_basic_ground_shadow_v5993.lua',failed,
          ROOT/'audit_v5995_basic_kano_p1/stderr.log'):
  report['inputHashes'][str(p)]=sha(p)
 report['retainedFailedBinding']=str(failed)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v6000_basic_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh immutable corrected ordinary capture')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
