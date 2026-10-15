"""Aggregate four full CURRENT cross-Pit live render and raster reviews.

Original full scene/earned/fault gates remain authoritative, not replaced
by this binder. No sound-waveform, later visual-rejoin, mirror, stock-victim,
whole stage-finisher or whole-port acceptance is inferred.
"""
import hashlib
import json
from pathlib import Path
import native_process_census_v6647 as census

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_current_cross_pit_render_matrix_checked'


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def read(path):
    return json.loads(path.read_text())


def run():
    need(not OUT.exists() and not census.census(), 'Fresh matrix after actual native terminals')
    scope_path = ROOT / 'audit_native_paired_stumble_table_bounded_source/report.json'
    scope = read(scope_path)
    need(scope['passed'] and len(scope['originalNaturalIntegrationRequirements']) == 14 and
         len(scope['originalRemainingWorkGroups']) == 6, 'Full original integration objective preserved')
    pins = {}

    def bind(items):
        for path, digest in items.items():
            need(sha(path) == digest, 'Unchanged actual executed source/evidence ' + path)
            need(path not in pins or pins[path] == digest, 'Consistent shared input hashes')
            pins[path] = digest

    bind(scope['inputHashes'])
    cases = []
    for fighter in ('kano', 'sonya'):
        for side in (1, 2):
            leaf = f'audit_native_current_cross_pit_globals_{fighter}_p{side}_render'
            folder, output = ROOT / (leaf+'_ram'), ROOT / (leaf+'_checked')
            report_path = output / 'report.json'
            review_path = output / 'native_visual_review_and_ram_retirement.json'
            meta_path, ledger_path = folder / 'result.json', folder / 'continuous_scene_records.json'
            report, review, meta, ledger = map(read, (report_path, review_path, meta_path, ledger_path))
            own = 17 if fighter == 'kano' else 18
            ids = [own if slot == side else 35-own for slot in (1, 2)]
            need(report['passed'] and review['passed'] and
                 report['candidate'] == meta['candidate'] == 'diagnostic_native_paired_stumble_table_ps7' and
                 report['fighter'] == meta['fighter'] == fighter and report['side'] == meta['side'] == side and
                 report['truePhysicalIDs'] == meta['truePhysicalIDs'] == ids,
                 'Actual current true actors, performer and physical slot')
            need(meta['captureCompleted'] and meta['exit_code'] == 0 and not meta['modelErrors'] and
                 meta['ramGuestSHA256'] == scope['proposedGuestSHA256'] and
                 meta['guest_writes'] == 0 and meta['assistance'] == 'none' and not meta['cheats_enabled'] and
                 (folder/'stderr.log').read_text() == '', 'Whole independently reconstructed current guest and unassisted terminal')
            scene = report['nativeScene']
            movie, physical = scene['movie'], scene['nativeState']
            need(scene['currentLiveContinuousPipelineAccepted'] and
                 scene['historicalReferenceIsPhysicalInputOnly'] and not scene['currentPitAudioWaveformAccepted'] and
                 report['historicalSoundReferenceIsPhysicalInputOnly'] and not report['currentPitAudioWaveformAccepted'] and
                 physical == report['nativePitPhysicalState'] and physical['earned_matches'] == 7 and
                 physical['consecutive_fields'] == 801 and physical['native_action'] == 'FF8BDDE0' and
                 physical['action_frame'] == scene['origin'], 'Whole earned CURRENT live path, no historical waveform or retrospective substitute')
            need(movie['actualID'] == 35-own and movie['nextScreen'] == scene['retired'] and
                 movie['physicalPointerRetirement'] < movie['enter'] < movie['impact'] < movie['originalNativeMode9Exit'] < scene['retired'] and
                 movie['actualMovieAddressRepurposed'] == scene['retired']+8 and
                 movie['fallingGroups'] == 20 and movie['impactGroups'] == movie['initialPreloads'] == 1 and
                 movie['observedPreservedRegisters'] == 7 and
                 len(scene['visibleMoviePoses']) == len(scene['actualMoviePoses']) == 6 and
                 scene['visibleMoviePoses'] == scene['actualMoviePoses'],
                 'Own six visible victim poses, native cadence/initializer/owner and separate cinematic teardown')
            frames = list(range(scene['origin']+1, scene['retired']+31))
            need([row['frame'] for row in ledger] == frames and
                 len(frames) == report['sampledFrames'] == meta['modelExactFields'] == meta['observedRGBFields'] == review['completeSceneFrames'] and
                 report['exactRGBPixels'] == scene['exactRGBPixels'] == review['completeSceneRGBPixels'] == len(frames)*400*254 and
                 all(row['exactVRAMWords'] == 512*512 and row['exactRGBPixels'] == 400*254 for row in ledger),
                 'Every complete consecutive original one-base native render field and pixel')
            need(report['oneInitialBaseOnly'] and report['laterTargetsNeverUsedAsAnchors'] and
                 report['continuousExactPreBuffers'] == report['continuousExactFlips'] > 600 and
                 report['nativeShiftLoads'] == report['nativeShiftFills'] > 600 and
                 report['nativeShiftTransfers'] > 0 and report['fullPhysicalPaletteChecks'] > 0 and
                 report['nativeCrossPaletteSelectors'] == {'1': [False], '2': [False]},
                 'Whole actual original CPU/DMA/FIFO/shift/erase/normal palette pipeline retained')
            policy, ground = scene['actualNativePitShadowPolicy'], scene['actualNativePhaseGround']
            need(scene['wholeNativePitShadowPolicyAccepted'] and policy['passed'] and
                 policy['currentPitShadowSchedulingMatchesOriginal'] and policy['physicalShadowFlagsRetained'] and
                 policy['ownCinematicNoShadowFlagsMatchOriginal'] and
                 policy['actualCurrentFloorShadowCommands'] == scene['nativeShadowCopies'] == review['nativeShadowCopies'] == 0 and
                 all(row['shadowPixels'] == 0 for row in ledger) and
                 ground['passed'] and ground['originalVictimFloorDisplacement'] == 1024 and
                 ground['standingAnchors'] == {'17': 134, '18': 135},
                 'Exact source-native launched floor and independently measured stock Pit shadow omission, not disabled actors')
            need(len(scene['actualMovieFaultsRejected']) == 31 and
                 len(scene['actualEarnedFaultsRejected']) == 12 and
                 len(scene['actualNativePhaseGroundFaultsRejected']) == 6 and
                 len(policy['actualShadowPolicyFaultsRejected']) == 5 and
                 len(report['sourcePreflight']['rejectedProxyTuples']) == 5 and
                 len(report['actualPixelFaultsRejected']) == 2,
                 'Every original movie/earned/floor/shadow/proxy/actual-pixel fault suite retained')
            viewed = review['individuallyViewedFields']
            by_frame = {row['frame']: row for row in ledger}
            need(len(viewed) == review['originalNativeRasterBuffersReleased'] == 18 and
                 len({row['frame'] for row in viewed}) == 18 and
                 all(row['individuallyViewedOriginalRaster'] and row['rgbSHA256'] == by_frame[row['frame']]['rgbSHA256'] for row in viewed) and
                 review['reviewServerClosed'] and review['originalCaptureRAMDictionaryCleared'] and
                 review['exactTerminalNativeIdentity'] == read(folder/'native_identity.json') and
                 review['exactTerminalNativeIdentity']['ProcessId'] == read(folder/'process.json')['pid'],
                 'Actual individual full raster review, original birth identity and complete RAM retirement')
            need(review['finiteCrossPitSceneOnly'] and not review['currentPitAudioWaveformAccepted'] and
                 not review['laterContinueVisualClearingAccepted'] and review['nativeModeTransitionIsNotDisplayClearProof'] and
                 not report['fullPortAcceptance'] and not review['fullPortAcceptance'] and
                 not report['allMirrorBranchesAndSlotsAccepted'] and not review['allStageFinishersAccepted'] and
                 not report['completeStageVictimAudioAccepted'] and
                 not report['publicPlayableOrReleaseChanged'] and not review['publicPlayableChanged'] and
                 meta['rawImageAudioVRAMROMCopiesWritten'] == report['rawImageAudioVRAMROMCopiesWritten'] == 0 and
                 not any(folder.rglob('*.png')) and not any(folder.rglob('*.wav')) and not any(folder.rglob('*.bin')),
                 'Finite render context only, not broader sounds/visual rejoin/mirrors/stock victims/release')
            bind(report['inputHashes'])
            bind(review['inputHashes'])
            for path in (report_path, review_path, meta_path, ledger_path):
                bind({str(path): sha(path)})
            cases.append(dict(fighter=fighter, physicalSlot=side, truePhysicalIDs=ids,
                              actualCinematicVictim=movie['actualID'], capture=str(folder),
                              renderReport=str(report_path), reviewReceipt=str(review_path),
                              sampledFrames=len(frames), exactRGBPixels=report['exactRGBPixels'],
                              individuallyReviewedAndReleasedRasters=18, originalFaultsRetained=61))
    for path in (Path(__file__).resolve(), Path(census.__file__).resolve(), scope_path):
        bind({str(path): sha(path)})
    result = dict(passed=True, currentBothCharactersBothSlotsOppositeVictimPitRenderAccepted=True,
                  cases=cases, totalConsecutiveRenderFields=sum(row['sampledFrames'] for row in cases),
                  totalExactRGBPixels=sum(row['exactRGBPixels'] for row in cases),
                  originalNativeRastersReviewedAndReleased=sum(row['individuallyReviewedAndReleasedRasters'] for row in cases),
                  currentPitAudioWaveformAccepted=False, laterContinueVisualClearingAccepted=False,
                  allMirrorsAndStockVictimsAccepted=False, allStageFinishersAccepted=False,
                  fullPortAcceptance=False, publicPlayableChanged=False,
                  originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
                  inputHashes=pins, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0, goalStatus='active')
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    result = run()
    print(json.dumps({k:v for k,v in result.items() if k not in
                     ('inputHashes', 'originalNaturalIntegrationRequirements', 'originalRemainingWorkGroups')}, indent=2))
