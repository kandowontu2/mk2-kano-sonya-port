"""Whole6030 native RAM transport/OS identity, real air catches and paired followups."""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_native_contacts_v6030 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
LUA=ROOT/'mk2ks_air_throw_roles_v6039.lua'

def run(fighter,side,victim):
 source=inspect.getsource(earlier.run)
 for before,after in(
  ('def run(fighter,side):','def run(fighter,side,victim):'),
  ('audit_v6031_contacts_{fighter}_p{side}','audit_v6041_air_{fighter}_p{side}_{victim}'),
  ("LUA,ROOT/'mk2ks_close_contacts_v6025.lua',ROOT/'mk2ks_special_shadow_v5131.lua'","LUA,ROOT/'mk2ks_special_shadow_v5131.lua'"),
  ("results[0]['phases']=='7'","results[0]['phases']=='2'"),
  ("len(scenes)>=36 and any(s['stage']=='contacts_final'for s in scenes)","len(scenes)>=35 and any(s['stage']=='air_final'for s in scenes)"),
  ("('own_high_punch_block_phase32','own_low_kick_crouch_block_phase32','own_ground_throw_entry','own_ground_throw_phase48','stock_ground_throw_phase48','contacts_final')",
   "('air_1_catch','air_1_phase32','air_1_phase48','air_2_phase48','air_2_follow64','air_final')"),
  ("folder/'contacts_preview.png'","folder/'air_preview.png'"),
  ("original=original,fighter=fighter)","original=original,fighter=fighter,victim=victim)"),
  ("scope['capture']('knife'if fighter=='kano'else'ring',side,'kitana')","scope['capture']('knife'if fighter=='kano'else'ring',side,victim)"),
  ("'audit_v6031_contacts_'+fighter+'_p'+str(side)in identity['CommandLine']","'audit_v6041_air_'+fighter+'_p'+str(side)+'_'+victim in identity['CommandLine']")):
  need(source.count(before)==1,'Exact whole native RAM air-role transport adaptation '+before[:75]);source=source.replace(before,after,1)
 scope=dict(earlier.run.__globals__,LUA=LUA,__file__=__file__)
 exec(compile(source,__file__+'::whole_native_air_role_RAM_transport','exec'),scope)
 report=scope['run'](fighter,side,victim)
 report['inputHashes'][str(Path(earlier.__file__).resolve())]=sha(earlier.__file__)
 report.update(actualAirCatchRolesAndOrdinaryFollowupProofPending=True,wholeAirBodyFloorShadowProofPending=True,
               fullPortAcceptance=False)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True)
 parser.add_argument('--victim',choices=('kitana','sonya','jax'),required=True);a=parser.parse_args()
 need(a.fighter=='kano'or a.victim=='jax','Sonya is a living victim of stock air throw, not an invented attacker')
 out=ROOT/f'audit_v6042_air_{a.fighter}_p{a.side}_{a.victim}_observed';need(not out.exists(),'Fresh immutable actual airborne case')
 try:report=run(a.fighter,a.side,a.victim)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
