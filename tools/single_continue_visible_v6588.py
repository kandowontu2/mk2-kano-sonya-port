"""Unchanged full continue/control gate; wait for actual visible cursor.

Mode4 can precede both FFFF and valid stale-roster replacement. Native CSS
pixels prove the screen exists before reading/physically moving the cursor.
Also retain full actual ladder RGB buffers in RAM; no new native game build.
"""
import argparse,inspect
from pathlib import Path
import single_continue_controls_v6580 as prior
ROOT,need,sha,rows=prior.ROOT,prior.need,prior.sha,prior.rows
LUA=ROOT/'mk2ks_single_continue_visible_v6587.lua'
DEPENDENCIES=[*prior.DEPENDENCIES,prior.LUA,LUA,Path(prior.__file__),Path(__file__),
 ROOT/'audit_v6585_single_continue_controls_kano_p2_to_kano/report.json',
 ROOT/'audit_v6584_single_continue_controls_same_native_checked/report.json',
 ROOT/'audit_v6589_single_continue_visible_kano_p2_to_kano/executed_sources/mk2ks_single_continue_visible_v6587.lua',
 ROOT/'audit_v6589_single_continue_visible_kano_p2_to_kano/executed_sources/single_continue_visible_v6588.py',
 ROOT/'audit_v6589_single_continue_visible_kano_p2_to_kano/report.json']
def payment_schedule(side):
 return [('Coin',20,5),('Coin',50,5),('Start',80,5)]if side==2 else [('Coin',20,5),('Coin',270,5),('Start',310,5)]
def damage_origin(q,enemy):
 if enemy['state']!='0' or enemy['actor']!=enemy['owner']:return False
 if q['a8']==enemy['actor']and q['a13']==enemy['main']:return True
 # Native paired leg damage runs in the real victim Main. Its original
 # grabber actor/Main fields must resolve back to the live CPU Sonya18.
 if q['a8']==q['actor']and q['a13']==q['main']and q['ctxOwner']==q['actor']:
  return enemy['id']=='18'and q['pairActor']==enemy['actor']and q['pairMain']==enemy['main']and q['pairAction']=='272'
 # Native projectile Main owns its actual child object and records its
 # originating fighter Main at+230; neither is a substituted human actor.
 return (q['a8']not in (q['actor'],enemy['actor'])and q['a13']not in (q['main'],enemy['main'])and
         q['ctxOwner']==q['a8']and q['parent']==enemy['main']and q['ctxID']==enemy['id'])
def adapt_damage_gate(source):
 before="len(enemy)==1 and enemy[0]['state']=='0'and q['a8']==enemy[0]['actor']and q['a13']==enemy[0]['main']"
 need(source.count(before)==1,'Original complete native damage gate; resolve actual paired/projectile ownership')
 return source.replace(before,'len(enemy)==1 and damage_origin(q,enemy[0])',1)
binding_source=inspect.getsource(prior.bindings)
for a,b in {
 "for button,start,hold in [('Coin',20,5),('Coin',270,5),('Start',310,5)]:":"for button,start,hold in payment_schedule(side):",
 'actual_controls=actual_controls)':'actual_controls=actual_controls,payment_schedule=payment_schedule,damage_origin=damage_origin)',
 'source=inspect.getsource(original.gate)':'source=adapt_damage_gate(inspect.getsource(original.gate))',
}.items():
 need(binding_source.count(a)==1,'Whole control gate with exact physical P2 timing');binding_source=binding_source.replace(a,b,1)
binding_scope=dict(prior.__dict__,payment_schedule=payment_schedule,damage_origin=damage_origin,adapt_damage_gate=adapt_damage_gate)
exec(compile(binding_source,__file__+'::whole_prior_binding_physical_p2_payment','exec'),binding_scope)
base_gate,_=binding_scope['bindings']()
def gate(text,fighter,side,target):
 good=base_gate(text,fighter,side,target);e=good['events']
 need(not[q for q in rows(text,'MODE')if e['continue']<=int(q['frame'])<e['reselect']and q['mode']=='11'],
      'Paid native continue, not Game Over followed by a new game')
 return good
source=inspect.getsource(prior.original.capture)
for a,b in {'audit_v6569_single_continue_':'audit_v6591_single_continue_visible_',
 'for p in (LUA,Path(__file__),':'for p in (*DEPENDENCIES,LUA,Path(__file__),'} .items():
 need(source.count(a)==1,'Whole original collector, fresh visible-cursor proof and full pins');source=source.replace(a,b,1)
scope=dict(prior.capture.__globals__,__file__=__file__,LUA=LUA,DEPENDENCIES=DEPENDENCIES,gate=gate)
exec(compile(source,__file__+'::whole_original_capture_visible_native_cursor','exec'),scope)
capture=scope['capture']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=prior.original.IDS,required=True);p.add_argument('--side',type=int,choices=(1,2),required=True)
 p.add_argument('--target',choices=prior.original.IDS,required=True);p.add_argument('--hold',action='store_true');a=p.parse_args()
 capture(a.fighter,a.side,a.target,a.hold)
