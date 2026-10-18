"""Explicit current-build finite special/side cases, not all-moveset approval."""
import hashlib
import csv
import json
from pathlib import Path
import sys
import zipfile
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest().upper()

def profile(arguments):
    mirror='--mirror' in arguments
    kinds=[name for name in ('projectiles','special','blade','choke','bike','leg') if '--'+name in arguments]
    assert len(kinds)==1, 'Exactly one fixture family required'
    kind=kinds[0]
    assert '--square' not in arguments or kind=='special'
    if kind=='projectiles':
        return kind,[(17,'knife',2 if mirror else 1),(18,'ring',1 if mirror else 2)]
    move=('square' if '--square' in arguments else 'ball') if kind=='special' else kind
    actor=17 if move in ('ball','blade','choke') else 18
    side=(2 if mirror else 1) if actor==17 else (1 if mirror else 2)
    return kind,[(actor,move,side)]

def qualify(names):
    assert len(names)==14 and len(set(names))==14, 'Supply fourteen distinct completed current-ROM fixtures'
    cases=[]
    for name in names:
        assert name and Path(name).name==name and '/' not in name and '\\' not in name
        folder=BASE/name
        receipt=json.loads((folder/'execution.json').read_text())
        proof=json.loads((folder/'qualification.json').read_text())
        assert receipt['exitCode']==0 and not receipt['timedOut']
        assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
        assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
        assert receipt['controllerSHA256']==sha(folder/'autoboot.lua')
        with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
        trace,entries=profile(receipt['testArguments'])
        with (folder/(trace+'.csv')).open() as stream:last=list(csv.DictReader(stream))[-1]
        assert int(last['frame'])==9000 and proof['currentFull26ROMBytesVerified']
        if 'frames' in proof:assert proof['frames']==9000
        for path,digest in proof['pins'].items():assert sha(Path(path))==digest
        for actor,move,side in entries:
            if trace=='projectiles':
                item=proof['moves']['kano' if actor==17 else 'sonya']
                assert item['side']==side and item['firstWrongDirectionRejected']
                assert item['ownProjectileIdentityAndArt'] and item['recoveryAndCleanupObserved']
            elif trace=='special':
                assert proof['actorID']==actor and proof['physicalSide']==side
                assert proof['negativeFirstAttemptRejected'] and proof['firstActivationHitAndReturnedToStance']
            else:assert proof['side']==side
            cases.append(dict(run=name,move=move,actor=actor,side=side,
                              qualificationSHA256=sha(folder/'qualification.json')))
    expected={(actor,move,side) for actor,moves in
              ((17,('knife','ball','blade','choke')),(18,('ring','square','bike','leg')))
              for move in moves for side in (1,2)}
    assert len(cases)==16 and {(r['actor'],r['move'],r['side']) for r in cases}==expected
    report=dict(scope='Eight own specials on both physical sides against the other own fighter',
        cases=cases,allSixteenFiniteCasesPassed=True,currentAll26ROMsVerified=True,
        allVictimsBossesEdgesInterruptionsVerified=False,nativeAudioMixVerified=False,
        fullPortVerified=False,releaseReady=False,verifierSHA256=sha(Path(__file__)))
    (PORT/'SPECIAL_MATRIX_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':print(json.dumps(qualify(sys.argv[1:])))
