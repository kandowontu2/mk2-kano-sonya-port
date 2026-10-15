"""Full original render retirement, plus current Pit movie/ground/shadow scope."""
import inspect
import json
from pathlib import Path
import retire_native_current_tomb_render as original
import retire_native_current_tomb_render_json_checked as canonical

need, sha = original.need, original.sha


def retire(ram, viewed_frames):
    report = ram['report']
    proof = report['nativeScene']
    need(report['passed'] and report['actualCurrentCrossNativePitWholeRenderPaletteShadowEraseAccepted'] and
         not report['currentPitAudioWaveformAccepted'] and report['historicalSoundReferenceIsPhysicalInputOnly'] and
         proof['currentLiveContinuousPipelineAccepted'] and proof['historicalReferenceIsPhysicalInputOnly'] and
         not proof['currentPitAudioWaveformAccepted'], 'Entire actual live current Pit only; no retrospective or audio substitution')
    need(proof['nativeState']['earned_matches'] == 7 and proof['nativeState']['consecutive_fields'] == 801 and
         proof['nativeState']['native_action'] == 'FF8BDDE0' and
         proof['movie']['nextScreen'] == proof['retired'] > proof['movie']['physicalPointerRetirement']+60 and
         proof['movie']['actualMovieAddressRepurposed'] == proof['retired']+8 and
         len(proof['visibleMoviePoses']) == len(proof['actualMoviePoses']) == 6,
         'Original earned seven-match path, six actually visible movie phases and separate physical/cinematic teardown')
    need(len(proof['actualMovieFaultsRejected']) == 31 and
         len(proof['actualEarnedFaultsRejected']) == 12 and
         len(proof['actualNativePhaseGroundFaultsRejected']) == 6 and
         len(proof['actualNativePitShadowPolicy']['actualShadowPolicyFaultsRejected']) == 5 and
         proof['wholeNativePitShadowPolicyAccepted'] and proof['nativeShadowCopies'] == 0 and
         proof['actualNativePhaseGround']['originalVictimFloorDisplacement'] == 1024 and
         proof['actualNativePitShadowPolicy']['currentPitShadowSchedulingMatchesOriginal'],
         'Whole original actual movie, earned-state, phase-ground and independently measured stock shadow fault contracts')
    failure_path = canonical.FAILURE / 'failure.json'
    failure = json.loads(failure_path.read_text())
    need(not failure['passed'] and all(sha(path) == digest for path, digest in failure['inputHashes'].items()),
         'Original JSON comparison failure/source/native results remain preserved')
    body = inspect.getsource(original.retire)
    changes = (
        ("report == ram['report'] and report['passed'] and meta == ram['terminal']",
         "report == json.loads(json.dumps(ram['report'])) and report['passed'] and meta == json.loads(json.dumps(ram['terminal']))"),
        ('finiteCrossTombSceneOnly=True',
         'finiteCrossPitSceneOnly=True, currentPitAudioWaveformAccepted=False, laterContinueVisualClearingAccepted=False, nativeModeTransitionIsNotDisplayClearProof=True'),
        ('Path(__file__), report_path, meta_path',
         'Path(__file__), Path(original.__file__), Path(canonical.__file__), failure_path, report_path, meta_path'),
    )
    for before, after in changes:
        need(body.count(before) == 1, 'Exactly declared full original retirement adaptation')
        body = body.replace(before, after, 1)
    namespace = dict(vars(original), __file__=__file__, original=original,
                     canonical=canonical, failure_path=failure_path)
    exec(compile(body, __file__+'::whole_original_native_raster_retirement_Pit_scope', 'exec'), namespace)
    return namespace['retire'](ram, viewed_frames)
