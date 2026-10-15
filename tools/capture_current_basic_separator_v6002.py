"""Whole5994 transport with explicit Lua comment/driver separator; no game edits."""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_basic_ground_v5994 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
LUA=ROOT/'mk2ks_basic_ground_separator_v6001.lua'

def run(fighter,side):
 failed=[ROOT/'audit_v5996_basic_kano_p1_observed/report.json',ROOT/'audit_v6000_basic_kano_p1_observed/report.json']
 need(all(not json.loads(p.read_text())['passed']for p in failed)and
      '5993.lua:13: assertion failed'in(ROOT/'audit_v5995_basic_kano_p1/stderr.log').read_text()and
      'syntax error near'in(ROOT/'audit_v5999_basic_kano_p1/stderr.log').read_text(),'Both actual frame0 observer-binding failures retained')
 source=inspect.getsource(earlier.run)
 before='audit_v5995_basic_{fighter}_p{side}';need(source.count(before)==1,'One fresh capture folder')
 source=source.replace(before,'audit_v6003_basic_{fighter}_p{side}',1)
 scope=dict(earlier.run.__globals__,LUA=LUA,__file__=__file__)
 exec(compile(source,__file__+'::whole5994_explicit_comment_separator','exec'),scope)
 report=scope['run'](fighter,side)
 for p in(Path(earlier.__file__).resolve(),ROOT/'mk2ks_basic_ground_shadow_v5993.lua',ROOT/'mk2ks_basic_ground_binding_v5997.lua',
          ROOT/'tools/capture_current_basic_binding_v5998.py',*failed,ROOT/'audit_v5995_basic_kano_p1/stderr.log',ROOT/'audit_v5999_basic_kano_p1/stderr.log'):
  report['inputHashes'][str(p)]=sha(p)
 report['retainedFailedBindings']=[str(p)for p in failed]
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v6004_basic_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh immutable ordinary separator capture')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
