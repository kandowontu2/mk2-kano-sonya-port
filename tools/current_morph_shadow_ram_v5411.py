"""Preserve actual v5407 snapshot-size harness failure; use native 400x254.

Only snapshot dimensions change. Original controller and body/shadow observer,
complete native trajectory, all source/geometry/cadence gates remain unchanged.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import current_morph_shadow_ram_v5407 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
BASE=ROOT/'audit_v5412_current_morph_shadow_ram'
OUT=ROOT/'audit_v5413_current_morph_shadow_checked'

def run(target,side):
 failure=ROOT/'audit_v5409_current_morph_shadow_checked/kano_p1/report.json'
 need(not json.loads(failure.read_text())['passed'],'Original actually executed capture failure preserved')
 stderr=ROOT/'audit_v5408_current_morph_shadow_ram/kano_p1/stderr.log'
 need(stderr.read_text().count('actual_native_morph_body_shadow_v5407:137: assertion failed!')==6,
  'All six actual snapshot dimensions failed observer assertion, not original controller')
 source=inspect.getsource(original.capture)
 before=" command[command.index('-autoboot_script')+1]=str(LUA)"
 need(source.count(before)==1,'Exact command snapshot-size adaptation point')
 source=source.replace(before,before+"\n command[command.index('-snapsize')+1]='400x254'",1)
 before=' for file in(LUA,Path(__file__).resolve(),Path(native.__file__),'
 after=' for file in(LUA,Path(__file__).resolve(),Path(original.__file__),failure,stderr,Path(native.__file__),'
 need(source.count(before)==1,'Bind actual failed evidence and both executed harness sources');source=source.replace(before,after,1)
 ns=dict(original.capture.__globals__,BASE=BASE,OUT=OUT,__file__=__file__,original=original,failure=failure,stderr=stderr)
 exec(compile(source,__file__+'::entire_original_capture_native_snapshot_size','exec'),ns)
 return ns['capture'](target,side)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--target',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 try:run(a.target,a.side)
 except Exception as error:
  value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  path=OUT/f'{a.target}_p{a.side}';path.mkdir(parents=True,exist_ok=True)
  need(not(path/'report.json').exists(),'Immutable result');original.save(path/'report.json',value)
  print(json.dumps(value,indent=2),flush=True);raise SystemExit(1)
