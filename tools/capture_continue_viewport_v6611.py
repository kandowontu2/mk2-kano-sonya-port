"""Original ordinary-CMD collector with genuine continue/native viewport gates."""
import argparse,inspect
from pathlib import Path
import numpy as np
import continue_viewport_contract_v6610 as contract
prior=contract.original
ROOT,need,sha=contract.ROOT,contract.need,contract.sha
LUA=ROOT/'mk2ks_continue_ladder_positions_v6605.lua'
DEPENDENCIES=[*contract.DEPENDENCIES,Path(__file__)]
gate=contract.gate
source=inspect.getsource(prior.prior.current.executed.prior.original.capture)
for a,b in {
 'audit_v6569_single_continue_':'audit_v6612_continue_viewport_',
 'for p in (LUA,Path(__file__),':'for p in (*DEPENDENCIES,LUA,Path(__file__),',
 "need(key not in images,'Unique displayed native scene')":
 "need(key not in images or key[1].startswith('ui_')and images[key]==raw,'Duplicated original UI callback is byte-identical')",
 "(tag!='HEALTH'or 'pc=FF836700 'in l and ('slot='+str(side)+' ')in l))":
 "(tag!='HEALTH'or loss_damage(l,result,side)))",
 "result=gate(text,fighter,side,target);faults=[]":
 "result=gate(text,fighter,side,target);result['actualUIPixels']=contract.render(out,text,target,side,load=lambda name:np.frombuffer(images[(int(name[3:7]),name)],np.uint8).reshape(254,400,4)[:,:,2::-1].copy());faults=[]",
 "need(gate(text,fighter,side,target)==result and all(sha(p)==h for p,h in pins.items())":
 "need(gate(text,fighter,side,target)=={k:v for k,v in result.items()if k!='actualUIPixels'} and all(sha(p)==h for p,h in pins.items())",
}.items():
 need(source.count(a)==1,'Exact original collector and finite actual viewport adaptation')
 source=source.replace(a,b,1)
scope=dict(prior.capture.__globals__,__file__=__file__,LUA=LUA,DEPENDENCIES=DEPENDENCIES,
           gate=gate,contract=contract,np=np)
exec(compile(source,__file__+'::whole_ordinary_CMD_continue_UI_viewport','exec'),scope)
capture=scope['capture']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True)
 p.add_argument('--side',type=int,choices=(1,2),required=True)
 p.add_argument('--target',choices=('kano','sonya'),required=True);p.add_argument('--hold',action='store_true')
 a=p.parse_args();capture(a.fighter,a.side,a.target,a.hold)
