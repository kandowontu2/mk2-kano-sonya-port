"""Preserve the first explicit-physical-role model result, including failures."""
import json
from pathlib import Path
import verify_physical_p2_cpu_pair_v1440 as model
import verify_native_grab_audio_v1415 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1441_physical_p2_cpu_state'
if __name__=='__main__':
 assert not OUT.exists()
 cases={p:model.verify_log((ROOT/f'audit_v1439_cpu_sonya_p2_human_{p}/run.log').read_text(encoding='utf-8-sig'),p) for p in ('kano','sonya')}
 pins={str(p):source.prior.digest(p) for p in (Path(__file__),Path(model.__file__))}
 for player in cases:
  for path in (ROOT/f'audit_v1439_cpu_sonya_p2_human_{player}').rglob('*'):
   if path.is_file():pins[str(path)]=source.prior.digest(path)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=all(p['passed']for p in cases.values()),candidate=source.NAME,cases=cases,inputHashes=pins,fullPortAccepted=False),indent=2)+'\n')
 print(json.dumps({p:dict(passed=r['passed'],errors=r['errors'])for p,r in cases.items()},indent=2))
