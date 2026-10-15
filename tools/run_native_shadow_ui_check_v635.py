"""Strict current-build UI verification for both native fighters and slots."""
import json
from verify_native_ui_flow_v635 import ROOT, verify

if __name__ == '__main__':
    cases = {}
    for side in (1, 2):
        for fighter in ('kano', 'sonya'):
            folder = ROOT / f'audit_v{638 if side == 1 else 637}_native_shadow_ui_{fighter}_p{side}'
            cases[f'{fighter}_p{side}'] = verify(folder, fighter, side)
    print(json.dumps(dict(scope='Both native slots selection/ladder/first-match UI only',
                         candidate='diagnostic_v635_native_shadow_rows', cases=cases,
                         fullPortAcceptance=False), indent=2))
