"""Read-only native-palette candidate Friendship scaled complete-render diagnostic, not universal acceptance.
Preserve independently detected unsupported renderer/transition cases. Scene
scanouts, full DMA replay, continuous erasure and child lifecycle are separate
gates; actual captured evidence is never edited to obtain a passing result.
"""
import argparse,json,re,struct,traceback,copy
from pathlib import Path
import numpy as np
from PIL import Image
import verify_current_friendship_shadow_inventory_v2696 as native
import verify_native_friendship_palette_assembly_v2750 as assembly
import inspect_secondary_display_v1231 as raster
import inspect_ball_register_erase_v1843 as erase
import inspect_current_cpu_knife_raster_v1975 as scaling
from verify_native_floor_display_v602 import check_latch
ROOT=native.ROOT
need=native.need
def verify(folder):
 pins={}
 def pin(path,wanted=None):
  path=str(path);actual=native.scene.launch.sha(path)
  need(wanted is None or actual==wanted,'Unchanged authoritative input '+path)
  need(path not in pins or pins[path]==actual,'Consistent actual dependency '+path);pins[path]=actual
 scaling.source(pins)
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 before=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/assembly.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(meta['exit_code']==0 and meta['candidate']==assembly.NAME and meta['assistance']=='none' and meta['guest_writes']==0 and meta['cheats_enabled'] is False and meta['command_case']=='positive' and meta['requested_gap']==160 and meta['observation']==1600 and meta['samples_enabled'] and before==meta['input_hashes'],'Actual isolated-candidate physical terminal capture')
 need(meta['executable_sha256']==build['executable_sha256']=='F7CE88667B33BA8AB7316F3C254B3B75A7A23ACA8C78524BB08B6E6055B90650' and meta['payload_sha256']==build['payload_sha256']=='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D' and all(before.get(file)==wanted for file,wanted in build['input_hashes'].items()),'Exact newly compiled native-palette executable/payload and compiled inputs')
 for file,wanted in before.items():
  pin(file,wanted)
  if Path(file).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
 source=(ROOT/'mk2ks_current_friendship_full_render_v2702.lua').read_text()
 prefix="-- Read-only full rendering observer; existing physical Friendship driver is unchanged.\ndofile('mk2ks_current_friendship_shadow_v2689.lua')\n"
 need(source.startswith(prefix) and source.count('dofile(')==1 and not re.search(r':write_|set_value|clear_value|load_?state|\.value\s*=(?!=)',source),'No added physical controls, guest/register writes or state injection')
 guest,_,payload,*_=assembly.expected()
 pins.update(assembly.source_check())
 need((folder/'guest_maincpu.bin').read_bytes()==guest and (ROOT/assembly.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Whole isolated native-palette guest/payload independently reconstructed')
 fighter,side=meta['winner'],meta['side'];baseline=ROOT/f'audit_v2691_current_{fighter}_friendship_shadow_p{side}'
 pin(baseline/'run.log');rows=native.scene.previous.parse(folder/'run.log');old=native.scene.previous.parse(baseline/'run.log')
 physical=lambda rs:[(tag,row) for tag,row in rs if not tag.startswith('SHADOW_')]
 need(physical(rows)==physical(old),'Every actual physical input, health, native pose, child part, WIN, voice and transition record unchanged')
 log=(folder/'run.log').read_text(encoding='utf-8-sig')
 need(not re.search(r'LUA ERROR|fatal error|access violation|stack traceback|WRONG CHECKSUMS',log,re.I),'No native/observer runtime errors')
 image=bytearray(native.graphics.graphics(pins))
 control=native.inventory(rows,fighter,side,guest,image)
 for header,magic,source_at,dest in ((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),(0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
  need(payload[header:header+4]==magic,'Current native effect graphics source header')
  first,count,destination=struct.unpack_from('<III',payload,header+4)
  need(first==source_at and destination==dest and count>0 and first+count<=len(payload) and dest+count<=len(image),'Complete bounded effect graphics source')
  image[dest:dest+count]=payload[first:first+count]
 groups,buffers,*_=raster.data(folder)
 for row in groups['FLOOR_GFX']:
  first,count=row['first'],row['bytes']
  need(0<=first<first+count<=len(image) and bytes.fromhex(row['data'])==image[first:first+count],'Every actual scenery/body/shadow/effect buffer is source-bound')
 windows=groups['FLOOR_WINDOW'];final=groups['FLOOR_RESULT'];snaps=groups['FLOOR_SNAP']
 need(len(windows)==len(final)==1 and windows[0]['window']==control['window'] and final[0]['origin']==control['action'],'Actual native finish window and action context')
 expected=list(range(control['window']+1,control['window']+1601))
 need([row['frame'] for row in snaps]==expected and final[0]['snapshots']==1600,'All 1600 consecutive actual scene/transition scanouts retained')
 displays={row['frame']:row for row in groups['FLOOR_DISPLAY']}
 latches={row['snapshot']:row for row in groups['FLOOR_LATCH']};held={row['snapshot']:row for row in groups['FLOOR_HELD']}
 need(len(latches)+len(held)==1600 and not set(latches)&set(held) and set(latches)|set(held)==set(expected) and set(displays)==set(expected),'Each actual scanout has exactly one original latch/held context')
 bindings=[];negatives=[]
 for snap in snaps:
  frame=snap['frame'];display=displays[frame];context=latches.get(frame,held.get(frame))
  picture=np.asarray(Image.open(folder/'snap'/snap['file']).convert('RGB'));raw=(folder/context['file']).read_bytes();palette=(folder/display['palette_file']).read_bytes()
  need(all(context[k]==display[k] for k in ('start','control','tap')),'Actual screenshot display registers equal native context')
  value=check_latch(picture,raw,palette,context['start'],context['control'],context['tap'])
  bindings.append(dict(frame=frame,held=frame in held,**value))
  if len(negatives)==0:
   changed=picture.copy();changed[0,0,0]^=1
   try:check_latch(changed,raw,palette,context['start'],context['control'],context['tap'])
   except ValueError as error:
    need('Every screenshot pixel matches' in str(error),'Intended single rendered-pixel mismatch rejection');negatives.append(dict(name='one_actual_rendered_pixel_changed',rejectedBy=str(error)))
   else:raise ValueError('Changed screenshot accepted')
 need(len(negatives)==1,'Non-vacuous actual raster corruption rejected')
 print('Bound',len(bindings),'actual complete scanouts; independently replaying all native writes',flush=True)
 diagnostics={}
 for name,run in (('drawing',raster.inspect),('continuousErasure',erase.inspect)):
  try:
   value=run(folder)
   if name=='drawing':need(value['frames']==len(latches) and all(row['vram_mismatches']==row['displayed_mismatches']==row['shadow_mismatches']==0 for row in value['records']),'Every actual native drawing pass and visible shadow pixel independently exact')
   else:need(value['passed'] and value['oneInitialBaseOnly'] and not value['laterBuffersUsedAsAnchors'] and value['continuousExactFlips']==len(latches),'Every native inter-pass write/erase exactly reconstructed from one initial base')
   diagnostics[name]=dict(passed=True,**{key:val for key,val in value.items() if key not in ('passed','inputHashes')})
   for file,wanted in value.get('inputHashes',{}).items():pin(file,wanted)
  except Exception as error:diagnostics[name]=dict(passed=False,error=repr(error),traceback=traceback.format_exc())
 for path in folder.rglob('*'):
  if path.is_file():pin(path)
 pin(Path(__file__).resolve());native.scene.launch.module_pins(pins)
 all_pass=all(value['passed'] for value in diagnostics.values())
 return dict(passed=True,diagnosticCompleted=True,fighter=fighter,side=side,control=control,physicalInputAndNativeChronologyUnchanged=True,wholeActualGuestAndPayloadReconstructed=True,allActualGraphicsBuffersROMBound=True,
  actualConsecutiveScanouts=1600,actualBoundPixels=1600*400*254,heldOriginalScanouts=len(held),actualRenderedPixelCounterexamples=negatives,finalUnmodifiedBindingControlsPassed=True,
  diagnostics=diagnostics,fullDrawingAndContinuousErasureAccepted=all_pass,childObjectCleanupAccepted=False,completeSceneRasterShadowAudioAccepted=False,fullFinisherAcceptance=False,fullPortAcceptance=False,gameChanged=True,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable actual render diagnostic')
 try:r=verify(a.folder)
 except Exception as error:r=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k not in ('inputHashes','diagnostics')},indent=2),flush=True)
 for name,result in r.get('diagnostics',{}).items():print(name,json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
 raise SystemExit(0 if r['passed'] else 1)
