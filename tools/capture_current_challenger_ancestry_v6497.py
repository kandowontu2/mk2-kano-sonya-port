"""Same failed inputs and terminal-first RAM collector, passive error entry."""
import inspect
from pathlib import Path
import capture_current_challenger_v6487 as executed
import qualify_current_challenger_boundary_v6489 as qualified
ROOT,need=executed.ROOT,executed.need

def capture():
 source=inspect.getsource(executed.bindings)
 changes={
  "'audit_v6480_current_continue_':'audit_v6488_current_challenger_'":
  "'audit_v6480_current_continue_':'audit_v6498_current_challenger_ancestry_'",
  'lua=ROOT/\'mk2ks_current_challenger_v6486.lua\'':
  'lua=ROOT/\'mk2ks_current_challenger_ancestry_v6496.lua\'',
  '"driver.count(\'manager.machine:exit()\')==2"':'"driver.count(\'dofile(\')==1"',
  "'paths=[LUA,DRIVER,Path(prior.__file__),Path(__file__),'":
  "'paths=[LUA,DRIVER,ROOT/\"mk2ks_current_challenger_v6486.lua\",Path(prior.__file__),Path(executed.__file__),Path(qualified.__file__),Path(__file__),'",
  'scope=dict(prior.__dict__,__file__=__file__,prior=prior,LUA=lua,DRIVER=lua,gate=gate)':
  'scope=dict(prior.__dict__,__file__=__file__,prior=prior,executed=executed,qualified=qualified,LUA=lua,DRIVER=lua,gate=gate)',
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Exact ancestry diagnostic adaptation '+before);source=source.replace(before,after,1)
 scope=dict(executed.__dict__,__file__=__file__,executed=executed,qualified=qualified,gate=qualified.gate)
 exec(compile(source,__file__+'::same_failed_inputs_passive_ancestry','exec'),scope)
 scope['bindings']()('sonya',2)

if __name__=='__main__':capture()
