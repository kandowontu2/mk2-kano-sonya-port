"""Whole air-role native transport; real ready flags and complete callback evidence."""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_air_throw_roles_v6040 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
LUA=ROOT/'mk2ks_air_native_dispatch_v6047.lua'

def run(fighter,side,victim):
 source=inspect.getsource(earlier.run)
 for before,after in(
  ('audit_v6041_air_{fighter}_p{side}_{victim}','audit_v6049_air_{fighter}_p{side}_{victim}'),
  ("LUA,ROOT/'mk2ks_special_shadow_v5131.lua'","LUA,ROOT/'mk2ks_air_throw_roles_v6039.lua',ROOT/'mk2ks_special_shadow_v5131.lua'"),
  ("'audit_v6041_air_'+fighter+'_p'+str(side)+'_'+victim in identity['CommandLine']","'audit_v6049_air_'+fighter+'_p'+str(side)+'_'+victim in identity['CommandLine']")):
  need(source.count(before)==1,'Exact complete air transport native-dispatch adaptation '+before[:70]);source=source.replace(before,after,1)
 scope=dict(earlier.run.__globals__,LUA=LUA,__file__=__file__)
 exec(compile(source,__file__+'::whole_air_role_transport_native_dispatch','exec'),scope)
 report=scope['run'](fighter,side,victim)
 report['inputHashes'][str(Path(earlier.__file__).resolve())]=sha(earlier.__file__)
 report.update(nativeSharedScratchValueNotMistakenForActiveAirCallback=True,actualCallbackRetirementAndNextJumpResetProofPending=True)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True)
 parser.add_argument('--victim',choices=('kitana','sonya','jax'),required=True);a=parser.parse_args()
 need(a.fighter=='kano'or a.victim=='jax','Sonya remains a native living victim, not a new air-throw attacker')
 out=ROOT/f'audit_v6050_air_{a.fighter}_p{a.side}_{a.victim}_observed';need(not out.exists(),'Fresh immutable actual-dispatch air-role capture')
 try:report=run(a.fighter,a.side,a.victim)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
