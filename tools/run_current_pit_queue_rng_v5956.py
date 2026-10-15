"""Whole5945 RAM-only capture/mix with additional passive queue/RNG state."""
import argparse,hashlib,json,traceback
from types import SimpleNamespace
import run_current_subzero_pit_audio_v5945 as predecessor
import qualify_current_pit_queue_rng_v5957 as source
ROOT,need,sha,current,model=predecessor.ROOT,predecessor.need,predecessor.sha,predecessor.current,predecessor.model
state=predecessor.state;once=predecessor.once
LUA='mk2ks_current_pit_queue_rng_campaign_v5955.lua'
OBSERVER='mk2ks_current_pit_queue_rng_v5954.lua'
EXTRA_INPUTS=predecessor.EXTRA_INPUTS+(LUA,OBSERVER,'tools/run_current_pit_queue_rng_v5956.py','tools/qualify_current_pit_queue_rng_v5957.py')

def collector():
 old,_=predecessor.collector();code=old.source
 for before,after in(('audit_v5947_current_subzero_pit_mix_','audit_v5959_current_pit_queue_rng_'),
                      ("lua='"+predecessor.LUA+"'","lua='"+LUA+"'"),
                      ('    files.update(ROOT/p for p in '+repr(predecessor.EXTRA_INPUTS)+')',
                       '    files.update(ROOT/p for p in '+repr(EXTRA_INPUTS)+')')):
  code=once(code,before,after)
 scope=dict(old.__globals__,__file__=__file__,__doc__=__doc__,source=source,OBSERVER=OBSERVER)
 exec(compile(code,__file__+'::entire5945_passive_queue_rng','exec'),scope)
 fn=scope['capture'];fn.source=code
 return fn,hashlib.sha256(code.encode()).hexdigest().upper()

code=predecessor.run.source
scope=dict(predecessor.run.__globals__,__file__=__file__,__doc__=__doc__,source=source,collector=collector,LUA=LUA,OBSERVER=OBSERVER)
exec(compile(code,__file__+'::entire5945_unchanged_native_mixer','exec'),scope)
run=scope['run'];run.source=code

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 folder=ROOT/f'audit_v5959_current_pit_queue_rng_{args.fighter}_p{args.side}_samples'
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():(folder/'audio_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
