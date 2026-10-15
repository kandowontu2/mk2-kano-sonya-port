"""Same terminal-first current CMD/RAM collector; actual challenger contract."""
import argparse,inspect,re
from pathlib import Path
import capture_current_continue_v6479 as prior
ROOT,need,sha,rows=prior.ROOT,prior.need,prior.sha,prior.rows

def gate(text,fighter,side):
 results=rows(text,'MK2_JR_RESULT');need(len(results)==1,'One actual full challenger terminal')
 r=results[0];events={k:int(r[k]) for k in ('coldCSS','coldMatch','join','css','match','ready','terminal')}
 need(events['coldCSS']>0 and all(a<b for a,b in zip(events.values(),list(events.values())[1:])),
      'Entire actual cold CPU/challenger/native selection/match/ready/terminal chronology')
 need(events['join']==events['coldMatch']+600 and events['terminal']==events['ready']+600,
      'Complete600-field real CPU opening and600-field joined ordinary play, no deadline pass')
 own=17 if fighter=='kano' else 18;ids={side:own,3-side:18 if own==17 else 17}
 starts=rows(text,'MK2_JR_JOIN');need(len(starts)==1 and starts[0]['ownState']=='1' and starts[0]['otherState']=='0' and starts[0]['mode']=='2',
      'Other participant was a real CPU before joining, not an already joined two-human match')
 fields=rows(text,'MK2_CR_FIELD');indexed={(int(q['frame']),int(q['slot'])):q for q in fields}
 for frame in range(events['coldMatch']+1,events['join']+1):
  for n in (1,2):
   q=indexed.get((frame,n));need(q is not None and q['owner']==q['actor'] and q['id']==q['roster'] and q['writes']=='0' and q['assistance']=='none',
                             'Every original CPU-game owner/roster callback observed')
   need(q['state']==str(1 if n==side else 0) and (n!=side or q['id']==str(own)),
        'Whole600-field original human/CPU roles and true selected human identity')
 highlights=rows(text,'MK2_JR_HIGHLIGHT');need(len(highlights)==2 and {int(q['slot']) for q in highlights}=={1,2} and
  all(int(q['frame'])==events['css']+156 and q['expected']==q['roster']==str(ids[int(q['slot'])]) and q['state']=='3' for q in highlights),
  'Both actual added-fighter highlights and selectable human controllers')
 controls=rows(text,'MK2_JR_INPUT')
 for button,at in (('Coin',10),('Coin',30),('Start',60)):
  selected=[int(q['frame']) for q in controls if q['slot']==str(3-side) and q['button']==button and events['join']+at<=int(q['frame'])<events['join']+at+5]
  need(selected==list(range(events['join']+at,events['join']+at+5)),'All actual challenger coin/start pulses '+button)
 post=[]
 for frame in range(events['match']+1,events['terminal']+1):
  for n in (1,2):
   q=indexed.get((frame,n));need(q is not None,'No omitted post-join native actor callback')
   need(q['id']==q['roster']==str(ids[n]) and q['owner']==q['actor'] and q['state']=='1' and q['mode']=='2' and q['writes']=='0' and q['assistance']=='none',
        'Every rebuilt fighter retains real identity, Main owner and human control')
   post.append(q)
 for n in (1,2):
  tail=[q for q in post if int(q['slot'])==n and int(q['frame'])>=events['ready']]
  need(len(tail)==601,'Both complete ordinary tails')
  need(len({q['x'] for q in tail if events['ready']+24<=int(q['frame'])<=events['ready']+44})>1,'Joined ordinary walking slot '+str(n))
  need(any(int(q['y'])<int(q['floor']) for q in tail if events['ready']+64<=int(q['frame'])<=events['ready']+110),'Joined genuine jump slot '+str(n))
  need(len({q['pose'] for q in tail if events['ready']+135<=int(q['frame'])<=events['ready']+165})>1,'Joined duck/stand body progression slot '+str(n))
  end=tail[-1];need(end['y']==end['floor'] and end['vx']==end['vy']==end['gravity']=='00000000' and int(end['flags'],16)&0x1c==0 and 0<int(end['hp'])<=161,
                   'Both final grounded native owners without stale velocities/locks')
 health=rows(text,'MK2_JR_HEALTH');hits=[q for q in health if events['ready']<=int(q['frame'])<=events['terminal'] and int(q['before'])>int(q['after'])]
 need(hits and all(q['pc']=='FF836700' and 0<=int(q['after'])<int(q['before'])<=161 for q in hits),
      'Joined ordinary contact is real native collision, not HP assistance')
 need(not rows(text,'MK2_JR_ERROR'),'No physical route deadline')
 events['reLive']=events['match'] # collector's actual-record fault selector only
 return dict(fighter=fighter,physicalSlot=side,events=events,trueJoinedIdentities=ids,joinedActorFields=len(post),
             originalCPUFields=600,ordinaryTailFieldsPerSlot=601,actualNativeDamageStores=len(hits),
             scope='current cold CPU game then real challenger join, both highlights, rebuilt owners and ordinary combat; no post-ending/single-player continue or complete UI/audio/special-move acceptance')

def bindings():
 source=inspect.getsource(prior.capture)
 changes={
  'audit_v6480_current_continue_':'audit_v6488_current_challenger_',
  "driver.count('screen:snapshot(file)')==1":"driver.count('manager.machine:exit()')==2",
  'paths=[LUA,DRIVER,Path(__file__),':'paths=[LUA,DRIVER,Path(prior.__file__),Path(__file__),',
  "r'MK2_GROUND_(CSS|LIVE|READY|KO|ROUND_RESET|NEXT_READY|SECOND_KO|CONTINUE|RESELECT |RESELECT_EXIT|RE_LIVE|RE_READY|RESULT)'":
  "r'MK2_JR_(COLD_CSS|COLD_MATCH|JOIN|CSS|HIGHLIGHT|MATCH|READY|RESULT|ERROR)'",
  "('false ready','MK2_GROUND_RESULT','reReady','-1')":"('false ready','MK2_JR_RESULT','ready','-1')",
  "('incomplete walk tail','MK2_GROUND_RESULT','frame','1')":"('incomplete walk tail','MK2_JR_RESULT','terminal','1')",
  'actualCurrentContinuation=result':'actualCurrentChallenger=result',
 }
 for before,after in changes.items():need(source.count(before)==1,'Exact challenger RAM transport adaptation '+before[:70]);source=source.replace(before,after,1)
 lua=ROOT/'mk2ks_current_challenger_v6486.lua'
 scope=dict(prior.__dict__,__file__=__file__,prior=prior,LUA=lua,DRIVER=lua,gate=gate)
 exec(compile(source,__file__+'::whole_terminal_first_current_CMD_RAM_transport','exec'),scope)
 return scope['capture']

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));parser.add_argument('--side',required=True,type=int,choices=(1,2));a=parser.parse_args();bindings()(a.fighter,a.side)
