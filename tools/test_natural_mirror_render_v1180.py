"""Focused in-memory negatives on the real current alternate Sonya render."""
import copy,io,json
from unittest.mock import patch
import verify_natural_mirror_finish_display_v1179 as proof
OUT=proof.ROOT/'audit_v1180_natural_mirror_render_corruption_checks'
assert not OUT.exists(),'Preserve negative evidence'
folder=proof.ROOT/'audit_v1177_sonya_mirror_finish_winner_p2_confirm_p1'
baseline=proof.state.split.reconstruct();real_data=proof.native.raster.data
observed=real_data(folder);results={}
def rejected(name,call):
 try:call()
 except (AssertionError,ValueError) as error:
  results[name]=dict(rejected=True,error=str(error));print(name+' rejected',flush=True)
 else:raise AssertionError(name+' was incorrectly accepted')
with patch.object(proof.state.split,'reconstruct',return_value=baseline):
 accepted=proof.verify('sonya',2);assert accepted['passed'];results['baseline']=dict(passed=True,replayedFrames=accepted['replayed']['frames'])
 print('Real naturally selected alternate Sonya render accepted',flush=True)
 for name in ('imported_graphics_byte_changed','foreign_physical_id','component_width_changed','single_orb_descriptor_changed','missing_native_retirement_store'):
  changed=copy.deepcopy(observed);groups=changed[0]
  if name=='imported_graphics_byte_changed':
   row=next(r for r in groups['FLOOR_GFX'] if 0xc00000<=r['first'] and r['first']+r['bytes']<=0x1e00000)
   raw=bytearray.fromhex(row['data']);raw[0]^=1;row['data']=raw.hex()
  elif name=='foreign_physical_id':next(r for r in groups['FLOOR_QUEUE'] if r['slot']==2)['id']=1
  elif name=='component_width_changed':next(r for r in groups['FLOOR_QUEUE_PART'] if r['slot']==2)['width']+=1
  elif name=='single_orb_descriptor_changed':
   row=groups['FLOOR_SINGLE_DESCRIPTOR'][0];raw=bytearray.fromhex(row['data']);raw[-1]^=1;row['data']=raw.hex()
  else:groups['FLOOR_POINTER_STORE'].pop()
  with patch.object(proof.native.raster,'data',return_value=changed):rejected(name,lambda:proof.verify('sonya',2))
 read=proof.Path.read_bytes;opened=proof.Image.open
 palette_file=folder/observed[0]['FLOOR_DISPLAY'][0]['palette_file']
 image_file=folder/'snap'/observed[0]['FLOOR_SNAP'][0]['file']
 for name,target in (('whole_initialized_guest_changed',folder/'guest_maincpu.bin'),('actual_full_palette_changed',palette_file)):
  def corrupt(path,selected=target):
   data=read(path)
   if path!=selected:return data
   altered=bytearray(data);altered[0x0300*4+4 if selected==palette_file else -1]^=1;return bytes(altered)
  with patch.object(proof.Path,'read_bytes',corrupt):rejected(name,lambda:proof.verify('sonya',2))
 def black(path,*args,**kwargs):
  if isinstance(path,(str,proof.Path)) and proof.Path(path)==image_file:
   # Deliberately invalid presented pixels exist only in memory for this
   # counterexample. No source art or captured PNG is changed on disk.
   image=opened(path).convert('RGB');image.paste((0,0,0),(0,0,image.width,image.height));return image
  return opened(path,*args,**kwargs)
 with patch.object(proof.Image,'open',black):rejected('actual_presented_pixels_black',lambda:proof.verify('sonya',2))
OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,checks=results,
 inMemoryOnly=True,actualRuntimeEvidenceChanged=False,fullPortAccepted=False),indent=2)+'\n')
print('Eight render counterexamples rejected; actual files unchanged')
