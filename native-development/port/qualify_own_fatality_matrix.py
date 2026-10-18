"""Explicit current-byte own-victim matrix; never whole-port acceptance."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from verify_finisher_roms import verify
from finisher_observation_end import verify_end
from recovery_evidence import verify as verify_recovery_evidence

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest().upper()

def profile(arguments):
    kinds=[kind for kind in ('extract','laser','kiss','bubble') if '--'+kind in arguments]
    assert len(kinds)==1 and '--finisher-rejoin' in arguments
    assert '--negative' not in arguments
    kind=kinds[0]
    return kind,2 if '--mirror' in arguments else 1,18 if kind in ('extract','laser') else 17

def qualify(names):
    assert len(names)==8 and len(set(names))==8,'Supply eight distinct completed current-ROM fixtures'
    cases=[]
    for name in names:
        assert name and Path(name).name==name and '/' not in name and '\\' not in name
        folder=BASE/name
        receipt=json.loads((folder/'execution.json').read_text())
        move=json.loads((folder/'qualification.json').read_text())
        rejoin=json.loads((folder/'FINISHER_REJOIN_QUALIFICATION.json').read_text())
        verify_recovery_evidence(folder,rejoin)
        kind,side,victim=profile(receipt['testArguments'])
        assert receipt['exitCode']==0 and not receipt['timedOut']
        assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
        assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
        assert receipt['controllerSHA256']==sha(folder/'autoboot.lua')
        with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:verify(archive,receipt)
        assert move['side']==side and move['victimID']==victim
        assert move['nativeCompletionObserved'] and move['currentFull26ROMBytesVerified']
        assert move['nativeActionFields']==(231 if kind in ('extract','kiss') else 176)
        assert rejoin['kind']==kind and rejoin['performerSide']==side
        verify_end(folder,receipt,move['frames'])
        assert rejoin['actualHardwarePaletteRGBVerified'] and rejoin['freshMatchPaletteColorComparisons']==78000
        for path,digest in move['pins'].items():assert sha(Path(path))==digest
        if kind in ('laser','bubble'):
            assert move[('beam' if kind=='laser' else 'bubble')+'ObjectAndDummyProcessRetired']
            assert rejoin['trackedEffectObjectAndProcessAbsentAtCompletion']
        cases.append(dict(run=name,kind=kind,side=side,victim=victim,
            nativeActionFields=move['nativeActionFields'],freshCombatFields=rejoin['freshCombatFields'],
            qualificationSHA256=sha(folder/'qualification.json'),rejoinSHA256=sha(folder/'FINISHER_REJOIN_QUALIFICATION.json')))
    assert {(r['kind'],r['side']) for r in cases}=={(k,s) for k in ('extract','laser','kiss','bubble') for s in (1,2)}
    report=dict(scope='Four own fatalities, two player sides, other own victim only',
        cases=cases,currentAll26ROMsVerified=True,allEightCasesPassed=True,
        arbitraryVictimCoverage=False,allCleanupAndAudioVerified=False,
        fullPortVerified=False,releaseReady=False,verifierSHA256=sha(Path(__file__)),
        recoveryEvidenceVerifierSHA256=sha(PORT/'recovery_evidence.py'))
    (PORT/'OWN_FATALITY_MATRIX_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':print(json.dumps(qualify(sys.argv[1:])))
