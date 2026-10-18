"""Finite own-pair stage cases; not exhaustive chord/victim/audio acceptance."""
import csv
import hashlib
import json
import sys
from pathlib import Path
import zipfile
from verify_finisher_roms import verify
from stage_profiles import profile

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest().upper()
cases=[]
names=sys.argv[1:]
assert len(names)==16 and len(set(names))==16,'Supply sixteen distinct completed current stage fixtures'
catalog=[]
for name in names:
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    folder=BASE/name
    args=json.loads((folder/'execution.json').read_text())['testArguments']
    catalog.append((folder,profile(args)))
assert len([1 for _,p in catalog if p[0] in ('deadpool','tomb')])==8
assert len([1 for _,p in catalog if p[0]=='negative'])==4
assert len([1 for _,p in catalog if p[0]=='pit'])==4
for folder,(kind,actor,side) in catalog:
    if kind not in ('deadpool','tomb'):continue
    receipt=json.loads((folder/'execution.json').read_text())
    deadpool=kind=='deadpool'
    proof_path=folder/('DEADPOOL_QUALIFICATION.json' if deadpool else 'qualification.json')
    proof=json.loads(proof_path.read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['controllerSHA256']==sha(folder/'autoboot.lua')
    assert ('--mirror' in receipt['testArguments'])==(side==2)
    assert ('--sonya' in receipt['testArguments'])==(actor==18)
    assert '--stage' in receipt['testArguments'] and '--own-victim' in receipt['testArguments']
    assert ('--deadpool' in receipt['testArguments'])==deadpool
    assert '--deadpool-no-chord' not in receipt['testArguments']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
    assert proof['currentFull26ROMBytesVerified'] and proof['nativeCompletionObserved']
    for name,digest in proof['pins'].items():assert sha(Path(name))==digest
    with (folder/'stage.csv').open() as stream:last=list(csv.DictReader(stream))[-1]
    assert int(last['frame'])==(9000 if deadpool else 18000)
    if deadpool:
        assert proof['actor']==actor and proof['performerPlayer']==side
        assert proof['victim']==(18 if actor==17 else 17)
        assert proof['naturalKnockouts']==2 and proof['nativeSlimeFallObserved']
        assert proof['ownVisibleVictimArtVerified'] and not proof['chordNegativeRejected']
    else:
        assert proof['actorID']==actor and proof['physicalActorSide']==side
        assert proof['victimID']==(18 if actor==17 else 17)
        assert proof['naturalKnockouts']==4 and proof['nativeSpikeFields']==64
        assert proof['initialDeadPoolStageCommandRejected'] and proof['originalStageGatePreserved']
    cases.append(dict(run=folder.name,stage='deadpool' if deadpool else 'tomb',
        actor=actor,side=side,qualificationSHA256=sha(proof_path)))
negative_cases=[]
for folder,(kind,actor,side) in catalog:
    if kind!='negative':continue
    receipt=json.loads((folder/'execution.json').read_text())
    proof_path=folder/'DEADPOOL_QUALIFICATION.json'
    proof=json.loads(proof_path.read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert receipt['controllerSHA256']==sha(folder/'autoboot.lua')
    assert '--deadpool-no-chord' in receipt['testArguments']
    assert ('--mirror' in receipt['testArguments'])==(side==2)
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
    for name,digest in proof['pins'].items():assert sha(Path(name))==digest
    assert proof['currentFull26ROMBytesVerified'] and proof['actor']==actor
    assert proof['performerPlayer']==side and proof['naturalKnockouts']==2
    assert proof['finishWindowUppercutFrames'] and proof['nativeVictimHitReactionObserved']
    assert proof['ordinaryRoundResultObserved'] and proof['chordNegativeRejected']
    assert not proof['nativeCompletionObserved'] and not proof['nativeSlimeFallObserved']
    negative_cases.append(dict(run=folder.name,actor=actor,side=side,qualificationSHA256=sha(proof_path)))
pit_cases=[]
for folder,(kind,actor,side) in catalog:
    if kind!='pit':continue
    receipt=json.loads((folder/'execution.json').read_text())
    cinematic=json.loads((folder/'qualification.json').read_text())
    cleanup=json.loads((folder/'cleanup_qualification.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert receipt['controllerSHA256']==sha(folder/'autoboot.lua')
    assert ('--mirror' in receipt['testArguments'])==(side==2)
    assert '--pit-progress' in receipt['testArguments'] and '--pit-rejoin' in receipt['testArguments']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
    for proof in (cinematic,cleanup):
        for name,digest in proof['pins'].items():assert sha(Path(name))==digest
        assert proof['actorID']==actor and proof['physicalActorSide']==side
        assert proof['victimID']==(18 if actor==17 else 17)
    assert cinematic['currentFull26ROMBytesVerified'] and cinematic['naturalRoundKnockouts']==14
    assert cinematic['backgroundVisits']==list(range(7)) and cinematic['nativeCompletionObserved']
    assert cinematic['nativePitActionFields']==(206 if side==1 else 205)
    assert cinematic['ownFallFields']==58 and cinematic['ownImpactObservedFields']==241
    assert cinematic['allFiveOwnFallPosesAndImpactObserved']
    assert cleanup['nextMatchObservedFields']==601 and cleanup['freshMatchStartedWithFullHealth']
    assert cleanup['actualCombatDamageObserved'] and cleanup['noRetainedPitDrawingShapes']
    pit_cases.append(dict(run=folder.name,actor=actor,side=side,
        qualificationSHA256=sha(folder/'qualification.json'),cleanupSHA256=sha(folder/'cleanup_qualification.json')))
assert {(r['stage'],r['actor'],r['side']) for r in cases}=={(k,a,s) for k in ('deadpool','tomb') for a in (17,18) for s in (1,2)}
for group in (negative_cases,pit_cases):
    assert {(r['actor'],r['side']) for r in group}=={(a,s) for a in (17,18) for s in (1,2)}
report=dict(scope='Finite own-pair stage cases on both sides: Dead Pool/Tomb, missing chord, Pit/rejoin',
    cases=cases,allEightPositiveCasesPassed=True,currentAll26ROMsVerified=True,
    missingChordCases=negative_cases,allFourMissingChordCasesPassed=True,
    pitCases=pit_cases,allFourOwnPairPitCasesPassed=True,allChordsVictimsEdgesAndCleanupVerified=False,
    fullPortVerified=False,releaseReady=False,verifierSHA256=sha(Path(__file__)))
(PORT/'STAGE_POSITIVE_MATRIX_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
