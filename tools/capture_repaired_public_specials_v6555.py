"""Actual promoted ordinary CMD: both projectile moves in both player slots.

The entire physical two-cycle/recovery controller, RAM-only guest/GFX/RGB and
native identity/health/ownership/pose/FIFO gates remain. No additional builds,
production settings changes or pre-existing capture overwrite/restart.
"""
import argparse,inspect
from pathlib import Path
import capture_current_cmd_specials_v6263 as original
import native_projectile_identifiers_context_v6509 as candidate
ROOT,need=candidate.ROOT,candidate.need

def bindings():
 source=inspect.getsource(original.bindings)
 changes={
  "scope=dict(prior.capture.__globals__,__file__=__file__)":
  "scope=dict(prior.capture.__globals__,__file__=__file__,current=candidate,original=original)",
  "'audit_v6264_current_cmd_special_'":"'audit_v6556_repaired_public_special_'",
  "text=text.replace(before,'for p in(Path(prior.__file__),LUA,LAUNCHER,',1)":
  "text=text.replace(before,'for p in(Path(prior.__file__),Path(original.__file__),ROOT/\"PLAY_CURRENT_V6508_CHECKED.cmd\",ROOT/\"tools/check_repaired_playtest_v6552.ps1\",ROOT/\"audit_v6554_repaired_default_launcher_checked/report.json\",LUA,LAUNCHER,',1)\n   text=text.replace('check,_,_=context.bindings();report','check,_,_=context.bindings();check.__globals__[\"native\"]=current;report',1)",
 }
 for a,b in changes.items():need(source.count(a)==1,'Only candidate/actual new CMD pin/destination binding');source=source.replace(a,b,1)
 scope=dict(original.__dict__,__file__=__file__,candidate=candidate,original=original)
 exec(compile(source,__file__+'::whole_original_canonical_CMD_physical_capture','exec'),scope)
 return scope['bindings']()

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--move',choices=('knife','ring'));p.add_argument('--side',type=int,choices=(1,2));a=p.parse_args()
 need(bool(a.move)==bool(a.side),'Both move and side, or whole four-case projectile launch matrix')
 capture,_=bindings()
 for move,side in [(a.move,a.side)]if a.move else[(m,s)for m in ('knife','ring')for s in (1,2)]:capture(move,side)
