"""Genuine released-input stage-zero continue, including its native viewport.

The cold-start verifier assumes a complete tower pan. A normal continued tower
starts at the retained stage. Do not require an offscreen icon on screen, or
claim its raster rendered: bind its actual native allocation/world position and
require exact source rasters for every added tower icon in the visible viewport.
Cold-start both-icon raster acceptance is a separate requirement and proof.
"""
import inspect,re,struct
from pathlib import Path
import numpy as np
import capture_continue_presentation_v6603 as original
import native_projectile_identifiers_context_v6509 as context
model=original.model
ROOT,need,sha,rows=original.ROOT,original.need,original.sha,original.rows
DEPENDENCIES=[*original.DEPENDENCIES,Path(__file__),Path(context.__file__),
 ROOT/'mk2ks_continue_ladder_positions_v6605.lua',ROOT/'tools/capture_continue_ladder_positions_v6606.py',
 ROOT/'source_v6502_native_projectile_identifiers/midtunit_m.cpp',ROOT/'tools/verify_p2_campaign.py']

# Retain the entire natural-loss/payment/ownership gate. Only replace its old
# SELECT transport with the complete actual original UI selection transport.
source=inspect.getsource(original.prior.current.executed.prior.original.gate)
for a,b in {
 "e['reLive']<int(q['frame'])<=terminal":"e['reLive']<=int(q['frame'])<terminal",
 "range(e['reLive']+1,terminal+1)":"range(e['reLive'],terminal)",
 "len(enemy)==1 and enemy[0]['state']=='0'and q['a8']==enemy[0]['actor']and q['a13']==enemy[0]['main']":
 "len(enemy)==1 and origin(q,enemy[0])",
 "selected=[q for q in rows(text,'SELECT')if int(q['origin'])==e['reselect']]":
 "selected=model.records(text,'SELECT')",
 "selected[-1]['roster']==selected[-1]['wanted']==str(IDS[target])":
 "selected[-1]['roster']==str(IDS[target]) and selected[-1]['fighter']==target and selected[-1]['side']==str(side)",
}.items():
 need(source.count(a)==1,'Whole original continue gate and exact corrected transport')
 source=source.replace(a,b,1)
first=source.index(" need(len({q['x']");last=source.index(" health=rows(text,'HEALTH')",first)
source=source[:first]+""" controls=rows(text,'INPUT')
 for button,start,hold in [('Coin',20,5),('Coin',270,5),('Start',310,5)]:
  want=list(range(e['continue']+start,e['continue']+start+hold))
  need([int(q['frame'])for q in controls if q['button']==button and e['continue']+start<=int(q['frame'])<e['continue']+start+hold]==want,'Exact native paid continue input '+button)
"""+source[last:]
namespace=dict(original.prior.current.executed.prior.original.__dict__,
 origin=original.prior.current.origin,model=model)
exec(compile(source,__file__+'::whole_natural_loss_owned_continue_UI','exec'),namespace)
base_gate=namespace['gate']

def continued_trace(text,events):
 """Check all original ladder consumers before scoping the one UI session.

Only boot-game LADDER records are omitted from the original single-UI model;
the immutable full trace retains them, and no other row is filtered.
 """
 css=int(model.unique(model.records(text,'CSS'),'continued CSS')['frame'])
 for q in model.records(text,'LADDER'):
  pid=int(q['id']);at=0xffff3000+pid*32;frame=int(q['frame'])
  need(pid in (17,18)and int(q['pc'],16)==0xff8a0c00 and int(q['at'],16)==int(q['a0'],16)==at and
       int(q['mask'],16)==0xffff and int(q['descriptor'],16)==(0x2a00 if pid==17 else 0x2b00),
       'Every initial/continued native ladder read has the real consumer and descriptor')
  need(events['css']<frame<events['live']or css<frame<events['reLive'],
       'Every ladder read belongs to an actual native game/UI interval')
 return '\n'.join(line for line in text.splitlines()if not(line.startswith('MK2_UI_LADDER ')and
       int(dict(re.findall(r'(\w+)=([^\s]+)',line))['frame'])<css))

def gate(text,fighter,side,target):
 result=base_gate(text,fighter,side,target);e=result['events'];terminal=e['reReady']+180
 need(not[q for q in rows(text,'MODE')if e['continue']<=int(q['frame'])<e['reselect']and q['mode']=='11'],
      'Genuine paid continue, not Game Over/restart')
 # Native frame_done runs once at frame zero before the first frame callback.
 io=rows(text,'IO');need([int(q['frame'])for q in io]==list(range(terminal)),
      'Every actual native input-port field, no missing release observations')
 if side==2:
  held=[int(q['frame'])for q in io if int(q['in0'],16)&0x10==0]
  need(len(held)==4 and all(300<=f<=305 for f in held)and held==list(range(held[0],held[0]+4)),
       'P1 startup HP really released; no persistent other-player input')
 else:need(all(int(q['in0'],16)&0x1000 for q in io),'Other-player P2 HP never held')
 ui=model.verify_log(continued_trace(text,e),target,side)
 need(ui['live']==e['reLive']and ui['terminal']==terminal and e['reselect']>=ui['css']and ui['css']>e['continue'],
      'Whole UI/navigation/teardown/owned match follows genuine CPU loss and payment')
 result.update(actualUIState=ui,actualOtherPlayerStartupKeyReleased=True,
  scope='released-input genuine stage-zero paid continue and native UI/viewport/owned match; not all audio, post-ending joins or all port contexts')
 return result

