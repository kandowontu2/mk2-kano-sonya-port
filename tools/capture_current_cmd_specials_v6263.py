"""Correct Windows host command quoting; preserve the unstarted 6262 failure.

The earlier CMD did not start any emulator. This uses the same argument-list
form as the already qualified ordinary launcher test, without embedded quotes.
All native observations, terminal draining and semantic gates stay unchanged.
"""
import argparse,inspect
import capture_current_cmd_specials_v6261 as prior
from pathlib import Path
need=prior.need

def bindings():
 scope=dict(prior.capture.__globals__,__file__=__file__)
 for function in(prior.load_case,prior.capture):
  text=inspect.getsource(function)
  need(text.count('audit_v6262_current_cmd_special_')==1,'Only fresh terminal evidence path')
  text=text.replace('audit_v6262_current_cmd_special_','audit_v6264_current_cmd_special_',1)
  if function is prior.capture:
   before="command=['cmd.exe','/d','/s','/c','\"'+subprocess.list2cmdline(args)+'\"']"
   need(text.count(before)==1,'Exact failed host command quoting only')
   text=text.replace(before,"command=[os.environ['ComSpec'],'/d','/c',*args]",1)
   before='for p in(LUA,LAUNCHER,'
   need(text.count(before)==1,'Preserve prior executed collector source pin')
   text=text.replace(before,'for p in(Path(prior.__file__),LUA,LAUNCHER,',1)
  exec(compile(text,__file__+'::'+function.__name__,'exec'),dict(scope,prior=prior),local_scope:={})
  scope[function.__name__]=local_scope[function.__name__]
  # Ensure capture uses the new load function, not its original function globals.
  scope[function.__name__].__globals__.update(scope)
 return scope['capture'],scope['load_case']

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=prior.original.SPECS);parser.add_argument('--side',type=int,choices=(1,2));a=parser.parse_args()
 need(bool(a.move)==bool(a.side),'Both move and side required, or neither')
 capture,_=bindings()
 cases=[(a.move,a.side)]if a.move else[(m,s)for m in prior.original.SPECS for s in(1,2)]
 for move,side in cases:capture(move,side)
