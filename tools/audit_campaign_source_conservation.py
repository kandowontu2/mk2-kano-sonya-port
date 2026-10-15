"""Recheck complete retained campaigns and quantify current repair exposure.

This does not relabel an old boot as current, or claim current ending audio.
No native boot, build, raw media or public-launcher changes are made.
"""
import datetime
import hashlib
import json
import subprocess
import traceback
from pathlib import Path

import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
import verify_corrected_campaign_terminal_v5234 as p1
import verify_current_kano_p2_campaign_v5623 as k2
import verify_verified_subzero_sonya_p2_campaign_v5690 as s2

ROOT = current.ROOT
OUT = ROOT / 'audit_campaign_source_conservation'
need = current.need


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest().upper()


def seal(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    digest = sha(path)
    subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/F', '/I', '/Q', str(path)],
                   capture_output=True, check=True)
    need(sha(path) == digest, 'Lossless immutable proof compression')


def main():
    need(not OUT.exists() and not native.census(), 'Fresh audit; no live native game')
    OUT.mkdir()
    pins = {str(Path(__file__).resolve()): sha(__file__)}
    cases = []
    try:
        parentpath = ROOT / 'audit_cross_continue_adaptive_progress_storage/report.json'
        parent = json.loads(parentpath.read_text())
        need(parent['passed'] and parent['completedReleasedCrossCharacterStageZeroRoutes'] == 4,
             'Previous turn made verified runtime progress')
        for path, digest in parent['inputHashes'].items():
            need(sha(path) == digest, 'Latest authoritative source/evidence pin: ' + path)
            pins[path] = digest
        pins[str(parentpath)] = sha(parentpath)
        print(json.dumps(dict(checkpointPinsVerified=len(pins), nativeGames=native.census())), flush=True)

        guest = current.expected()
        old = current.prior.old.expected()
        packed = current.prior.repair.expected_guest(old)
        need(current.repair.expected_guest(packed) == guest, 'Entire independently reconstructed repair chain')
        changed = [i for i, (a, b) in enumerate(zip(old, guest)) if a != b]
        spans = [(0xfd700, 0xfd74c), (0xfd750, 0xfd79c),
                 (current.prior.repair.offset(0xff8b5d30), current.prior.repair.offset(0xff8b5d30) + 4),
                 (current.prior.repair.offset(0xff8b6580), current.prior.repair.offset(0xff8b6580) + 4),
                 (0xffbc0, 0xffd80)]
        need(len(changed) == 404 and all(any(lo <= i < hi for lo, hi in spans) for i in changed),
             'Only two packed tables/two operands and the reviewed Kano roll marker/branches')
        oldbuild = ROOT / current.prior.old.NAME
        newbuild = ROOT / current.NAME
        before = json.loads((oldbuild / 'build-info.json').read_text(encoding='utf-8-sig'))
        after = json.loads((newbuild / 'build-info.json').read_text(encoding='utf-8-sig'))
        compiled_before = {str(Path(p).resolve()): h for p, h in before['canonical_source_hashes_at_compile'].items()}
        compiled_after = {str(Path(p).resolve()): h for p, h in after['canonical_source_hashes_at_compile'].items()}
        need(compiled_before.keys() == compiled_after.keys(), 'No added/omitted native compilation inputs')
        deltas = [p for p in compiled_before if compiled_before[p] != compiled_after[p]]
        need({Path(p).name for p in deltas} == {'midtunit_m.cpp', 'midtunit.cpp', 'midtunit.h'},
             'Exactly the fully reviewed guest/audio/sample-registration source deltas')
        # Whole source reconstruction in current.expected() proves all other source text unchanged.
        sample_checks = []
        for path in sorted((oldbuild / 'samples/mk2ks').glob('*.wav')):
            target = newbuild / path.relative_to(oldbuild)
            need(target.is_file() and sha(path) == sha(target), 'Unchanged complete old sample: ' + path.name)
            pins[str(path)] = pins[str(target)] = sha(path)
            sample_checks.append(path.name)
        need(len(sample_checks) == 16, 'All sixteen prior samples, not just announcers')
        need(sha(oldbuild / 'roms/mk2ks/mk2ks.mdata') == sha(newbuild / 'roms/mk2ks/mk2ks.mdata'),
             'Whole graphics/character/endings payload unchanged')
        source = dict(oldCandidate=current.prior.old.NAME, currentCandidate=current.NAME,
                      changedGuestBytes=len(changed), allowedByteSpans=spans,
                      compiledSourceInputCount=len(compiled_after), changedCompiledSources=deltas,
                      unchangedWholeSamples=sample_checks, unchangedWholePayload=True,
                      guestOutsideReviewedRepairSpansByteIdentical=True,
                      allOldRollInstructionsReconstructedExactly=True,
                      sourceImpact={
                          'packed_identifier_repair': 'Projectile task/render-family assignment and challenger cleanup; stock packed rows identical.',
                          'roll_marker': 'Six native words plus four internal branch relocations; old roll instructions conserved, but native timing changes.',
                          'launch_ownership': 'Host sample channels 10..13, both-slot stored actor/Main/health/ID, timer retirement and reset. All launch users and scene boundaries remain exposed.',
                          'sample_registration': 'New sample16 only; prior sample0..15 files and registration order preserved.'},
                      conservedButNotFreshRuntime=['Tower order and true IDs; native health/winner/continue/boss/ending guest instructions outside listed spans',
                                                  'Ending photos, story/font/shadow/background payload and native graphics/scanout implementation',
                                                  'Existing stock DCS dispatch, sample0..15 waveform data, ordinary/finisher/stage/secret guest code outside listed spans'],
                      notTransferred=['Full old waveform or same-timing claim for a run that executes Kano roll',
                                      'Current whole campaign/ending/attract runtime or post-ending fresh-join audio acceptance'])
        seal(OUT / 'source_conservation.json', source)
        print(json.dumps(dict(sourceConserved=True, changedGuestBytes=404, oldSamplesUnchanged=16)), flush=True)

        # Run the complete original verifier functions, not just read their green receipts.
        # Only OUT is an unused freshness sentinel; these functions return proofs, not files.
        k2.OUT = OUT / 'unused_kano_p2_freshness_sentinel'
        s2.OUT = OUT / 'unused_sonya_p2_freshness_sentinel'
        jobs = [('kano', 1, lambda: p1.run('kano')),
                ('sonya', 1, lambda: p1.run('sonya')),
                ('kano', 2, k2.whole_run), ('sonya', 2, s2.whole_run)]
        for fighter, side, run in jobs:
            print(json.dumps(dict(startedRetainedWholeGate=fighter, side=side)), flush=True)
            proof = run()
            case = proof['case']
            need(proof['passed'] and case['passed'] and case['unassisted_clear_proven'] and
                 case['stages_reached'] == list(range(13)) + [14, 15, 16] and not case['errors'],
                 'Whole original native button-only campaign/boss/ending/attract gate')
            for path, digest in proof['inputHashes'].items():
                need(sha(path) == digest and (path not in pins or pins[path] == digest),
                     'Actual complete retained campaign input pin: ' + path)
                pins[path] = digest
            summary = dict(fighter=fighter, side=side, oldNativeCandidate=current.prior.old.NAME,
                           wholeOriginalGateExecutedAgain=True, nativeCase=case,
                           currentNativeBootClaim=False,
                           faultCount=len(proof.get('actualNativeAndRAMProofFaultsRejected',
                                                   proof.get('actualCurrentRowFaultsRejected', []))))
            # Native case contains the original complete provenance map; keep it compressed.
            seal(OUT / f'{fighter}_p{side}_retained_gate.json', summary)
            cases.append({k: v for k, v in summary.items() if k != 'nativeCase'})
            print(json.dumps(dict(retainedWholeGatePassed=fighter, side=side,
                                  stages=case['stages_reached'], faults=summary['faultCount'])), flush=True)

        need(not native.census(), 'Read-only audit never started a native game')
        for path in OUT.iterdir():
            if path.is_file(): pins[str(path)] = sha(path)
        report = dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      previousGoalTurnClassification='progress: four actual released cross-continues and native UI/controls qualified',
                      thisGoalTurnClassification='progress: complete retained four-campaign gates rerun, exact current source repair exposure quantified; old campaign/ending code is not an untouched work group',
                      sourceConservation=str(OUT / 'source_conservation.json'), cases=cases,
                      currentWholeCampaignRuntimeAccepted=False, fullPortAcceptance=False, goalStatus='active',
                      nextAction='Use conserved campaign/ending/render code as retained coverage, not a fresh current boot. Focus remaining runtime on scene-boundary launch ownership/audio and uncovered secret/cinematic/stock-victim branches; then final combined playable regression and matching CMD/ZIP.',
                      newNativeBoots=0, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                      publicPlayableChanged=False, inputHashes=pins)
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                      completedCases=cases, fullPortAcceptance=False, goalStatus='active', inputHashes=pins)
    seal(OUT / 'report.json', report)
    print(json.dumps({k: v for k, v in report.items() if k not in ('inputHashes', 'traceback')}), flush=True)
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
