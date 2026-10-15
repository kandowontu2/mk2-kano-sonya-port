"""Source-explicit native screen-bitmap versus video-snapshot phase contract.

Keep the three6189 failures. The original driver calls screen:pixels before
the continuous observer calls video:snapshot_pixels in the same frame_done.
All twelve overlapping moving/held native pictures match the preceding video
snapshot exactly, not a nearest-frame search. Keep every complete original
state, RGB, FIFO, palette, floor, shadow and negative-control predicate.
"""
from pathlib import Path
import copy

adapter_source=Path(__file__).with_name('qualify_current_subzero_scene_v6189.py')

def native_api_overlap(sparse,raw_proof,rgb):
 import current_payload_metadata_context_v5229 as current
 need=current.need
 actual=raw_proof['actualFourNativeRGBStages']
 need(len(sparse)==len(actual)==4,'All four complete independently observed original screen bitmap stages')
 overlaps=[]
 for old,new in zip(sparse,actual):
  need(old['frame']==new['frame']and old['sha256']==new['sha256']and
       old['actualRGBSHA256']==new['actualRGBSHA256'],'All four actual screen:pixels frames byte-identical to qualified sparse capture, including next CPU match')
 for stage in actual[:3]:
  frame=stage['frame'];display_frame=frame-1
  need(rgb[display_frame]==stage['actualRGBSHA256'],
       'Whole actual prior video snapshot equals original screen bitmap before same-callback snapshot render')
  overlaps.append(dict(originalScreenBitmapCallbackFrame=frame,continuousVideoSnapshotFrame=display_frame,
                       actualRGBSHA256=stage['actualRGBSHA256'],everyPixelExactlyEqual=True,
                       comparisonUsesFixedSourceCallbackPhase=True,nearestFrameSearch=False))
 need(all(rgb[s['frame']]!=s['actualRGBSHA256']for s in actual[:2]),
      'Moving freeze/fracture stages non-vacuously distinguish pre-render bitmap from same-callback video snapshot')
 return overlaps

def native_api_faults(sparse,raw_proof,rgb):
 import current_payload_metadata_context_v5229 as current
 faults=[]
 for label in ('changed_actual_screen_pixel_digest','shifted_actual_screen_callback_frame','changed_continuous_prior_display_digest'):
  changed=copy.deepcopy(raw_proof);display=dict(rgb)
  if label=='changed_actual_screen_pixel_digest':changed['actualFourNativeRGBStages'][0]['actualRGBSHA256']='0'*64
  elif label=='shifted_actual_screen_callback_frame':changed['actualFourNativeRGBStages'][0]['frame']+=1
  else:display[changed['actualFourNativeRGBStages'][0]['frame']-1]='0'*64
  try:native_api_overlap(sparse,changed,display)
  except(ValueError,KeyError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual original native screen/snapshot phase fault admitted '+label)
 current.need(len(faults)==3,'All real native API overlap faults rejected')
 return faults

outer=adapter_source.read_text()
outer=outer.replace('audit_v6190_current_subzero_','audit_v6192_current_subzero_')
anchor="exec(compile(source,__file__+'::whole_actual_protocol_and_native_FIFOfloor','exec'),globals())"
assert outer.count(anchor)==1,'Exact complete original qualifier execution'
repair='''
before=" for s in sparse[:3]:need(rgb[s['frame']]==s['actualRGBSHA256'],'Each of three complete overlapping current native finisher RGB stages identical, no donor/modelled substitute')"
assert source.count(before)==1,'Exact erroneous same-frame API assertion preserved in executed precursor'
source=source.replace(before," overlap=native_api_overlap(sparse,raw_proof,rgb)\\n overlap_faults=native_api_faults(sparse,raw_proof,rgb)",1)
before="observed,prior_qualifier,position_repair,Path(__file__),Path(current.__file__)"
assert source.count(before)==1,'Pin all executed precursor/current sources'
source=source.replace(before,"observed,prior_qualifier,position_repair,adapter_source,Path(__file__),Path(current.__file__)",1)
before="             completeCurrentStateRowsEqualIndependentQualifiedReference=True,threeOverlappingNativeRGBStagesExactlyEqual=True,"
assert source.count(before)==1,'Retain whole original state and native raster checks'
source=source.replace(before,before+"\\n             actualSourcePhasedNativeRGBOverlap=overlap,actualNativeAPIPhaseFaults=overlap_faults,",1)
before=" for p in folder.rglob('*'):"
assert source.count(before)==1,'Bind actual callback implementations and preserve failed reports'
source=source.replace(before," for p in (ROOT/'mk2ks_native_subzero_legs_body_v4997.lua',ROOT/'mk2ks_native_subzero_legs_lifecycle_v4999.lua',ROOT/'mk2ks_jax_clap_native_scene_ram_v4019.lua',ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp',ROOT/'mame-mkp/src/frontend/mame/luaengine_render.cpp',ROOT/'mame-mkp/src/emu/screen.cpp',ROOT/'mame-mkp/src/emu/video.cpp'):\\n  pins[str(p.resolve())]=sha(p)\\n"+before,1)
'''
outer=outer.replace(anchor,repair+'\n'+anchor,1)
exec(compile(outer,__file__+'::complete_native_API_phase_and_FIFO_shadow','exec'),globals())
