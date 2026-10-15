"""Current native Bicycle: whole5324 physical trace, unchanged3642 raster."""
import argparse,gzip,inspect,json
from pathlib import Path
import capture_current_cpu_compound_render_v6433 as prior
import native_cpu_bicycle_hit_contract_v3317 as phase
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
FOLDER=ROOT/'audit_v6467_current_cpu_bicycle_render_ram'
LUA=ROOT/'mk2ks_current_cpu_bicycle_render_ram_v6465.lua'
model,init_model,CHAIN=prior.model,prior.init_model,prior.CHAIN


def full_phase(text,guest):
 # Retain the complete paired vertical/choreography/health contract. Native
 # horizontal body push is separately qualified from the new cache observations.
 bicycle=phase.verify(text,guest)
 compound=prior.full_phase(text,guest)
 need((bicycle['start'],bicycle['hit'],bicycle['victimReady'])==(2663,2680,2767),'Existing real Bicycle chronology')
 return dict(phase=bicycle,wholeOriginalMixedMatch=compound)


def prepare():
 source=inspect.getsource(prior.prepare)
 before="list(range(timeline['leg']['start']+1,timeline['ordinaryContinuation']['lastObservedTail']+1))"
 need(source.count(before)==1,'Only actual Bicycle continuous window bounds change')
 source=source.replace(before,"list(range(timeline['phase']['start']-1,timeline['phase']['victimReady']+31))",1)
 before='extra_pins={legacy,'
 need(source.count(before)==1,'Pin whole reused Lua source and current phase/audio evidence')
 source=source.replace(before,"extra_pins={ROOT/'mk2ks_current_cpu_compound_render_ram_v6432.lua',ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json',ROOT/'audit_v6447_current_cpu_compound_audio_checked/report.json',legacy,",1)
 source=source.replace('Every third-leg field, overlapping victim/Square handoff, ordinary attack and thirty-field cleanup tail',
                       'Every Bicycle pre-entry/startup/seek/lift/float/release and both native recoveries plus thirty-field tail')
 scope=dict(prior.__dict__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,full_phase=full_phase)
 exec(compile(source,__file__+'::whole6433_terminal_first_Bicycle_context','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 need(not FOLDER.exists()and not prior.original.previous.terminal.process_tools.census(),'Fresh observation job, empty native census')
 run=prepare()
 if preflight:
  guest,_,_,_,_=init_model()
  result=full_phase(prior.miss.REFERENCE.read_text(),guest)
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,wholeCollectorCompiled=True,phase=result['phase'])),flush=True);return
 return run()


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 main(args.preflight)
