"""Full native CPU ball raster, unchanged controls/build and original3642 model."""
import argparse,hashlib,inspect,json
from types import SimpleNamespace
import capture_current_cpu_effect_render_v6348 as original
import current_tomb_ram_model_v3642 as plain
from current_cpu_ball_context_v6451 import phase_gate
ROOT,need,sha=original.ROOT,original.need,original.sha
FOLDER=ROOT/'audit_v6453_current_cpu_ball_render_ram'
LUA=ROOT/'mk2ks_current_cpu_ball_render_v6450.lua'
source=inspect.getsource(plain.Model)
before='len(self.ids)==2 and set(self.ids)=={17,18}'
need(source.count(before)==1,'Only explicitly observed Kano17/Kano17 physical tuple differs')
source=source.replace(before,'self.ids==(17,17)',1)
scope=dict(plain.__dict__)
exec(compile(source,__file__+'::whole_original_3642_raster_explicit_Kano_mirror','exec'),scope)
model=SimpleNamespace(original=plain,Model=scope['Model'],Transport=plain.Transport,digest=plain.digest,
                      parse=plain.parse,MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper())


def init_model():
 scope=dict(original.init_model.__globals__,model=model)
 exec(compile(inspect.getsource(original.init_model),__file__+'::whole_original_independent_3642_Kano_mirror','exec'),scope)
 return scope['init_model']()


def prepare():
 source=inspect.getsource(original.main)
 changes={
  'audit_v6344_current_cpu_blade_allocation_checked/report.json':'audit_v6299_current_kano_cpu_ball_checked/report.json',
  'full_phase=phase.phase_gate()':'full_phase=phase_gate()',
  "MK2KS_CPU_PAIR_CONFIRM_AGE='265'":"MK2KS_CPU_PAIR_CONFIRM_AGE='264'",
  'audit_v6342_current_cpu_blade_allocation_ram/run.log.gz':'audit_v6293_current_kano_cpu_extended_ram/run.log.gz',
  'list(range(1870,2511))':'list(range(1814,1919))',
  'Every consecutive field through blade, KO/round reset, knife and cleanup':'Every pre-entry ball field, roll, rebound, both recoveries and thirty-field tail',
 }
 for before,after in changes.items():
  need(source.count(before)>=1,'Only real ball context and passive coverage differs '+before);source=source.replace(before,after)
 first=source.index(' extra_pins={parent,');last=source.index(' for module in tuple(sys.modules.values()):',first)
 source=source[:first]+" extra_pins={parent,ROOT/'mk2ks_native_tomb_ram_v3624.lua',ROOT/'mk2ks_current_kano_cpu_extended_ram_v6290.lua',ROOT/'mk2ks_physical_p2_cpu_ring_display_v2014.lua',ROOT/'mk2ks_special_shadow_v5131.lua',ROOT/'mk2ks_physical_p2_cpu_continuation_v3300.lua',ROOT/'mk2ks_physical_p2_cpu_choice_trace_v3303.lua',ROOT/'audit_v6293_current_kano_cpu_extended_ram/run.log.gz',ROOT/'audit_v5823_current_held_tomb_kano_p1_render_checked/report.json'}\n"+source[last:]
 source=source.replace(" return scope['capture']()"," return scope['capture']",1)
 scope=dict(original.__dict__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,model=model,init_model=init_model,phase_gate=phase_gate)
 exec(compile(source,__file__+'::whole_terminal_first_preentry_ball_renderer','exec'),scope)
 return scope['main']()


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 run=prepare()
 if args.preflight:print(json.dumps(dict(preflightPassed=True,nativeBoots=0,wholeCollectorCompiled=True)),flush=True)
 else:run()
