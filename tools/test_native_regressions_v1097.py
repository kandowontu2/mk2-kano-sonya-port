"""In-memory counterexamples; never alter native evidence or game sources."""
import json
from pathlib import Path
from unittest.mock import patch
import verify_native_regressions_v1092 as proof

OUT = proof.ROOT / 'audit_v1097_native_regression_proof_units'


def main():
    if OUT.exists():
        raise ValueError('Preserve verification evidence')
    baseline = proof.verify()
    assert baseline['passed'], baseline['errors']
    assert len(baseline['cases']) == 20 and not baseline['fullPortAccepted']
    checks = []
    original_text = Path.read_text
    original_bytes = Path.read_bytes
    case = proof.ROOT / 'audit_v1091_cage_kano_p1_palette_regression'
    log_path = case / 'run.log'
    log = original_text(log_path, encoding='utf-8-sig')
    wrap = next(line for line in log.splitlines() if 'MK2_STOCK_HEAD_V921_WRAP ' in line)
    assert 'age=185 ' in wrap
    changed_log = log.replace(wrap, wrap.replace('age=185 ', 'age=184 '), 1)

    def fake_text(path, *args, **kwargs):
        return changed_log if path == log_path else original_text(path, *args, **kwargs)

    with patch.object(Path, 'read_text', fake_text):
        result = proof.verify()
    assert not result['passed'] and any(
        'All native physical/art observations unchanged' in error and case.name in error
        for error in result['errors'])
    checks.append({'name': 'one-field native wrap timing corruption', 'rejected': True})

    picture = next((case / 'snap').rglob('*.png'))
    actual_picture = original_bytes(picture)

    def fake_picture(path):
        return actual_picture + b'in-memory-counterexample' if path == picture else original_bytes(path)

    with patch.object(Path, 'read_bytes', fake_picture):
        result = proof.verify()
    assert not result['passed'] and any(
        'Actual presented PNG unchanged' in error and case.name in error
        for error in result['errors'])
    checks.append({'name': 'different actual presented PNG bytes', 'rejected': True})

    source = proof.DRIVER
    actual_source = original_bytes(source)

    def fake_source(path):
        return actual_source + b'\n// in-memory-counterexample\n' if path == source else original_bytes(path)

    with patch.object(Path, 'read_bytes', fake_source):
        result = proof.verify()
    assert not result['passed'] and any('Build input ' + str(source) == error for error in result['errors'])
    checks.append({'name': 'changed current compiled source', 'rejected': True})
    assert original_text(log_path, encoding='utf-8-sig') == log
    assert original_bytes(picture) == actual_picture and original_bytes(source) == actual_source
    report = {'passed': True, 'baselineCurrentCases': 20, 'checks': checks,
              'corruptionChecks': len(checks), 'evidenceFilesModified': False,
              'sourceFilesModified': False, 'fullPortAccepted': False}
    OUT.mkdir()
    (OUT / 'unit-results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
