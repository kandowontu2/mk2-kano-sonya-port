"""Seal the actual current earned-stage capture without retaining raw media."""
import hashlib
import json
from pathlib import Path
import audit_campaign_source_conservation as seal_source
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
import launch_stage_advance_contract as failed_stage
import launch_stage_advance_contract_v2 as failed_stage2
import launch_stage_advance_contract_v3 as stage
import launch_stage_advance_audio as failed_audio
import launch_stage_advance_audio_v2 as audio
import check_launch_stage_advance as checks

ROOT, need, sha = current.ROOT, current.need, seal_source.sha


def seal(c, game, waveform, launches, announcements, packet, channels, semantics, source_faults, owner_faults, dac, rom):
    out = ROOT/'audit_launch_stage_advance_checked_kano_p2'
    need(not out.exists() and not native.census(), 'Fresh proof; the actual native game is terminal')
    need(c['terminal']['pid'] == 39428 and c['terminal']['nativeExit'] == 0 and
         c['report']['passed'] and not c['decodeErrors'], 'The original captured job exited normally, not a replacement boot')
    need(current.expected() == c['guest'] and current.prior.expected_gfx() == c['gfx'],
         'Whole actual initialized guest and GFX match independently reconstructed source identities')
    pins = dict(c['pins'])
    parentpath = ROOT/'audit_campaign_source_conservation_progress_storage/report.json'
    parent = json.loads(parentpath.read_text())
    need(parent['passed'] and len(parent['remaining']) == 6, 'Full original integration and release scope retained')
    pins[str(parentpath)] = sha(parentpath)
    for path, digest in parent['inputHashes'].items():
        need(sha(path) == digest and (path not in pins or pins[path] == digest), 'Every exact previous source/proof pin intact')
        pins[path] = digest
    need(stage.gate(c['text'], c['guest'])[0] == game and game['nextLadderIndex'] == 1 and
         game['nextArenaId'] == 2 and game['nextNativeOpponent'] == 7,
         'Whole current native earned-advance/continue/controls contract executed again')
    need(checks.channels(c, launches, announcements) == channels and waveform['passed'] and
         waveform['differentChannelSamples'] == 0 and waveform['comparedStereoFrames'] == 5739840 and
         len(waveform['completeSourceClocks']) == len(c['pcmHeaders']) == 5979 and
         waveform['actualSHA256'] == waveform['predictedSHA256'],
         'Full native callback/source-clock/mixed waveform qualification, never a trimmed interval')
    need(packet == audio.packet_gate(c['text']) and len(semantics['actualFaultsRejected']) == 26 and
         len(source_faults['actualFaultsRejected']) == 10 and len(owner_faults['actualFaultsRejected']) == 11 and
         len(waveform['actualWaveformFaultsRejected']) == 7 and len(dac['faults']) == 4 and len(rom['faults']) == 8,
         'All actual native/input/source/complete-waveform/DAC/ROM counterexamples completed')
    failed = []
    for module, message, klass in [(failed_stage, "module 'qualify_launch_challenger_transition' has no attribute 're'", AttributeError),
                                   (failed_stage2, 'Each winning round follows real native lethal collision', ValueError)]:
        try:
            module.gate(c['text'], c['guest'])
        except klass as error:
            need(str(error) == message, 'Exact originally executed host checker rejection')
            failed.append(dict(passed=False, error=str(error), source=str(Path(module.__file__).resolve()),
                               sourceSHA256=sha(module.__file__), nativeGameFailure=False, reproducedFromSameCapture=True))
        else:
            raise ValueError('Originally rejected gate unexpectedly passes')
    # This complete original audio checker was actually executed and rejected
    # at the captured auxiliary stream cutoff. Keep its bytes/error distinct.
    failed.append(dict(passed=False, source=str(Path(failed_audio.__file__).resolve()),
                       sourceSHA256=sha(failed_audio.__file__), nativeGameFailure=False,
                       observedErrorPrefix='Complete native CPU/announcer/stage-advance waveform source equality: [[4584001, 0], [4584001, 1]',
                       originalExecutionAccepted=False, correctedOnlySeparateAuxiliaryStreamUpdate=True))
    viewed = []
    for index in (7, 11, 14):
        frame = c['rgbFrames'][index]
        need(hashlib.sha256(frame['pixels']).hexdigest().upper() == frame['header']['sha256'], 'Entire actual viewed native screen bytes')
        viewed.append(frame['header'])
    for module in (failed_stage, failed_stage2, stage, failed_audio, audio, checks, seal_source, current, native):
        path = Path(module.__file__).resolve()
        pins[str(path)] = sha(path)
    pins[str(Path(__file__).resolve())] = sha(__file__)
    for path in c['folder'].rglob('*'):
        if path.is_file():
            pins[str(path.resolve())] = sha(path)
    for event in launches+announcements:
        name = {0: 'kano_select', 2: 'kano_wins', 3: 'sonya_wins', 13: 'sonya_square_launch',
                14: 'sonya_bicycle_launch', 15: 'sonya_bicycle_cry'}[event['sample_id']]
        path = ROOT/'samples/mk2ks'/(name+'.wav')
        pins[str(path)] = sha(path)
    need(all(sha(p) == h for p, h in pins.items()), 'Every executed source, waveform asset, previous proof and capture remains exact')
    public = ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need('PLAY_CURRENT_V6508_CHECKED.cmd' in public.read_text() and
         len([p for p in ROOT.iterdir() if p.is_dir() and (p/'mkport_candidate.exe').is_file()]) == 16 and
         not (ROOT/'mame-mkp/build/mingw-gcc').exists(), 'No public promotion, new compiled folder or compiler cache')
    simplify = lambda e: {k: v for k, v in e.items() if k not in ('sample', 'positions', 'gain')}
    proof = dict(passed=True, candidate=current.NAME, nativeTerminal=c['terminal'],
                 wholeEarnedStageAndNativeHealth=game, completeSourceWaveform=waveform,
                 completeSourceChannelClocks=channels, completeNativeDCSDelivery=packet,
                 actualSemanticFaults=semantics, actualSourceChannelFaults=source_faults,
                 actualSourceOwnershipFaults=owner_faults, sourceDAC=dac, wholeSoundROM=rom,
                 sourceEvents=[simplify(e) for e in launches], announcerEvents=[simplify(e) for e in announcements],
                 preservedOriginalCheckerRejections=failed,
                 finiteVisualReview=dict(viewedFrameHeaders=viewed, imageFilesWritten=0,
                                        observations=['Earned next opponent is Raiden; actual Kano body and correct lifebar name are visible.',
                                                      'Selector portraits and poses are absent in all three viewed next-match frames.',
                                                      'Punch and final Block-survival appearance are visible; callback screenshots do not independently prove the jump/recovery animation.'],
                                        fullRasterAcceptance=False, fullArenaGroundingAcceptance=False),
                 partialLaunchInterruptedAtStageBoundaryAccepted=False,
                 stageBoundaryObservation='Actual CPU launches retired before ladder advance; all channels remain clean through the earned next arena/opponent.',
                 humanKanoBallLaunchInThisCapture=False, allCurrentCampaignStagesAccepted=False,
                 fullPortAcceptance=False, goalStatus='active', remaining=parent['remaining'],
                 previousGoalTurnClassification='no progress: acknowledgement only; resumed retained capture and authoritative terminal evidence',
                 thisGoalTurnClassification='progress: current genuine earned stage advance, full physical/health/source-audio checks, actual fault rejections and finite viewed next-match frames',
                 newNativeBootsForThisQualification=0, capturedNativeBoots=1, newBuilds=0, newROMCopies=0,
                 newRawMedia=0, newZIPs=0, publicPlayableChanged=False, rootDocumentsChanged=False,
                 nextAction='Audit concrete remaining finisher/secret/cinematic changed-source exposure against preserved whole native branch evidence; identify real integration gaps before combined current regression and matching CMD/final release ZIP.',
                 inputHashes=pins)
    out.mkdir()
    seal_source.seal(out/'report.json', proof)
    print(json.dumps(dict(passed=True, report=str(out/'report.json'), stereoFrames=waveform['comparedStereoFrames'],
                          actualFaultsRejected=66, nativeExit=0, newBuilds=0)), flush=True)
    return proof
