"""Whole5930 actual scene qualification, original native globals restored."""
import argparse
from verify_current_pit_original_shadow_scene_v5930 import *
import verify_current_pit_original_shadow_scene_v5930 as executed
import current_pit_shadow_schedule_bindings_v5932 as contract
FAILED=ROOT/'audit_v5931_current_kano_p1_pit_original_shadow_scene_checked/report.json'
source=executed.run.source
old=" for p in (Path(previous.__file__),contract.REFERENCE,contract.ORDINARY):pins[str(p)]=sha(p)"
need(source.count(old)==1,'Only repaired namespace and retained failure/source pins added')
source=source.replace(old,old+"\n for p in (FAILED,Path(executed.__file__),Path(contract.executed.__file__)):pins[str(p)]=sha(p)",1)
scope=dict(executed.run.__globals__,__file__=__file__,__doc__=__doc__,contract=contract,FAILED=FAILED,executed=executed)
exec(compile(source,__file__+'::entire5930_original_continuous_binding_restored','exec'),scope)
run=scope['run'];run.source=source

if __name__=='__main__':
 failure=json.loads(FAILED.read_text());need(not failure['passed']and failure['error']=="NameError(\"name 'continuous' is not defined\")",'Actual5931 binding failure retained')
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 OUT=ROOT/f'audit_v5934_current_{args.fighter}_p{args.side}_pit_native_shadow_scene_checked'
 need(not OUT.exists(),'Fresh immutable complete current scene qualification')
 try:report=run(args.fighter,args.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(report,indent=2)+'\n')
 for p in (Path(__file__),Path(contract.__file__),path):
  before=sha(p);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(done.returncode==0 and sha(p)==before,'Lossless bounded immutable source/evidence')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','nativeScene')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
