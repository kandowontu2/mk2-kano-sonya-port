"""Freeze actual current UI/ladder pictures and all earlier current evidence."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import numpy as np
import PIL
import verify_native_ui_flow as v
from test_native_ui_flow import CASES
from verify_cpu_air_runtime import NAME, EXE, PAYLOAD, SOURCE, need
from verify_cpu_air_gate import digest

ROOT = v.ROOT
OUT = ROOT/'audit_v425_native_ui_flow_checked_inputs'


def run():
    need(not OUT.exists(), 'Refusing to overwrite evidence')
    previous = [ROOT/name for name in ('audit_v422_cpu_projectile_followup_checked_inputs',
        'audit_v418_cpu_roundhouse_recovery_checked_inputs', 'audit_v413_cpu_action_recovery_checked_inputs',
        'audit_v409_human_air_height_checked_inputs')]
    manifests = [json.loads((folder/'input_hashes_before.json').read_text()) for folder in previous]
    old = {}
    for manifest in manifests:
        for filename, sha in manifest.items():
            need(filename not in old or old[filename] == sha, 'Earlier manifests disagree')
            need(digest(filename) == sha, 'Earlier frozen input changed: '+filename)
            old[filename] = sha
    proofs = [v.verify(ROOT/f'audit_v424_native_ui_{fighter}_p{side}', fighter, side) for fighter, side in CASES]
    failed = ROOT/'audit_v423_native_ui_kano_p1'
    failed_result = json.loads((failed/'result.json').read_text(encoding='utf-8-sig'))
    failed_log = (failed/'run.log').read_text(encoding='utf-8-sig')
    need(failed_result['exit_code'] == 3 and 'syntax error' in failed_log and not failed_result['passed'],
         'Failed original observer remains rejected')
    before = json.loads((failed/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    for filename, sha in before.items():
        need(digest(filename) == sha, 'Failed observer live source was rewritten')
        if Path(filename).suffix in ('.lua', '.ps1', '.json'):
            need(digest(failed/'input_sources'/Path(filename).name) == sha, 'Failed frozen source was rewritten')
    suites = [('test_native_ui_flow.py', 46), ('test_cpu_projectile_followup.py', 77),
              ('test_cpu_roundhouse_recovery.py', 49), ('test_cpu_action_recovery.py', 49),
              ('test_human_air_height.py', 28), ('test_cpu_air_runtime.py', 34)]
    runs = []
    for name, count in suites:
        process = subprocess.run([sys.executable, 'tools/'+name], cwd=ROOT, capture_output=True, text=True)
        need(process.returncode == 0 and re.search(r'Ran '+str(count)+' tests', process.stdout+process.stderr),
             'Exact current suite '+name+'\n'+process.stdout+process.stderr)
        runs.append(process)
    files = {ROOT/'tools/audit_native_ui_flow.py', ROOT/'tools/verify_native_ui_flow.py',
             ROOT/'tools/test_native_ui_flow.py', ROOT/'PLAY_MK2_KANO_SONYA.cmd',
             ROOT/'mame-mkp/mkport.exe', ROOT/'roms/mk2ks/mk2ks.ui'}
    for suffix in ('', '_v2'):
        files.update((ROOT/('mk2ks_native_ui_flow'+suffix+'_probe.lua'),
                      ROOT/('tools/run_native_ui_flow'+suffix+'_probe.ps1')))
    for name, count in suites:files.add(ROOT/'tools'/name)
    for folder in previous:files.update(folder/name for name in ('input_hashes_before.json', 'tests.log', 'result.json'))
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename and Path(filename).resolve().parent == (ROOT/'tools').resolve():files.add(Path(filename).resolve())
    for pattern in ('audit_v423_native_ui_*', 'audit_v424_native_ui_*', NAME):
        for folder in ROOT.glob(pattern):
            files.update(p for p in folder.rglob('*') if p.is_file())
            manifest_path = folder/'input_hashes_before.json'
            if manifest_path.exists():
                launch_inputs = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
                files.update(Path(filename) for filename in launch_inputs)
    hashes = {str(p): digest(p) for p in sorted(files)}
    for filename, sha in {**old, **hashes}.items():need(digest(filename) == sha, 'Input changed during audit')
    (OUT/'input_sources').mkdir(parents=True)
    for p in files:
        if p.parent in (ROOT, ROOT/'tools') and p.suffix in ('.py', '.lua', '.ps1') or p.name == 'mk2ks.ui':
            shutil.copy2(p, OUT/'input_sources'/p.name)
    (OUT/'input_hashes_before.json').write_text(json.dumps(hashes, indent=2)+'\n')
    (OUT/'tests.log').write_text('\n'.join(p.stdout+p.stderr for p in runs))
    result = dict(passed=True, candidate=NAME, executable_sha256=EXE, payload_sha256=PAYLOAD,
                  source_sha256=SOURCE, ui_sha256=v.UI_SHA, source_or_gameplay_changed=False,
                  actual_UI_cases=proofs, new_tests=46, repeated_current_tests=237,
                  total_current_passing_tests=283, checked_inputs=len(hashes),
                  previous_unchanged_input_counts={folder.name: len(m) for folder, m in zip(previous, manifests)},
                  phase_matched_cursor_samples=sum(p['rendered']['phase_matched_cursor_samples'] for p in proofs),
                  observed_selection_fields=sum(p['selection_fields'] for p in proofs),
                  observed_post_selection_fields=sum(p['outside_fields'] for p in proofs),
                  observed_first_match_participant_fields=sum(p['first_match_participant_fields'] for p in proofs),
                  native_lifebar_name_shadow_checks=sum(p['rendered']['native_name_shadow_checks'] for p in proofs),
                  failed_syntax_capture_preserved=True, earlier_verifiers_and_raw_traces_not_rewritten=True,
                  preserved_legacy_source_guard_rejection_not_relabelled_pass=True,
                  visual_runtime=dict(numpy=np.__version__, pillow=PIL.__version__),
                  scope=v.SCOPE, production_not_promoted=True, whole_character_integration_complete=False,
                  next_required='Current wider native combat/CPU/victims/interruptions/KO, ground-shadow/grounding stages, tower/continue/finishers/endings/art/audio; matching final CMD and ZIP')
    for filename, sha in {**old, **hashes}.items():need(digest(filename) == sha, 'Input changed while freezing evidence')
    (OUT/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':run()
