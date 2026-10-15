"""Freeze the narrow CPU eligibility change and current close regressions."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import verify_cpu_air_gate as check

ROOT = check.ROOT
OUT = ROOT / 'audit_v390_cpu_air_gate_checked_inputs'
PRIORS = ('audit_v363_morph_palette_checked_inputs', 'audit_v365_stock_reaction_checked_inputs',
          'audit_v372_natural_cpu_pair_checked_inputs', 'audit_v377_natural_p1_cpu_pair_checked_inputs',
          'audit_v380_native_cpu_recovery_checked_inputs')
SOURCE = ROOT / 'mame-mkp/src/mame/midway/midtunit_m.cpp'
OLD_SOURCE = '410C682822A858AE20328B09C1DEC3EA2887CDEF0C37D8DB7853725E36F3F7C9'
NEW_SOURCE = '3A998D08823F0F7DF0527C5A46E361EF3FF51D7A600E983A348599D323808DF8'


def run():
    if OUT.exists():
        raise SystemExit('Refusing to overwrite evidence')
    if check.digest(SOURCE) != NEW_SOURCE:
        raise SystemExit('Exact current source required')
    revalidated, intentional_changes = 0, []
    for name in PRIORS:
        manifest = json.loads((ROOT / name / 'input_hashes_before.json').read_text())
        for file, expected in manifest.items():
            actual = check.digest(file)
            if actual != expected:
                if Path(file) != SOURCE or expected != OLD_SOURCE or actual != NEW_SOURCE:
                    raise SystemExit('Unexpected changed historical input: ' + file)
                intentional_changes.append({'manifest': name, 'file': file, 'before': expected, 'after': actual})
            else:
                revalidated += 1
    build = json.loads((ROOT / check.NAME / 'build-info.json').read_text(encoding='utf-8-sig'))
    old_build = json.loads((ROOT / 'diagnostic_v357_native_morph_palette/build-info.json').read_text(encoding='utf-8-sig'))
    changes = [file for file, expected in old_build['input_hashes'].items() if build['input_hashes'].get(file) != expected]
    if changes != [str(SOURCE)] or build['payload_sha256'] != check.PAYLOAD:
        raise SystemExit('More than the declared driver source changed')
    scouts = [dict(case='audit_v389_cpu_air_' + name, **check.verify_case(ROOT / ('audit_v389_cpu_air_' + name)))
              for name in ('sonya_jump604', 'kano_wait604')]
    close = [dict(case=f'audit_v389_cpu_recovery_{p}_boot{b}', **check.verify_recovery_case(ROOT / f'audit_v389_cpu_recovery_{p}_boot{b}', p))
             for p, b in (('kano', 604), ('cage', 605))]
    process = subprocess.run([sys.executable, 'tools/test_cpu_air_gate.py'], cwd=ROOT, capture_output=True, text=True)
    test_output = process.stdout + process.stderr
    if process.returncode or not re.search(r'Ran 15 tests', test_output):
        raise SystemExit(test_output)
    rejected_log = (ROOT / 'audit_v387_cpu_air_kano_wait604/run.log').read_text(encoding='utf-8-sig')
    try:
        check.verify_dump(rejected_log, (ROOT / 'mk2/mk2-maincpu.bin').read_bytes())
    except ValueError as error:
        rejected_reason = str(error)
    else:
        raise SystemExit('Incorrect earlier compiled branch was not rejected')
    files = {SOURCE, ROOT / 'tools/audit_cpu_air_gate.py', ROOT / 'tools/verify_cpu_air_gate.py',
             ROOT / 'tools/test_cpu_air_gate.py', ROOT / 'tools/verify_cpu_recovery.py',
             ROOT / 'tools/verify_p1_cpu_pair.py', ROOT / 'tools/verify_cpu_pair.py', ROOT / 'tools/verify_p2_campaign.py',
             ROOT / 'mk2/mk2-maincpu.bin', ROOT / 'mk2ks_cpu_air_gate_v2_probe.lua', ROOT / 'mk2ks_cpu_recovery_probe.lua',
             ROOT / 'tools/run_cpu_air_gate_v2_probe.ps1', ROOT / 'tools/run_cpu_recovery_probe.ps1',
             ROOT / 'PLAY_MK2_KANO_SONYA.cmd', ROOT / 'mame-mkp/mkport.exe'}
    for prefix in ('audit_v381_cpu_air_*', 'audit_v384_cpu_air_*', 'audit_v387_cpu_air_*', 'audit_v389_cpu_*',
                   'diagnostic_v382_native_cpu_air_catch', 'diagnostic_v383_native_cpu_air_catch',
                   'diagnostic_v385_native_cpu_air_catch', 'diagnostic_v386_native_cpu_air_catch', check.NAME):
        for folder in ROOT.glob(prefix):
            files.update(p for p in folder.rglob('*') if p.is_file())
    for prior in PRIORS:
        files.update((ROOT / prior / 'result.json', ROOT / prior / 'input_hashes_before.json'))
    hashes = {str(p): check.digest(p) for p in sorted(files)}
    if hashes[str(ROOT / 'PLAY_MK2_KANO_SONYA.cmd')] != '9ECEF168B79FC38E436329973CA4B9A744BB1E9FA9F4F0987E01CD4AABC494E7' or hashes[str(ROOT / 'mame-mkp/mkport.exe')] != '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':
        raise SystemExit('Production launcher/generic emulator changed')
    (OUT / 'input_sources').mkdir(parents=True)
    for file in files:
        if file.suffix in ('.py', '.ps1', '.lua', '.cpp') and file.parent.name not in ('input_sources',):
            if file.name in ('midtunit_m.cpp', 'audit_cpu_air_gate.py', 'verify_cpu_air_gate.py', 'test_cpu_air_gate.py',
                             'verify_cpu_recovery.py', 'mk2ks_cpu_air_gate_v2_probe.lua', 'run_cpu_air_gate_v2_probe.ps1'):
                shutil.copy2(file, OUT / 'input_sources' / file.name)
    (OUT / 'input_hashes_before.json').write_text(json.dumps(hashes, indent=2) + '\n')
    (OUT / 'tests.log').write_text(test_output)
    result = dict(passed=True, candidate=check.NAME, executable_sha256=check.EXE, payload_sha256=check.PAYLOAD,
                  source_sha256=NEW_SOURCE, game_code_changed=True, only_declared_driver_source_changed=True,
                  compiled_identity_routes=19, retained_stock_eligibility_and_unwind=True,
                  CPU_air_throw_runtime_acceptance=False, current_native_close_recoveries=close, input_only_scouts=scouts,
                  total_new_tests=15, checked_inputs=len(hashes), unchanged_historical_inputs_revalidated=revalidated,
                  historical_source_intentionally_superseded=intentional_changes,
                  historical_tests_not_relabelled_current=True, rejected_v386_reason=rejected_reason,
                  production_unchanged=True, whole_character_integration_complete=False,
                  scope='compiled real-ID CPU catch eligibility and two complete current close regressions; not CPU catch completion, full pixels/audio/tower')
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    for file, expected in hashes.items():
        if check.digest(file) != expected:
            raise SystemExit('Audit input changed: ' + file)
    print(json.dumps({key: value for key, value in result.items() if key not in ('input_only_scouts', 'current_native_close_recoveries', 'historical_source_intentionally_superseded')}, indent=2))


if __name__ == '__main__':
    run()
