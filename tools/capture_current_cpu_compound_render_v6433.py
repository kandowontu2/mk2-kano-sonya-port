"""Full native third leg -> Square -> ordinary screen, no raw disk media.

Original5324 physical inputs and current whole guest; unchanged3642 raster.
Native terminal precedes host acceptance. Original standalone rejection retained.
"""
import argparse,hashlib,inspect,json,sys
from pathlib import Path
from types import SimpleNamespace
import capture_current_cpu_ring_render_v6377 as original
import capture_current_cpu_ring_miss_render_v6412 as miss
import current_tomb_ram_model_v3642 as plain
import verify_current_cpu_leg_square_compound_v6282 as compound

ROOT,need,sha=original.ROOT,original.need,original.sha
FOLDER=ROOT/'audit_v6434_current_cpu_compound_render_ram'
LUA=ROOT/'mk2ks_current_cpu_compound_render_ram_v6432.lua'
CHAIN=miss.CHAIN
model=SimpleNamespace(original=plain,Model=plain.Model,Transport=plain.Transport,
                      parse=plain.parse,digest=plain.digest,MODEL_SOURCE_SHA256=sha(plain.__file__))


def init_model():
 source=inspect.getsource(original.previous.init_model)
 need(source.count('(17,17)')==1,'Only explicit physical Kano17/Sonya18 tuple')
 scope=dict(original.previous.init_model.__globals__,model=model)
 exec(compile(source.replace('(17,17)','(17,18)',1),__file__+'::whole_original_independent_guest_GFX','exec'),scope)
 return scope['init_model']()


def full_phase(text,guest):
 return compound.gate(text,guest,compound.square_through_handoff()[0])


def prepare():
 source=inspect.getsource(original.prepare)
 changes={
  'audit_v3432_current_cpu_ring_checked/report.json':'audit_v6281_current_existing_cpu_inventory/report.json',
  "prior['inputHashes']={str(Path(k).resolve()):v for k,v in prior['inputHashes'].items()}":
   "prior['inputHashes']={str(Path(k).resolve()):v for k,v in {**json.loads(legacy.read_text())['inputHashes'],**prior['inputHashes']}.items()}",
  "MK2KS_CPU_CONTINUATION_POLICY='retreat'":"MK2KS_CPU_CONTINUATION_POLICY='jump_on_launch'",
  "MK2KS_CPU_PAIR_APPROACH='original'":"MK2KS_CPU_PAIR_APPROACH='guard_until_close'",
  "audit_v3430_current_cpu_ring_kano/run.log":"audit_v5324_current_cpu_bicycle_ram_samples/run.log",
  "'MK2_CPU_OVERLAP_','MK2_RING_PAIR_'":"'MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_CPU_SQUARE_'",
  'extra_pins={ROOT/':"extra_pins={legacy,ROOT/'mk2ks_special_shadow_v5131.lua',ROOT/'mk2ks_current_cpu_ring_render_ram_v6375.lua',ROOT/'mk2ks_current_cpu_ring_miss_render_ram_v6410.lua',ROOT/'mk2ks_current_cpu_ring_miss_audio_v6422.lua',ROOT/",
  'scope=dict(previous.terminal.capture.__globals__,__file__=__file__,':
   'scope=dict(previous.terminal.capture.__globals__,__file__=__file__,legacy=legacy,',
  "timeline=report['independentSemantics']['ring']['acceptedRings'][0]":
   "timeline=report['independentSemantics']",
  "list(range(timeline['start']+1,max(timeline['ownReady'],timeline['retirement'])+31))":
   "list(range(timeline['leg']['start']+1,timeline['ordinaryContinuation']['lastObservedTail']+1))",
  'Every consecutive Ring field and complete thirty-field cleanup tail':
   'Every third-leg field, overlapping victim/Square handoff, ordinary attack and thirty-field cleanup tail',
 }
 for before,after in changes.items():
  need(source.count(before)>=1,'Exact whole collector compound adaptation '+before)
  source=source.replace(before,after)
 scope=dict(original.__dict__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,CHAIN=CHAIN,
            legacy=miss.LEGACY,full_phase=full_phase,init_model=init_model,model=model)
 exec(compile(source,__file__+'::whole_original_terminal_first_compound_scene','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 need(not FOLDER.exists() and not original.previous.terminal.process_tools.census(),'Fresh native compound scene; no current live job')
 function=prepare()
 if preflight:
  guest,_,_,_,_=init_model()
  result=full_phase(miss.REFERENCE.read_text(),guest)
  need(result['leg']['start']==2920 and result['ordinaryContinuation']['lastObservedTail']==3124,
       'Passive coverage bounds derive from original actual completed compound')
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,wholeCollectorCompiled=True,
                       first=2921,last=3124,unchangedRendererSHA256=model.MODEL_SOURCE_SHA256)),flush=True)
  return
 return function()


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 main(args.preflight)
