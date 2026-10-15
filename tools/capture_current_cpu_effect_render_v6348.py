"""One full current CPU blade/knife screen replay, RAM-only targets.

Reuse whole terminal-first6285 transport and full qualified phase contract.
Drain same process on model rejection; native terminal before acceptance.
No builds, source-tree copies, raw media or comparison-target reseeding.
"""
import datetime,gzip,hashlib,inspect,json,re,subprocess,sys,traceback
from pathlib import Path
import numpy as np
import capture_current_cpu_knife_v6285 as terminal
import verify_current_cpu_blade_allocation_v6333 as phase
import current_cpu_effect_render_model_v6347 as model
import run_current_tomb_ram_matrix_v3648 as graphics
ROOT,need,sha=terminal.ROOT,terminal.need,terminal.sha
FOLDER=ROOT/'audit_v6349_current_cpu_effect_render_ram'
LUA=ROOT/'mk2ks_current_cpu_effect_render_ram_v6346.lua'


def init_model():
 guest=terminal.current.expected();build=ROOT/terminal.current.NAME
 payload=(build/'roms/mk2ks/mk2ks.mdata').read_bytes()
 pins={};image=bytearray(graphics.source_graphics(payload,pins));added=terminal.current.expected_gfx()
 need(len(added)==18976,'Current complete appended body graphics')
 image[0x1fa0000:0x1fa0000+11944]=added[:11944];image[0x1fa4000:0x1fa4000+7032]=added[11944:]
 # Use a completed whole-scene proof that actually pins this renderer version.
 sourceproof=ROOT/'audit_v5823_current_held_tomb_kano_p1_render_checked/report.json'
 proof=json.loads(sourceproof.read_text());need(proof['passed'],'Earlier full continuous raster positive control')
 need(sha(model.original.__file__)==proof['inputHashes'][str(Path(model.original.__file__).resolve())],
      'Entire qualified original continuous raster model unchanged')
 return guest,build,model.Model(guest,payload,bytes(image),(17,17)),model.Transport(),pins


