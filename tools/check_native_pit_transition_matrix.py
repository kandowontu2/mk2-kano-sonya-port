"""Consolidate four original earned Pit/paid-rejoin captures, not port completion.

Retain the entire initial Pit contract and original later native state, input,
health and semantic fault suites. Later completed scanout is source-defined;
it is not an independent later CPU/DMA model or an initial-model anchor.
"""
import gzip
import inspect
import json
from pathlib import Path
import check_native_tomb_transition_matrix as original
import retire_native_tomb_transition_scanout as retirement_reference

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_pit_transition_matrix_checked'
need, sha, read = original.need, original.sha, original.read


def state_and_faults(text, states, ids):
    body = inspect.getsource(original.original_state.retire)
    begin = body.index('    facts = state_facts(text,states)')
    end = body.index('    need(set(viewed_later_frames)', begin)
    code = 'def actual_states(text,states):\n' + body[begin:end] + '    return facts,rejected\n'
    namespace = dict(vars(original.original_state), state_facts=original.state_gate(ids))
    exec(compile(code, __file__ + '::whole_original_state_input_health12_faults', 'exec'), namespace)
    return namespace['actual_states'](text, states)


def run():
    need(not OUT.exists() and not original.census.census(),
         'Fresh consolidation only after all four real native terminals')
    scope_path = ROOT / 'audit_native_paired_stumble_table_bounded_source/report.json'
    scope = read(scope_path)
    need(scope['passed'] and len(scope['originalNaturalIntegrationRequirements']) == 14 and
         len(scope['originalRemainingWorkGroups']) == 6, 'Full original natural-integration objective intact')
    pins = {}

    def bind(items):
        for path, digest in items.items():
            need(sha(path) == digest and (path not in pins or pins[path] == digest),
                 'Exact frozen native/source/proof bytes ' + path)
            pins[path] = digest

    bind(scope['inputHashes'])
    for name in ('audit_native_current_cross_pit_render_matrix_checked',
                 'audit_native_current_pit_19_four_owned_audio_checked',
                 'audit_native_tomb_transition_matrix_checked'):
        path = ROOT / name / 'report.json'
        proof = read(path)
        need(proof['passed'] and not proof['fullPortAcceptance'], 'Whole prior finite proofs stay frozen')
        bind(proof['inputHashes'])
        bind({str(path): sha(path)})

    cases = []
    for fighter in ('kano', 'sonya'):
        for side in (1, 2):
            folder = ROOT / f'audit_native_pit_transition_rejoin_direct_{fighter}_p{side}_ram'
            output = ROOT / f'audit_native_pit_transition_rejoin_direct_{fighter}_p{side}_checked'
            report_path = output / 'report.json'
            retire_path = output / 'native_effective_scanout_visual_review_and_ram_retirement.json'
            meta_path, identity_path = folder / 'result.json', folder / 'native_identity.json'
            base_path = output.parent / (output.name + '_original_scene_report.json')
            report, retired, meta, identity, base = map(read, (report_path, retire_path, meta_path, identity_path, base_path))
            own = 17 if fighter == 'kano' else 18
            ids = [own if slot == side else 35 - own for slot in (1, 2)]
            need(report['passed'] and base['passed'] and retired['passed'] and
                 report['fighter'] == meta['fighter'] == retired['performer'] == fighter and
                 report['side'] == meta['side'] == retired['physicalSlot'] == side and
                 report['candidate'] == meta['candidate'] == 'diagnostic_native_paired_stumble_table_ps7' and
                 report['truePhysicalIDs'] == meta['truePhysicalIDs'] == ids and
                 meta['ramGuestSHA256'] == scope['proposedGuestSHA256'] and
                 meta['executable_sha256'] == 'E56DD49DB8B918BC1DF806E3C70C34A557716116DCAADB2F683532DBACAFBD3D' and
                 meta['payload_sha256'] == 'A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3',
                 'Same actual current executable, whole guest, payload and true physical characters')
            process = read(folder / 'process.json')
            command = process['command']
            need(meta['captureCompleted'] and meta['exit_code'] == 0 and not meta['modelErrors'] and
                 meta['guest_writes'] == 0 and meta['assistance'] == 'none' and not meta['cheats_enabled'] and
                 meta['input_hashes'] == read(folder / 'input_hashes_before.json') and
                 (folder / 'stderr.log').read_text() == '' and identity == retired['exactTerminalNativeIdentity'] and
                 identity['ProcessId'] == process['pid'] and identity['ParentProcessId'] == process['hostPID'] and
                 identity['createdUnix'] > 0 and '-samples' in command and '-nocheat' in command and
                 command[command.index('-wavwrite') + 1] == 'NUL' and
                 command[command.index('-autoboot_script') + 1] == str(ROOT / 'mk2ks_native_pit_rejoin_direct_scanout_display.lua'),
                 'Exact original native birth/path/parent/command, normal terminal, no state assistance')
            scene = report['nativeScene']
            earned, movie, policy = scene['nativeState'], scene['movie'], scene['actualNativePitShadowPolicy']
            fields = scene['retired'] + 30 - scene['origin']
            need(fields == (677 if side == 1 else 676) and
                 report['actualCurrentCrossNativePitWholeRenderPaletteShadowEraseAccepted'] and
                 report['sampledFrames'] == base['sampledFrames'] == meta['observedRGBFields'] == meta['modelExactFields'] == fields and
                 report['exactRGBPixels'] == scene['exactRGBPixels'] == fields * 101600 and
                 report['oneInitialBaseOnly'] and report['laterTargetsNeverUsedAsAnchors'] and
                 scene['oneInitialBaseOnly'] and scene['laterTargetsNeverUsedAsAnchors'] and
                 scene['currentLiveContinuousPipelineAccepted'] and scene['wholeNativePitShadowPolicyAccepted'] and
                 earned['passed'] and earned['earned_matches'] == 7 and earned['consecutive_fields'] == 801 and
                 earned['native_action'] == 'FF8BDDE0' and earned['action_frame'] == scene['origin'] and
                 earned['arena'] == 6 and movie['actualID'] == 35 - own and
                 movie['nextScreen'] == scene['retired'] and movie['actualMovieAddressRepurposed'] == scene['retired'] + 8 and
                 scene['visibleMoviePoses'] == scene['actualMoviePoses'] and len(scene['visibleMoviePoses']) == 6 and
                 scene['nativeShadowCopies'] == 0 and policy['passed'] and policy['currentPitShadowSchedulingMatchesOriginal'] and
                 scene['actualNativePhaseGround']['passed'] and
                 scene['actualNativePhaseGround']['originalVictimFloorDisplacement'] == 1024 and
                 len(scene['actualMovieFaultsRejected']) == 31 and len(scene['actualEarnedFaultsRejected']) == 12 and
                 len(scene['actualNativePhaseGroundFaultsRejected']) == 6 and len(policy['actualShadowPolicyFaultsRejected']) == 5 and
                 len(report['sourcePreflight']['rejectedProxyTuples']) == 5 and len(report['actualPixelFaultsRejected']) == 2,
                 'Entire original earned Pit movie/ground/stock-shadow/independent-renderer/proxy/pixel contracts')
            records_path, states_path = folder / 'post_scene_records.json', folder / 'post_state_records.json'
            records, states = map(read, (records_path, states_path))
            with gzip.open(folder / 'run.log.gz', 'rt') as reader:
                text = reader.read()
            post = original.exact.verify_rejoin(text, records, states, ids)
            faults = original.exact.faults(text, records, states, ids)
            facts, state_faults = state_and_faults(text, states, ids)
            saved = report['laterNativeTransitionAndPhysicalRejoin']
            need(post == {key: value for key, value in saved.items() if key != 'actualSemanticFaultsRejected'} and
                 faults == saved['actualSemanticFaultsRejected'] and len(faults) == 12 and
                 facts == retired['actualNativeGameplayFacts'] and
                 state_faults == retired['actualStateAndInputFaultsRejected'] and len(state_faults) == 12 and
                 retired['finiteNativePitTransitionAndPaidRejoinAccepted'] and
                 retired['actualVisibleTransitionAndPlayabilityReviewed'] and
                 retired['originalCaptureRAMDictionaryCleared'] and retired['reviewServerClosed'] and
                 retired['originalIndependentSceneFields'] == fields and
                 retired['laterSourceDefinedNativeDisplayFields'] == len(records) and
                 retired['laterSourceDefinedNativeRGBPixels'] == len(records) * 101600 and
                 facts['resumedNativeFields'] == 181,
                 'Entire later rejoin, all original24 semantic/state/input/health faults, contact and reviewed retirement')
            for state, record in zip(states, records, strict=True):
                timing = record['timing']
                effective = (timing['dpyadr'] + (timing['vsblnk'] - timing['veblnk']) * (timing['control'] & 0x03fc)) & 0xffff
                need(state == {key: record[key] for key in state} and record['passed'] and record['pixels'] == 101600 and
                     record['nativeDPYADRSourceDefinedAddressOnly'] and record['currentVRAMNeverSelectedAsPassingTarget'] and
                     record['effectiveNativeStart'] == effective and record['queuedNativeStart'] == state['start'] and
                     timing['vcount'] == timing['vsblnk'] - 1 and timing['vsblnk'] - timing['veblnk'] == 254 and
                     timing['vtotal'] >= timing['vsblnk'] and timing['control'] == state['control'] and timing['tap'] == state['tap'] and
                     timing['control'] & 0x03fc == 16 and timing['dpystart'] & 3 == timing['dpyadr'] & 3 == 0,
                     'Every original later field uses one source-defined completed native scanout')
            differences = [dict(frame=record['frame'], queued=record['queuedNativeStart'], effective=record['effectiveNativeStart'],
                                nativeVCOUNT=record['timing']['vcount'], nativeHCOUNT=record['timing']['hcount'])
                           for record in records if record['queuedStartDiffersFromEffective']]
            need(differences and differences == retired['actualQueuedCompletedAddressDifferences'] and
                 all(row['queued'] != row['effective'] for row in differences), 'Actual queued/completed address differences retained')
            ledger = {row['frame']: row for row in read(folder / 'continuous_scene_records.json')}
            need(len(ledger) == fields, 'Entire original independent initial chronology present')
            ledger.update({row['frame']: row for row in records})
            views = retired['individuallyReviewedFields']
            need(len(views) == retired['originalNativeRasterBuffersReleased'] and len(views) >= 20 and
                 len({row['frame'] for row in views}) == len(views) and
                 all(row['individuallyViewedNow'] and not row['exactSamePreviouslyViewedRaster'] and
                     row['rgbSHA256'] == ledger[row['frame']]['rgbSHA256'] for row in views),
                 'Every held original raster freshly individually inspected, released and bound to original pixels')
            need(not report['fullPortAcceptance'] and not report['allMirrorBranchesAndSlotsAccepted'] and
                 not saved['laterFullIndependentRendererModel'] and not retired['fullPortAcceptance'] and
                 not retired['allStageFinishersAccepted'] and not report['publicPlayableOrReleaseChanged'] and
                 not report['currentPitAudioWaveformAccepted'] and report['inheritedTombProtocolTagsAreTransportOnly'] and
                 report['rawImageAudioVRAMROMCopiesWritten'] == meta['rawImageAudioVRAMROMCopiesWritten'] == 0 and
                 not any(path.suffix.lower() in ('.png', '.wav', '.bin', '.exe', '.zip')
                         for path in folder.rglob('*') if path.is_file()),
                 'Finite opposite-victim Pit/rejoin scope, explicit separate audio/later-model scope and no raw copies')
            for collection in (report['inputHashes'], report['extensionSourceHashes'], meta['input_hashes'], retired['inputHashes']):
                bind(collection)
            for path in (report_path, retire_path, meta_path, identity_path, base_path, records_path, states_path):
                bind({str(path): sha(path)})
            cases.append(dict(fighter=fighter, physicalSlot=side, truePhysicalIDs=ids, initialIndependentFields=fields,
                              laterNativeScanoutFields=len(records), laterRGBPixels=len(records) * 101600,
                              admitted=facts['admitted'], completed=facts['completed'], resumedFields=181,
                              individuallyReviewedRasters=len(views), actualHealthDecrements=facts['actualHealthDecrements']))
    for path in (Path(__file__).resolve(), Path(original.__file__), Path(original.exact.__file__),
                 Path(original.original_state.__file__), Path(retirement_reference.__file__), scope_path):
        bind({str(path): sha(path)})
    initial_fields = sum(case['initialIndependentFields'] for case in cases)
    need(initial_fields == 2706, 'Complete four initial Pit intervals, no truncated case')
    result = dict(passed=True, cases=cases, finiteBothCharactersBothSlotsOppositeVictimPitTransitionAccepted=True,
                  originalIndependentFields=initial_fields, originalIndependentRGBPixels=initial_fields * 101600,
                  laterNativeScanoutFields=sum(case['laterNativeScanoutFields'] for case in cases),
                  laterSourceDefinedNativeRGBPixels=sum(case['laterRGBPixels'] for case in cases),
                  individuallyReviewedNativeRasters=sum(case['individuallyReviewedRasters'] for case in cases),
                  actualRejoinSemanticFaults=48, actualNativeStateInputHealthFaults=48,
                  originalMovieFaults=124, originalEarnedFaults=48, originalPhaseGroundFaults=24,
                  originalStockShadowPolicyFaults=20, originalProxyTupleFaults=20, originalPixelFaults=8,
                  laterFullIndependentRendererAccepted=False, allStockVictimsAndMirrorsAccepted=False,
                  allStageFinishersAccepted=False, fullPortAcceptance=False,
                  originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=scope['originalRemainingWorkGroups'], inputHashes=pins,
                  newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0, publicPlayableChanged=False, goalStatus='active')
    OUT.mkdir()
    (OUT / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    result = run()
    print(json.dumps({key: value for key, value in result.items() if key not in
                     ('inputHashes', 'originalNaturalIntegrationRequirements', 'originalRemainingWorkGroups')}, indent=2))
