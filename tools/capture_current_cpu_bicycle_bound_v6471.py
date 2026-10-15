"""Whole6466 collector plus missing original3395 passive contact provenance."""
import argparse,inspect,json
import capture_current_cpu_bicycle_render_v6466 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
FOLDER=ROOT/'audit_v6472_current_cpu_bicycle_bound_ram'
LUA=ROOT/'mk2ks_current_cpu_bicycle_render_bound_v6470.lua'
model,init_model,CHAIN,phase=prior.model,prior.init_model,prior.CHAIN,prior.phase


def full_phase(text,guest):
 result=prior.full_phase(text,guest)
 reference=prior.prior.miss.REFERENCE.read_text()
 rows=lambda value:[s for s in value.splitlines()if s.startswith('MK2_MOBILITY_')]
 need(rows(text)==rows(reference)and rows(text),'Every actual original3395 contact/flags/health/code row equals original5324')
 return result


def prepare():
 source=inspect.getsource(prior.prepare)
 before="extra_pins={ROOT/'mk2ks_current_cpu_compound_render_ram_v6432.lua',"
 after="extra_pins={ROOT/'mk2ks_current_cpu_bicycle_render_ram_v6465.lua',ROOT/'mk2ks_native_cpu_audio_mobility_v3395.lua',ROOT/'audit_v6467_current_cpu_bicycle_render_ram/result.json',ROOT/'mk2ks_current_cpu_compound_render_ram_v6432.lua',"
 need(source.count(before)==1,'Entire original missing-contact capture preserved, whole3395 added to source pins')
 scope=dict(prior.__dict__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,full_phase=full_phase)
 exec(compile(source.replace(before,after,1),__file__+'::whole6466_collector_additional_contact_observer_pins','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 need(not FOLDER.exists()and not prior.prior.original.previous.terminal.process_tools.census(),'Prior native process terminal, fresh actual observer scope')
 run=prepare()
 if preflight:
  guest,_,_,_,_=init_model()
  result=full_phase(prior.prior.miss.REFERENCE.read_text(),guest)
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,wholeCollectorCompiled=True,phase=result['phase'])),flush=True);return
 return run()


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 main(args.preflight)
