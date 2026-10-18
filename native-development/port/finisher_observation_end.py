"""Accept bounded observation only with a separately pinned fresh-match proof."""
import hashlib
import json
from pathlib import Path

def verify_end(run,execution,frame):
    if '--finisher-rejoin' not in execution['testArguments']:
        assert frame==9000
        return
    proof=json.loads((run/'FINISHER_REJOIN_QUALIFICATION.json').read_text())
    assert proof['run']==run.name and proof['freshCombatFields']==600
    for gate in ('currentFull26ROMBytesVerified','ownIdentitiesPreserved',
                 'fullStartingHealth','combatDamageObserved','noTrackedFinisherChild',
                 'deathAndWinnerStateReset'):
        assert proof[gate],gate
    assert proof['observerSHA256']==execution['controllerSHA256']
    required={run/'execution.json',run/'autoboot.lua',run/(proof['kind']+'.csv'),
              Path(__file__).parent/'qualify_finisher_rejoin.py'}
    assert {str(path) for path in required}<=set(proof['evidenceSHA256'])
    for name,digest in proof['evidenceSHA256'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest().upper()==digest
    assert frame==proof['freshMatchFrame']+599