def ram(line,stream,scene,transport,errors):
 row=dict(re.findall(r'(\w+)=([^\s]+)',line));encoded=next(stream).strip()
 if line.startswith('MK2_TOMB_RAM_BUFFER '):
  raw=transport.decode(row,encoded)
  if row['file']=='guest_maincpu.bin':need(raw==scene.guest,'Additional complete original-observer guest compared in RAM')
  elif not errors:scene.raw[row['file']]=raw
  digest=model.digest(raw)
 else:
  need(row['bytes']=='406400'and row['width']=='400'and row['height']=='254'and
       row['encoding']=='u32le_numeric_hex'and len(encoded)==812800,'Full actual native RGB transport')
  words=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').reshape(254,400)
  rgb=np.stack([(words>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8)
  digest=model.digest(rgb.tobytes())
  if not errors:scene.rgb[row['file']]=rgb
 return line.strip()+'_DIGEST sha256='+digest+'\n'


def draw(line,scene,errors):
 if not errors:scene.line(line)
 if re.search(r'\bdata=',line):
  raw=bytes.fromhex(re.search(r'\bdata=([^\s]+)',line).group(1))
  line=re.sub(r'\bdata=[^\s]+','data_sha256='+hashlib.sha256(raw).hexdigest().upper(),line)
 return line


def main():
 parent=ROOT/'audit_v6344_current_cpu_blade_allocation_checked/report.json';proof=json.loads(parent.read_text())
 need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Actual current complete lifetime/phase proof unchanged')
 full_phase=phase.phase_gate()
 source=inspect.getsource(terminal.capture)
 changes={
  'guest=current.expected();build=ROOT/current.NAME':'guest,build,scene,transport,graphics_pins=init_model()',
  "prior=json.loads(prior_path.read_text())":"prior=json.loads(prior_path.read_text());prior['inputHashes']={str(Path(k).resolve()):v for k,v in prior['inputHashes'].items()}",
  'for p in (LUA,Path(__file__).resolve(),':"for p in (*extra_pins,LUA,Path(__file__).resolve(),",
  "MK2KS_TEST_BOOT_FRAME='960'":"MK2KS_TEST_BOOT_FRAME='605',MK2KS_CPU_CONTINUATION_POLICY='retreat'",
  "MK2KS_CPU_PAIR_CONFIRM_AGE='264'":"MK2KS_CPU_PAIR_CONFIRM_AGE='265'",
  "'-noautoframeskip','-frameskip','0','-str','95'":"'-noautoframeskip','-frameskip','0','-snapsize','400x254','-str','95'",
  'errors=[];proof=None;scenes=[];':'pins.update(graphics_pins)\n errors=[];proof=None;scenes=[];',
  "if line.startswith(('MK2_KNIFE_RAM_RGB ','MK2_KNIFE_RAM_GUEST ')):":"if line.startswith(('MK2_TOMB_RAM_BUFFER ','MK2_TOMB_RAM_PIXELS ')):\n      log.write(ram(line,process.stdout,scene,transport,errors))\n     elif line.startswith(('MK2_KNIFE_RAM_RGB ','MK2_KNIFE_RAM_GUEST ')):",
  "need('hex='not in line,'Never persist raw media/guest');log.write(line)":"need('hex='not in line,'Never persist raw media/guest');log.write(draw(line,scene,errors))",
  'except Exception as error:errors.append(repr(error))\n   code=process.wait()':"except Exception as error:\n     if not errors:errors.append(dict(error=repr(error),traceback=traceback.format_exc(),line=re.sub(r'\\bdata=[^\\s]+','data=RAM_ONLY',line[:1500])))\n   code=process.wait()",
  'report=dict(passed=False,':"(FOLDER/'buffer_digests.json').write_text(json.dumps(transport.records,indent=2)+'\\n')\n (FOLDER/'continuous_scene_records.json').write_text(json.dumps(scene.records,indent=2)+'\\n')\n report=dict(passed=False,",
  "report['independentSemantics']=original.verify(text,guest)":"report['independentSemantics']=full_phase(text,guest)\n  with gzip.open(ROOT/'audit_v6342_current_cpu_blade_allocation_ram/run.log.gz','rt',encoding='utf-8')as reader:previous=reader.read()\n  prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_BLADE_ALLOC_')\n  need([s for s in text.splitlines()if s.startswith(prefixes)]==[s for s in previous.splitlines()if s.startswith(prefixes)],'Whole actual input/AI/RNG/health/state/pool chronology unchanged')\n  report['originalWholePhysicalTrajectoryUnchanged']=True\n  report['continuousRender']=dict(fields=len(scene.records),exactRGBPixels=sum(r['exactRGBPixels']for r in scene.records),preBuffers=scene.pre_count,flips=scene.flip_count,shiftLoads=scene.loads,shiftFills=scene.fills,shiftTransfers=scene.transfers,cpuWrites=scene.cpu_count,paletteChecks=scene.palette_checks,actualPixelFaultsRejected=scene.counterexamples,oneInitialBaseOnly=True,comparisonTargetsNeverSeedReplay=True)\n  need([r['frame']for r in scene.records]==list(range(1870,2511)),'Every consecutive field through blade, KO/round reset, knife and cleanup')",
 }
 extra_pins={parent,ROOT/'mk2ks_native_tomb_ram_v3624.lua',ROOT/'mk2ks_physical_p2_cpu_knife_display_v1966.lua',
             ROOT/'mk2ks_current_cpu_blade_allocation_v6340.lua',ROOT/'mk2ks_current_kano_cpu_extended_ram_v6290.lua',
             ROOT/'mk2ks_physical_p2_cpu_continuation_v3300.lua',ROOT/'mk2ks_physical_p2_cpu_choice_trace_v3303.lua',
             ROOT/'audit_v6342_current_cpu_blade_allocation_ram/run.log.gz',ROOT/'audit_v5823_current_held_tomb_kano_p1_render_checked/report.json'}
 for module in tuple(sys.modules.values()):
  file=getattr(module,'__file__',None)
  if file and Path(file).resolve().is_relative_to(ROOT/'tools'):extra_pins.add(Path(file).resolve())
 for before,after in changes.items():
  need(source.count(before)==1,'Single complete collector adaptation '+before[:60]);source=source.replace(before,after,1)
 scope=dict(terminal.capture.__globals__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,ROOT=ROOT,
            init_model=init_model,ram=ram,draw=draw,extra_pins=extra_pins,full_phase=full_phase)
 exec(compile(source,__file__+'::whole_terminal_first_current_full_scene_RAM','exec'),scope)
 return scope['capture']()


if __name__=='__main__':main()
