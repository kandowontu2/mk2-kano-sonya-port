"""Current matched build, real selection/join and complete mobility contacts.

Cold contact evidence does not prove endings, CPU variety, audio or a release.
"""
import argparse
import hashlib
import json
from pathlib import Path

from verify_restart_lifecycle import verify_mobility_join
from verify_mobility_contact import verify as contact
from verify_projectile_choreography import ROOT, PAYLOAD_SHA
from verify_current_post_ending_choreography import EXE_SHA, CANDIDATE


def verify(folder, target, side, scenario, candidate=CANDIDATE, exe_sha=EXE_SHA, payload_sha=PAYLOAD_SHA):
    errors = []
    def check(ok, label):
        if not ok and label not in errors:
            errors.append(label)
    try:
        metadata = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        log = (folder/'run.log').read_text(encoding='utf-8-sig')
        check((metadata.get('exit_code'), metadata.get('target'), metadata.get('side'), metadata.get('scenario'), metadata.get('candidate')) ==
              (0, target, side, scenario, candidate), 'Exact terminal current case/build/scope')
        check(metadata.get('passed') is True and metadata.get('observer_pass') is True and
              metadata.get('independent_verification_exit_code') == 0 and metadata.get('cheats') is False and
              metadata.get('memory_assistance') == 'none', 'Unassisted terminal real-input case')
        check(metadata.get('candidate_executable_sha256', '').lower() == exe_sha.lower() and
              metadata.get('payload_sha256', '').lower() == payload_sha.lower(), 'Exact independently requested executable and payload')
        hashes = metadata.get('input_hashes', {})
        before = json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        check(before == hashes, 'Original frozen launch manifest matches terminal inputs')
        required = {'mkport_candidate.exe', 'mk2ks.mdata', 'build-info.json', 'mk2ks_join_mobility_probe.lua',
                    'mk2ks_restart_lifecycle.lua', 'mk2ks_selector_exit_test.lua', 'mk2ks_mobility_contact.lua',
                    'run_join_mobility_probe.ps1', 'verify_restart_lifecycle.py', 'verify_mobility_contact.py',
                    'verify_current_lifecycle.py', 'verify_projectile_contact.py'}
        check(required <= {Path(p).name for p in hashes}, 'Complete frozen launcher/driver/verifier inventory')
        for path, expected in hashes.items():
            item = Path(path)
            if item.suffix.lower() in ('.lua', '.ps1', '.py', '.json'):
                item = folder/'input_sources'/item.name
            check(item.exists() and hashlib.sha256(item.read_bytes()).hexdigest().upper() == expected,
                  'Exact frozen input: '+item.name)
        joined = verify_mobility_join(log, target, side, require_restart=False)
        move = contact(log, target, side)
        errors.extend(joined['errors'])
        errors.extend('Contact: '+e for e in move['errors'])
        check(move.get('scenario') == scenario, 'Actual requested contact scenario')
        check(not any(x in log for x in ('MK2KS_DIAGNOSTIC_HEALTH_WRITE', 'MK2KS_DIAGNOSTIC_P1_REGEN',
                                        'MK2KS_CPU_DIAGNOSTIC_WRITE', 'MK2KS_CPU_DIAGNOSTIC_LADDER_WRITE')),
              'No diagnostic guest-state assistance')
        return dict(passed=not errors, errors=errors, target=target, side=side, scenario=scenario,
                    contact=move, joined=joined,
                    scope='current_cold_native_start_real_join_full_mobility_contact_and_followup_not_ending_CPU_variety_audio_or_release',
                    whole_character_integration_complete=False)
    except (OSError, ValueError, KeyError, TypeError) as error:
        return dict(passed=False, errors=errors+['Missing/malformed evidence: '+str(error)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    parser.add_argument('--target', choices=('kano', 'sonya'), required=True)
    parser.add_argument('--side', choices=(1, 2), type=int, required=True)
    parser.add_argument('--scenario', choices=('hit', 'block', 'miss'), required=True)
    args = parser.parse_args()
    result = verify(args.folder, args.target, args.side, args.scenario)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
