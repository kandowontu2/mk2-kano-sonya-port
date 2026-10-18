"""Current punch-ineligible commands, not exhaustive input-boundary testing."""
import hashlib
import json
import sys
from pathlib import Path
import zipfile
from verify_finisher_roms import verify
from nonlethal_profiles import profile

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest().upper()
cases=[]
names=sys.argv[1:]
assert len(names)==8 and len(set(names))==8,'Supply eight distinct completed current punch-ineligible fixtures'
for name in names:
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    result=json.loads((folder/'qualification.json').read_text())
    kind,actor,side,victim=profile(receipt['testArguments'],negative=True)
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert receipt['controllerSHA256']==sha(folder/'autoboot.lua')
    assert '--punch-wins' in receipt['testArguments'] and '--'+kind in receipt['testArguments']
    assert ('--mirror' in receipt['testArguments'])==(side==2)
    assert '--finisher-rejoin' not in receipt['testArguments']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
    assert result['actorID']==actor and result['physicalActorSide']==side
    assert result['victimID']==(18 if actor==17 else 17)
    assert result['frames']==9000 and result['naturalKnockouts']>=2
    assert result['nativeActionFields']==0 and not result['nativeCompletionObserved']
    gate='punchEligibilityRejected' if kind=='friend' else 'punchEligibilityRejectionObserved'
    assert result[gate] and result['currentFull26ROMBytesVerified']
    assert result['nativeIneligibleCommandObservedFrames']
    for name,digest in result['pins'].items():assert sha(Path(name))==digest
    cases.append(dict(run=folder.name,kind=kind,actor=actor,side=side,
        nativeCommandObservations=len(result['nativeIneligibleCommandObservedFrames']),
        qualificationSHA256=sha(folder/'qualification.json')))
assert {(r['kind'],r['actor'],r['side']) for r in cases}=={(k,a,s) for k in ('friend','baby') for a in (17,18) for s in (1,2)}
report=dict(scope='Both own nonlethal commands rejected after punch use on both sides',
    cases=cases,allEightPunchIneligibleCasesPassed=True,currentAll26ROMsVerified=True,
    exactInputTimingBoundariesVerified=False,allInvalidCommandsVerified=False,
    fullPortVerified=False,releaseReady=False,verifierSHA256=sha(Path(__file__)))
(PORT/'NEGATIVE_NONLETHAL_MATRIX_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