def viewport(log,matches,images):
 live=model.unique(model.records(log,'LIVE'),'viewport live');exit_at=int(model.records(log,'EXIT')[0]['frame'])
 order=(int(live['schedule'],16)-0xfffa3000)//0x180;stage=int(live['stage'])
 need(stage==0 and order in range(6),'Declared finite actual continued stage-zero viewport')
 guest=context.expected();off=lambda a:(a-0xff800000)//8
 positions=struct.unpack_from('<17H',guest,0xf4740);scroll=struct.unpack_from('<17H',guest,0xf4780)[stage]
 need(positions==tuple(940-(754*i+7)//15 for i in range(16))+(128,)and scroll==784 and
      struct.unpack_from('<I',guest,off(0xff8a05c0))[0]==0xfffa3a00 and
      struct.unpack_from('<I',guest,off(0xff8a0df0))[0]==0xfffa3c00,
      'Actual native tower position/scroll operands and all source-authored positions')
 order_ids=model.expected_orders()[order];lookups=model.records(log,'LADDER')
 tracked=model.records(log,'LADDER_OBJECT');need(bool(tracked),'Actual passive continued ladder object observations')
 worlds={};expected={};visible=[]
 for pid in (17,18):
  slot=order_ids.index(pid);world=positions[slot]-3;top=positions[slot]-scroll
  rows_at=[q for q in tracked if q['id']==str(pid)and int(q['xraw'],16)==266<<16 and
           exit_at+2<=int(q['frame'])<=exit_at+100]
  actors={q['actor']for q in rows_at}
  need(len(actors)==1,'One native tower allocation for each added scheduled ID')
  actor=next(iter(actors));born={int(q['born'])for q in rows_at}
  need(len(born)==1 and any(q['id']==str(pid)and q['a8']==actor and int(q['frame'])in born for q in lookups),
       'Actual world object belongs to the native descriptor consumer, not a hint')
  need([int(q['frame'])for q in rows_at]==list(range(exit_at+2,exit_at+101))and
       all(int(q['yraw'],16)==world<<16 and q['flags']=='0000'for q in rows_at),
       'Every settled tower object field matches its source schedule and world position')
  worlds[str(pid)]=dict(actor=actor,born=next(iter(born)),slot=slot,worldY=world,projectedTop=top,
                      nativeObjectFields=len(rows_at),actuallyRasterVisible=False)
  expected[str(pid)]=(248,top)
  if 0<=top and top+45<=254:
   visible.append(pid)
   actual=[q for q in matches[pid]if exit_at+2<=q['frame']<=exit_at+100]
   need(len(actual)>=3 and all(tuple(q['position'])==(248,top)for q in actual),
        'Every visible scheduled added icon has repeated complete source-raster matches at its native position')
   worlds[str(pid)]['actuallyRasterVisible']=True
  else:
   need(top+45<=0 or top>=254,'Offscreen classification is complete, not partial clipping')
 need(bool(visible),'Continued viewport contains a source-checked added tower icon')
 return dict(order=order,stage=stage,nativeScroll=scroll,objects=worlds,
             visibleSourceRasterIDs=visible,offscreenRasterRenderingNotClaimed=True)

# All original border, number, blink, source portrait, backdrop, animation,
# every-post-exit icon/pose erasure, and actual HUD name-shadow checks remain.
source=inspect.getsource(model.render)
before="""    need(len(outside_files) > 60 and all(len(values) >= 3 for values in matches.values()),
         'Both complete source-authored ladder icons actually rendered during native reveal')"""
need(source.count(before)==1,'Only cold full-pan requirement changes to actual continued viewport contract')
source=source.replace(before,"""    need(len(outside_files) > 60, 'Complete continued transition raster coverage')
    projection = viewport(log, matches, images)""",1)
before="first_ladder_icon_matches={str(k): values[0] for k, values in matches.items()}, native_name_shadow_checks=name_checks)"
need(source.count(before)==1,'Truthful zero matches for offscreen raster')
source=source.replace(before,"first_ladder_icon_matches={str(k): values[0] if values else None for k, values in matches.items()}, native_name_shadow_checks=name_checks, continuedViewport=projection)",1)
namespace=dict(model.__dict__,viewport=viewport)
exec(compile(source,__file__+'::whole_source_native_UI_pixels_continued_viewport','exec'),namespace)
render=namespace['render']
