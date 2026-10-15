"""In-memory counterexamples only; never alter accepted images or game state."""
import json
import re
from pathlib import Path
import numpy as np
import verify_arm_rng_differential_v1087 as proof

ROOT=proof.ROOT;OUT=ROOT/'audit_v1089_arm_rng_proof_units'
if OUT.exists():raise ValueError('Preserve counterexample evidence')
report=ROOT/'audit_v1087_arm_rng_differential_checked/report.json'
assert json.loads(report.read_text())['passed']
path=ROOT/'audit_v1086_jax_kano_p1_new_rng/run.log'
text=path.read_text(encoding='utf-8-sig');pins={str(path):proof.normal.digest(path),str(report):proof.normal.digest(report)}
tests=[]

def rejects(label,fn):
    try:fn()
    except AssertionError:tests.append(label)
    else:raise AssertionError('Counterexample accepted: '+label)

proof.rng(text)
beam=next(l for l in text.splitlines() if l.startswith('MK2_ARM_RNG_V1085_HCOUNT ') and 'serial=89 'in l)
broken=re.sub(r'count=[0-9A-F]+','count=0000',beam)
rejects('Changed actual HCOUNT without matching original RNG result',lambda:proof.rng(text.replace(beam,broken,1)))
entry=next(l for l in text.splitlines() if l.startswith('MK2_ARM_RNG_V1085_ENTRY ') and 'serial=89 'in l)
broken=re.sub(r'seed=[0-9A-F]+','seed=00000000',entry)
rejects('Changed seed before original shift/carry',lambda:proof.rng(text.replace(entry,broken,1)))

def altered_fighter():
    original=proof.nonblood(text)
    fighter=next(l for l in text.splitlines() if l.startswith('MK2_ARM_RNG_V1085_FIFO ') and 'id=11 'in l)
    value=int(re.search(r' x=(-?\d+)',fighter)[1])
    broken=re.sub(r' x=-?\d+',f' x={value+1}',fighter)
    assert original==proof.nonblood(text.replace(fighter,broken,1))
rejects('One-pixel true fighter shift',altered_fighter)
a=np.zeros((254,400,3),dtype=np.uint8);b=a.copy();b[0,0]=255
rejects('Unrelated image pixel outside actual blood coverage',lambda:proof.require_blood_only(a,b,np.zeros((254,400),dtype=bool)))
for path,wanted in pins.items():assert proof.normal.digest(Path(path))==wanted
OUT.mkdir();result={'passed':True,'corruptionChecks':len(tests),'rejected':tests,
                  'filesModifiedByFixtures':False,'inputHashes':pins,'fullPortAccepted':False}
(OUT/'unit-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='inputHashes'},indent=2))
