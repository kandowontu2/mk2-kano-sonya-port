"""Real paid continue: original full UI pixel/state gate, released startup key.

Reuse the whole natural CPU-loss/payment/identity/health proof and the entire
independent stock-controlled UI model. This window uses the original180-field
physical Block policy, not the previously qualified walk/jump/punch policy.
Every native displayed pixel is RAM-only; this is not all audio acceptance.
"""
import argparse,inspect,re
from pathlib import Path
import numpy as np
import single_continue_faults_v6596 as prior
import verify_native_ui_flow_v814 as model
ROOT,need,sha,rows=prior.ROOT,prior.need,prior.sha,prior.rows
LUA=ROOT/'mk2ks_continue_presentation_v6602.lua'
DEPENDENCIES=[*prior.DEPENDENCIES,LUA,Path(prior.__file__),Path(__file__),Path(model.__file__),
 ROOT/'mk2ks_native_ui_flow_v2_probe.lua',ROOT/'roms/mk2ks/mk2ks.ui',
 ROOT/'mame-mkp/src/emu/ioport.cpp',ROOT/'mame-mkp/src/frontend/mame/luaengine_input.cpp',
 ROOT/'mame-mkp/src/mame/midway/midtunit.cpp',ROOT/'audit_v6601_input_release_discrepancy/README.md']
source=inspect.getsource(prior.current.executed.prior.original.gate)
for a,b in {
 "e['reLive']<int(q['frame'])<=terminal":"e['reLive']<=int(q['frame'])<terminal",
 "range(e['reLive']+1,terminal+1)":"range(e['reLive'],terminal)",
 "len(enemy)==1 and enemy[0]['state']=='0'and q['a8']==enemy[0]['actor']and q['a13']==enemy[0]['main']":
 "len(enemy)==1 and origin(q,enemy[0])",
}.items():need(source.count(a)==1,'Whole original native continue gate, actual callbacks and native damage ownership');source=source.replace(a,b,1)
first=source.index(" need(len({q['x']");last=source.index(" health=rows(text,'HEALTH')",first)
source=source[:first]+""" controls=rows(text,'INPUT')
 for button,start,hold in [('Coin',20,5),('Coin',270,5),('Start',310,5)]:
  want=list(range(e['continue']+start,e['continue']+start+hold))
  need([int(q['frame'])for q in controls if q['button']==button and e['continue']+start<=int(q['frame'])<e['continue']+start+hold]==want,'Exact normal native paid continue input '+button)
"""+source[last:]
scope=dict(prior.current.executed.prior.original.__dict__,origin=prior.current.origin)
exec(compile(source,__file__+'::whole_original_natural_continue_native_UI_policy','exec'),scope)
base_gate=scope['gate']
def gate(text,fighter,side,target):
 result=base_gate(text,fighter,side,target);e=result['events'];terminal=e['reReady']+180
 need(not[q for q in rows(text,'MODE')if e['continue']<=int(q['frame'])<e['reselect']and q['mode']=='11'],
      'Real paid continue, not Game Over/restart')
 io=rows(text,'IO');need([int(q['frame'])for q in io]==list(range(1,terminal)),'Every actual completed native input-port callback')
 if side==2:
  held=[int(q['frame'])for q in io if int(q['in0'],16)&0x10==0]
  need(len(held)==4 and all(300<=f<=305 for f in held)and held==list(range(held[0],held[0]+4)),
       'Other-player startup HP released after four actual native fields; no permanent P1 input/skip')
 else:need(all(int(q['in0'],16)&0x1000 for q in io),'Other-player P2 HP never artificially held')
 ui=model.verify_log(text,target,side)
 need(ui['live']==e['reLive']and ui['terminal']==terminal and e['reselect']>=ui['css']and
      ui['css']>e['continue'],'Entire original native UI follows real CPU loss and paid continue')
 result.update(actualUIState=ui,actualOtherPlayerStartupKeyReleased=True,
  scope='real CPU-earned paid continuation followed by complete original UI navigation/blink/number/background/teardown/native ladder/owned match/name-shadow gate; not all audio or all game contexts')
 return result
source=inspect.getsource(prior.current.executed.prior.original.capture)
for a,b in {
 'audit_v6569_single_continue_':'audit_v6604_continue_presentation_',
 'for p in (LUA,Path(__file__),':'for p in (*DEPENDENCIES,LUA,Path(__file__),',
 "need(key not in images,'Unique displayed native scene')":
 "need(key not in images or key[1].startswith('ui_')and images[key]==raw,'Every duplicated original UI snapshot byte-identical')",
 "(tag!='HEALTH'or 'pc=FF836700 'in l and ('slot='+str(side)+' ')in l))":
 "(tag!='HEALTH'or loss_damage(l,result,side)))",
 "result=gate(text,fighter,side,target);faults=[]":
 "result=gate(text,fighter,side,target);result['actualUIPixels']=model.render(out,text,target,side,load=lambda name:np.frombuffer(images[(int(name[3:7]),name)],np.uint8).reshape(254,400,4)[:,:,2::-1].copy());faults=[]",
 "need(gate(text,fighter,side,target)==result and all(sha(p)==h for p,h in pins.items())":
 "need(gate(text,fighter,side,target)=={k:v for k,v in result.items()if k!='actualUIPixels'} and all(sha(p)==h for p,h in pins.items())",
}.items():need(source.count(a)==1,'Complete original collector with whole native UI raster/model/fault scope');source=source.replace(a,b,1)
scope=dict(prior.capture.__globals__,__file__=__file__,LUA=LUA,DEPENDENCIES=DEPENDENCIES,gate=gate,model=model,np=np)
exec(compile(source,__file__+'::whole_normal_CMD_continue_full_native_UI_capture','exec'),scope)
capture=scope['capture']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True)
 p.add_argument('--target',choices=('kano','sonya'),required=True);p.add_argument('--hold',action='store_true');a=p.parse_args()
 capture(a.fighter,a.side,a.target,a.hold)
