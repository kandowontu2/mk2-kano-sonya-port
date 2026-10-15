"""Reject in-memory corruption without altering real mirror runtime evidence."""
import json,re
from unittest.mock import patch
import verify_natural_mirror_finish_v1169 as proof
OUT=proof.ROOT/'audit_v1171_natural_mirror_finish_corruption_checks'
assert not OUT.exists(),'Preserve negative checks'
baseline=proof.split.reconstruct()
texts={case:(proof.ROOT/case/'run.log').read_text(encoding='utf-8-sig') for case in proof.CASES}
case=proof.CASES[0];results={}
with patch.object(proof.split,'reconstruct',return_value=baseline):
 good=proof.verify(texts,check_files=False);assert good['passed'],good['errors'];results['baseline']={'passed':True,'cases':4}
 print('Four real baselines accepted',flush=True)
 for name,pattern,replace in (
  ('missing_native_alternate_assignment',r'^MK2_NATURAL_MIRROR_FINISH_V1166_FLAG_WRITE[^\n]*pc=FF895450[^\n]*\n',''),
  ('broken_native_damage_chain',r'(MK2_NATURAL_MIRROR_FINISH_V1166_HEALTH[^\n]*before=)161',r'\g<1>160'),
  ('foreign_physical_finisher_id',r'(MK2_NATURAL_MIRROR_FINISH_V1166_FINISH_FIFO[^\n]*actor=01034E90[^\n]*id=)17',r'\g<1>1'),
  ('missing_actual_last_button',r'^MK2_NATURAL_MIRROR_FINISH_V1166_INPUT[^\n]*frame=3132[^\n]*button=High_Kick[^\n]*\n',''),
  ('wrong_native_completion_owner',r'(MK2_NATURAL_MIRROR_FINISH_V1166_WRAP[^\n]*actor=)01034E90',r'\g<1>010350A0'),
 ):
  changed,count=re.subn(pattern,replace,texts[case],count=1,flags=re.M);assert count==1,name
  report=proof.verify({**texts,case:changed},check_files=False)
  assert not report['passed'] and report['errors'],name
  results[name]={'rejected':True,'errors':report['errors']};print(name+' rejected',flush=True)
 real_read=proof.Path.read_bytes
 for name,target in (
  ('whole_actual_guest_changed',proof.ROOT/case/'guest_maincpu.bin'),
  ('actual_alternate_hardware_palette_changed',proof.ROOT/proof.CASES[1]/'finish_palette_p2_020.bin'),
 ):
  def corrupt(path,selected=target):
   data=real_read(path)
   if path!=selected:return data
   altered=bytearray(data);altered[40 if 'palette' in selected.name else -1]^=1;return bytes(altered)
  with patch.object(proof.Path,'read_bytes',corrupt):report=proof.verify(texts,check_files=False)
  assert not report['passed'] and report['errors'],name
  results[name]={'rejected':True,'errors':report['errors']};print(name+' rejected',flush=True)
OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,checks=results,
 inMemoryOnly=True,actualRuntimeEvidenceChanged=False,fullPortAccepted=False),indent=2)+'\n')
print('Seven in-memory negatives rejected; actual runtime evidence unchanged')
