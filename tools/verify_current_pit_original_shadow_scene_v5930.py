"""Whole actual5906 complete current Pit scene with original stock shadow policy.

No native reboot or reconstructed raw comparison targets. All full movie31,
source-native floor6, earned12 and new shadow/font5 faults remain mandatory.
Keep broader victim/audio/choreography/gameplay/release scope open.
"""
import argparse,inspect
from verify_current_cross_pit_retained_scene_v5909 import *
import verify_current_cross_pit_retained_scene_v5909 as previous
import current_pit_shadow_schedule_contract_v5929 as contract
source=inspect.getsource(previous.run)
old=" for p in (matrixpath,failed_out/'report.json',Path(__file__).resolve(),Path(contract.__file__).resolve()):pins[str(p)]=sha(p)"
need(source.count(old)==1,'Whole executed renderer, failed gates and independent current audio retained')
source=source.replace(old,old+"\n for p in (Path(previous.__file__),contract.REFERENCE,contract.ORDINARY):pins[str(p)]=sha(p)",1)
old='actualCurrentCrossPitCompleteRetainedNativeSceneAccepted=True,'
need(source.count(old)==1,'Finite whole-current Pit scene only, not broader game or audio acceptance')
source=source.replace(old,old+'wholeNativePitShadowPolicyAccepted=True,completeNativePitSceneAccepted=True,',1)
scope=dict(vars(previous),__file__=__file__,__doc__=__doc__,contract=contract,previous=previous)
exec(compile(source,__file__+'::whole5909_original_native_shadow_successor','exec'),scope)
run=scope['run'];run.source=source

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 OUT=ROOT/f'audit_v5931_current_{args.fighter}_p{args.side}_pit_original_shadow_scene_checked'
 need(not OUT.exists(),'Fresh immutable full current finite scene qualification')
 try:report=run(args.fighter,args.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(report,indent=2)+'\n')
 for p in (Path(__file__),Path(contract.__file__),path):
  before=sha(p);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(done.returncode==0 and sha(p)==before,'Bounded immutable source/evidence compression')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','nativeScene')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
