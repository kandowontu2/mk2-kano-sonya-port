"""Apply the original 78 real corruption tests to the corrected candidate capture.

Only proof addresses/case keys and envelope shape change. All mutation bodies,
original positive controls and rejection assertions remain unchanged.
"""
import inspect
import json
import sys
import traceback
from pathlib import Path
from unittest.mock import patch
import verify_current_cpu_square_v3280 as current
import test_native_cpu_square_hit_v3042 as phase_test
import test_native_cpu_square_render_v3083 as render_test
import test_native_cpu_square_hit_erase_v3052 as erase_test
import current_cpu_capture_contract_v3270 as snapshots

ROOT = current.ROOT
OUT = ROOT / 'audit_v3286_current_cpu_square_counterexamples'

def adapt(function, replacements):
    source = inspect.getsource(function)
    for before, after in replacements:
        current.need(source.count(before) == 1, 'Exactly one declared proof-address adaptation: ' + before)
        source = source.replace(before, after)
    namespace = dict(function.__globals__)
    exec(compile(source, str(Path(__file__).resolve()) + '::' + function.__module__, 'exec'), namespace)
    return namespace[function.__name__]

def snapshot_tests():
    folder = ROOT / current.CASE
    map_path = folder / 'source_snapshot_paths.json'
    mapping = json.loads(map_path.read_text(encoding='utf-8-sig'))
    before = json.loads((folder / 'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    reports = [file for file in mapping if Path(file).name == 'report.json']
    current.need(len(reports) >= 2, 'Actual captured basename collision exists')
    file = reports[0]
    def pin(path, wanted=None):
        actual = current.assembly.sha(path)
        current.need(wanted is None or actual == wanted, 'Actual frozen source bytes unchanged')
    original_read = Path.read_text
    def check(altered):
        def reader(path, *args, **kwargs):
            return json.dumps(altered) if path == map_path else original_read(path, *args, **kwargs)
        with patch.object(Path, 'read_text', reader):
            snapshots.pin_snapshot(folder, file, before[file], pin)
    tests = []
    variants = []
    removed = dict(mapping); removed.pop(file)
    variants.append(('missing original JSON snapshot', removed))
    extra = dict(mapping); extra[str(ROOT/'invented.json')] = str(folder/'input_sources/tree/invented.json')
    variants.append(('invented snapshot entry', extra))
    duplicate = dict(mapping); duplicate[file] = mapping[reports[1]]
    variants.append(('different report.json inputs share a snapshot', duplicate))
    flat = dict(mapping); flat[file] = str(folder/'input_sources/report.json')
    variants.append(('old flat JSON basename address', flat))
    external = dict(mapping); external[file] = str(ROOT/'report.json')
    variants.append(('snapshot outside capture tree', external))
    wrong = dict(mapping); wrong[file] = str(folder/'input_sources/tree/wrong/report.json')
    variants.append(('wrong original source hierarchy', wrong))
    other = dict(mapping); other[file] = str(ROOT/'audit_v3264_current_native_cpu_square_hit/input_sources/tree/report.json')
    variants.append(('snapshot borrowed from different capture', other))
    missing_lua = dict(mapping); missing_lua.pop(next(p for p in mapping if Path(p).suffix == '.lua'))
    variants.append(('missing original Lua snapshot', missing_lua))
    for label, altered in variants:
        current.need(altered != mapping, 'Actual nonvacuous snapshot-address mutation')
        try:
            check(altered)
        except ValueError as error:
            current.need(str(error) in (
                'All original snapshots distinct and complete, no basename aliases for JSON',
                'Exact immutable before-run original-source hierarchy'), 'Specific snapshot rejection, not an unrelated failure')
            tests.append(dict(name=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('Accepted corrupt actual source snapshot mapping: '+label)
    for selected in mapping:
        snapshots.pin_snapshot(folder, selected, before[selected], pin)
    return tests

def run():
    positive_path = current.OUT / 'report.json'
    positive = json.loads(positive_path.read_text())
    current.need(positive['passed'] and positive['candidate'] == current.current.CANDIDATE and
                 positive['fullCurrentSquareHitPhaseArtShadowEraseAccepted'] and
                 not positive['fullPortAcceptance'], 'Completed corrected candidate proof required')
    expected = current.expected_current()
    current.assembly.NAME = current.current.CANDIDATE
    current.assembly.expected = lambda: expected
    phase_test.model.OUT = current.STATE_OUT
    render_test.model = current.render
    render_test.model.CASES = {'current_kano': (current.CASE, 'new', 'kano')}
    phase_result = adapt(phase_test.verify, [("proof['cases']['new_kano']", "proof['cases']['current_kano']")])()
    render_result = adapt(render_test.run, [
        ("checked=ROOT/f'audit_v3013_native_cpu_square_render_{player}_checked/report.json'", "checked=ROOT/'audit_v3282_current_cpu_square_render_erase_checked/report.json'"),
        ("proof=json.loads(checked.read_text());", "proof=json.loads(checked.read_text())['scene'];"),
        ("assert len(tests)==32,", "assert len(tests)==16,"),
        ("candidate='diagnostic_v2753_native_friendship_palette'", "candidate='diagnostic_v3172_native_morph_shadow'")])()
    current.erase.source_contract()
    erase_result = adapt(erase_test.run, [
        ("path=ROOT/'audit_v3047_native_cpu_square_hit_erase_checked/report.json'", "path=ROOT/'audit_v3282_current_cpu_square_render_erase_checked/report.json'"),
        ("proof['originalContinuousReplayContractUnchanged'] and\n         proof['oneInitialBaseOnlyPerActualFixture']", "proof['erase']['oneInitialBaseOnly']"),
        ("render={'cases':proof['cases']}", "render={'cases':{'new_kano':{**proof['erase'],'case':proof['case'],'candidate':proof['candidate']}}}"),
        ("proof['cases'][key][k]", "proof['erase'][k]"),
        ("groups,buffers,a,b,owners=model.raster.data(folder)",
         "groups,buffers,a,b,owners=model.raster.data(folder)\n        with patch.object(model.raster,'data',return_value=copy.deepcopy((groups,buffers,a,b,owners))):\n            positive=model.inspect(folder,image,case['candidate'])\n        need(positive['passed'] and positive['continuousExactFlips']==case['continuousExactFlips'],'Same mocked-path erase positive control')")])()
    snapshot_result = snapshot_tests()
    current.need(phase_result['actualCounterexamplesRejected'] == 44 and
                 render_result['actualCounterexamplesRejected'] == 16 and
                 erase_result['actualOriginalEraseCounterexamplesRejected'] == 18 and
                 len(snapshot_result) == 8 and render_result['sameMockedPathPositiveControlAccepted'] and
                 render_result['unrelatedMissingEventExceptionsNeverAccepted'], 'All original 78 gameplay/raster/erase plus 8 collision-free snapshot tests')
    pins = dict(positive['inputHashes'])
    pins[str(positive_path)] = current.assembly.sha(positive_path)
    for result in (phase_result, render_result, erase_result):
        for file, digest in result['inputHashes'].items():
            current.need(file not in pins or pins[file] == digest, 'Consistent executed proof pins')
            pins[file] = digest
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools') and Path(file).suffix == '.py':
            pins[str(Path(file).resolve())] = current.assembly.sha(file)
    for file, digest in pins.items():
        current.need(current.assembly.sha(file) == digest, 'Actual sources and captures unchanged after counterexamples')
    return dict(passed=True, candidate=current.current.CANDIDATE, case=current.CASE,
                actualGameplayRasterEraseCounterexamplesRejected=78,
                actualSnapshotMappingCounterexamplesRejected=8,
                unmodifiedPositiveControlsAccepted=True, sameMockedPathRenderAndErasePositiveControlsAccepted=True,
                unrelatedMissingEventExceptionsNeverAccepted=True, actualCapturesUnmodified=True,
                phase=phase_result['counterexamples'], render=render_result['counterexamples'],
                erase=erase_result['counterexamples'], snapshots=snapshot_result,
                gameBytesChanged=False, allCPUContextsArenasKOOverlapAudioAccepted=False,
                fullPortAcceptance=False, inputHashes=pins)

if __name__ == '__main__':
    current.need(not OUT.exists(), 'Immutable current-candidate negative evidence')
    try:
        value = run()
    except Exception as error:
        value = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), fullPortAcceptance=False)
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(value, indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items() if k not in ('inputHashes','phase','render','erase','snapshots')}, indent=2), flush=True)
    raise SystemExit(0 if value['passed'] else 1)
