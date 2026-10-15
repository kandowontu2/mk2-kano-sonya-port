"""Preserve genuine repeated-grab evidence; do not label it ordinary follow-up."""
import json
from pathlib import Path
import verify_physical_p1_cpu_pair_v1448 as model
import verify_native_grab_audio_v1415 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1450_physical_p1_repeated_grab_pending'
if __name__=='__main__':
 assert not OUT.exists()
 folder=ROOT/'audit_v1446_cpu_p1_boot605_human_kano'
 log=(folder/'run.log').read_text(encoding='utf-8-sig')
 proof=model.verify_log(log,'kano')
 assert not proof['passed'],'A second full paired action must not be called ordinary'
 entries=model.rows(log,'ENTRY');events=model.rows(log,'EVENT');terminal=model.rows(log,'RESULT')
 assert len(entries)==2 and all(r['id']==18 and r['vid']==17 for r in entries)
 second=[r for r in events if r['cycle']==2]
 assert len([r for r in second if r['kind']=='step'])==5
 assert len([r for r in second if r['kind']=='own_regain'])==1
 assert not any(r['kind']=='victim_regain'for r in second)
 pins={str(path):source.prior.digest(path)for path in folder.rglob('*')if path.is_file()}
 for path in (Path(__file__),Path(model.__file__)):pins[str(path.resolve())]=source.prior.digest(path)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,candidate=source.NAME,ordinaryFollowupCorrectlyRejected=True,ordinaryModelResult=proof,
  actualEntries=entries,actualSecondActionEvents=second,terminal=terminal,secondVictimRecoveryNotYetObserved=True,
  nextAction='Extend a successor input-only capture through the second actual victim handoff; verify both full pairs and native scanouts without relabelling either action.',
  inputHashes=pins,CPUAccepted=False,fullPortAccepted=False),indent=2)+'\n')
 print('Actual repeated Sonya CPU leg contact preserved; second victim handoff needs longer capture, not ordinary-profile relaxation.',flush=True)
