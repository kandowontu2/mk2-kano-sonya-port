"""In-memory native-format counterexamples; immutable images stay untouched."""
import json
from pathlib import Path
from unittest.mock import patch
import verify_native_arm_blood_v1064 as proof
import build_native_projectile_impacts as codec

OUT=proof.ROOT/'audit_v1069_arm_blood_proof_units'
if OUT.exists():raise ValueError('Preserve proof evidence')
baseline=proof.verify();assert baseline['passed'],baseline['errors']
guest,graphics,assets=proof.reconstruct()
path=proof.ROOT/proof.CANDIDATE/'roms/mk2ks/mk2ks.mdata'
original_read=Path.read_bytes
current=original_read(path)
old=original_read(proof.ROOT/'diagnostic_v1048_owned_jax_arm_tables/roms/mk2ks/mk2ks.mdata')
checks=[]
def reject(name,payload):
 assert payload!=current
 def fake_read(target):return payload if target==path else original_read(target)
 with patch.object(Path,'read_bytes',fake_read):
  try:proof.reconstruct()
  except AssertionError as error:
   assert str(error)=='Independently encoded own source raster',str(error)
  else:raise AssertionError('Counterexample accepted: '+name)
 checks.append({'name':name,'rejectedByIndependentRasterReconstruction':True})
reject('old blue-blood raster restored',old)
graphic,asset=next((g,a) for g,a in assets.items() if a['fighter']=='kano' and a['kind']=='body' and a['pose']==0)
header=proof.struct.unpack_from('<4s15I',current,0x1c3000)
g=graphic//8-0x1f40000
at=header[1]+g if g<header[2] else header[3]+g-header[2]
red=asset['colors'][asset['indices']]
indices=asset['indices'].copy()
yy,xx=proof.np.where((indices!=0)&(red[:,:,0].astype(int)>red[:,:,2].astype(int)+20)&(indices!=48))
assert len(yy)>0 and not asset['bloodMask'].any()
indices[yy[0],xx[0]]=48
fixture=bytearray(current);packed=codec.pack_indices(indices.tobytes());fixture[at:at+len(packed)]=packed
reject('costume trim incorrectly remapped as blood',bytes(fixture))
indices=asset['indices'].copy();yy,xx=proof.np.where(indices==0);assert len(yy)>0
indices[yy[0],xx[0]]=48
fixture=bytearray(current);packed=codec.pack_indices(indices.tobytes());fixture[at:at+len(packed)]=packed
reject('transparent sprite boundary painted opaque',bytes(fixture))
assert original_read(path)==current
OUT.mkdir();report={'passed':True,'checks':checks,'corruptionChecks':len(checks),
 'evidenceFilesModified':False,'sourceSpritesModified':False,'fullPortAccepted':False}
(OUT/'unit-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
