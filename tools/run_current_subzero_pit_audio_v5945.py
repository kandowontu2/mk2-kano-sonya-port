"""Whole5894 current Pit RAM-only native DAC/ROM/PCM and winner source mixer.

Normal own17/18 versus explicitly selected stock8 in both physical slots.
Added passive Main+140 metadata never changes packet/channel/DAC algorithms.
No full raster, wider stock victims, complete stage audio or release claim.
"""
import argparse,gzip,hashlib,inspect,json,time,traceback
from types import SimpleNamespace
from pathlib import Path
import run_current_cross_pit_winner_mix_v5894 as original
import current_subzero_pit_state_v5943 as state
import qualify_current_subzero_pit_audio_v5944 as source
ROOT,need,sha,current,model=original.ROOT,original.need,original.sha,original.current,original.model
once,fields=original.once,original.fields
LUA='mk2ks_current_subzero_pit_campaign_v5942.lua'
OBSERVER='mk2ks_current_subzero_pit_audio_v5941.lua'
EXTRA_INPUTS=original.EXTRA_INPUTS+('mk2ks_current_subzero_pit_driver_v5940.lua',LUA,OBSERVER,
 'tools/current_subzero_pit_state_v5943.py','tools/qualify_current_subzero_pit_audio_v5944.py','tools/run_current_subzero_pit_audio_v5945.py')

def collector():
 old,_=original.collector();code=old.source
 for before,after in (('audit_v5897_current_cross_pit_winner_mix_','audit_v5947_current_subzero_pit_mix_'),
                      ("lua='"+original.LUA+"'","lua='"+LUA+"'"),('    files.update(ROOT/p for p in '+repr(original.EXTRA_INPUTS)+')',
                                        '    files.update(ROOT/p for p in '+repr(EXTRA_INPUTS)+')')):
  code=once(code,before,after)
 namespace=dict(old.__globals__,__file__=__file__,__doc__=__doc__,state=state,source=source,current=current,model=model,OBSERVER=OBSERVER)
 exec(compile(code,__file__+'::entire5894_real_SubZero_victim_RAM_capture','exec'),namespace)
 fn=namespace['capture'];fn.source=code
 return fn,hashlib.sha256(code.encode()).hexdigest().upper()

code=original.run.source
scope=dict(original.run.__globals__,__file__=__file__,__doc__=__doc__,current=current,model=model,
 runtime=SimpleNamespace(state=state),state=state,source=source,collector=collector,LUA=LUA,OBSERVER=OBSERVER)
exec(compile(code,__file__+'::entire5894_native_winner_mix_original_stock_opponent','exec'),scope)
run=scope['run'];run.source=code

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 folder=ROOT/f'audit_v5947_current_subzero_pit_mix_{args.fighter}_p{args.side}_samples'
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():(folder/'audio_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
