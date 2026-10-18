"""Eight explicit current transformed-fatality recovery cases; not full-port proof."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from verify_finisher_roms import verify

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()

def qualify(names):
    assert len(names)==8 and len(set(names))==8,'Supply eight distinct explicit completed runs'
    cases=[]
    for name in names:
        assert name and Path(name).name==name and '/' not in name and '\\' not in name
        folder=BASE/name
        receipt=json.loads((folder/'execution.json').read_text())
        args=receipt['testArguments']
        assert '--finisher-morph' in args and '--finisher-rejoin' in args
        kinds=[kind for kind in ('extract','kiss','laser','bubble') if '--'+kind in args]
        assert len(kinds)==1
        kind=kinds[0];side=2 if '--mirror' in args else 1
        actor=17 if kind in ('extract','laser') else 18
        assert receipt['exitCode']==0 and not receipt['timedOut']
        assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
        assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
        assert receipt['controllerSHA256']==sha(folder/'autoboot.lua')
        with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
        detail=json.loads((folder/'qualification.json').read_text())
        recovery=json.loads((folder/'FINISHER_REJOIN_QUALIFICATION.json').read_text())
        assert detail['currentFull26ROMBytesVerified'] and detail['nativeCompletionObserved']
        assert detail['transformedFinisher'] and detail['selectedCharacter']==6 and detail['activeFinisherCharacter']==actor
        assert recovery['run']==name and recovery['kind']==kind and recovery['performerSide']==side
        assert recovery['transformedFinisher'] and recovery['freshSelectedCharacter']==6 and recovery['freshCombatFields']==600
        for gate in ('currentFull26ROMBytesVerified','ownIdentitiesPreserved','fullStartingHealth',
                     'combatDamageObserved','noTrackedFinisherChild','deathAndWinnerStateReset',
                     'observedOldEffectShapesAbsentFromActiveObjectList','originalPaletteSourcesRestoredFirst60Fields',
                     'actualHardwarePaletteRGBVerified'):
            assert recovery[gate],gate
        assert recovery['verifierSHA256']==sha(PORT/'qualify_finisher_rejoin.py')
        for pins in (detail['pins'],recovery['evidenceSHA256']):
            assert all(sha(Path(path))==digest for path,digest in pins.items())
        cases.append(dict(run=name,kind=kind,side=side,activeFinisherCharacter=actor,
                          freshCombatFields=600,paletteComparisons=recovery['freshMatchPaletteColorComparisons'],
                          detailSHA256=sha(folder/'qualification.json'),recoverySHA256=sha(folder/'FINISHER_REJOIN_QUALIFICATION.json')))
    assert {(c['kind'],c['side']) for c in cases}=={(k,s) for k in ('extract','kiss','laser','bubble') for s in (1,2)}
    report=dict(scope='Finite both-sided transformed lethal fatalities followed by physical fresh-Shang matches',
                cases=cases,allEightCasesPassed=True,allActual26ROMsVerified=True,
                allObjectsAudioAndInteractionsVerified=False,fullPortVerified=False,releaseReady=False,
                verifierSHA256=sha(Path(__file__)))
    (PORT/'MORPH_FINISHER_REJOIN_MATRIX_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':print(json.dumps(qualify(sys.argv[1:]),indent=2))
