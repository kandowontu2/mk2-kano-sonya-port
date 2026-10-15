"""Whole6487 native capture with the independently qualified callback boundary.

No controller change, added native tail or invented post-exit callback.
"""
import argparse,inspect
from pathlib import Path
import capture_current_challenger_v6487 as executed
import qualify_current_challenger_boundary_v6489 as qualified
ROOT,need=executed.ROOT,executed.need

def bindings():
 source=inspect.getsource(executed.bindings)
 changes={
  "'audit_v6480_current_continue_':'audit_v6488_current_challenger_'":
  "'audit_v6480_current_continue_':'audit_v6492_current_challenger_'",
  "'paths=[LUA,DRIVER,Path(prior.__file__),Path(__file__),'":
  "'paths=[LUA,DRIVER,Path(prior.__file__),Path(executed.__file__),Path(qualified.__file__),Path(__file__),'",
  'scope=dict(prior.__dict__,__file__=__file__,prior=prior,LUA=lua,DRIVER=lua,gate=gate)':
  'scope=dict(prior.__dict__,__file__=__file__,prior=prior,executed=executed,qualified=qualified,LUA=lua,DRIVER=lua,gate=gate)',
 }
 for before,after in changes.items():need(source.count(before)==1,'Only qualified terminal boundary/source pins/evidence destination differ');source=source.replace(before,after,1)
 scope=dict(executed.__dict__,__file__=__file__,executed=executed,qualified=qualified,gate=qualified.gate)
 exec(compile(source,__file__+'::whole_original_capture_with_current_boundary','exec'),scope)
 return scope['bindings']()

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));parser.add_argument('--side',required=True,type=int,choices=(1,2));a=parser.parse_args();bindings()(a.fighter,a.side)
