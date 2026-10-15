"""Freeze current human height checks and real original-Jax controls.

Keep early command/stock fixture/close-clinch traces as distinct rejected
catch or follow-up evidence; never relabel them full green cases.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import verify_human_air_height as check
from verify_cpu_air_runtime import verify as verify_cpu
from verify_cpu_air_gate import rows
from test_human_air_height import CASES

ROOT = check.ROOT
OUT = ROOT / 'audit_v409_human_air_height_checked_inputs'


def run():
    if OUT.exists():
        raise SystemExit('Refusing to overwrite evidence')
    prior = ROOT / 'audit_v404_cpu_air_runtime_checked_inputs'
    old = json.loads((prior / 'input_hashes_before.json').read_text())
    for filename, expected in old.items():
        check.need(check.digest(filename) == expected, 'Previous current input changed: ' + filename)
    catches = [dict(case=name, **check.verify(ROOT / name)) for name in CASES]
    cpu = [verify_cpu(ROOT / f'audit_v401_cpu_air_{p}_jump604') for p in ('kano', 'sonya')]
    processes = [subprocess.run([sys.executable, 'tools/' + name], cwd=ROOT, capture_output=True, text=True)
                 for name in ('test_human_air_height.py', 'test_cpu_air_runtime.py')]
    for process, count in zip(processes, (28, 34)):
        check.need(process.returncode == 0 and re.search(r'Ran ' + str(count) + ' tests', process.stdout + process.stderr), 'Exact matched test suite: ' + process.stdout + process.stderr)
    rejected = []
    for name in ('audit_v405_human_air_jax_sub_zero_p1_d20', 'audit_v406_human_air_jax_sub_zero_p2_d20',
                 'audit_v407_stock_jax_air_p1', 'audit_v407_stock_jax_air_p2'):
        try:
            check.verify(ROOT / name)
        except ValueError as error:
            rejected.append(dict(case=name, full_acceptance=False, reason=str(error)))
        else:
            raise ValueError('Earlier nonmatching stock full-follow-up fixture accepted')
    folder = ROOT / 'audit_v405_human_air_kano_sonya_p1_d2'
    meta, early, original = check.match_inputs(folder)
    result = check.one(early, 'RESULT')
    failed = check.one(early, 'FAILED')
    gates = [r for r in check.records(early, 'EVENT') if r['entry'] == 'FF8643E0']
    check.need(len(gates) == 1 and check.clean(gates[0], 'a') and check.clean(gates[0], 'v') and
               not check.records(early, 'CAUGHT') and result['caught'] == '-1' and
               not check.records(early, 'HEALTH') and check.clean(failed, 'a') and check.clean(failed, 'v'), 'Early grounded command is not a hidden air catch/damage/softlock')
    fields = check.records(early, 'FIELD')
    check.need(all(r['writes'] == '0' and r['assistance'] == 'none' and r['astate'] == r['vstate'] == '1' and
                   r['aid'] == r['aroster'] == '17' and r['vid'] == r['vroster'] == '18' and r['ahp'] == r['vhp'] == '161' for r in fields), 'Grounded command actual live identity/health continuity')
    early_proof = dict(case=folder.name, accepted_full_air_throw=False, diagnostic_failure_preserved=True,
                       actual_gate_grounded=True, later_both_ordinary_jumps_observed=True,
                       final_both_grounded_clear=True, no_damage=True,
                       scope='grounded_Block_gate_before_actual_jump_not_successful_air_catch_or_all_air_misses')
    for prefix in ('a', 'v'):
        check.need(sum(int(r[prefix + 'y']) < int(r[prefix + 'floor']) for r in fields) == 38, 'Actual ordinary jump after early grounded gate, not fabricated airborne catch')
    files = {ROOT / 'tools/audit_human_air_height.py', ROOT / 'tools/verify_human_air_height.py',
             ROOT / 'tools/test_human_air_height.py', ROOT / 'tools/verify_cpu_air_runtime.py',
             ROOT / 'tools/test_cpu_air_runtime.py', ROOT / 'tools/verify_cpu_air_counter.py', ROOT / 'tools/verify_cpu_air_gate.py',
             ROOT / 'mk2ks_human_air_height_probe.lua', ROOT / 'mk2ks_human_air_control_probe.lua',
             ROOT / 'tools/run_human_air_height_probe.ps1', ROOT / 'tools/run_human_air_stock_control.ps1',
             ROOT / 'tools/run_human_air_stock_control_v2.ps1', ROOT / 'mk2ks_selector_exit_test.lua', ROOT / 'mk2ks_native_shang_morph.lua',
             ROOT / 'mame-mkp/src/mame/midway/midtunit_m.cpp', ROOT / 'mk2/mk2-maincpu.bin',
             prior / 'result.json', prior / 'input_hashes_before.json', prior / 'tests.log',
             ROOT / 'PLAY_MK2_KANO_SONYA.cmd', ROOT / 'mame-mkp/mkport.exe'}
    for glob in ('audit_v405_human_air_*', 'audit_v406_human_air_*', 'audit_v407_stock_jax_air_*', 'audit_v408_stock_jax_air_*', check.NAME):
        for folder in ROOT.glob(glob):
            files.update(p for p in folder.rglob('*') if p.is_file())
    for filename in old:
        # Keep prior CPU acceptance inputs transitively pinned by its manifest;
        # direct repeated test imports/compiled ROM controls are also included.
        if Path(filename).parent.name in ('audit_v401_cpu_air_kano_jump604', 'audit_v401_cpu_air_sonya_jump604'):
            files.add(Path(filename))
    hashes = {str(p): check.digest(p) for p in sorted(files)}
    check.need(hashes[str(ROOT / 'PLAY_MK2_KANO_SONYA.cmd')] == '9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7' and
               hashes[str(ROOT / 'mame-mkp/mkport.exe')] == '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891', 'Production launcher/generic unchanged')
    (OUT / 'input_sources').mkdir(parents=True)
    for path in files:
        if path.name in ('audit_human_air_height.py', 'verify_human_air_height.py', 'test_human_air_height.py',
                         'mk2ks_human_air_height_probe.lua', 'mk2ks_human_air_control_probe.lua',
                         'run_human_air_height_probe.ps1', 'run_human_air_stock_control_v2.ps1') and path.parent.name != 'input_sources':
            shutil.copy2(path, OUT / 'input_sources' / path.name)
    (OUT / 'input_hashes_before.json').write_text(json.dumps(hashes, indent=2) + '\n')
    (OUT / 'tests.log').write_text('\n'.join(p.stdout + p.stderr for p in processes))
    result = dict(passed=True, candidate=check.NAME, executable_sha256=check.EXE, payload_sha256=check.PAYLOAD,
                  source_sha256=check.SOURCE, game_code_changed=False, human_catches=catches[:4], stock_Jax_controls=catches[4:],
                  current_CPU_air_regressions=cpu, native_fields=sum(p['native_match_fields'] for p in catches),
                  original_cleanup_store_provenance=True, held_Kano_fields=sum(p['held_fields'] for p in catches[:4]),
                  total_new_tests=28, repeated_current_CPU_tests=34, total_current_tests=62,
                  checked_inputs=len(hashes), unchanged_prior_current_inputs_revalidated=len(old),
                  historical_source_not_relabelled_current=True, rejected_stock_full_followup_fixtures=rejected,
                  early_grounded_command=early_proof, current_sonya_CPU_followup_still_rejected=True,
                  production_not_promoted=True, whole_character_integration_complete=False,
                  next_required='Native CPU walk-to-punch/projectile-follow-up provenance, wider natural CPU/KO and current whole UI/tower/art/audio/finisher regression plus matched final launcher/ZIP',
                  scope='four_current_human_Kano_catches_two_slots_two_heights_and_two_original_Jax_controls_full_physics_damage_cleanup_and_normal_controls_not_all_victims_heights_CPU_Jax_KO_pixels_audio_or_final_release')
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    for filename, wanted in hashes.items():
        check.need(check.digest(filename) == wanted, 'Audit input changed: ' + filename)
    print(json.dumps({key: value for key, value in result.items() if key not in ('human_catches', 'stock_Jax_controls', 'current_CPU_air_regressions', 'rejected_stock_full_followup_fixtures')}, indent=2))


if __name__ == '__main__':
    run()
