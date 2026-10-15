"""Lexical RAM snapshot successor; retain whole original physical controller.

The HP location is also used as an original temporary inter-round counter.
Only the two independently observed live combat windows are damage windows;
all other native writes remain in the retained full chronological ledger.
"""
import argparse,inspect
from pathlib import Path
import capture_current_continue_v6479 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha

def bindings():
 source=inspect.getsource(prior.gate)
 before="damage=[q for q in health if q['slot']==str(side) and int(q['before'])>int(q['after']) and int(q['frame'])<=int(r['secondKO'])]"
 after="""windows=((int(r['ready']),int(r['ko'])),(int(r['nextReady']),int(r['secondKO'])))
 damage=[q for q in health if q['slot']==str(side) and int(q['before'])>int(q['after']) and any(lo<=int(q['frame'])<=hi for lo,hi in windows)]"""
 need(source.count(before)==1,'Only false inter-round HP interpretation changes')
 source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,prior=prior,LUA=ROOT/'mk2ks_current_continue_bound_v6481.lua')
 exec(compile(source,__file__+'::whole_continuation_live_damage_windows','exec'),scope)
 capture=inspect.getsource(prior.capture)
 changes={
  'audit_v6480_current_continue_':'audit_v6483_current_continue_',
  'paths=[LUA,DRIVER,Path(__file__),':'paths=[LUA,ROOT/"mk2ks_current_continue_ram_v6478.lua",DRIVER,Path(prior.__file__),Path(__file__),',
  "guest=current.expected();gfx=current.expected_gfx();build=ROOT/current.NAME":
  """guest=current.expected();gfx=current.expected_gfx();build=ROOT/current.NAME
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 lo=(0xff9dec00-0xff800000)//8;hi=(0xff9df000-0xff800000)//8
 need(guest[lo:hi]==stock[lo:hi],'Whole original inter-round temporary-state kernel unchanged')""",
  "paths=[LUA,ROOT/\"mk2ks_current_continue_ram_v6478.lua\",DRIVER,Path(prior.__file__),Path(__file__),":
  "paths=[LUA,ROOT/\"mk2ks_current_continue_ram_v6478.lua\",DRIVER,Path(prior.__file__),Path(__file__),ROOT/\"mk2/mk2-maincpu.bin\",",
 }
 for before,after in changes.items():
  need(capture.count(before)==1,'Exact successor adaptation '+before[:80]);capture=capture.replace(before,after,1)
 exec(compile(capture,__file__+'::whole_original_current_native_capture','exec'),scope)
 return scope['capture'],scope['gate']

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));parser.add_argument('--side',required=True,type=int,choices=(1,2));a=parser.parse_args()
 capture,_=bindings();capture(a.fighter,a.side)
