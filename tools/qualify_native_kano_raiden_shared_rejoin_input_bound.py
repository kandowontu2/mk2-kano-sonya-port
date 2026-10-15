"""Same retained native trial; correct the verifier's truncated Start interval.

All five actual Start inputs are required, not three from a bounded display
query. Preserve the failed verifier and its traceback. No native replay or
changed gameplay, health, recovery, handoff, visual or scope gates.
"""
import inspect
import json
from pathlib import Path
import qualify_native_kano_raiden_shared_rejoin as failed

ROOT, need, sha, once = failed.ROOT, failed.need, failed.sha, failed.once
FAILURE = ROOT / 'audit_native_kano_raiden_shared_rejoin_qualification_failure/failure.json'


def qualify_and_retire(ram, viewed_frames):
    actual_failure = ram['qualification_failure']
    need(not FAILURE.parent.exists() and not failed.OUT.exists() and
         actual_failure['error'] == "ValueError('Entire actual physical paid/cursor/confirmation input Start')" and
         not actual_failure['nativeTrialChanged'] and actual_failure['nativeBootsAdded'] == 0,
         'Actual retained verifier failure, no gameplay rerun or waiver')
    preserved = dict(actual_failure)
    preserved.update(originalVerifierSourceSHA256=sha(failed.__file__),
                     originalVerifierSource=str(Path(failed.__file__).resolve()),
                     wholeGameTrialUnchanged=True, fullPortAcceptance=False,
                     inputHashes={str(Path(path).resolve()):sha(path)
                                  for path in (failed.__file__, __file__, failed.FOLDER / 'run.log.gz',
                                               failed.FOLDER / 'native_terminal.json')})
    FAILURE.parent.mkdir()
    FAILURE.write_text(json.dumps(preserved, indent=2) + '\n')
    body = inspect.getsource(failed.recovery)
    body = once(body, "('Start', list(range(37903, 37906)))",
                "('Start', list(range(37903, 37908)))")
    scope = dict(vars(failed), __file__=__file__, failure_path=FAILURE,
                 previous_file=failed.__file__)
    exec(compile(body, __file__ + '::whole_original_recovery_exact_five_Start_inputs', 'exec'), scope)
    body = inspect.getsource(failed.qualify_and_retire)
    body = once(body, "    pins = dict(metadata['inputHashes']); pins.update(source['inputHashes'])",
                "    pins = dict(metadata['inputHashes']); pins.update(source['inputHashes'])\n"
                "    for path in (failure_path, Path(previous_file)):\n"
                "        pins[str(path.resolve())] = sha(path)")
    body = once(body, '    proof = dict(passed=True, finiteSingleKanoRaidenVictimAndOrdinaryPaidRecoveryAccepted=True,',
                '    proof = dict(passed=True, previousActualQualificationFailurePreserved=True,\n'
                '                 finiteSingleKanoRaidenVictimAndOrdinaryPaidRecoveryAccepted=True,')
    exec(compile(body, __file__ + '::whole_original_qualification_and_retirement', 'exec'), scope)
    return scope['qualify_and_retire'](ram, viewed_frames)
