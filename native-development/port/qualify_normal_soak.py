"""Finite native two-player stress coverage, not campaign/all-move acceptance."""
import csv
import json
from pathlib import Path
import re
import sys
import zipfile
from campaign_rounds import require_clean_runtime_log
from inspect_normal_runtime import BASE, PORT, sha
from verify_finisher_roms import verify


def summarize(rows, actors, required_fields=24000, minimum_combat=5000):
    assert [int(r['frame']) for r in rows] == list(range(1, required_fields + 1))
    assert all(r['missing'] == '0' for r in rows)
    owned = [r for r in rows if r['mode'] == '2' and r['locked'] == '1']
    assert len(owned) >= minimum_combat
    for row in owned:
        assert row['p1state'] == row['p2state'] == '1', 'Both players must be native active humans'
        for side, actor in enumerate(actors, 1):
            assert row[f'p{side}selected'] == row[f'p{side}char'] == str(actor)
    assert all(min(int(r[f'p{side}hp']) for r in owned) < 161 for side in (1, 2))
    fresh = []; results = []; previous = None; was_result = False; human_context = False
    for row in rows:
        if row['mode'] in ('1','4'):
            human_context = False
        if row['mode'] == '2' and row['locked'] == '1':
            human_context = True
        correct = all(row[f'p{side}selected'] == row[f'p{side}char'] == str(actor)
                      for side, actor in enumerate(actors, 1))
        if (row['mode'] == '2' and row['locked'] == '1' and correct and
            (previous is None or previous['mode'] != '2') and
            row['p1hp'] == row['p2hp'] == '161' and row['p1wins'] == row['p2wins'] == '0'):
            fresh.append(int(row['frame']))
        result = (human_context and row['mode'] == '5' and correct and row['winner'] in ('1', '2') and
                  row['p' + row['winner'] + 'wins'] == '2' and
                  row['p' + str(3-int(row['winner'])) + 'hp'] == '0' and
                  int(row['p' + row['winner'] + 'hp']) > 0)
        if result and not was_result:
            results.append(int(row['frame']))
            human_context = False
        was_result = result; previous = row
    assert len(fresh) >= 2 and results and any(results[0] < f for f in fresh[1:])
    return dict(controlledCombatFields=len(owned), freshMatchEntryFrames=fresh,
                nativeTwoWinResultEntryFrames=results,
                firstControlledCombatFrame=int(owned[0]['frame']),
                lastControlledCombatFrame=int(owned[-1]['frame']))


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run = BASE / name
    receipt = json.loads((run / 'execution.json').read_text())
    assert '--normal-soak' in receipt['testArguments'] and '--normal-moves' in receipt['testArguments']
    assert receipt['exitCode'] == 0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['controllerSHA256'] == sha(run / 'autoboot.lua')
    source = (run / 'autoboot.lua').read_text()
    assert ':write_u' not in source and not re.search(r'\.value\s*=(?!=)', source)
    assert receipt['emulatorSHA256'] == 'AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    require_clean_runtime_log((run / 'mame.log').read_text())
    with zipfile.ZipFile(run / 'roms/mk3.zip') as archive:
        verify(archive, receipt)
    with (run / 'soak_state.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    actors = (18, 17) if '--mirror' in receipt['testArguments'] else (17, 18)
    result = summarize(rows, actors)
    symbols = {n: int(a, 16) for a, n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',
        (BASE / 'mk2-rebuild-main/srcp/MK2P.MAP').read_text())}
    assert all(int(r['pc'], 16) != symbols['illegal_opcode'] + 0x50 for r in rows)
    report = dict(scope='24000-field physical-input normal-combat and natural fresh-match stress trial',
        actors=list(actors), currentAll26ROMBytesVerified=True, noMissingMarkersOrObservedIllegalRecovery=True,
        everyAnimationVisuallyApproved=False, specialsOrFatalitiesProvedByThisTrial=False,
        fullPortVerified=False, **result,
        pins={str(p): sha(p) for p in (run / 'execution.json', run / 'autoboot.lua', run / 'soak_state.csv',
                                     run / 'normals.csv', run / 'mame.log', Path(__file__))})
    (run / 'NORMAL_SOAK_QUALIFICATION.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Combat fields', result['controlledCombatFields'], 'fresh matches', len(result['freshMatchEntryFrames']),
          'native two-win result entries', len(result['nativeTwoWinResultEntryFrames']))


if __name__ == '__main__':
    assert len(sys.argv) == 2
    main(sys.argv[1])
