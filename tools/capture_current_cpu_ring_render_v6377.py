"""Current native Ring contact and full scene, no builds/copies/raw buffers.

Keep6285 terminal-first capture and3642 full CPU/DMA/shift/raster algorithm.
Whole original1997 physical controls and2014 passive observations unchanged.
"""
import argparse,gzip,inspect,json,re,sys,traceback
from pathlib import Path
import capture_current_cpu_effect_render_v6348 as previous
import current_cpu_ring_render_model_v6376 as model
import verify_native_cpu_ring_v2971 as phase
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
FOLDER=ROOT/'audit_v6378_current_cpu_ring_render_ram'
LUA=ROOT/'mk2ks_current_cpu_ring_render_ram_v6375.lua'
CHAIN=('mk2ks_physical_p2_cpu_continuation_v1997.lua','mk2ks_physical_p2_cpu_round_trace_v1998.lua',
       'mk2ks_physical_p2_cpu_overlap_trace_v1999.lua','mk2ks_physical_p2_cpu_ring_trace_v2013.lua','mk2ks_physical_p2_cpu_ring_display_v2014.lua')


def init_model():
 source=inspect.getsource(previous.init_model)
 need(source.count('(17,17)')==1,'Explicit current physical Kano/Sonya tuple only')
 source=source.replace('(17,17)','(17,18)',1)
 scope=dict(previous.init_model.__globals__,model=model)
 exec(compile(source,__file__+'::whole_current_independent_guest_GFX_ring_roles','exec'),scope)
 return scope['init_model']()


def full_phase(text,guest):
 ring=phase.ring_contract.verify(text,guest,'kano')
 health,by=phase.health_ledger(text,guest,'kano');state=phase.state_ledgers(text,guest,'kano',by)
 completed=phase.pair.rows(text,'COMPLETE')
 pairs=[phase.pair.verify_pair(text,'kano',r['cycle'],guest)for r in completed]
 need(ring['reached']and len(ring['acceptedRings'])==1 and pairs,'Whole actual ring contact plus complete natural paired continuations')
 return dict(ring=ring,wholeNativeHealth=health,wholeNativeState=state,pairedContinuations=pairs)


