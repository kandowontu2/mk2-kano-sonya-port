"""Preserve original Pit preflight failure; restore complete helper globals.

No movie, raster, grounding, stock-shadow or fault predicate changes.
"""
import argparse
import code
import inspect
import json
import traceback
from pathlib import Path
import run_native_current_cross_pit_render as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
RAM = {}
FAILURE = ROOT / 'audit_native_current_cross_pit_kano_p1_render_checked/report.json'


def paths(fighter, side):
    need(fighter in ('kano', 'sonya') and side in (1, 2), 'Exact true character/physical slot')
    leaf = f'audit_native_current_cross_pit_globals_{fighter}_p{side}_render'
    return ROOT / (leaf+'_ram'), ROOT / (leaf+'_checked')


def functions():
    failure = json.loads(FAILURE.read_text())
    need(not failure['passed'] and failure['error'] == 'NameError("name \'once\' is not defined")' and
         '::whole_passive_Pit_controls' in failure['traceback'] and
         not (ROOT/'audit_native_current_cross_pit_kano_p1_render_ram').exists(),
         'Exact immutable original helper-binding failure happened before native boot')
    namespace = dict(vars(previous), __file__=__file__, RAM=RAM, paths=paths,
                     original_file=previous.__file__, failure_path=FAILURE)
    body = inspect.getsource(previous.initialize)
    before = "leaf = f'audit_native_current_cross_pit_{fighter}_p{side}_render'"
    need(body.count(before) == 1, 'Exactly fresh independent initializer paths')
    body = body.replace(before, "leaf = f'audit_native_current_cross_pit_globals_{fighter}_p{side}_render'", 1)
    before = 'pins = dict(historical[\'inputHashes\'])'
    need(body.count(before) == 1, 'Preserve original executed source/failure in whole input manifest')
    body = body.replace(before, before+"\n    pins[str(Path(original_file))] = sha(original_file)\n    pins[str(failure_path)] = sha(failure_path)", 1)
    exec(compile(body, __file__+'::whole_current_initializer_fresh_paths_and_failure_pins', 'exec'), namespace)
    body = inspect.getsource(previous.functions)
    before = 'namespace = dict(previous.run.__globals__, __file__=__file__, __doc__=__doc__,'
    need(body.count(before) == 1, 'Only original missing helper globals are restored')
    body = body.replace(before,
        'namespace = dict({**previous.controls.__globals__, **previous.preflight.__globals__, **previous.run.__globals__}, __file__=__file__, __doc__=__doc__,', 1)
    exec(compile(body, __file__+'::whole_original_Pit_factory_with_complete_original_namespaces', 'exec'), namespace)
    return namespace


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fighter', choices=('kano', 'sonya'), required=True)
    parser.add_argument('--side', type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    folder, output = paths(args.fighter, args.side)
    need(not folder.exists() and not output.exists(), 'Fresh immutable complete-Pit-global successor')
    try:
        namespace = functions()
        current = namespace['initialize'](args.fighter, args.side)
        scope = namespace['functions'](current)
        report = scope['run'](args.fighter, args.side)
        report.update(currentPitAudioWaveformAccepted=False, historicalSoundReferenceIsPhysicalInputOnly=True,
                      originalPhaseGroundAndStockShadowContractSHA256=previous.contract.CONTRACT_SOURCE_SHA256)
        RAM['report'] = report
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                      fullPortAcceptance=False, currentPitAudioWaveformAccepted=False, goalStatus='active')
        print(json.dumps(report), flush=True)
    need(not output.exists(), 'Never replace current full-Pit outcome')
    output.mkdir()
    (output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    if report['passed']:
        print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes', 'nativeScene')}, indent=2), flush=True)
        RAM['server'] = previous.review.start(RAM['images'], folder)
    code.interact(banner='Same current Pit successor; original bounded RGB stays in RAM.', local=dict(RAM=RAM))
