"""Freeze current natural CPU shots without replacing prior narrow evidence."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import verify_cpu_projectile_followup as v
from test_cpu_projectile_followup import CASES
from verify_cpu_air_runtime import NAME, EXE, PAYLOAD, SOURCE, matched_launch, need
from verify_cpu_air_gate import digest

ROOT = v.ROOT
OUT = ROOT/'audit_v422_cpu_projectile_followup_checked_inputs'


def run():
    need(not OUT.exists(), 'Refusing to overwrite frozen evidence')
    previous = [ROOT/'audit_v418_cpu_roundhouse_recovery_checked_inputs',
                ROOT/'audit_v413_cpu_action_recovery_checked_inputs',
                ROOT/'audit_v409_human_air_height_checked_inputs']
    earlier = [json.loads((p/'input_hashes_before.json').read_text()) for p in previous]
    combined = {}
    for manifest in earlier:
        for filename, expected in manifest.items():
            need(filename not in combined or combined[filename] == expected, 'Prior manifests disagree')
            need(digest(filename) == expected, 'Prior frozen input changed: '+filename)
            combined[filename] = expected
    proofs = [v.verify(ROOT/name, identity, scenario, version) for name, identity, scenario, version in CASES]
    rejected = []
    for name, identity, version, reason in (
        ('audit_v419_cpu_projectile_kano604', 17, '', 'duplicate_coordinate_keys_and_no_actual_knife'),
        ('audit_v419_cpu_projectile_sonya_cage605', 18, '', 'duplicate_coordinate_keys'),
        ('audit_v420_cpu_projectile_kano604', 17, '_v2', 'no_actual_knife_entry_before_terminal')):
        _, log, original = matched_launch(ROOT/name,
            'mk2ks_cpu_projectile_followup'+version+'_probe.lua',
            'run_cpu_projectile_followup'+version+'_probe.ps1')
        try:
            v.verify_log(log, identity, 'block', original)
        except ValueError as e:
            rejected.append(dict(capture=name, reason=reason, verifier_rejection=str(e), preserved=True))
        else:
            raise ValueError('Invalid or incomplete diagnostic accepted: '+name)
    suites = [('test_cpu_projectile_followup.py', 77), ('test_cpu_roundhouse_recovery.py', 49),
              ('test_cpu_action_recovery.py', 49), ('test_human_air_height.py', 28),
              ('test_cpu_air_runtime.py', 34)]
    runs = []
    for name, count in suites:
        process = subprocess.run([sys.executable, 'tools/'+name], cwd=ROOT, capture_output=True, text=True)
        need(process.returncode == 0 and re.search(r'Ran '+str(count)+' tests', process.stdout+process.stderr),
             'Exact current suite '+name+'\n'+process.stdout+process.stderr)
        runs.append(process)
    files = {ROOT/'tools/audit_cpu_projectile_followup.py', ROOT/'tools/verify_cpu_projectile_followup.py',
             ROOT/'tools/test_cpu_projectile_followup.py', ROOT/'mk2ks_cold_p2_selection.lua',
             ROOT/'PLAY_MK2_KANO_SONYA.cmd', ROOT/'mame-mkp/mkport.exe'}
    for version in ('', '_v2', '_v3'):
        files.update((ROOT/('mk2ks_cpu_projectile_followup'+version+'_probe.lua'),
                      ROOT/('tools/run_cpu_projectile_followup'+version+'_probe.ps1')))
    for folder in previous:
        files.update(folder/p for p in ('input_hashes_before.json', 'tests.log', 'result.json'))
    for name, count in suites:
        files.add(ROOT/'tools'/name)
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename and Path(filename).resolve().parent == (ROOT/'tools').resolve():
            files.add(Path(filename).resolve())
    for pattern in ('audit_v419_cpu_projectile_*', 'audit_v420_cpu_projectile_*',
                    'audit_v421_cpu_projectile_*', NAME):
        for folder in ROOT.glob(pattern):
            files.update(p for p in folder.rglob('*') if p.is_file())
    hashes = {str(p): digest(p) for p in sorted(files)}
    for filename, expected in {**combined, **hashes}.items():
        need(digest(filename) == expected, 'Input changed during verification: '+filename)
    (OUT/'input_sources').mkdir(parents=True)
    for p in files:
        if p.parent in (ROOT, ROOT/'tools') and p.suffix in ('.py', '.lua', '.ps1'):
            shutil.copy2(p, OUT/'input_sources'/p.name)
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes, indent=2)+'\n')
    (OUT/'tests.log').write_text('\n'.join(p.stdout+p.stderr for p in runs))
    result = dict(passed=True, candidate=NAME, executable_sha256=EXE, payload_sha256=PAYLOAD, source_sha256=SOURCE,
                  source_or_gameplay_changed=False, natural_CPU_projectiles=proofs,
                  rejected_diagnostics=rejected, new_tests=77, repeated_current_tests=160,
                  total_current_passing_tests=237, checked_inputs=len(hashes),
                  previous_unchanged_input_counts={p.name: len(m) for p, m in zip(previous, earlier)},
                  preserved_legacy_source_guard_rejection_not_relabelled_pass=True,
                  observed_child_fields=sum(p['child_fields'] for p in proofs),
                  observed_native_clean_walk_fields=sum(p['native_clean_walk_fields'] for p in proofs),
                  scope=v.SCOPE, production_not_promoted=True, whole_character_integration_complete=False,
                  next_required='Broader natural CPU moves/victims/misses/interruptions/KO and both CPU slots; current full UI/ladder/tower/continue/finishers/art/audio/ground-shadow acceptance; matched final CMD and release ZIP')
    for filename, expected in {**combined, **hashes}.items():
        need(digest(filename) == expected, 'Input changed while freezing audit: '+filename)
    (OUT/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':run()
