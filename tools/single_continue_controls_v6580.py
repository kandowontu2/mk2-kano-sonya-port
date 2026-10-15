"""Actual single-player losses, paid continue, real reselection and controls.

CPU remains CPU; every move must actually occur before its observed recovery.
Native exit is pre-render, so compare every real callback, not fictitious ones.
No game edits, HP/position/CPU/RNG writes, proxies or rewritten failed results.
"""
import argparse,inspect,re
from pathlib import Path
import capture_single_continue_v6568 as original
ROOT,need,sha,rows=original.ROOT,original.need,original.sha,original.rows
LUA=ROOT/'mk2ks_single_continue_controls_v6579.lua'
DEPENDENCIES=[ROOT/'mk2ks_single_continue_v6567.lua',LUA,Path(original.__file__),Path(__file__),
 ROOT/'audit_v6578_single_continue_control_rejection/failure.json',
 ROOT/'audit_v6581_single_continue_controls_kano_p1_to_kano/executed_sources/mk2ks_single_continue_controls_v6579.lua',
 ROOT/'audit_v6581_single_continue_controls_kano_p1_to_kano/executed_sources/single_continue_controls_v6580.py',
 ROOT/'audit_v6581_single_continue_controls_kano_p1_to_kano/report.json']

def actual_controls(text,e,fields,side,terminal):
 r=rows(text,'RESULT')[0];events={k:int(r[k])for k in ('walk','jump','punch','recover')}
 need(e['reReady']<events['walk']<events['jump']<events['punch']<events['recover'] and terminal==events['recover']+180,
      'Actual ordered walk/jump/punch/recovery then complete180-field survival tail')
 indexed={int(q['frame']):q for q in fields if q['slot']==str(side)}
 controls=rows(text,'INPUT');health=rows(text,'HEALTH')
 for tag in ('WALK','JUMP','PUNCH','RECOVER'):
  event=rows(text,tag);need(len(event)==1 and int(event[0]['frame'])==events[tag.lower()],'One actual observed control event '+tag)
  q=indexed[events[tag.lower()]-1]
  need(q['hp']!='0' and q['id']==q['roster']==r['target'].replace('kano','17').replace('sonya','18')and q['owner']==q['actor'],
       'Real living requested owner at each observed control')
  if tag=='RECOVER':
   need(q['y']==q['floor'] and q['vx']==q['vy']==q['gravity']=='00000000'and int(q['flags'],16)&0x1c==0 and q['action']in ('0','771'),
        'Actual final control recovery, not knockdown or an input marker')
   continue
  start=int(event[0]['start']);at=int(event[0]['frame'])
  need(e['reReady']<=start<at,'Physical input precedes actual response')
  pulses=[v for v in controls if start<=int(v['frame'])<at]
  if tag=='WALK':
   need(int(event[0]['fromX'])!=int(event[0]['toX'])and int(q['x'])==int(event[0]['toX'])and q['y']==q['floor']and q['action']=='0'and
        any(v['button']in ('Left','Right')for v in pulses),'Actual grounded physical movement')
  elif tag=='JUMP':
   need(int(q['y'])<int(q['floor'])and q['action']!='1283'and any(v['button']=='Up'for v in pulses)and
        not any(v['slot']==str(side)and start<=int(v['frame'])<at and int(v['before'])>int(v['after'])for v in health),
        'Actual physical jump, not CPU-hit airborne reaction')
  else:need(q['action']=='257'and any(v['button']=='High_Punch'for v in pulses),'Actual ordinary punch, not a button marker')
 block=[int(q['frame'])for q in controls if q['button']=='Block'and int(q['frame'])>=events['recover']]
 need(block==list(range(events['recover']+1,terminal)),'Every finite survival field uses only ordinary physical Block')
 e.update(events)

def bindings():
 source=inspect.getsource(original.gate)
 changes={
  "terminal==e['reReady']+180":"terminal==int(r['recover'])+180",
  "e['reLive']<int(q['frame'])<=terminal":"e['reLive']<=int(q['frame'])<terminal",
  "range(e['reLive']+1,terminal+1)":"range(e['reLive'],terminal)",
  "[('Coin',20,5),('Start',80,5)]":"[('Coin',20,5),('Coin',270,5),('Start',310,5)]",
  "if q['button']==button and e['continue']<=int(q['frame'])<e['reselect']":
   "if q['button']==button and e['continue']+start<=int(q['frame'])<e['continue']+start+hold",
 }
 for a,b in changes.items():need(source.count(a)==1,'Exact source-boundary or physical payment adaptation');source=source.replace(a,b,1)
 first=source.index(" need(len({q['x']")
 last=source.index(" health=rows(text,'HEALTH')",first)
 source=source[:first]+" actual_controls(text,e,fields,side,terminal)\n"+source[last:]
 # Payment checking was in the replaced fixed-age control block. Keep it whole.
 source=source.replace(" actual_controls(text,e,fields,side,terminal)\n", """ actual_controls(text,e,fields,side,terminal)
 controls=rows(text,'INPUT')
 for button,start,hold in [('Coin',20,5),('Coin',270,5),('Start',310,5)]:
  want=list(range(e['continue']+start,e['continue']+start+hold))
  need([int(q['frame'])for q in controls if q['button']==button and e['continue']+start<=int(q['frame'])<e['continue']+start+hold]==want,'Exact paid normal continue input '+button)
""",1)
 scope=dict(original.__dict__,__file__=__file__,LUA=LUA,DEPENDENCIES=DEPENDENCIES,actual_controls=actual_controls)
 exec(compile(source,__file__+'::whole_round_identity_health_gate_actual_controls','exec'),scope)
 source=inspect.getsource(original.capture)
 for a,b in {'audit_v6569_single_continue_':'audit_v6585_single_continue_controls_',
  'for p in (LUA,Path(__file__),':'for p in (*DEPENDENCIES,LUA,Path(__file__),'} .items():
  need(source.count(a)==1,'Fresh normal-CMD collector with full dependency pins');source=source.replace(a,b,1)
 exec(compile(source,__file__+'::whole_original_native_capture_actual_controls','exec'),scope)
 return scope['gate'],scope['capture']

gate,capture=bindings()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=original.IDS,required=True);p.add_argument('--side',type=int,choices=(1,2),required=True)
 p.add_argument('--target',choices=original.IDS,required=True);p.add_argument('--hold',action='store_true');a=p.parse_args()
 capture(a.fighter,a.side,a.target,a.hold)
