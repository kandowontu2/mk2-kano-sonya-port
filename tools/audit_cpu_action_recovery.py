"""Freeze the current Sonya continuation proof without rewriting old evidence."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import verify_cpu_action_recovery as pair
import verify_cpu_action_flow as flow
import verify_stock_cpu_uppercut as stock
from verify_cpu_air_runtime import NAME, EXE, PAYLOAD, SOURCE, matched_launch
from verify_cpu_air_gate import digest
from test_cpu_action_recovery import SONYA, KANO, STOCK

ROOT = pair.ROOT
OUT = ROOT / 'audit_v413_cpu_action_recovery_checked_inputs'


def run():
    if OUT.exists():
        raise SystemExit('Refusing to overwrite evidence')
    prior = ROOT / 'audit_v409_human_air_height_checked_inputs'
    manifest = json.loads((prior / 'input_hashes_before.json').read_text())
    for filename, expected in manifest.items():
        flow.need(digest(filename) == expected, 'Prior current input drift: ' + filename)
    sonya, kano = pair.verify(SONYA, 'cage'), pair.verify(KANO, 'kano')
    flow.need(sonya['passed'] and kano['passed'], 'Both current paired regressions')
    control = stock.verify(STOCK)
    flow.need(sonya['original_uppercut_followup']['authored_fields'] ==
              control['uppercut']['authored_fields'] == 33, 'Stock and actual Sonya full native cadence')
    # Earlier raw trace reaches KO rather than the observed cleanup. Keep it
    # as a partial setup control; do not reinterpret its timeout as success.
    earlier = ROOT / 'audit_v411_cpu_action_stock_baraka601'
    _, old_log, original = matched_launch(earlier, 'mk2ks_cpu_action_transition_v2_probe.lua',
                                          'run_cpu_action_transition_v2_probe.ps1')
    rejected = pair.rows(old_log, 'STOCK_END')
    flow.need(len(rejected) == 1 and rejected[0]['clear'] == -1, 'Old stock control remains incomplete')
    native_instruction_pins = flow.original_instructions(original)
    suites = [('test_cpu_action_recovery.py', 49), ('test_human_air_height.py', 28),
              ('test_cpu_air_runtime.py', 34)]
    processes = []
    for name, count in suites:
        process = subprocess.run([sys.executable, 'tools/' + name], cwd=ROOT,
                                 capture_output=True, text=True)
        flow.need(process.returncode == 0 and
                  re.search(r'Ran ' + str(count) + ' tests', process.stdout + process.stderr),
                  'Exact suite failed: ' + name + '\n' + process.stdout + process.stderr)
        processes.append(process)
    # This historical suite includes a launch pinned to superseded v357
    # source. Its current-build guard MUST reject that old fixture. Preserve
    # the failure in full; do not count the suite as current acceptance.
    historical = subprocess.run([sys.executable, 'tools/test_cpu_recovery.py'], cwd=ROOT,
                                capture_output=True, text=True)
    historical_output = historical.stdout + historical.stderr
    flow.need(historical.returncode == 1 and 'Ran 63 tests' in historical_output and
              'FAILED (failures=1)' in historical_output and
              'FAIL: test_both_full_native_pairs_and_individual_handoffs' in historical_output and
              'Exact current build input:' in historical_output and
              'midtunit_m.cpp' in historical_output, 'Historical source guard rejection differs: ' + historical_output)
    processes.append(historical)
    files = {ROOT / 'tools/audit_cpu_action_recovery.py', ROOT / 'tools/test_cpu_action_recovery.py',
             ROOT / 'tools/verify_cpu_action_recovery.py', ROOT / 'tools/verify_cpu_action_flow.py',
             ROOT / 'tools/verify_stock_cpu_uppercut.py', ROOT / 'mk2ks_cpu_action_transition_probe.lua',
             ROOT / 'mk2ks_cpu_action_transition_v2_probe.lua', ROOT / 'mk2ks_cpu_action_transition_v3_probe.lua',
             ROOT / 'tools/run_cpu_action_transition_probe.ps1', ROOT / 'tools/run_cpu_action_transition_v2_probe.ps1',
             ROOT / 'tools/run_cpu_action_transition_v3_probe.ps1', ROOT / 'PLAY_MK2_KANO_SONYA.cmd',
             ROOT / 'mame-mkp/mkport.exe', prior / 'result.json', prior / 'input_hashes_before.json', prior / 'tests.log'}
    for name, _ in suites:
        files.add(ROOT / 'tools' / name)
    files.add(ROOT / 'tools/test_cpu_recovery.py')
    # Actual imported Python dependencies, plus transitive earlier audit pins.
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename and Path(filename).resolve().parent == (ROOT / 'tools').resolve():
            files.add(Path(filename).resolve())
    for folder in [SONYA, KANO, STOCK, earlier, ROOT / NAME,
                   ROOT / 'audit_v410_cpu_action_sonya_cage605']:
        files.update(p for p in folder.rglob('*') if p.is_file())
    hashes = {str(p): digest(p) for p in sorted(files)}
    flow.need(hashes[str(ROOT / 'PLAY_MK2_KANO_SONYA.cmd')] ==
              '9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7' and
              hashes[str(ROOT / 'mame-mkp/mkport.exe')] ==
              '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
              'Production launcher/generic executable unchanged')
    (OUT / 'input_sources').mkdir(parents=True)
    for file in files:
        if file.parent in (ROOT / 'tools', ROOT) and file.suffix in ('.py', '.lua', '.ps1'):
            shutil.copy2(file, OUT / 'input_sources' / file.name)
    (OUT / 'tests.log').write_text('\n'.join(p.stdout + p.stderr for p in processes))
    (OUT / 'input_hashes_before.json').write_text(json.dumps(hashes, indent=2) + '\n')
    result = dict(passed=True, candidate=NAME, executable_sha256=EXE, payload_sha256=PAYLOAD,
                  source_sha256=SOURCE, game_code_changed=False, sonya_pair_and_full_uppercut=sonya,
                  stock_Baraka_uppercut=control, Kano_pair_regression=kano,
                  original_instruction_pins=native_instruction_pins,
                  new_tests=49, repeated_current_tests=62, total_current_passing_tests=111,
                  historical_suite=dict(tests=63, failures=1, current_acceptance=False,
                                        expected_rejection='v379/v357 frozen launch is not current v400 driver source',
                                        full_original_output_preserved=True),
                  checked_inputs=len(hashes),
                  unchanged_prior_current_inputs_revalidated=len(manifest),
                  old_verifier_and_rejections_preserved=True,
                  incomplete_stock_control=dict(case=earlier.name, full_recovery_accepted=False, clear=-1),
                  production_not_promoted=True, whole_character_integration_complete=False,
                  next_required='Kano delayed next-action write/recovery, both CPU projectile follow-ups, wider natural CPU/KO and current whole UI/tower/art/audio/finisher acceptance plus matched final launcher/ZIP',
                  scope='declared_Sonya_leg_grab_and_original_uppercut_full_recovery_stock_control_and_Kano_choke_pair_only_not_all_CPU_actions_victims_KO_or_full_goal')
    for filename, expected in hashes.items():
        flow.need(digest(filename) == expected, 'Audit input changed: ' + filename)
    for filename, expected in manifest.items():
        flow.need(digest(filename) == expected, 'Prior input changed during audit: ' + filename)
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('sonya_pair_and_full_uppercut', 'stock_Baraka_uppercut', 'Kano_pair_regression')}, indent=2))


if __name__ == '__main__':
    run()
