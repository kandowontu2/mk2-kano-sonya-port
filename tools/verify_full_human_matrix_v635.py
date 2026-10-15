"""Fresh 52-case human matrix on exact v635; not full-game acceptance."""
import json
import re
import verify_native_candidate_v635 as build
import verify_human_special_matrix as positive
import verify_human_special_negative_v5 as negative
from verify_ko_round_floor_shadows import need, digest, rgb

ROOT = build.ROOT

def case_folder(name):
    return ROOT/('audit_v652_'+name)

def check_case(log, move, side, scenario=None, air=False):
    case = (positive.verify_log(log, move, side, air) if scenario is None
            else negative.verify_log(log, move, side, scenario))
    if move == 'ball':
        if scenario is not None:
            negative.verify_repel(log, side)
        if scenario != 'miss':
            case.update(negative.verify_rebound(log, side, scenario == 'block'))
    return case

def verify():
    inputs = {}
    cases = []
    for move in positive.SPECS:
        for side in (1, 2):
            fixtures = [(None, False)]
            if move == 'square': fixtures.append((None, True))
            fixtures += [('block', False), ('miss', False)]
            if move == 'leg': fixtures.append(('duck_block', False))
            for scenario, air in fixtures:
                name = (f'positive_{move}{"_air" if air else ""}_p{side}' if scenario is None
                        else f'negative_{move}_{scenario}_p{side}')
                folder = case_folder(name)
                build.matched(folder, inputs)
                launch = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
                need((launch['move'], launch['side']) == (move, side), 'Exact real-input launch')
                need(launch.get('air') == air if scenario is None else
                     (launch['scenario'], launch['victim']) == (scenario, 'sub_zero'),
                     'Exact fixture, no substitution')
                observer_name=('mk2ks_human_special_matrix_v2.lua' if scenario is None
                               else 'mk2ks_human_special_negative_v9.lua')
                observer=(folder/'input_sources'/observer_name).read_text()
                need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),
                     'Standalone input-only observer; no guest state assistance')
                log = (folder / 'run.log').read_text(encoding='utf-8-sig')
                case = check_case(log, move, side, scenario, air)
                case['capture'] = folder.name
                cases.append(case)
                for image_name in ('special_before.png', 'special_recovered.png', 'special_final.png'):
                    path = folder / 'snap' / image_name
                    need(rgb(path).shape == (254, 400, 3), 'Native screenshot dimensions, not artwork acceptance')
                    inputs[str(path)] = digest(path)
    need(len(cases) == 52, 'Complete requested human fixture inventory')
    for module in (build, positive, negative):
        path = ROOT / 'tools' / (module.__name__ + '.py')
        inputs[str(path)] = digest(path)
    for name in ('verify_full_human_matrix_v635.py', 'test_full_human_matrix_v635.py',
                 'verify_ko_round_floor_shadows.py', 'inspect_ground_presentation.py'):
        path = ROOT / 'tools' / name
        inputs[str(path)] = digest(path)
    return dict(passed=False, boundedMatrixPassed=True, fullPortAcceptance=False,
                candidate=build.NAME, cases=cases,
                positiveCases=18, negativeCases=34,
                pairedFields=sum(case['fields'] for case in cases), inputHashes=inputs,
                scope='Fresh 18 positive and 34 defensive/recovery human cases versus Sub-Zero, both slots. '
                      'Includes square-wave airborne contact, leg duck-block and actual cannonball flight/recoil. '
                      'Wider roster outcomes and contact fidelity remain under review; interruptions/KO, CPU, '
                      'selection/ladder, full campaign, finishers/endings/audio and release are not accepted here.')

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
