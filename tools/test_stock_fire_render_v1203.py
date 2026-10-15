"""In-memory corruption checks; immutable real runtime evidence."""
import copy,json
from unittest.mock import patch
import verify_stock_fire_display_v1201 as proof
OUT=proof.ROOT/'audit_v1203_stock_fire_render_corruption_checks';assert not OUT.exists()
folder=proof.ROOT/'audit_v1199_fire_sonya_p2';real_data=proof.native.raster.data
observed=real_data(folder);baseline=proof.state.split.reconstruct();checks={}
def rejected(name,call):
 try:call()
 except (AssertionError,ValueError) as error:checks[name]={'rejected':True,'error':str(error)};print(name+' rejected',flush=True)
 else:raise AssertionError(name+' incorrectly accepted')
with patch.object(proof.state.split,'reconstruct',return_value=baseline):
 result=proof.verify('sonya',2);assert result['passed'];checks['baseline']={'passed':True,'replayedFields':result['replayed']['frames']}
 for name in ('original_burn_gfx_byte_changed','foreign_victim_id','native_component_width_changed','actor_pixel_facing_changed','native_retirement_store_missing'):
  changed=copy.deepcopy(observed);groups=changed[0]
  if name=='original_burn_gfx_byte_changed':
   source=next(q['source'] for q in groups['FLOOR_QUEUE'] if q['slot']==2 and q['pose'] in proof.state.BURN)
   row=next(r for r in groups['FLOOR_GFX'] if r['first']==source//8);raw=bytearray.fromhex(row['data']);raw[0]^=1;row['data']=raw.hex()
  elif name=='foreign_victim_id':next(q for q in groups['FLOOR_QUEUE'] if q['slot']==2)['id']=1
  elif name=='native_component_width_changed':next(q for q in groups['FLOOR_QUEUE_PART'] if q['slot']==2)['width']+=1
  elif name=='actor_pixel_facing_changed':next(q for q in groups['FLOOR_QUEUE'] if q['slot']==2)['facing']^=16
  else:groups['FLOOR_POINTER_STORE'].pop()
  def data(path,altered=changed):return altered if proof.Path(path)==folder else real_data(path)
  with patch.object(proof.native.raster,'data',side_effect=data):rejected(name,lambda:proof.verify('sonya',2))
 read=proof.Path.read_bytes;guest_file=folder/'guest_maincpu.bin'
 def corrupt(path):
  raw=read(path)
  if path!=guest_file:return raw
  changed=bytearray(raw);changed[-1]^=1;return bytes(changed)
 with patch.object(proof.Path,'read_bytes',corrupt):rejected('whole_actual_guest_changed',lambda:proof.verify('sonya',2))
 groups=observed[0];display=next(d for d in groups['FLOOR_DISPLAY'] if any(q['slot']==2 and q['pose'] in proof.state.BURN and q['frame']==d['frame']-1 for q in groups['FLOOR_QUEUE']))
 palette_file=folder/display['palette_file'];actual_fromfile=proof.np.fromfile
 def recolor(path,*args,**kwargs):
  values=actual_fromfile(path,*args,**kwargs)
  if proof.Path(path)==palette_file:values=values.copy();values[0x0500+1]^=1
  return values
 with patch.object(proof.np,'fromfile',recolor):rejected('actual_burn_palette_changed',lambda:proof.verify('sonya',2))
 opened=proof.Image.open;image_file=folder/'snap'/groups['FLOOR_SNAP'][0]['file']
 def black(path,*args,**kwargs):
  if isinstance(path,(str,proof.Path)) and proof.Path(path)==image_file:
   image=opened(path).convert('RGB');image.paste((0,0,0),(0,0,image.width,image.height));return image
  return opened(path,*args,**kwargs)
 with patch.object(proof.Image,'open',black):rejected('actual_presented_scene_black',lambda:proof.verify('sonya',2))
OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,checks=checks,inMemoryOnly=True,actualRuntimeEvidenceChanged=False,fullPortAccepted=False),indent=2)+'\n');print('Eight counterexamples rejected; actual files unchanged')
