"""Current missed Ring continuous source raster, same original5324 inputs.

Reuse full terminal-first collector and source-qualified6376 renderer; only
the existing physical driver version/policy and miss semantic branch differ.
"""
import argparse,inspect,json,sys
from pathlib import Path
import capture_current_cpu_ring_render_v6377 as original
import current_cpu_ring_miss_phase_v6411 as miss

ROOT,need,sha=original.ROOT,original.need,original.sha
FOLDER=ROOT/'audit_v6413_current_cpu_ring_miss_render_ram'
LUA=ROOT/'mk2ks_current_cpu_ring_miss_render_ram_v6410.lua'
CHAIN=('mk2ks_physical_p2_cpu_continuation_v3300.lua','mk2ks_physical_p2_cpu_round_trace_v3301.lua',
       'mk2ks_physical_p2_cpu_overlap_trace_v3302.lua','mk2ks_physical_p2_cpu_choice_trace_v3303.lua',
       'mk2ks_physical_p2_cpu_square_trace_v3304.lua','mk2ks_physical_p2_cpu_ring_trace_v2013.lua',
       'mk2ks_physical_p2_cpu_ring_display_v2014.lua')
REFERENCE=ROOT/'audit_v5324_current_cpu_bicycle_ram_samples/run.log'
LEGACY=ROOT/'audit_v3432_current_cpu_ring_checked/report.json'


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
  'extra_pins={ROOT/':"extra_pins={legacy,ROOT/'mk2ks_current_cpu_ring_render_ram_v6375.lua',ROOT/",
  'scope=dict(previous.terminal.capture.__globals__,__file__=__file__,':
   'scope=dict(previous.terminal.capture.__globals__,__file__=__file__,legacy=legacy,',
 }
 for before,after in changes.items():
  need(source.count(before)>=1,'Exact existing miss physical/phase/trajectory scope '+before)
  source=source.replace(before,after)
 scope=dict(original.__dict__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,CHAIN=CHAIN,legacy=LEGACY,full_phase=miss.full_phase)
 exec(compile(source,__file__+'::whole_original_terminal_first_missed_Ring_scene','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 need(not FOLDER.exists() and not original.previous.terminal.process_tools.census(),'Fresh current miss capture, no existing live job')
 function=prepare()
 if preflight:
  guest=original.previous.terminal.current.expected()
  old=REFERENCE.read_text()
  #5324 has the full original physical/round/child/choice/Square stream,
  # but not2013's additional source/guard windows. Its unchanged observer
  # bytes and whole current guest are validated before actual new capture.
  need(miss.compound.gate(old,guest,miss.compound.square_through_handoff()[0])['passed'],'Original full compound/state/health context passes before new scene observation')
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,wholeCollectorCompiled=True)),flush=True);return
 return function()

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 main(args.preflight)
