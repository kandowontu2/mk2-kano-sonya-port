"""Entire 6643 physical controller/gate, prompt native kernel identity census.

The immutable 6644 P1 run missed its identity census and remains failed. This
uses a fresh leaf, polls the actual process immediately and changes no input,
native game speed, guest bytes, audio, semantics, or terminal draining.
"""
import argparse,inspect
from pathlib import Path
import capture_kano_launch_specials_v6643 as prior
import native_process_census_v6647 as identity
need=prior.need

def bindings():
 capture,load=prior.bindings();scope=dict(capture.__globals__,__file__=__file__,census=identity.census,native_identity_tools=identity)
 for fn in(load,capture):
  source=inspect.getsource(fn)if fn.__code__.co_filename==__file__ else None
  # Dynamically compiled original collector source is recovered from the
  # unchanged underlying functions, with all earlier adaptations reapplied.
  if fn is load:
   source=inspect.getsource(prior.corrected.prior.load_case)
  else:
   source=inspect.getsource(prior.corrected.prior.capture)
  changes={'audit_v6262_current_cmd_special_':'audit_v6649_kano_launch_special_'}
  if fn is capture:
   changes.update({
    "command=['cmd.exe','/d','/s','/c','\"'+subprocess.list2cmdline(args)+'\"']":"command=[os.environ['ComSpec'],'/d','/c',*args]",
    'for p in(LUA,LAUNCHER,':'for p in(Path(prior.__file__),Path(native_identity_tools.__file__),Path(corrected.__file__),Path(corrected.prior.__file__),LUA,LAUNCHER,',
    'canonicalCMDUsed=True':'canonicalCMDUsed=False,isolatedCandidateCMDUsed=True',
    'check,_,_=context.bindings();report':'check,_,_=context.bindings();check.__globals__["native"]=current;report',
    'time.sleep(2);jobs=census()':
    "jobs=[]\n   for observation in range(100):\n    jobs=census()\n    if any(j['ParentProcessId']==process.pid for j in jobs):break\n    if process.poll()is not None:break\n    time.sleep(.02)",
   })
  for before,after in changes.items():
   need(source.count(before)==1,'Exact original capture/kernel census adaptation '+before);source=source.replace(before,after,1)
  scope.update(prior=prior,identity=identity,corrected=prior.corrected)
  exec(compile(source,__file__+'::whole_original_'+fn.__name__,'exec'),scope)
 return scope['capture'],scope['load_case']

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=prior.corrected.prior.original.SPECS);parser.add_argument('--side',type=int,choices=(1,2));a=parser.parse_args()
 need(bool(a.move)==bool(a.side),'Both move and side, or the complete matrix')
 capture,_=bindings();cases=[(a.move,a.side)]if a.move else [('ball',1),('ball',2)]+[(m,s)for m in prior.corrected.prior.original.SPECS if m!='ball'for s in(1,2)]
 for move,side in cases:capture(move,side)
