"""Entire original chronological native erase replay with raw reads bound to RAM."""
import copy,inspect,io,json,re,struct,types
from pathlib import Path
import numpy as np
from PIL import Image
import current_payload_metadata_context_v5229 as current
import verify_native_cpu_ring_erase_v2985 as erase
import inspect_current_cpu_knife_raster_v1975 as raster
import verify_move_phase_shadow_v5089 as graphics
from verify_native_floor_display_v602 import check_latch
ROOT,need,sha=current.ROOT,current.need,current.sha

def parser(log):
 source=inspect.getsource(raster.data)
 before="with(Path(folder)/'run.log').open(encoding='utf-8-sig')as stream:"
 need(source.count(before)==1,'Only original log transport changed')
 source=source.replace(before,'with io.StringIO(memory_log)as stream:',1)
 namespace=dict(raster.data.__globals__,io=io,memory_log=log)
 exec(compile(source,__file__+'::entire_original_RAM_scene_parser','exec'),namespace)
 return namespace['data'](ROOT)

def replay_binding(folder,ram,log):
 groups,buffers,_,_,owners=parser(log)
 # Preserve the exact native unit/scaled decoder and all CPU operations.
 source=inspect.getsource(raster.base.Replay.begin)
 before="raw=(self.folder/base['file']).read_bytes()"
 need(source.count(before)==1,'Only original initial base read changed')
 source=source.replace(before,"raw=ram[base['file']]",1)
 namespace=dict(raster.base.Replay.begin.__globals__,ram=ram)
 exec(compile(source,__file__+'::entire_original_RAM_initial_base','exec'),namespace)
 class RAMReplay(raster.Replay):pass
 RAMReplay.begin=namespace['begin']
 scoped=types.SimpleNamespace(data=lambda _: (groups,buffers,None,None,owners),Replay=RAMReplay)
 source=inspect.getsource(erase.inspect)
 substitutions={
  "(folder/'guest_maincpu.bin').read_bytes()":"ram['guest_maincpu.bin']",
  "(folder/r['file']).read_bytes()":"ram[r['file']]",
  "np.fromfile(folder/target['file'],dtype='<u2')":"np.frombuffer(ram[target['file']],dtype='<u2')"}
 for before,after in substitutions.items():
  need(source.count(before)==1,'Only raw source I/O substituted: '+before);source=source.replace(before,after,1)
 namespace=dict(erase.inspect.__globals__,ram=ram,raster=scoped)
 exec(compile(source,__file__+'::entire_original_CPU_DMA_shift_Fill_one_base_erase_RAM','exec'),namespace)
 return namespace['inspect'],groups,buffers

