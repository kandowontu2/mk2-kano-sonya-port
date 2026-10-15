"""Keep full retirement contract; compare JSON-backed tuples/keys canonically."""
import inspect
import json
import traceback
from pathlib import Path
import retire_native_current_tomb_render as previous

FAILURE = Path(previous.census.__file__).resolve().parents[1] / 'audit_native_current_tomb_render_json_retirement_failure'


def retire(ram, viewed_frames):
    if not FAILURE.exists():
        try:
            previous.retire(ram, viewed_frames)
        except ValueError as error:
            previous.need(str(error) == 'Same actually normal terminal and complete accepted native scene',
                          'Exact original retirement comparison failure')
            previous.need(not previous.census.census() and ram['terminal']['exit_code'] == 0 and
                          ram['report']['passed'], 'Actual normal terminal is not the failing condition')
            previous.need(json.loads(json.dumps(ram['report'])) == json.loads((ram['output'] / 'report.json').read_text()) and
                          json.loads(json.dumps(ram['terminal'])) == json.loads((ram['folder'] / 'result.json').read_text()),
                          'Only original tuple/integer-key JSON round-trip representation differs')
            FAILURE.mkdir()
            paths = (Path(previous.__file__), ram['output'] / 'report.json', ram['folder'] / 'result.json')
            (FAILURE / 'failure.json').write_text(json.dumps(dict(passed=False, error=repr(error),
                traceback=traceback.format_exc(), releaseOccurred=False,
                inputHashes={str(p):previous.sha(p) for p in paths}, fullPortAcceptance=False), indent=2) + '\n')
        else:
            raise ValueError('Expected original JSON representation failure no longer reproduces')
    failure = json.loads((FAILURE / 'failure.json').read_text())
    previous.need(not failure['passed'] and all(previous.sha(p) == h for p,h in failure['inputHashes'].items()),
                  'Original failed comparison and actual native results frozen')
    body = inspect.getsource(previous.retire)
    before = "report == ram['report'] and report['passed'] and meta == ram['terminal']"
    previous.need(body.count(before) == 1, 'Exactly the original JSON-backed report comparison')
    body = body.replace(before, "report == json.loads(json.dumps(ram['report'])) and report['passed'] and meta == json.loads(json.dumps(ram['terminal']))", 1)
    before = 'Path(__file__), report_path, meta_path'
    previous.need(body.count(before) == 1, 'Bind full original source and observed failure')
    body = body.replace(before, "Path(__file__), Path(previous.__file__), FAILURE / 'failure.json', report_path, meta_path", 1)
    scope = dict(vars(previous), __file__=__file__, previous=previous, FAILURE=FAILURE)
    exec(compile(body, __file__ + '::entire_original_retirement_JSON_round_trip_only', 'exec'), scope)
    return scope['retire'](ram, viewed_frames)
