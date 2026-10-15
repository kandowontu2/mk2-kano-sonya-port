"""Whole5956 successor correcting only the terminal-failed boot deadline."""
import argparse,hashlib,json,traceback
import run_current_pit_queue_rng_v5956 as failed_host
import qualify_current_pit_queue_rng_v5962 as source
ROOT,need,sha,current,model=failed_host.ROOT,failed_host.need,failed_host.sha,failed_host.current,failed_host.model
state=failed_host.state;once=failed_host.once
LUA='mk2ks_current_pit_queue_rng_campaign_v5960.lua'
OBSERVER=failed_host.OBSERVER
EXTRA_INPUTS=failed_host.EXTRA_INPUTS+(LUA,'tools/run_current_pit_queue_rng_v5961.py','tools/qualify_current_pit_queue_rng_v5962.py')

def collector():
 old,_=failed_host.collector();code=old.source
 for before,after in(('audit_v5959_current_pit_queue_rng_','audit_v5964_current_pit_queue_rng_'),
                      ("lua='"+failed_host.LUA+"'","lua='"+LUA+"'"),
                      ('    files.update(ROOT/p for p in '+repr(failed_host.EXTRA_INPUTS)+')',
                       '    files.update(ROOT/p for p in '+repr(EXTRA_INPUTS)+')')):
  code=once(code,before,after)
 scope=dict(old.__globals__,__file__=__file__,__doc__=__doc__,source=source)
 exec(compile(code,__file__+'::whole5956_corrected_boot_deadline','exec'),scope)
 fn=scope['capture'];fn.source=code
 return fn,hashlib.sha256(code.encode()).hexdigest().upper()

code=failed_host.run.source
scope=dict(failed_host.run.__globals__,__file__=__file__,__doc__=__doc__,source=source,collector=collector,LUA=LUA)
exec(compile(code,__file__+'::whole5956_native_mixer_unchanged','exec'),scope)
run=scope['run'];run.source=code

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 folder=ROOT/f'audit_v5964_current_pit_queue_rng_{args.fighter}_p{args.side}_samples'
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():(folder/'audio_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
