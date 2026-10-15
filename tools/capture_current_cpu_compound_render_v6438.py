"""Same native compound, observation precedes first entry body draw by2fields.

Retain earlier204-field raster; no game/input change. Whole original collector.
"""
import argparse,inspect,json
from pathlib import Path
import capture_current_cpu_compound_render_v6433 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
FOLDER=ROOT/'audit_v6439_current_cpu_compound_render_ram'
LUA=ROOT/'mk2ks_current_cpu_compound_render_ram_v6437.lua'
model,init_model,compound=original.model,original.init_model,original.compound


def prepare():
 source=inspect.getsource(original.prepare)
 before="timeline['leg']['start']+1,timeline['ordinaryContinuation']['lastObservedTail']+1"
 need(source.count(before)==1,'Only passive continuous coverage starts two fields earlier')
 source=source.replace(before,"timeline['leg']['start']-1,timeline['ordinaryContinuation']['lastObservedTail']+1",1)
 before='extra_pins={legacy,'
 need(source.count(before)==1,'Retain whole executed original observer and exact prior capture')
 source=source.replace(before,"extra_pins={ROOT/'mk2ks_current_cpu_compound_render_ram_v6432.lua',ROOT/'audit_v6434_current_cpu_compound_render_ram/result.json',legacy,",1)
 scope=dict(original.__dict__,__file__=__file__,FOLDER=FOLDER,LUA=LUA)
 exec(compile(source,__file__+'::whole_original_terminal_first_preentry_scene','exec'),scope)
 return scope['prepare']()


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 need(not FOLDER.exists()and not original.original.previous.terminal.process_tools.census(),'Fresh expanded observation only after original native job terminal')
 run=prepare()
 if args.preflight:print(json.dumps(dict(preflightPassed=True,wholeCollectorCompiled=True,nativeBoots=0)),flush=True)
 else:run()
