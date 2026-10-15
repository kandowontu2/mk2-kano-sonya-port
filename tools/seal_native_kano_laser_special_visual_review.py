"""Seal 64 individually reviewed original native special rasters, without replay."""
import hashlib
import json
from pathlib import Path
import capture_native_kano_laser_audio as current


def seal(cases):
    root = current.ROOT
    source = root / 'audit_native_kano_laser_special_shadow_checked/report.json'
    out = root / 'audit_native_kano_laser_special_visual_review'
    current.need(not out.exists(), 'Fresh immutable visual receipt')
    report = json.loads(source.read_text())
    current.need(report['passed'] and report['actualCases'] == 16 and
                 report['actualVerifiedSpecialCycles'] == 32 and
                 report['originalSpecialFaults'] == 194 and
                 len(report['originalShadowFaults']) == 176 and
                 report['everyReadyOwnedBodyShadowFieldSourceBound'] and
                 not report['actualSquareContactVerified'] and
                 report['candidate'] == current.NAME, 'Full current finite physical/body/shadow gates')
    for group in ('inputHashes', 'outputHashes'):
        current.need(all(current.sha(p) == h for p, h in report[group].items()),
                     'Executed inputs and actual terminal evidence unchanged')
    current.need(set(cases) == {f'{move}_p{side}' for move in
                 ('ball', 'knife', 'blade', 'choke', 'ring', 'square', 'bicycle', 'leg')
                 for side in (1, 2)}, 'All original sixteen native captures')
    records = []
    for case in report['cases']:
        key = f"{case['move']}_p{case['side']}"
        folder, text, images = cases[key]
        selected = [s for s in case['actualScenes'] if s['stage'] == 'phase_16' or
                    (s['attempt'] == 2 and s['stage'] in ('special_recovered', 'special_final'))]
        current.need(len(selected) == 4, 'Both activations, second recovery, and physical follow-up viewed')
        for scene in selected:
            pixels = images[f"ui_{scene['frame']:04d}.png"]
            current.need(pixels.shape == (254, 400, 3), 'Original unscaled native raster')
            records.append(dict(case=key, frame=scene['frame'], attempt=scene['attempt'],
                                stage=scene['stage'], sourceRawBGRXSHA256=scene['sha256'],
                                nativeRGBSHA256=hashlib.sha256(pixels.tobytes()).hexdigest().upper(),
                                individuallyViewed=True))
    current.need(len(records) == 64, 'All 64 selected original rasters individually reviewed')
    value = dict(passed=True, candidate=current.NAME, sourceReportSHA256=current.sha(source),
                 reviewSourceSHA256=current.sha(Path(__file__)), sampledNativeRasters=records,
                 observations=['Own Kano/Sonya bodies and MK2 lifebar names remain in both player slots',
                               'Move poses, opponent reactions, and later normal poses render without persistent selection overlays',
                               'Black floor shadows visible under moving/grounded actors in the sampled Prison frames',
                               'Square Wave crosses over the grounded opponent and recovers; these samples are not airborne-contact proof'],
                 requirements=['selection', 'transition', 'identity', 'names', 'human_moves', 'cpu_moves',
                               'ordinary_combat', 'ground_shadows', 'audio', 'finishers_victims',
                               'stage_finishers', 'campaign_cinematics', 'cmd_release', 'storage'],
                 remainingGroups=['startup_audio_full_UI_ground', 'broader_CPU_projectile_arena_shadow_audio',
                                  'stage_reselect_rejoin_postending', 'Pit_Tomb_stock_victims_sound_priority',
                                  'secret_morph_cinematic', 'combined_acceptance_CMD_finished_ZIP'],
                 finiteSpecialVisualReviewAccepted=True, actualSquareContactVerified=False,
                 fullVisualTimelineAccepted=False, allArenasAccepted=False, fullAudioAcceptance=False,
                 fullPortAcceptance=False, publicPlayableChanged=False, newBuilds=0,
                 newNativeBoots=0, newROMCopies=0, newRawMedia=0, newZIPs=0, goalStatus='active')
    out.mkdir()
    (out / 'report.json').write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(dict(passed=True, individuallyViewedNativeRasters=64, fullPortAcceptance=False)), flush=True)
    return value
