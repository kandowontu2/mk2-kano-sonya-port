"""In-memory malformed mirror evidence must fail unchanged current predicates."""
import json,re
from pathlib import Path
import verify_current_natural_mirror_finish_v1674 as check
ROOT=check.ROOT;OUT=ROOT/'audit_v1681_current_mirror_finish_negative_checks'
def mutate(log,tag,field,value):
 pattern=r'(^MK2_NATURAL_MIRROR_FINISH_V1166_'+tag+r' [^\n]*)'
 def change(match):
  line,count=re.subn(r'\b'+field+r'=\S+',lambda m:field+'='+value,match[0],count=1)
  assert count==1;return line
 result,count=re.subn(pattern,change,log,count=1,flags=re.M)
 assert count==1 and result!=log
 return result
if __name__=='__main__':
 assert not OUT.exists()
 proof=ROOT/'audit_v1674_current_natural_mirror_finish_checked/report.json'
 accepted=json.loads(proof.read_text());assert accepted['passed']
 texts={case:(ROOT/case/'run.log').read_text(encoding='utf-8-sig')for case in check.CASES}
 before={case:check.digest(ROOT/case/'run.log')for case in check.CASES}
 target=check.CASES[0];rejected=[]
 for label,tag,field,value in (
  ('proxy_live_identity','FIRST_LIVE','ids','1,17'),
  ('lost_alternate_costume','FIRST_LIVE','flags','0012,0012'),
  ('wrong_finisher_entry','ACTION','address','FFFAB200'),
  ('assisted_health_store','HEALTH','pc','FF800000'),
  ('wrong_wrap_timing','WRAP','age','234'),
  ('cache_overrun','RESULT','cache_errors','1')):
  changed=dict(texts);changed[target]=mutate(texts[target],tag,field,value)
  report=check.verify(texts=changed,check_files=False)
  assert not report['passed'],label+' escaped unchanged predicates'
  rejected.append(dict(label=label,errors=report['errors']))
  print(label+' rejected',flush=True)
 assert before=={case:check.digest(ROOT/case/'run.log')for case in check.CASES}
 pins={str(proof):check.digest(proof),str(Path(__file__)):check.digest(Path(__file__)),str(Path(check.__file__)):check.digest(Path(check.__file__))}
 pins.update({str(ROOT/case/'run.log'):value for case,value in before.items()})
 report=dict(passed=True,rejectedInMemoryCorruptions=rejected,actualCapturesUnmodified=True,acceptancePredicatesUnmodified=True,inputHashes=pins,fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
