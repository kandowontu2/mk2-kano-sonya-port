"""Whole5933 scene gate; preserve its actual capture-host alias collision.

Restore only original5909's executed renderer module (5905) in its namespace.
Retain every source/native/current/reference/shadow/font/fault predicate.
"""
import argparse
from verify_current_pit_shadow_bound_scene_v5933 import *
import verify_current_pit_shadow_bound_scene_v5933 as failed_validator
import verify_current_cross_pit_retained_scene_v5909 as retained
FAILED_ALIAS=ROOT/'audit_v5934_current_kano_p1_pit_native_shadow_scene_checked/report.json'
source=failed_validator.run.source
old=" for p in (FAILED,Path(executed.__file__),Path(contract.executed.__file__)):pins[str(p)]=sha(p)"
need(source.count(old)==1,'Whole preceding gates unchanged, failed namespace/capture sources added')
source=source.replace(old,old+"\n for p in (FAILED_ALIAS,Path(failed_validator.__file__),ROOT/'tools/verify_current_pit_original_shadow_scene_v5930.py'):pins[str(p)]=sha(p)",1)
scope=dict(failed_validator.run.__globals__,__file__=__file__,__doc__=__doc__,executed=retained.executed,
           FAILED_ALIAS=FAILED_ALIAS,failed_validator=failed_validator)
exec(compile(source,__file__+'::whole5933_correct_original_renderer_module','exec'),scope)
run=scope['run'];run.source=source
need(run.__globals__['executed']is retained.executed and run.__globals__['contract'].scene_contract.__globals__['continuous']is retained.contract.previous.continuous,
     'Both exact original renderer bindings resolved before any evidence qualification')

if __name__=='__main__':
 failure=json.loads(FAILED_ALIAS.read_text());need(not failure['passed']and failure['error']=="AttributeError(\"module 'verify_current_pit_original_shadow_scene_v5930' has no attribute 'paths'\")",'Preserve actual5934 module-alias failure')
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 OUT=ROOT/f'audit_v5936_current_{args.fighter}_p{args.side}_pit_stock_shadow_scene_checked'
 need(not OUT.exists(),'Fresh immutable complete finite Pit scene qualification')
 try:report=run(args.fighter,args.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(report,indent=2)+'\n')
 for p in (Path(__file__),path):
  before=sha(p);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(done.returncode==0 and sha(p)==before,'Lossless bounded source/evidence compression')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','nativeScene')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