def prepare():
 source=inspect.getsource(previous.terminal.capture)
 changes={
  'guest=current.expected();build=ROOT/current.NAME':'guest,build,scene,transport,graphics_pins=init_model()',
  "prior_path=ROOT/'audit_v1963_current_kano_cpu_overlap_checked/report.json'":"prior_path=ROOT/'audit_v3432_current_cpu_ring_checked/report.json'",
  'prior=json.loads(prior_path.read_text())':"prior=json.loads(prior_path.read_text());prior['inputHashes']={str(Path(k).resolve()):v for k,v in prior['inputHashes'].items()}",
  'for p in (LUA,Path(__file__).resolve(),':'for p in (*extra_pins,LUA,Path(__file__).resolve(),',
  "MK2KS_TEST_BOOT_FRAME='960'":"MK2KS_TEST_BOOT_FRAME='613',MK2KS_CPU_CONTINUATION_POLICY='retreat'",
  "MK2KS_CPU_PAIR_APPROACH='guard_until_close'":"MK2KS_CPU_PAIR_APPROACH='original'",
  "'-noautoframeskip','-frameskip','0','-str','95'":"'-noautoframeskip','-frameskip','0','-snapsize','400x254','-str','95'",
  'errors=[];proof=None;scenes=[];':'pins.update(graphics_pins)\n errors=[];proof=None;scenes=[];',
  "if line.startswith(('MK2_KNIFE_RAM_RGB ','MK2_KNIFE_RAM_GUEST ')):":"if line.startswith(('MK2_TOMB_RAM_BUFFER ','MK2_TOMB_RAM_PIXELS ')):\n      log.write(previous.ram(line,process.stdout,scene,transport,errors))\n     elif line.startswith(('MK2_KNIFE_RAM_RGB ','MK2_KNIFE_RAM_GUEST ')):",
  "need('hex='not in line,'Never persist raw media/guest');log.write(line)":"need('hex='not in line,'Never persist raw media/guest');log.write(previous.draw(line,scene,errors))",
  'except Exception as error:errors.append(repr(error))\n   code=process.wait()':"except Exception as error:\n     if not errors:errors.append(dict(error=repr(error),traceback=traceback.format_exc(),line=re.sub(r'\\bdata=[^\\s]+','data=RAM_ONLY',line[:1500])))\n   code=process.wait()",
  'report=dict(passed=False,':"(FOLDER/'buffer_digests.json').write_text(json.dumps(transport.records,indent=2)+'\\n')\n (FOLDER/'continuous_scene_records.json').write_text(json.dumps(scene.records,indent=2)+'\\n')\n report=dict(passed=False,",
  "report['independentSemantics']=original.verify(text,guest)":"report['independentSemantics']=full_phase(text,guest)\n  timeline=report['independentSemantics']['ring']['acceptedRings'][0]\n  need([r['frame']for r in scene.records]==list(range(timeline['start']+1,max(timeline['ownReady'],timeline['retirement'])+31)),'Every consecutive Ring field and complete thirty-field cleanup tail')\n  report['continuousRender']=dict(fields=len(scene.records),exactRGBPixels=sum(r['exactRGBPixels']for r in scene.records),paletteChecks=scene.palette_checks,actualPixelFaultsRejected=scene.counterexamples,oneInitialBaseOnly=True,comparisonTargetsNeverSeedReplay=True,modelSourceSHA256=model.MODEL_SOURCE_SHA256)\n  with (ROOT/'audit_v3430_current_cpu_ring_kano/run.log').open(encoding='utf-8-sig')as file:prior_text=file.read()\n  prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_RING_PAIR_')\n  report['wholeEarlierPhysicalTrajectoryIdentical']=[s for s in text.splitlines()if s.startswith(prefixes)]==[s for s in prior_text.splitlines()if s.startswith(prefixes)]",
 }
 for before,after in changes.items():
  need(source.count(before)==1,'One full terminal collector adaptation '+before[:55]);source=source.replace(before,after,1)
 extra_pins={ROOT/'audit_v6359_current_cpu_effect_render_checked/report.json',ROOT/'audit_v3430_current_cpu_ring_kano/run.log',
             ROOT/'mk2ks_native_tomb_ram_v3624.lua',Path(previous.__file__),ROOT/'audit_v5823_current_held_tomb_kano_p1_render_checked/report.json'}
 for module in tuple(sys.modules.values()):
  file=getattr(module,'__file__',None)
  if file and Path(file).resolve().is_relative_to(ROOT/'tools'):extra_pins.add(Path(file).resolve())
 scope=dict(previous.terminal.capture.__globals__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,CHAIN=CHAIN,
            original=phase,previous=previous,model=model,extra_pins=extra_pins,init_model=init_model,full_phase=full_phase)
 exec(compile(source,__file__+'::whole_terminal_first_current_CPU_ring_scene','exec'),scope)
 return scope['capture']


def main(preflight=False):
 need(not FOLDER.exists() and not previous.terminal.process_tools.census(),'Fresh actual job, no live native emulator')
 function=prepare()
 if preflight:
  guest,_,scene,_,_=init_model()
  old=(ROOT/'audit_v3430_current_cpu_ring_kano/run.log').read_text(encoding='utf-8-sig')
  positive=full_phase(old,guest)
  print(json.dumps(dict(preflightPassed=True,wholeModelSourceSHA256=model.MODEL_SOURCE_SHA256,olderPhaseOnCurrentGuest=positive['ring'],newNativeBoots=0)),flush=True);return
 return function()


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if FOLDER.exists():(FOLDER/'host_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
