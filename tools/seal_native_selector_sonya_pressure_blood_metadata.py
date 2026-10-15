"""Preserve the actual storage-only failure and correct its stat property use.

Run in the retained capture host. No native game or proof is rerun; the whole
original source/evidence/pin/compression contract remains unchanged.
"""
import inspect
import json
import sys
import traceback
from pathlib import Path
import seal_native_selector_sonya_pressure_blood as original

ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT / 'audit_native_selector_sonya_pressure_blood_sealed_metadata.json'
FAILURE = ROOT / 'audit_native_selector_sonya_pressure_blood_storage_failure.json'
ORIGINAL_SHA = '5523356FA8755C25BDA97268A951D16EDDE3DD55F1625DE8DEE892C876E760EC'
SCOPE = None


def execute():
    global SCOPE
    need(sha(original.__file__) == ORIGINAL_SHA,
         'Actual executed storage-failure source remains unchanged')
    need(not original.OUT.exists() and not OUT.exists() and not FAILURE.exists(),
         'No original failed seal or successor receipt overwritten')
    error = sys.last_exc
    trace = ''.join(traceback.format_exception(error))
    need(isinstance(error, TypeError) and str(error) == "'int' object is not callable" and
         original.__file__ in trace and 'nvram.stat().st_size()' in trace,
         'Actual retained storage-only exception, never reconstructed gameplay failure')
    FAILURE.write_text(json.dumps(dict(
        passed=False, error=repr(error), traceback=trace,
        executedSource=str(Path(original.__file__).resolve()),
        executedSourceSHA256=ORIGINAL_SHA,
        failedBeforeCompression=True, originalSealAbsent=True,
        nativeGameplayFailure=False, goalStatus='active', fullPortAcceptance=False),
        indent=2) + '\n')
    source = inspect.getsource(original.execute)
    need(source.count('nvram.stat().st_size()==16384') == 1,
         'Only the incorrect stat property call is corrected')
    source = source.replace('nvram.stat().st_size()==16384',
                            'nvram.stat().st_size==16384', 1)
    before = 'files={Path(__file__).resolve(),report_path.resolve()}'
    need(source.count(before) == 1, 'Whole original file inventory retained')
    source = source.replace(before,
        'files={Path(__file__).resolve(),report_path.resolve(),Path(original.__file__).resolve(),FAILURE.resolve()}', 1)
    before = 'wholeObjectiveStillActive=True,newNativeGamesThisEvidenceChain=1)'
    need(source.count(before) == 1, 'Whole original acceptance limits retained')
    source = source.replace(before,
        'wholeObjectiveStillActive=True,newNativeGamesThisEvidenceChain=1,originalStorageTypeErrorPreserved=True)', 1)
    SCOPE = dict(original.__dict__, original=original, FAILURE=FAILURE,
                 OUT=OUT, __file__=__file__)
    exec(compile(source, __file__ + '::whole_original_storage_contract', 'exec'), SCOPE)
    return SCOPE['execute']()
