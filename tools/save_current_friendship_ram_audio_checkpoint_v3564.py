"""Record current human Friendship audio without narrowing the full objective."""
import json
import subprocess
from pathlib import Path
import run_current_friendship_ram_audio_v3561 as audio

ROOT, need, sha = audio.ROOT, audio.need, audio.sha
PREVIOUS = ROOT / 'audit_v3556_current_original_ending_frame_full_scope_checkpoint/checkpoint.json'
OUT = ROOT / 'audit_v3565_current_friendship_ram_audio_full_scope_checkpoint'


def main():
    need(not OUT.exists(), 'Fresh immutable full-scope checkpoint')
    state = json.loads(PREVIOUS.read_text())
    remaining = state['remaining']
    need(state['goalStatus'] == 'active' and len(remaining) == 5 and
         state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted'] and
         state['current3172BothNaturalP1StoryOriginalGlyphSpacingPunctuationBlackShadowsAccepted'] and
         state['current3172BothNaturalP1NativePhotoFrameOverpaintAndCommonBackgroundAccepted'] and
         not state['fullPortAcceptance'] and not state['finishedRelease'],
         'Preserve completed natural P1 gates and unfinished complete objective')
    fresh = {}

    def pin(path, wanted=None):
        key = str(Path(path).resolve())
        actual = sha(path)
        need(wanted is None or actual == wanted, 'Actual retained evidence/public input unchanged')
        need(key not in fresh or fresh[key] == actual, 'Consistent new evidence pin')
        need(key not in state['inputHashes'] or state['inputHashes'][key] == actual,
             'Never relabel inherited authoritative evidence')
        fresh[key] = actual

    path = audio.OUT / 'report.json'
    proof = json.loads(path.read_text())
    need(proof['passed'] and proof['candidate'] == audio.collector.CANDIDATE and
         proof['current3172BothHumanSlotFullRetainedFriendshipCueTailOverlapOwnershipAccepted'] and
         proof['wholeCurrentGuestAndPayloadIndependentlyReconstructed'] and
         proof['originalPhysicalControllerByteExactExceptReadOnlySnapshotOmission'] and
         proof['actualPhysicalCaptures'] == 8 and proof['actualAudibleCues'] == 80 and
         proof['actualQualifiedFaults'] == 36 and
         not proof['historicalOriginalRawReferencesRecreated'] and
         proof['rawAudioFilesWritten'] == proof['newExecutableOrROMCopies'] == 0 and
         not proof['allFriendshipVictimsArenasCPUOrCompleteRasterAccepted'] and
         not proof['allFinisherOrPortAcceptance'] and not proof['fullPortAcceptance'],
         'Actual eight current physical/audio captures, bounded human Friendship gate only')
    need({(c['winner'], c['side']) for c in proof['cases']} ==
         {(fighter, side) for fighter in ('kano', 'sonya') for side in (1, 2)} and
         all(c['samplesNeverChangedGameplay'] and c['samePathUnmodifiedPositive'] and
             c['nativeScene']['observedOriginalOwnWinnerDispatches'] == 2 for c in proof['cases']),
         'Both true-ID human slots, actual earned wins and unchanged sample-off controls')
    pin(path)
    for file, wanted in proof['inputHashes'].items():
        pin(file, wanted)
    # Original audio lineage was pinned when3538 audited the older build.
    # Do not recreate or rehash its retired raw hardware-reference captures.
    older = ROOT / 'audit_v3538_current_natural_ending_photo_full_scope_checkpoint/checkpoint.json'
    older_state = json.loads(older.read_text())
    pin(audio.OLD, older_state['inputHashes'][str(audio.OLD)])
    pin(older)
    machine_rel = 'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
    current_machine = ROOT / audio.collector.CANDIDATE / machine_rel
    old_machine = ROOT / 'diagnostic_v2753_native_friendship_palette' / machine_rel
    need(current_machine.read_bytes() == old_machine.read_bytes(),
         'Entire actual compiled machine/guest assembly/audio marker handlers retained')
    pin(current_machine)
    pin(old_machine)
    driver_rel = 'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    current_driver = ROOT / audio.collector.CANDIDATE / driver_rel
    old_driver = ROOT / 'diagnostic_v2753_native_friendship_palette' / driver_rel
    original = old_driver.read_text()
    before = 'CRC(4a606b51) SHA1(36a54a06e295ea08f1ce9bda9bfbce6353731ca9)'
    after = 'CRC(a65205cf) SHA1(b8f9602b0c1a620df3f7e13bd7f659185cc40afa)'
    need(original.count(before) == 1 and current_driver.read_text() == original.replace(before, after),
         'Only actual3172 corrected morph payload declaration differs; no audio/ROM routing change')
    pin(current_driver)
    pin(old_driver)
    for relative in (state['currentCMD'], state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        item = ROOT / relative
        pin(item, state['inputHashes'][str(item.resolve())])
    pin(PREVIOUS)
    pin(__file__)
    state['inputHashes'] = fresh
    state['currentScopeEvidenceAudit']['group3'] = (
        '3563 now verifies actual3172 both-character/both-human-slot complete retained original Friendship cue '
        'waveforms/tails/overlap/native allocation/ownership/earned wins/cleanup with8samples-on/off captures '
        'and80audible cues,36qualified faults. Whole guest/payload independently assembled and all positive '
        'physical/native records exactly retained from2753. Compiled machine identical and driver differs only '
        'morph payload checksum, not audio routing. No raw historical reference recreation. Friendship full '
        'raster/shadow reference remains bounded2753; current complete visual/mirror/other victim/arena/CPU '
        'and other finisher/secret/cinematic coverage is not automatically promoted.')
    state.update(
        previousCheckpoint=str(PREVIOUS),
        inputHashInheritance=dict(schema=1, parentCheckpoint=str(PREVIOUS),
            parentCheckpointSHA256=fresh[str(PREVIOUS)],
            mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: inspected3556full-scope/current dirty checkout and actual2753vs3172 compiled code. Entire machine identical; driver differs only corrected morph payload checksum. Preserve byte-exact original physical Friendship controls; omit only3read-only PNG calls and add read-only RAM PCM/channel observer. Existing3172 executable8cold physical captures earn two wins each, actualtrueKano/Sonya in bothhuman slots. Samples-on/off entire native gameplay records/PCM updates exactly aligned; whole actual guest/payload independently assembled.80actual retained original cues, complete tails/overlap, original allocation/owners and native cleanup pass unchanged strict audio thresholds;36actual qualified PCM/owner/cue faults reject with same-path positives. Original asset full source PCM digest recovered from unchanged retained assets and3538-bound2922 lineage, no raw hardware references recreated. No playable/source/public/newEXE/ROM/WAV changes. Full original5groups retained.',
        current3172BothHumanSlotsFullRetainedFriendshipAudioAccepted=True,
        current3172FriendshipAudioReport=str(path),
        current3172FriendshipActualPhysicalCaptures=8,
        current3172FriendshipActualAudibleCues=80,
        current3172FriendshipQualifiedAudioFaults=36,
        current3172FriendshipAllVictimsArenasCPUOrCompleteRasterAccepted=False,
        current3172FriendshipCompiledMachineUnchangedFrom2753=True,
        current3172FriendshipCompiledDriverOnlyMorphPayloadChecksumChanged=True,
        gameSourceAndPlayableBytesChangedThisTurn=False,
        nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,
        newRuntimeCapturesThisTurn=8,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),
        historicalPinMapCopiedAgain=False,
        nextAction='Do not rerun completed natural P1 campaigns/endings/photo/text/common-frame or current both-human-slot Friendship audio for continuity. Select missing current finisher visual/arena/stage-audio coverage after auditing actual code and victim/mirror branches.8current Friendship captures intentionally omit PNGs, so do not claim complete current raster/shadows from them. Preserve original five groups, bounded current move/morph/UI proofs, all accepted native P1 gates, public1836CMD/ZIP and retired storage exclusions. Final combined current selection/ladder/names/audio regression and refreshed release ZIP remain pending; no new build/ROM/raw-WAV copies for routine tests.')
    need(state['remaining'] == remaining, 'Five original requirement groups retained verbatim')
    OUT.mkdir()
    saved = OUT / 'checkpoint.json'
    saved.write_text(json.dumps(state, indent=2) + '\n')
    digest = sha(saved)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(saved)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(saved) == digest, 'Lossless compact checkpoint')
    print(json.dumps(dict(saved=str(saved), goalStatus='active', currentHumanFriendshipCues=80,
                         actualQualifiedFaults=36, freshPins=len(fresh),
                         gameOrPublicBytesChanged=False, fullPortAcceptance=False), indent=2))


if __name__ == '__main__':
    main()
