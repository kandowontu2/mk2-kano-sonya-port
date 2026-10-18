"""Eight current positive own-victim cases; not negative/all-cleanup proof."""
import hashlib
import json
import sys
from pathlib import Path
import zipfile
from verify_finisher_roms import verify
from finisher_observation_end import verify_end
from nonlethal_profiles import profile
from recovery_evidence import verify as verify_recovery_evidence

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest().upper()
cases=[]
names=sys.argv[1:]
assert len(names)==8 and len(set(names))==8,'Supply eight distinct completed current positive fixtures'
for name in names:
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    move=json.loads((folder/'qualification.json').read_text())
    rejoin=json.loads((folder/'FINISHER_REJOIN_QUALIFICATION.json').read_text())
    verify_recovery_evidence(folder,rejoin)
    kind,actor,side,victim=profile(receipt['testArguments'])
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['controllerSHA256']==sha(folder/'autoboot.lua')
    assert '--'+kind in receipt['testArguments'] and '--punch-wins' not in receipt['testArguments']
    assert ('--mirror' in receipt['testArguments'])==(side==2)
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
    assert move['actorID']==actor and move['physicalActorSide']==side and move['victimID']==victim
    assert move['nativeCompletionObserved'] and move['currentFull26ROMBytesVerified']
    expected=192 if kind=='baby' else (193 if actor==17 else 176)
    assert move['nativeActionFields']==expected
    assert rejoin['kind']==kind and rejoin['performerSide']==side
    verify_end(folder,receipt,move['frames'])
    assert rejoin['actualHardwarePaletteRGBVerified'] and rejoin['freshMatchPaletteColorComparisons']==78000
    for name,digest in move['pins'].items():assert sha(Path(name))==digest
    if kind=='baby':assert rejoin['observedBabyImageAbsentFromFreshActiveList']
    if kind=='friend' and actor==18:
        lifecycle=json.loads((folder/'FRIEND_LIFECYCLE_QUALIFICATION.json').read_text())
        for name,digest in lifecycle['evidenceSHA256'].items():assert sha(Path(name))==digest
        assert lifecycle['noChickenCommandsAfterSelection']
        assert lifecycle['danceContextAbsentFromSelectionThrough600FreshCombatFields']
    cases.append(dict(run=folder.name,kind=kind,actor=actor,side=side,victim=victim,
        nativeActionFields=expected,freshCombatFields=rejoin['freshCombatFields'],
        qualificationSHA256=sha(folder/'qualification.json'),rejoinSHA256=sha(folder/'FINISHER_REJOIN_QUALIFICATION.json')))
assert {(r['kind'],r['actor'],r['side']) for r in cases}=={(k,a,s) for k in ('friend','baby') for a in (17,18) for s in (1,2)}
report=dict(scope='Both own Friendships/Babalities, both sides, other own victim only',
    cases=cases,currentAll26ROMsVerified=True,allEightPositiveCasesPassed=True,
    currentNegativeEligibilityVerified=False,arbitraryVictimCoverage=False,
    allCleanupAndAudioVerified=False,fullPortVerified=False,releaseReady=False,
    verifierSHA256=sha(Path(__file__)),recoveryEvidenceVerifierSHA256=sha(PORT/'recovery_evidence.py'))
(PORT/'NONLETHAL_MATRIX_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
