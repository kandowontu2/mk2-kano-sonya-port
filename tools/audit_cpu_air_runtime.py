"""Freeze the v400 CPU air-catch checkpoint, including rejected regressions.

Historical source revisions are declared, never silently relabelled current.
This is not a release acceptance gate.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import verify_cpu_air_runtime as check
from verify_cpu_air_counter import verify_compiled
from verify_cpu_recovery import verify_log as close_log, flag_rows, rows as close_rows

ROOT = check.ROOT
OUT = ROOT / 'audit_v404_cpu_air_runtime_checked_inputs'
PRIORS = ('audit_v363_morph_palette_checked_inputs', 'audit_v365_stock_reaction_checked_inputs',
          'audit_v372_natural_cpu_pair_checked_inputs', 'audit_v377_natural_p1_cpu_pair_checked_inputs',
          'audit_v380_native_cpu_recovery_checked_inputs', 'audit_v390_cpu_air_gate_checked_inputs')
SOURCE = ROOT / 'mame-mkp/src/mame/midway/midtunit_m.cpp'
OLD = {'410C682822A858AE20328B09C1DEC3EA2887CDEF0C37D8DB7853725E36F3F7C9',
       '3A998D08823F0F7DF0527C5A46E361EF3FF51D7A600E983A348599D323808DF8'}


def run():
    if OUT.exists():
        raise SystemExit('Refusing to overwrite evidence')
    check.need(check.digest(SOURCE) == check.SOURCE, 'Exact current source')
    revalidated, changes = 0, []
    for name in PRIORS:
        manifest = json.loads((ROOT / name / 'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        for filename, expected in manifest.items():
            actual = check.digest(filename)
            if actual == expected:
                revalidated += 1
            else:
                check.need(Path(filename) == SOURCE and expected in OLD and actual == check.SOURCE,
                           'Unexpected historical input drift: ' + filename)
                changes.append(dict(manifest=name, file=filename, before=expected, after=actual))
    build = json.loads((ROOT / check.NAME / 'build-info.json').read_text(encoding='utf-8-sig'))
    old_build = json.loads((ROOT / 'diagnostic_v357_native_morph_palette/build-info.json').read_text(encoding='utf-8-sig'))
    changed = [f for f, sha in old_build['input_hashes'].items() if build['input_hashes'].get(f) != sha]
    check.need(changed == [str(SOURCE)] and build['payload_sha256'] == check.PAYLOAD, 'Only declared driver source and unchanged morph payload')
    catches = [dict(case=f'audit_v401_cpu_air_{p}_jump604', **check.verify(ROOT / f'audit_v401_cpu_air_{p}_jump604')) for p in ('kano', 'sonya')]
    clamp = check.verify_y_provenance(ROOT / 'audit_v403_cpu_air_sonya_y604')
    close = []
    for player, boot in (('kano', 604), ('cage', 605)):
        folder = ROOT / f'audit_v402_cpu_recovery_{player}_boot{boot}'
        launch, log, _ = check.matched_launch(folder, 'mk2ks_cpu_recovery_probe.lua', 'run_cpu_recovery_probe.ps1')
        check.need(launch['player'] == player, 'Declared close regression player')
        close.append(dict(case=folder.name, **close_log(log, player)))
    check.need(close[0]['passed'], 'Current full Kano close regression')
    check.need(not close[1]['passed'] and close[1]['errors'] == ['CPU busy state after cleanup is proven NEW original action setup, not waived residual locks'], 'Preserve actual Sonya follow-up rejection')
    rejected_log = (ROOT / close[1]['case'] / 'run.log').read_text(encoding='utf-8-sig')
    done = close_rows(rejected_log, 'COMPLETE')[0]
    sets = [r for r in flag_rows(rejected_log) if r['slot'] == 1 and close[1]['own_handoff'] < r['frame'] <= close[1]['complete'] and r['pc'] in (0xff838cf0, 0xff877d50)]
    check.need(done['action'] == 0x106 and len(sets) >= 2 and all(r['action'] == 0x303 for r in sets), 'Actual rejected walk-to-punch transition, not silently waived')
    old_log = (ROOT / 'audit_v397_cpu_air_liu_jump604/run.log').read_text(encoding='utf-8-sig')
    at = old_log.find('MK2_CPU_AIR_ROM start=FF9BEEF0', 1)
    try:
        verify_compiled(old_log[:at] if at > 0 else old_log)
    except ValueError as error:
        padding_rejection = str(error)
    else:
        raise ValueError('Missing guard NOP accepted')
    process = subprocess.run([sys.executable, 'tools/test_cpu_air_runtime.py'], cwd=ROOT, capture_output=True, text=True)
    output = process.stdout + process.stderr
    check.need(process.returncode == 0 and re.search(r'Ran 34 tests', output), 'New tests: ' + output)
    files = {SOURCE, ROOT / 'tools/audit_cpu_air_runtime.py', ROOT / 'tools/verify_cpu_air_runtime.py',
             ROOT / 'tools/test_cpu_air_runtime.py', ROOT / 'tools/verify_cpu_air_counter.py',
             ROOT / 'tools/verify_cpu_air_gate.py', ROOT / 'tools/verify_cpu_recovery.py',
             ROOT / 'tools/verify_restart_airthrow.py', ROOT / 'mk2/mk2-maincpu.bin',
             ROOT / 'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx',
             ROOT / 'mk2ks_cpu_air_height_probe.lua', ROOT / 'mk2ks_cpu_air_y_provenance_probe.lua',
             ROOT / 'tools/run_cpu_air_height_probe.ps1', ROOT / 'tools/run_cpu_air_y_provenance_probe.ps1',
             ROOT / 'mk2ks_cpu_recovery_probe.lua', ROOT / 'tools/run_cpu_recovery_probe.ps1',
             ROOT / 'PLAY_MK2_KANO_SONYA.cmd', ROOT / 'mame-mkp/mkport.exe'}
    for prefix in ('audit_v39*_cpu_*', 'audit_v401_cpu_*', 'audit_v402_cpu_*', 'audit_v403_cpu_*',
                   'diagnostic_v394_*', 'diagnostic_v396_*', 'diagnostic_v398_*', check.NAME,
                   'audit_mk3_airthrow_reference_v2'):
        for folder in ROOT.glob(prefix):
            files.update(p for p in folder.rglob('*') if p.is_file())
    for prior in PRIORS:
        files.update((ROOT / prior / 'result.json', ROOT / prior / 'input_hashes_before.json'))
    outer = Path('C:/Users/kando/Documents/Codex/2026-08-30/continue-the-mk2-kano-sonya-port')
    files.update((outer / 'MK2_Kano_Sonya_v258_playtest.zip', outer / 'PLAY_MK2_KANO_SONYA.cmd'))
    files.update((ROOT / 'diagnostic_v277_native_battle_photos/mkport_candidate.exe', ROOT / 'diagnostic_v277_native_battle_photos/roms/mk2ks/mk2ks.mdata'))
    hashes = {str(p): check.digest(p) for p in sorted(files)}
    for path, wanted in ((ROOT / 'PLAY_MK2_KANO_SONYA.cmd', '9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7'),
                         (ROOT / 'mame-mkp/mkport.exe', '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'),
                         (outer / 'MK2_Kano_Sonya_v258_playtest.zip', 'F548E7BA3A630A8ED5A7F280A27FDC27B1F4ED4E6CF5A250909B079B71B3901E'),
                         (outer / 'PLAY_MK2_KANO_SONYA.cmd', 'C94CFA01D231BE90597DF799FC8043FCAA18ED467886B347A984B32BFABC91B7')):
        check.need(hashes[str(path)] == wanted, 'Production file changed: ' + str(path))
    (OUT / 'input_sources').mkdir(parents=True)
    for path in files:
        if path.name in ('audit_cpu_air_runtime.py', 'verify_cpu_air_runtime.py', 'test_cpu_air_runtime.py',
                         'verify_cpu_air_counter.py', 'midtunit_m.cpp', 'mk2ks_cpu_air_y_provenance_probe.lua',
                         'run_cpu_air_y_provenance_probe.ps1') and path.parent.name != 'input_sources':
            shutil.copy2(path, OUT / 'input_sources' / path.name)
    (OUT / 'input_hashes_before.json').write_text(json.dumps(hashes, indent=2) + '\n')
    (OUT / 'tests.log').write_text(output)
    result = dict(passed=True, candidate=check.NAME, executable_sha256=check.EXE, payload_sha256=check.PAYLOAD,
                  source_sha256=check.SOURCE, natural_CPU_air_throw_runtime_acceptance=catches,
                  actual_original_impact_floor_word_control=clamp, current_close_regressions=close,
                  current_sonya_followup_rejected=True, rejected_followup_setup_action='0303', rejected_followup_final_action='0106',
                  rejected_v396_guard_padding_reason=padding_rejection, total_new_tests=34,
                  checked_inputs=len(hashes), unchanged_historical_inputs_revalidated=revalidated,
                  historical_source_intentionally_superseded=changes, historical_tests_not_relabelled_current=True,
                  only_declared_driver_source_changed=True, production_not_promoted=True,
                  whole_character_integration_complete=False,
                  next_required='Current human air catches both slots/heights and stock Jax; native CPU walk-to-punch follow-up ownership provenance; broader natural integration and matched release',
                  scope='only_declared_P1_CPU_air_catches_native_damage_full_held_flight_and_individual_postcleanup_ready_not_cleanup_store_provenance_all_art_audio_human_Jax_slots_victims_KO_or_whole_goal')
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    for filename, expected in hashes.items():
        check.need(check.digest(filename) == expected, 'Audit input changed: ' + filename)
    print(json.dumps({k: v for k, v in result.items() if k not in ('natural_CPU_air_throw_runtime_acceptance', 'current_close_regressions', 'historical_source_intentionally_superseded', 'actual_original_impact_floor_word_control')}, indent=2))


if __name__ == '__main__':
    run()
