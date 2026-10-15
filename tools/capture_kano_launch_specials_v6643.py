"""Whole original physical two-cycle special capture on the new launch build.

No changed gameplay controller, reduced semantic gate, public promotion, or
borrowed runtime acceptance. Complete guest/GFX match is required per cold boot.
"""
import argparse,inspect
from pathlib import Path
import capture_current_cmd_specials_v6263 as corrected
import kano_ball_launch_context_v6642 as candidate
need=corrected.need

def bindings():
 source=inspect.getsource(corrected.bindings)
 changes={
  'scope=dict(prior.capture.__globals__,__file__=__file__)':
  "scope=dict(prior.capture.__globals__,__file__=__file__,current=candidate,corrected=corrected,LAUNCHER=candidate.ROOT/'TEST_KANO_BALL_LAUNCH_V6640.cmd')",
  "'audit_v6264_current_cmd_special_'":"'audit_v6644_kano_launch_special_'",
  "text=text.replace(before,'for p in(Path(prior.__file__),LUA,LAUNCHER,',1)":
  "text=text.replace(before,'for p in(Path(prior.__file__),Path(corrected.__file__),LUA,LAUNCHER,',1)\n   text=text.replace('canonicalCMDUsed=True','canonicalCMDUsed=False,isolatedCandidateCMDUsed=True',1)\n   text=text.replace('check,_,_=context.bindings();report','check,_,_=context.bindings();check.__globals__[\"native\"]=current;report',1)",
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Exact whole physical capture adaptation '+before);source=source.replace(before,after,1)
 scope=dict(corrected.__dict__,__file__=__file__,candidate=candidate,corrected=corrected)
 exec(compile(source,__file__+'::whole_original_special_capture_and_semantics','exec'),scope)
 return scope['bindings']()

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=corrected.prior.original.SPECS);parser.add_argument('--side',type=int,choices=(1,2));a=parser.parse_args()
 need(bool(a.move)==bool(a.side),'Specify both move and side, or the whole matrix')
 capture,_=bindings();cases=[(a.move,a.side)]if a.move else[(m,s)for m in corrected.prior.original.SPECS for s in(1,2)]
 for move,side in cases:capture(move,side)
