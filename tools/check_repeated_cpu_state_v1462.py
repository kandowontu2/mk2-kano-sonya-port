"""Preserve initial repeated-state model result without editing evidence."""
import json
from pathlib import Path
import verify_repeated_sonya_cpu_v1461 as model
import verify_native_grab_audio_v1415 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1462_repeated_cpu_initial_state'
if __name__=='__main__':
 assert not OUT.exists()
 folder=ROOT/'audit_v1460_sonya_cpu_repeated_kano_p1'
 proof=model.verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),'kano')
 pins={str(p):source.prior.digest(p)for p in folder.rglob('*')if p.is_file()}
 for p in (Path(__file__),Path(model.__file__)):pins[str(p.resolve())]=source.prior.digest(p)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(candidate=source.NAME,passed=proof['passed'],proof=proof,inputHashes=pins,fullPortAccepted=False),indent=2)+'\n')
 print(dict(passed=proof['passed'],errors=proof['errors']))
