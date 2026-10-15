"""Reject plausible wrong split grammar without modifying evidence."""
import json
from pathlib import Path
from unittest.mock import patch
import verify_native_split_grammar_v1100 as proof

OUT = proof.ROOT/'audit_v1102_native_split_grammar_units'


def main():
    if OUT.exists():
        raise ValueError('Preserve counterexamples')
    baseline = proof.verify()
    assert baseline['passed'] and not baseline['kanoSonyaSplitAccepted']
    path = proof.ROOT/'audit_v1098_kung_lao_liu_kang_p2_split_native_trace/run.log'
    original_read = Path.read_text
    text = original_read(path, encoding='utf-8-sig')
    checks = []
    cases = (
        ('opposite mirror bit lost', 'at=FF842630', 'other_flags=E582', 'other_flags=E592', 'Opposite native X flip'),
        ('second half uses next frame', 'at=FF842690', 'a9=FF8CF990', 'a9=FF8CF9B0', 'Same original stream independently advanced'),
        ('main0 incorrectly treated as split stream', 'at=FF8CEDE0', 'a9=FF920580', 'a9=FF8CF990', 'MAIN0 only seeds original second actor'),
    )
    for name, address, before, after, expected in cases:
        line = next(s for s in text.splitlines() if s.startswith('MK2_SPLIT_V1098_STATE ') and address in s and ' id=1 ' in s)
        assert before in line
        changed = text.replace(line, line.replace(before, after, 1), 1)
        def fake_read(p, *args, **kwargs):
            return changed if p == path else original_read(p, *args, **kwargs)
        with patch.object(Path, 'read_text', fake_read):
            result = proof.verify()
        assert not result['passed'] and any(expected in error for error in result['errors']), (name, result['errors'])
        checks.append({'name': name, 'rejected': True})
    assert original_read(path, encoding='utf-8-sig') == text
    report = {'passed': True, 'checks': checks, 'corruptionChecks': 3, 'filesModifiedByFixtures': False, 'kanoSonyaSplitAccepted': False, 'fullPortAccepted': False}
    OUT.mkdir()
    (OUT/'unit-results.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
