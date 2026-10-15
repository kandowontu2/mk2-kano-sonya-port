"""In-memory negative checks of real native hat-kill evidence, no file edits."""
import io,json,re
from unittest.mock import patch
import verify_native_hat_kill_v1158 as verifier
OUT=verifier.ROOT/'audit_v1160_native_hat_corruption_checks'
if OUT.exists():raise ValueError('Preserve corruption evidence')
baseline=verifier.split.reconstruct()
texts={case:(verifier.ROOT/case/'run.log').read_text(encoding='utf-8-sig') for case in verifier.CASES+verifier.CONTROLS}
results={};case=verifier.CASES[0]
with patch.object(verifier.split,'reconstruct',return_value=baseline):
 good=verifier.verify(texts,check_files=False);assert good['passed'],good['errors']
 results['baseline']={'passed':True,'cases':len(good['cases'])};print('Six real current baselines accepted',flush=True)
 for name,pattern,replace in (
  ('missing_up_field',r'^MK2_STOCK_HEAD_V921_INPUT[^\n]*button=Up[^\n]*\n',''),
  ('outside_original_head_height',r'(MK2_HAT_V1155_STATE[^\n]*at=FFA16CB0[^\n]* a1=)[0-9A-F]+',r'\g<1>00000060'),
  ('foreign_victim_at_native_kill',r'(MK2_HAT_V1155_STATE[^\n]*at=FFA16CB0[^\n]* id=)17',r'\g<1>1'),
  ('missing_native_success_write',r'^MK2_HAT_V1155_SUCCESS_WRITE[^\n]*new=65535[^\n]*\n',''),
  ('foreign_separate_head_cache',r'(MK2_ROLLING_HEAD_V1003_QUEUE[^\n]*source=0F62B0A0[^\n]* cache=)[0-9A-F]+',r'\g<1>FFFD5000'),
 ):
  changed,count=re.subn(pattern,replace,texts[case],count=1,flags=re.M);assert count==1,name
  result=verifier.verify({**texts,case:changed},check_files=False)
  assert not result['passed'] and result['errors'],name+' must be rejected'
  results[name]={'rejected':True,'errors':result['errors']};print(name+' rejected',flush=True)
 real_bytes=verifier.Path.read_bytes;actual_open=verifier.Image.open
 selected_picture=verifier.Path(good['cases'][case]['pixelMatches'][1]['picture'])
 for name,target,typ in (
  ('whole_guest_byte_changed',verifier.ROOT/case/'guest_maincpu.bin','guest'),
  ('initialized_gfx_byte_changed',verifier.ROOT/case/'native_death_gfx.bin','gfx'),
  ('actual_presented_body_black',selected_picture,'png'),
 ):
  def corrupt(path,selected=target,kind=typ):
   data=real_bytes(path)
   if path!=selected:return data
   if kind=='png':
    image=actual_open(io.BytesIO(data)).convert('RGB');image.paste((0,0,0),(0,0,image.width,image.height))
    buffer=io.BytesIO();image.save(buffer,format='PNG');return buffer.getvalue()
   changed=bytearray(data);changed[-1]^=1;return bytes(changed)
  if typ=='png':
   def opened(path,*args,**kwargs):
    if isinstance(path,(str,verifier.Path)) and verifier.Path(path)==target:return actual_open(io.BytesIO(corrupt(target)),*args,**kwargs)
    return actual_open(path,*args,**kwargs)
   with patch.object(verifier.Path,'read_bytes',corrupt),patch.object(verifier.Image,'open',opened):result=verifier.verify(texts,check_files=False)
  else:
   with patch.object(verifier.Path,'read_bytes',corrupt):result=verifier.verify(texts,check_files=False)
  assert not result['passed'] and result['errors'],name+' must be rejected'
  results[name]={'rejected':True,'errors':result['errors']};print(name+' rejected',flush=True)
OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,checks=results,inMemoryOnly=True,
 baselineReconstruction='Independent v1133 exact current reconstruction cached unchanged only for repeated runtime counterexamples',
 actualRuntimeEvidenceChanged=False,scope='Six current native hat baselines and eight focused corruption checks',fullPortAccepted=False),indent=2)+'\n')
print(json.dumps(dict(passed=True,negativeChecks=len(results)-1,actualEvidenceChanged=False)))