def verify(folder,ram,log,guest,pins):
 erase.source_contract()
 prior=ROOT/'audit_v3282_current_cpu_square_render_erase_checked/report.json'
 qualified=json.loads(prior.read_text());need(qualified['passed'],'Original actual full scene/erase acceptance')
 for module in(erase,raster,raster.base,raster.scaling,graphics):
  p=Path(module.__file__).resolve()
  # Current full body graphics qualification is independently pinned in5356.
  if module is graphics:
   old=json.loads((ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json').read_text())
   need(sha(p)==old['inputHashes'][str(p)],'Whole independently interleaved graphics constructor unchanged')
  else:need(sha(p)==qualified['inputHashes'][str(p)],'Whole accepted native scene implementation unchanged')
  pins[str(p)]=sha(p)
 image=graphics.reconstruct(pins);payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 for header,magic,expected_source,expected_dest in((0x1c0000,b'KFX1',0x1c4000,0x1e04000),
  (0x1c1000,b'KPI1',0x1e6000,0x1e50000),(0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
  need(payload[header:header+4]==magic,'Entire source-owned graphics payload header')
  source,count,dest=struct.unpack_from('<III',payload,header+4)
  need(source==expected_source and dest==expected_dest and 0<count and source+count<=len(payload)and dest+count<=len(image),'Complete actual runtime graphics patch bounds')
  image[dest:dest+count]=payload[source:source+count]
 own=current.expected_gfx();image[0x1fa0000:0x1fa0000+11944]=own[:11944];image[0x1fa4000:0x1fa4000+7032]=own[11944:]
 new=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 old=ROOT/graphics.native.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 def declaration(p):return p.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0].split('ROM_REGION( 0x2000000, "gfxrom", ROMREGION_ERASE00 )',1)[1]
 need(declaration(new)==declaration(old),'Entire actual compiled graphics lane declaration matches independent constructor')
 for p in(prior,new,Path(__file__).resolve()):pins[str(p)]=sha(p)
 replay,groups,buffers=replay_binding(folder,ram,log)
 for r in groups['FLOOR_GFX']:
  raw=bytes.fromhex(r['data']);need(len(raw)==r['bytes']and raw==image[r['first']:r['first']+r['bytes']],'Every actual whole scene/effect/body/shadow graphics stream equals complete source-bound ROM')
 continuous=replay(folder,guest,current.NAME)
 need(continuous['passed']and continuous['oneInitialBaseOnly']and not continuous['laterBuffersUsedAsAnchors'],'Every native erase/CPU/DMA/shift/pre-buffer/flip continuously exact from one actual initial base')
 snaps=groups['FLOOR_SNAP'];displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
 latches={r['snapshot']:r for r in groups['FLOOR_LATCH']};held={r['snapshot']:r for r in groups['FLOOR_HELD']}
 need(len(snaps)==70 and [r['frame']for r in snaps]==list(range(2279,2349)),'Every full native square startup/hit/drop/landing/recovery scanout retained')
 need(set(latches).isdisjoint(held)and set(latches)|set(held)=={r['frame']for r in snaps},'Exactly one actual native latch or held display per scanout')
 rgb=[]
 for s in snaps:
  f=s['frame'];display=displays[f];latch=(latches|held)[f]
  picture=Image.frombytes('RGB',(400,254),ram[s['file']],'raw','BGRX')
  bound=check_latch(np.asarray(picture),ram[latch['file']],ram[display['palette_file']],latch['start'],latch['control'],latch['tap'])
  rgb.append(dict(frame=f,pixels=bound['pixels'],row=bound['row'],column=bound['column']))
 faults=[]
 # Mutate actual RAM targets/records; never use synthetic states or another anchor.
 first_pre=groups['FLOOR_PRE_FRAME'][0]['file'];first_flip=groups['FLOOR_LATCH'][0]['file']
 for label,target in(('wrong_actual_prebuffer',first_pre),('wrong_actual_displayed_VRAM',first_flip)):
  changed=dict(ram);bad=bytearray(changed[target]);bad[0]^=1;changed[target]=bytes(bad)
  bad_replay,_,_=replay_binding(folder,changed,log)
  try:value=bad_replay(folder,guest,current.NAME)
  except(AssertionError,ValueError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:need(not value['passed'],'Actual corrupt erase target rejected');faults.append(dict(fault=label,rejectedBy=value['failureKind']))
 # Actual first RGB pixel corruption must fail whole actual front-buffer binding.
 first=snaps[0];display=displays[first['frame']];latch=(latches|held)[first['frame']]
 raw=bytearray(ram[first['file']]);raw[0]^=1
 try:check_latch(np.asarray(Image.frombytes('RGB',(400,254),bytes(raw),'raw','BGRX')),ram[latch['file']],ram[display['palette_file']],latch['start'],latch['control'],latch['tap'])
 except ValueError as error:faults.append(dict(fault='wrong_actual_RGB_pixel',rejectedBy=str(error)))
 else:raise ValueError('Actual corrupt RGB pixel accepted')
 return dict(passed=True,continuous=continuous,fullRAMRGBBindings=rgb,exactScreenPixels=sum(r['pixels']for r in rgb),
  completeSourceBoundGraphicsStreams=len(buffers),actualRAMFaultsRejected=faults,
  wholeNativeSceneEraseAndScanoutAccepted=True,wholeArtisticFidelityAccepted=False,allArenasCPUAudioAccepted=False,fullPortAcceptance=False)
