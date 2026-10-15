"""Preserve actual unpaid test; use existing native cabinet's two-credit inputs.

Every original single-player round/health/identity/control gate stays intact.
No game edits, forced state, overwritten failed capture or new build.
"""
import argparse,inspect,json
from pathlib import Path
import capture_single_continue_v6568 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
LUA=ROOT/'mk2ks_single_continue_paid_v6570.lua'
FAILURE=ROOT/'audit_v6569_single_continue_kano_p1_to_kano/report.json'

def bindings():
 failure=json.loads(FAILURE.read_text());need(failure['passed']is False and failure['nativeExit']==0,'Actual unpaid native route failure preserved')
 stock=ROOT/'mk2ks_continue_reselect_probe.lua';source=stock.read_text()
 need('CONTINUE screen charges two credits'in source and 'age >= 310 and age < 315'in source,
      'Existing original single-player cabinet payment/timing reference, not guest assistance')
 source=inspect.getsource(prior.gate)
 before="[('Coin',20,5),('Start',80,5)]"
 need(source.count(before)==1,'Only explicit physical payment schedule correction')
 source=source.replace(before,"[('Coin',20,5),('Coin',270,5),('Start',310,5)]",1)
 # Two Coin windows must each be evaluated separately, not conflated.
 before="if q['button']==button and e['continue']<=int(q['frame'])<e['reselect']"
 after="if q['button']==button and e['continue']+start<=int(q['frame'])<e['continue']+start+hold"
 need(source.count(before)==1,'Every exact paid input window remains checked')
 source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,LUA=LUA)
 exec(compile(source,__file__+'::whole_original_single_player_gate_paid_cabinet_inputs','exec'),scope)
 source=inspect.getsource(prior.capture)
 changes={'audit_v6569_single_continue_':'audit_v6572_single_continue_paid_',
          'pins={str(p.resolve()):sha(p)for p in (LUA,Path(__file__),':'pins={str(p.resolve()):sha(p)for p in (LUA,ROOT/"mk2ks_single_continue_v6567.lua",ROOT/"mk2ks_continue_reselect_probe.lua",ROOT/"tools/capture_single_continue_v6568.py",FAILURE,Path(__file__),'}
 for a,b in changes.items():need(source.count(a)==1,'Exact provenance and fresh paid capture route');source=source.replace(a,b,1)
 scope.update(FAILURE=FAILURE)
 exec(compile(source,__file__+'::whole_original_native_capture_correct_paid_inputs','exec'),scope)
 return scope['capture'],scope['gate']

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=prior.IDS,required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);p.add_argument('--target',choices=prior.IDS,required=True);p.add_argument('--hold',action='store_true');a=p.parse_args()
 capture,_=bindings();capture(a.fighter,a.side,a.target,a.hold)
