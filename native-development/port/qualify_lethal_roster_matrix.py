"""Require exact earned-lethal coverage and unchanged per-case proof bindings."""
import hashlib
import json
from pathlib import Path
import sys
from run_lethal_victim_matrix import plan
from inspect_normal_runtime import BASE, PORT


def validate_coverage(cases,pilot=False,kind=None):
    actual=[(r['run'],r['kind'],r['victim'],r['side']) for r in cases]
    expected={(name,k,victim,side) for name,k,victim,side,_ in plan(pilot) if kind is None or k==kind}
    assert expected
    assert len(actual)==len(set(actual)) and set(actual)==expected, 'Incomplete or duplicate coverage'


def main(pilot=False,kind=None):
    assert kind is None or kind in ('extract','laser','kiss','bubble')
    fixtures=[r for r in plan(pilot) if kind is None or r[1]==kind]
    index=PORT/('LETHAL_ROSTER_PILOT_2219.json' if pilot else 'LETHAL_ROSTER_2219.json')
    if kind is None:
        data=json.loads(index.read_text())
        assert data['pilot']==pilot
        validate_coverage(data['cases'],pilot)
    hashes={}
    def digest(path):
        path=Path(path)
        if path not in hashes:
            checksum=hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda:stream.read(65536),b''):checksum.update(chunk)
            hashes[path]=checksum.hexdigest().upper()
        return hashes[path]
    cases=[]
    for name,move_kind,victim,side,args in fixtures:
        run=BASE/name
        receipt=json.loads((run/'execution.json').read_text())
        assert receipt['testArguments']==args and receipt['exitCode']==0 and not receipt['timedOut']
        assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
        assert receipt['controllerSHA256']==digest(run/'autoboot.lua')
        move=json.loads((run/'qualification.json').read_text())
        fresh=json.loads((run/'FINISHER_REJOIN_QUALIFICATION.json').read_text())
        assert move['side']==side and move['victimID']==victim
        assert move['nativeCompletionObserved'] and move['currentFull26ROMBytesVerified']
        assert fresh['kind']==move_kind and fresh['performerSide']==side
        assert fresh['freshCombatFields']==600 and fresh['currentFull26ROMBytesVerified']
        for field in ('ownIdentitiesPreserved','fullStartingHealth','combatDamageObserved',
                      'noTrackedFinisherChild','deathAndWinnerStateReset','actualHardwarePaletteRGBVerified'):
            assert fresh[field],(name,field)
        for pins in (move['pins'],fresh['evidenceSHA256']):
            assert all(digest(path)==value for path,value in pins.items()),name
        cases.append(dict(run=name,kind=move_kind,victim=victim,side=side,
            moveProofSHA256=digest(run/'qualification.json'),
            freshProofSHA256=digest(run/'FINISHER_REJOIN_QUALIFICATION.json')))
    validate_coverage(cases,pilot,kind)
    report=dict(scope='Exact finite lethal victim/side coverage with unchanged earned-completion and fresh-match proofs',
        cases=cases,pilot=pilot,selectedFamily=kind,allExpectedCasesQualified=True,
        allEdgesInterruptionsAIAndAudioVerified=False,fullPortVerified=False,
        indexSHA256=digest(index) if kind is None else None)
    output=PORT/(f'LETHAL_ROSTER_{kind.upper()}_ACCEPTANCE_2219.json' if kind else
        ('LETHAL_ROSTER_PILOT_ACCEPTANCE_2219.json' if pilot else 'LETHAL_ROSTER_ACCEPTANCE_2219.json'))
    output.write_text(json.dumps(report,indent=2)+'\n')
    print('Qualified exact lethal coverage',len(cases),'cases; unchanged proof hashes; not full-port approval.')


if __name__=='__main__':
    assert sys.argv[1:] in (['--pilot'],['--full']) or (len(sys.argv)==2 and sys.argv[1].startswith('--kind='))
    main(sys.argv[1]=='--pilot',sys.argv[1].split('=',1)[1] if sys.argv[1].startswith('--kind=') else None)
