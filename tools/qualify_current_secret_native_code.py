"""Loaded native entry/graphics code proof, not a successful secret lifecycle."""
import copy
import json
import re
import verify_native_source_sync as sync

sync.verify()
prep = sync.ROOT / 'audit_current_secret_native_code_preparation'
folder = sync.ROOT / 'audit_current_secret_native_code_runtime'
out = sync.ROOT / 'audit_current_secret_native_code_checked'
assert not out.exists()
expected = json.loads((prep / 'expected.json').read_text())
assert sync.sha(sync.ROOT / 'mk2/mk2-maincpu.bin') == expected['stockSHA256']
terminal = json.loads((folder / 'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes'] <= 320*1024*1024 and terminal['logBytes'] <= 10*1024*1024
assert not (folder / 'stderr.log').read_text().strip()
def load(path):
    text = path.read_text()
    assert 'LUA ERROR' not in text
    return [(l.split()[0].removeprefix('MK2_LIGHT_ATTRACT_'), dict(re.findall(r'(\w+)=([^\s]+)', l)))
            for l in text.splitlines() if l.startswith('MK2_LIGHT_ATTRACT_')]
rows = load(folder / 'run.log')
new = {'SECRET_CODE', 'SECRET_PREDICATE'}
assert [(t,r) for t,r in rows if t not in new] == load(sync.ROOT / 'audit_current_ending_asset_tables_runtime/run.log')
def gate(records):
    for tag,key in [('SECRET_CODE','stockIntervals'), ('SECRET_PREDICATE','predicates')]:
        actual = [r for t,r in records if t == tag]
        assert len(actual) == len(expected[key])
        for observed,wanted in zip(actual, expected[key]):
            assert observed['frame'] == '600' and observed['writes'] == '0' and observed['assistance'] == 'none'
            assert all(observed[k] == v for k,v in wanted.items())
gate(rows)
faults = []
for tag in sorted(new):
    bad = copy.deepcopy(rows)
    next(r for t,r in bad if t == tag)['mismatches'] = '1'
    try:
        gate(bad)
    except AssertionError:
        faults.append(tag)
    else:
        raise AssertionError('Changed loaded code accepted')
out.mkdir()
report = dict(currentLoadedSecretCodePassed=True, originalIntervals=expected['stockIntervals'],
              nativeFemalePredicates=expected['predicates'], stockSHA256=expected['stockSHA256'],
              allPriorAssetObservationsUnchanged=True, corruptionsRejected=faults,
              terminal=terminal, logSHA256=sync.sha(folder / 'run.log'),
              actualSecretEncounter=False, currentLateWatchdogResetFixed=False,
              currentCompleteSecretLifecycleAccepted=False, fullPortAccepted=False)
(out / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(dict(passed=True, intervals=8, predicates=3, runtimeEncounterAccepted=False)))
