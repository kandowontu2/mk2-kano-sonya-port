"""Conserve the actually executed first checker failure before repair."""
import gzip
import json
import traceback
from pathlib import Path
import verify_native_kano_laser_reference as checker


def main(capture):
    out = checker.ROOT/'audit_native_kano_laser_checker_failure'
    checker.need(not out.exists(), 'Fresh immutable actual checker failure')
    try:
        checker.inspect(checker.rows(capture['text']), capture['rgbFrames'])
    except ValueError as error:
        checker.need(str(error) == 'Actual combat damage routine earned both knockouts',
                     'Same actually observed initial checker failure reproduced against same RAM capture')
        failure = traceback.format_exc()
    else:
        raise ValueError('Expected actually executed checker failure no longer reproduced')
    path = Path(checker.__file__).resolve()
    sha = checker.reference.sha(path)
    out.mkdir()
    with gzip.open(out/'failed_executed_checker_source.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump(dict(path=str(path), sha256=sha, source=path.read_text(), traceback=failure), stream)
    (out/'report.json').write_text(json.dumps(dict(passed=False, actualCheckerFailure=True,
        nativeRunRestarted=False, originalNativeExit=0,
        failedSourceSHA256=sha, failure=failure,
        diagnosis='The native next-round bar fill reports65535 sentinel before4 atFFA96A90; it is not earned combat damage. Actual independent laser object has30 pose changes, not29.',
        originalRunSHA256=checker.reference.sha(checker.RUN/'run.log.gz')),
        indent=2)+'\n')
    print(json.dumps(dict(actualFailureConserved=True, nativeRunRestarted=False, sourceSHA256=sha)))


def next_failure(capture, suffix, expected):
    checker.need(suffix.isdecimal(), 'Explicit narrow failure sequence')
    out = checker.ROOT/('audit_native_kano_laser_checker_failure_'+suffix)
    checker.need(not out.exists(), 'Fresh immutable actual subsequent checker failure')
    try:
        checker.inspect(checker.rows(capture['text']), capture['rgbFrames'])
    except ValueError as error:
        checker.need(str(error) == expected, 'Exact actual subsequent failure reproduced')
        failure = traceback.format_exc()
    else:
        raise ValueError('Expected actual checker failure no longer reproduced')
    paths = [Path(checker.__file__).resolve(), Path(__file__).resolve()]
    out.mkdir()
    with gzip.open(out/'failed_executed_sources.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump({str(path):dict(sha256=checker.reference.sha(path),source=path.read_text())
                   for path in paths},stream)
    (out/'report.json').write_text(json.dumps(dict(passed=False, actualCheckerFailure=True,
        nativeRunRestarted=False, originalNativeExit=0, failure=failure,
        sourceHashes={str(path):checker.reference.sha(path)for path in paths},
        originalRunSHA256=checker.reference.sha(checker.RUN/'run.log.gz')),
        indent=2)+'\n')
    print(json.dumps(dict(actualFailureConserved=True,suffix=suffix,nativeRunRestarted=False)))
