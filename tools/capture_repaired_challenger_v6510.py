"""Whole original physical challenger policy on isolated candidate; native memory first.

No public CMD promotion, input retiming, forced state, HP assistance or test
deadline acceptance. The original Sonya failure remains an immutable failure.
"""
import argparse,inspect
from pathlib import Path
import capture_current_challenger_v6487 as executed
import qualify_current_challenger_boundary_v6489 as qualified
import native_projectile_identifiers_context_v6509 as candidate
ROOT,need=executed.ROOT,executed.need

def capture(fighter,side):
 factory=inspect.getsource(executed.bindings)
 changes={
  "'audit_v6480_current_continue_':'audit_v6488_current_challenger_'":
  "'audit_v6480_current_continue_':'audit_v6511_repaired_challenger_'",
  "'paths=[LUA,DRIVER,Path(prior.__file__),Path(__file__),'":
  "'paths=[LUA,DRIVER,ROOT/\"mk2ks_current_challenger_v6486.lua\",ROOT/\"mk2ks_current_challenger_ancestry_v6496.lua\",Path(prior.__file__),Path(executed.__file__),Path(qualified.__file__),Path(__file__),'",
  'lua=ROOT/\'mk2ks_current_challenger_v6486.lua\'':
  'lua=ROOT/\'mk2ks_current_challenger_cleanup_v6499.lua\'',
  '"driver.count(\'manager.machine:exit()\')==2"':'"driver.count(\'dofile(\')==1"',
  'scope=dict(prior.__dict__,__file__=__file__,prior=prior,LUA=lua,DRIVER=lua,gate=gate)':
  'scope=dict(prior.__dict__,__file__=__file__,prior=prior,executed=executed,qualified=qualified,current=candidate,LUA=lua,DRIVER=lua,gate=gate)',
  "source=inspect.getsource(prior.capture)":
  "source=inspect.getsource(prior.capture).replace(\"ROOT/'PLAY_MK2_KANO_SONYA.cmd'\",\"ROOT/'TEST_PROJECTILE_IDENTIFIERS_V6508.cmd'\")",
 }
 for before,after in changes.items():
  need(factory.count(before)==1,'Exact isolated-candidate collector adaptation '+before);factory=factory.replace(before,after,1)
 scope=dict(executed.__dict__,__file__=__file__,executed=executed,qualified=qualified,candidate=candidate,gate=qualified.gate)
 exec(compile(factory,__file__+'::whole_original_physical_policy_isolated_candidate','exec'),scope)
 scope['bindings']()(fighter,side)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));parser.add_argument('--side',required=True,type=int,choices=(1,2))
 a=parser.parse_args();capture(a.fighter,a.side)
