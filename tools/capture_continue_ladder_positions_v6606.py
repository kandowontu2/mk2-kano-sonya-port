"""Same genuine continued UI capture, with passive viewport diagnostics.

Deliberately retains the original failing gates while collecting the additional
native facts needed to distinguish invisible ladder rows from rendering faults.
No accepted full continued-ladder or whole-port claim follows from this alone.
"""
import argparse, inspect
from pathlib import Path
import capture_continue_presentation_v6603 as prior
LUA=prior.ROOT/'mk2ks_continue_ladder_positions_v6605.lua'
DEPENDENCIES=[*prior.DEPENDENCIES,LUA,Path(__file__)]
source=inspect.getsource(prior.prior.current.executed.prior.original.capture)
for a,b in {
 'audit_v6569_single_continue_':'audit_v6607_continue_ladder_positions_',
 'for p in (LUA,Path(__file__),':'for p in (*DEPENDENCIES,LUA,Path(__file__),',
 "need(key not in images,'Unique displayed native scene')":
 "need(key not in images or key[1].startswith('ui_')and images[key]==raw,'Every duplicated original UI snapshot byte-identical')",
 "(tag!='HEALTH'or 'pc=FF836700 'in l and ('slot='+str(side)+' ')in l))":
 "(tag!='HEALTH'or loss_damage(l,result,side)))",
}.items():
 prior.need(source.count(a)==1,'Exact original native collector adaptation')
 source=source.replace(a,b,1)
scope=dict(prior.capture.__globals__,__file__=__file__,LUA=LUA,DEPENDENCIES=DEPENDENCIES,gate=prior.gate)
exec(compile(source,__file__+'::whole_native_collector_passive_ladder_diagnostics','exec'),scope)
capture=scope['capture']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True)
 p.add_argument('--side',type=int,choices=(1,2),required=True)
 p.add_argument('--target',choices=('kano','sonya'),required=True);p.add_argument('--hold',action='store_true')
 a=p.parse_args();capture(a.fighter,a.side,a.target,a.hold)
