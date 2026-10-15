"""Run each remaining actual Tomb case with its own fresh manifest preflight.

The original preflight hardcodes Kano P1 and rejects after that capture exists.
Keep the whole collector, source/audio gates and physical inputs unchanged;
select only the requested case when checking its actual manifest before boot.
"""
import argparse
import code
import json
import traceback
from pathlib import Path
import prepare_native_cross_tomb_19_audio_manifest_checked as original

ROOT, need, sha = original.ROOT, original.need, original.sha
FAILURE = ROOT / 'audit_native_cross_tomb_19_audio_completed_case_preflight_failure'
RAM = original.RAM


def preflight(scope, fighter, side):
    if not FAILURE.exists():
        try:
            original.preflight(scope)
        except ValueError as error:
            need(str(error) == 'Fresh immutable actual capture',
                 'Exact observed hardcoded completed-case preflight failure')
            FAILURE.mkdir()
            (FAILURE / 'failure.json').write_text(json.dumps(dict(
                passed=False, error=repr(error), traceback=traceback.format_exc(),
                failureBeforeNativeBoot=True, nativeBoots=0,
                inputHashes={str(Path(original.__file__)): sha(original.__file__),
                             str(original.SOURCE / 'report.json'): sha(original.SOURCE / 'report.json')},
                fullPortAcceptance=False), indent=2) + '\n')
        else:
            raise ValueError('Expected original completed-case failure no longer reproduces')
    failure = json.loads((FAILURE / 'failure.json').read_text())
    need(not failure['passed'] and all(sha(p) == h for p, h in failure['inputHashes'].items()),
         'Original rejected preflight source and result frozen')
    scope['source_guard']()
    fn = scope['collector'](scope['context']())
    prefix = fn.source[:fn.source.index('    folder.mkdir();')] + '    return len(files),pins\n'
    namespace = dict(fn.__globals__)
    exec(compile(prefix, __file__ + '::whole_actual_requested_case_manifest', 'exec'), namespace)
    count, pins = namespace['capture'](fighter, side, True, None)
    need(count > 100 and all(sha(p) == h for p, h in pins.items()),
         'Entire actual requested-case input manifest validates before native boot')
    print(json.dumps(dict(passed=True, fighter=fighter, physicalSlot=side,
                         actualWholeInputManifestFiles=count, newNativeBoots=0)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fighter', choices=('kano', 'sonya'), required=True)
    parser.add_argument('--side', type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    scope = original.functions()
    preflight(scope, args.fighter, args.side)
    try:
        scope['run'](args.fighter, args.side)
    except Exception as error:
        folder = RAM.get('folder', ROOT / f'{original.PREFIX}{args.fighter}_p{args.side}_samples')
        failure = folder / 'current_19_audio_failure.json'
        if folder.exists() and not failure.exists():
            failure.write_text(json.dumps(dict(passed=False, error=repr(error),
                traceback=traceback.format_exc(), fullPortAcceptance=False), indent=2) + '\n')
        print(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc())), flush=True)
    code.interact(banner='Same actual requested Tomb case; raw sound retained only in RAM.', local=dict(RAM=RAM))
