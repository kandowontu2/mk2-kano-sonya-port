"""Preserve5463; distinguish frozen preboot pins from postboot evidence pins.

The5460 runner returns a shared pins dictionary that its final journal extends
with all completed evidence. Native result.json/input_hashes_before.json froze
the preboot dictionary earlier. All non-pin fields must remain exactly equal;
every frozen input must remain pinned and every final expanded pin must equal
the authoritative5462 map. No capture rerun or tolerance change.
"""
import inspect, json, traceback
from pathlib import Path
import qualify_current_primary_audio_progress_v5463 as original

ROOT, need, sha = original.ROOT, original.need, original.sha
FAILED = ROOT / 'audit_v5464_current_primary_audio_qualified_progress/progress.json'
OUT = ROOT / 'audit_v5466_current_primary_audio_qualified_progress'


def run():
    failed = json.loads(FAILED.read_text())
    need(not failed['passed'] and failed['error'] == "ValueError('Exact current native terminal fixture')",
         'Preserved exact preboot-versus-postboot provenance checker failure')
    source = inspect.getsource(original.run)
    before = 'result == case[key] and result[\'passed\']'
    after = "{k:v for k,v in result.items() if k != 'inputHashes'} == {k:v for k,v in case[key].items() if k != 'inputHashes'} and result['passed']"
    need(source.count(before) == 1, 'Only whole-result equality separates provenance scopes')
    source = source.replace(before, after)
    before = "'Actual preboot inputs bound to accepted matrix')"
    after = before + "\n            need(case[key]['inputHashes'] == parent['newInputHashes'] and all(case[key]['inputHashes'].get(p) == h for p,h in result['inputHashes'].items()), 'Exact extended final evidence map contains every immutable preboot input')"
    need(source.count(before) == 1, 'Full original immutable preboot input gate retained')
    source = source.replace(before, after)
    scope = dict(original.__dict__)
    scope.update(OUT=OUT, __file__=str(Path(__file__).resolve()))
    exec(compile(source, __file__ + '.whole5463_separated_provenance_maps', 'exec'), scope)
    report = scope['run']()
    for p in (FAILED, Path(original.__file__).resolve()):
        report['newInputHashes'][str(p)] = sha(p)
    report['preservedFailedQualifier'] = dict(file=str(FAILED), errorWasProvenanceScopeOnly=True,
        gameplayOrCaptureRerun=False, exactNonPinResultFieldsPreserved=True,
        everyImmutablePrebootAndExpandedPostbootFilesystemHashVerified=True,
        entireQualifiedSourceAdaptationSHA256=original.captured.digest(source.encode()))
    need(all(sha(p) == h for p,h in report['newInputHashes'].items()), 'All pins unchanged after provenance-scope correction')
    return report


if __name__ == '__main__':
    need(not OUT.exists(), 'Fresh immutable provenance-corrected primary-audio qualifier')
    try:
        report = run()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), goalStatus='active', fullPortAcceptance=False)
    OUT.mkdir()
    original.captured.save(OUT / 'progress.json', report)
    print(json.dumps({k:v for k,v in report.items() if k not in
                     ('cases', 'newInputHashes', 'remaining', 'terminalTextCompaction')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
