"""In-memory counterexamples against complete secondary rendering checks."""
import copy,json
from unittest.mock import patch
import verify_stock_secondary_display_v1232 as proof
OUT=proof.ROOT/'audit_v1233_stock_secondary_render_corruption_checks';assert not OUT.exists()
folder=proof.ROOT/'audit_v1230_secondary_sonya_p2';real_data=proof.raster.data
observed=real_data(folder);expected=proof.physical.headed.reconstruct();checks={}

def rejected(name,call):
 try:call()
 except (AssertionError,ValueError) as error:
  checks[name]=dict(rejected=True,error=str(error));print(name+' rejected',flush=True)
 else:raise AssertionError(name+' incorrectly accepted')

with patch.object(proof.physical.headed,'reconstruct',return_value=expected):
 result=proof.verify('sonya_p2');assert result['passed']
 checks['baseline']=dict(passed=True,replayedFields=result['replayed']['frames'])
 for name in ('owned_torso_source_byte_changed','foreign_physical_victim_id','native_component_width_changed',
              'actual_actor_facing_changed','native_retirement_store_missing','foreign_detached_torso_id','detached_allocation_missing'):
  changed=copy.deepcopy(observed);groups=changed[0]
  if name=='owned_torso_source_byte_changed':
   row=next(r for r in groups['FLOOR_GFX'] if 0x1f20000<=r['first']<0x1f40000)
   raw=bytearray.fromhex(row['data']);raw[0]^=1;row['data']=raw.hex()
  elif name=='foreign_physical_victim_id':next(q for q in groups['FLOOR_QUEUE'] if q['slot']==2)['id']=1
  elif name=='native_component_width_changed':next(q for q in groups['FLOOR_QUEUE_PART'] if q['slot']==4)['width']+=1
  elif name=='actual_actor_facing_changed':next(q for q in groups['FLOOR_QUEUE'] if q['slot']==4)['facing']^=16
  elif name=='native_retirement_store_missing':groups['FLOOR_POINTER_STORE'].pop()
  elif name=='foreign_detached_torso_id':groups['FLOOR_DETACHED_LINK'][0]['id']=1
  else:groups['FLOOR_DETACHED_ALLOC'].clear()
  with patch.object(proof.raster,'data',return_value=changed):rejected(name,lambda:proof.verify('sonya_p2'))
 read=proof.Path.read_bytes;guest_file=folder/'guest_maincpu.bin'
 def corrupt(path):
  raw=read(path)
  if path!=guest_file:return raw
  altered=bytearray(raw);altered[-1]^=1;return bytes(altered)
 with patch.object(proof.Path,'read_bytes',corrupt):rejected('whole_actual_guest_changed',lambda:proof.verify('sonya_p2'))
 groups=observed[0]
 display=next(d for d in groups['FLOOR_DISPLAY'] if any(q['slot']==4 and q['frame']==d['frame']-1 for q in groups['FLOOR_QUEUE']))
 torso=next(q for q in groups['FLOOR_QUEUE'] if q['slot']==4 and q['frame']==display['frame']-1)
 palette_file=folder/display['palette_file'];actual_fromfile=proof.np.fromfile
 def recolor(path,*args,**kwargs):
  values=actual_fromfile(path,*args,**kwargs)
  if proof.Path(path)==palette_file:values=values.copy();values[(torso['bank']&0x7f00)+1]^=1
  return values
 with patch.object(proof.np,'fromfile',recolor):rejected('actual_torso_palette_changed',lambda:proof.verify('sonya_p2'))
 opened=proof.Image.open;image_file=folder/'snap'/groups['FLOOR_SNAP'][0]['file']
 def black(path,*args,**kwargs):
  if isinstance(path,(str,proof.Path)) and proof.Path(path)==image_file:
   image=opened(path).convert('RGB');image.paste((0,0,0),(0,0,image.width,image.height));return image
  return opened(path,*args,**kwargs)
 with patch.object(proof.Image,'open',black):rejected('actual_presented_scene_black',lambda:proof.verify('sonya_p2'))
OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,checks=checks,inMemoryOnly=True,
 actualRuntimeEvidenceChanged=False,fullPortAccepted=False),indent=2)+'\n')
print('Ten rendering/ownership/source counterexamples rejected; actual files unchanged',flush=True)
