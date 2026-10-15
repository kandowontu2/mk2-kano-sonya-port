"""Bind all four current finite opposite-victim Tomb render/audio cases.

This is aggregation of original full scene, earned-state and fault evidence,
not replacement of those gates or acceptance of unobserved slots/branches.
"""
import hashlib
import json
from pathlib import Path
import native_process_census_v6647 as census

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_current_cross_tomb_render_matrix_checked'


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
    audio_path = ROOT / 'audit_native_cross_tomb_19_audio_matrix_checked/report.json'
    scope, audio = read(scope_path), read(audio_path)
    need(scope['passed'] and len(scope['originalNaturalIntegrationRequirements']) == 14 and
         len(scope['originalRemainingWorkGroups']) == 6 and audio['passed'] and
         audio['totalSampleChannels'] == 19 and len(audio['cases']) == 4,
         'Whole original integration scope and current all19 sound matrix preserved')
    pins = {}

    def bind(items):
        for path, digest in items.items():
            need(sha(path) == digest, 'Unchanged actual source/evidence ' + path)
            need(path not in pins or pins[path] == digest, 'Consistent common executed input')
            pins[path] = digest

    bind(scope['inputHashes'])
    bind(audio['inputHashes'])
    cases = []
    for fighter in ('kano', 'sonya'):
        for side in (1, 2):
            leaf = f'audit_native_current_cross_tomb_{fighter}_p{side}_render'
            folder, output = ROOT / (leaf + '_ram'), ROOT / (leaf + '_checked')
            report_path, review_path = output / 'report.json', output / 'native_visual_review_and_ram_retirement.json'
            meta_path, ledger_path = folder / 'result.json', folder / 'continuous_scene_records.json'
            report, review, meta, ledger = map(read, (report_path, review_path, meta_path, ledger_path))
            sound = next(q for q in audio['cases'] if q['fighter'] == fighter and q['physicalSlot'] == side)
            own = 17 if fighter == 'kano' else 18
            ids = [own if slot == side else 35-own for slot in (1, 2)]
            need(report['passed'] and review['passed'] and
                 report['candidate'] == meta['candidate'] == 'diagnostic_native_paired_stumble_table_ps7' and
                 report['fighter'] == meta['fighter'] == fighter and report['side'] == meta['side'] == side and
                 report['truePhysicalIDs'] == meta['truePhysicalIDs'] == ids,
                 'Actual true opposite actors, performer and physical slot')
            need(meta['captureCompleted'] and meta['exit_code'] == 0 and not meta['modelErrors'] and
                 meta['ramGuestSHA256'] == audio['guestSHA256'] == scope['proposedGuestSHA256'] and
                 meta['guest_writes'] == 0 and meta['assistance'] == 'none' and not meta['cheats_enabled'] and
                 (folder / 'stderr.log').read_text() == '', 'Whole current guest and ordinary native terminal')
            need(report['nativeBranch'] == sound['sourceQualifiedNativeBranch'] and
                 report['nativeBranch']['trueVictim'] == 35-own and
                 report['nativeScene']['truePhysicalIDs'] == ids,
                 'Exact actual independently accepted sound/RNG/motion/ownership branch')
            scene = report['nativeScene']
            frames = list(range(scene['origin']+1, scene['retired']+31))
            need([q['frame'] for q in ledger] == frames and
                 len(frames) == report['sampledFrames'] == meta['observedRGBFields'] == meta['modelExactFields'] == review['completeSceneFrames'] and
                 report['exactRGBPixels'] == review['completeSceneRGBPixels'] == len(frames)*400*254 and
                 all(q['exactVRAMWords'] == 512*512 and q['exactRGBPixels'] == 400*254 for q in ledger),
                 'Every consecutive full original native render field, no omissions')
            need(report['oneInitialBaseOnly'] and report['laterTargetsNeverUsedAsAnchors'] and
                 report['continuousExactFlips'] == report['continuousExactPreBuffers'] > 400 and
                 report['nativeShiftLoads'] == report['nativeShiftFills'] > 400 and
                 report['nativeShiftTransfers'] > 0 and report['fullPhysicalPaletteChecks'] > 0 and
                 scene['nativeShadowCopies'] == review['nativeShadowCopies'] > 0 and
                 report['nativeCrossPaletteSelectors'] == {'1': [False], '2': [False]},
                 'Entire original source-render/erase/physical palette/shadow proof retained')
            need(len(report['actualEarnedFaultsRejected']) == 12 and
                 len(report['actualOriginalBranchFaultsRejected']) == 4 and
                 len(report['sourcePreflight']['rejectedProxyTuples']) == 5 and
                 len(report['actualPixelFaultsRejected']) == 2 and
                 len(report['actualDropPhaseFaultsRejected']) == (4 if report['nativeBranch']['nativeDrop'] else 0),
                 'Full actual original state, branch, proxy, phase and pixel counterexamples')
            viewed = review['individuallyViewedFields']
            by_frame = {q['frame']: q for q in ledger}
            need(len(viewed) == review['originalNativeRasterBuffersReleased'] == 11 and
                 len({q['frame'] for q in viewed}) == 11 and
                 all(q['individuallyViewedOriginalRaster'] and q['rgbSHA256'] == by_frame[q['frame']]['rgbSHA256'] for q in viewed) and
                 review['reviewServerClosed'] and review['originalCaptureRAMDictionaryCleared'] and
                 review['exactTerminalNativeIdentity'] == read(folder / 'native_identity.json') and
                 review['exactTerminalNativeIdentity']['ProcessId'] == read(folder / 'process.json')['pid'],
                 'Actual individual original raster review, exact native birth and RAM retirement')
            need(not report['fullPortAcceptance'] and not review['fullPortAcceptance'] and
                 not report['allMirrorBranchesAndSlotsAccepted'] and not review['allStageFinishersAccepted'] and
                 not report['publicPlayableOrReleaseChanged'] and not review['publicPlayableChanged'] and
                 meta['rawImageAudioVRAMROMCopiesWritten'] == report['rawImageAudioVRAMROMCopiesWritten'] == 0 and
                 not any(folder.rglob('*.png')) and not any(folder.rglob('*.wav')) and not any(folder.rglob('*.bin')),
                 'Finite observed context only; no raw recording, release or broader substitution')
            bind(report['inputHashes'])
            bind(review['inputHashes'])
            for path in (report_path, review_path, meta_path, ledger_path):
                bind({str(path): sha(path)})
            cases.append(dict(fighter=fighter, physicalSlot=side, truePhysicalIDs=ids,
                              capture=str(folder), renderReport=str(report_path), reviewReceipt=str(review_path),
                              sampledFrames=len(frames), exactRGBPixels=report['exactRGBPixels'],
                              actualRandomValue=report['nativeBranch']['actualNativeRandomValue'],
                              observedNativeDrop=report['nativeBranch']['nativeDrop'],
                              nativeShadowCopies=scene['nativeShadowCopies'], individuallyViewedFrames=11))
    for path in (Path(__file__).resolve(), Path(census.__file__).resolve(), scope_path, audio_path):
        bind({str(path): sha(path)})
    result = dict(passed=True, currentBothFightersBothPhysicalSlotsOppositeVictimTombRenderAccepted=True,
                  sameObservedCurrent19ChannelAudioBound=True, cases=cases,
                  totalConsecutiveRenderFields=sum(q['sampledFrames'] for q in cases),
                  totalExactRGBPixels=sum(q['exactRGBPixels'] for q in cases),
                  originalNativeRastersReviewedAndReleased=sum(q['individuallyViewedFrames'] for q in cases),
                  allBranchesForEverySlotAccepted=False, allMirrorsAndStockVictimsAccepted=False,
                  allStageFinishersAccepted=False, laterRejoinForEveryCaseAccepted=False,
                  fullPortAcceptance=False, publicPlayableChanged=False,
                  originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
                  inputHashes=pins, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                  goalStatus='active')
    OUT.mkdir()
    (OUT / 'report.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    result = run()
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('inputHashes', 'originalNaturalIntegrationRequirements', 'originalRemainingWorkGroups')}, indent=2))
