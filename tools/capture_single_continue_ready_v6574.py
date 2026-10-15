"""Native valid-cursor observer boundary; preserve both executed failed tests.

Original whole single-player payment, true actor, CPU collision HP and control
gates remain. No native game edit, weakened outcome or capture overwrite.
"""
import argparse,inspect,json
from pathlib import Path
import capture_single_continue_paid_v6571 as prior
ROOT,need=prior.ROOT,prior.need
LUA=ROOT/'mk2ks_single_continue_ready_v6573.lua'
FAILURE=ROOT/'audit_v6572_single_continue_paid_kano_p1_to_kano/report.json'

def bindings():
 r=json.loads(FAILURE.read_text());need(r['passed']is False and r['nativeExit']==0,'Executed mode4 FFFF-cursor observer failure retained')
 stderr=(FAILURE.parent/'stderr.log').read_text()
 need('No original native selection route from 65535 to 17'in stderr,'Exact native uninitialized-cursor rejection, not gameplay acceptance')
 source=inspect.getsource(prior.bindings)
 changes={'audit_v6572_single_continue_paid_':'audit_v6575_single_continue_ready_',
          'ROOT/"mk2ks_single_continue_v6567.lua",':'ROOT/"mk2ks_single_continue_paid_v6570.lua",ROOT/"tools/capture_single_continue_paid_v6571.py",ROOT/"audit_v6572_single_continue_paid_kano_p1_to_kano/report.json",ROOT/"audit_v6574_unstarted_binding_failure/executed_source.py",ROOT/"audit_v6574_unstarted_binding_failure/failure.json",ROOT/"mk2ks_single_continue_v6567.lua",'}
 for a,b in changes.items():need(source.count(a)==1,'Only new observer/provenance/output binding');source=source.replace(a,b,1)
 scope=dict(prior.__dict__,__file__=__file__,LUA=LUA)
 exec(compile(source,__file__+'::whole_original_paid_capture_initialized_cursor','exec'),scope)
 return scope['bindings']()

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=prior.prior.IDS,required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);p.add_argument('--target',choices=prior.prior.IDS,required=True);p.add_argument('--hold',action='store_true');a=p.parse_args()
 capture,_=bindings();capture(a.fighter,a.side,a.target,a.hold)
