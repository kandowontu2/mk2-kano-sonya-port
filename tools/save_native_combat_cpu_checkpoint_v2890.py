"""Retain the full native-character objective after combat and CPU regressions.

Fresh bounded CPU successes never replace rejected cases, missing signatures,
render/audio/morph/victim/arena/campaign/ending/release requirements. The whole
historical graph is retained; only fresh relevant dependencies are rehashed.
No playable byte, user source, public CMD or release ZIP is modified here.
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_physical_p2_cpu_pair_v1456 as cpu

ROOT = assembly.ROOT
PREVIOUS = ROOT / 'audit_v2848_repeat_native_friendship_full_scope_checkpoint/checkpoint.json'
OUT = ROOT / 'audit_v2891_native_combat_cpu_full_scope_checkpoint'


def save():
    prior = json.loads(PREVIOUS.read_text())
    inherited, fresh = dict(prior['inputHashes']), {}
    assembly.need(prior['goalStatus'] == 'active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
                  len(prior['remaining']) == 5 and len(prior['currentSourceBoundBossCampaigns']) == 70 and
                  prior['currentRealShaoKahnMatchClears'] == 0 and not prior['actualEndingsAccepted'] and
                  prior['candidateUnderTestRepeatedNativeFriendshipAccepted'] and len(prior['candidatePromotionGates']) == 2,
                  'Retain full scope, public build, actual repeated finisher progress and missing boss clears/endings')

    def pin(path, wanted=None):
        path = Path(path)
        key = str((path if path.is_absolute() else ROOT / path).absolute())
        wanted = assembly.sha(key) if wanted is None else wanted
        assembly.need(key not in fresh or fresh[key] == wanted, 'Consistent fresh source/evidence ' + key)
        assembly.need(key not in inherited or inherited[key] == wanted, 'Immutable historical source/evidence ' + key)
        fresh[key] = wanted

    def proof(leaf):
        path = ROOT / leaf / 'report.json'
        value = json.loads(path.read_text())
        pin(path)
        assembly.need(value['passed'] and not value.get('fullPortAcceptance', False), 'Actual bounded terminal proof ' + leaf)
        for file, wanted in value['inputHashes'].items():
            pin(file, wanted)
        return value, str(path)

    combat, combat_path = proof('audit_v2855_native_combat_regression_checked')
    assembly.need(combat['candidate'] == assembly.NAME and len(combat['cases']) == 20 and
                  combat['originalPerFieldAcceptanceUnchanged'] and combat['wholeActualGuestCapturedAndReconstructedForEveryFixture'] and
                  combat['noEmulatedStateInjectionOrReset'] and combat['interruptionPairedFields'] == 9096 and
                  combat['knockoutPairedFields'] == 30170 and combat['exactCheckedBuildParticipantCases'] == 13 and
                  not combat['allInterruptionsAccepted'] and not combat['allKOPathsAccepted'],
                  'All twenty original per-field combat contracts, without universal interrupt/KO claims')
    combat_units, combat_units_path = proof('audit_v2857_native_combat_regression_units')
    assembly.need(combat_units['candidate'] == assembly.NAME and combat_units['methods'] == 31 and
                  combat_units['actualMutationNonVacuityRequired'] and combat_units['originalRejectionPredicatesUnchanged'] and
                  combat_units['actualCaptureFilesUnmodified'], 'Actual unchanged native combat rejection methods')
    difference_path = ROOT / 'audit_v2861_native_combat_differences/report.json'
    differences = json.loads(difference_path.read_text())
    pin(difference_path)
    assembly.need(differences['passed'] and differences['diagnosticOnly'] and differences['differencesNotAutomaticallyAccepted'],
                  'Every observed combat difference retained, not normalized away')
    for file, wanted in differences['inputHashes'].items():
        pin(file, wanted)
    changed = [r for r in differences['cases'] if r['changedParticipantFields']]
    assembly.need(len(changed) == 7 and all(set(r['changedKeyCounts']) == {'trail'} and
                  not r['sourceBoundCauseAccepted'] and r['noValuesMaskedOrNormalized'] for r in changed),
                  'Seven attached-blade allocation addresses remain an explicit provenance gate')

    inventory, inventory_path = proof('audit_v2887_native_cpu_start_inventory_checked')
    assembly.need(inventory['candidate'] == assembly.NAME and inventory['diagnosticInventoryOnly'] and len(inventory['cases']) == 24 and
                  inventory['acceptedPairFixtures'] == 9 and inventory['acceptedPairsByActualCPU'] == {'kano': 8, 'sonya': 1} and
                  inventory['scenarioMisses'] == 10 and inventory['originalContractRejectedFixtures'] == 5 and
                  inventory['originalTypedContractsUnchanged'] and not inventory['allFixturesGameplayAccepted'] and
                  not inventory['allCPUAccepted'] and not inventory['publicPromotionAccepted'],
                  'All actual normal-input CPU attempts retained: nine strict accepts, ten misses, five rejects')
    accepted = [r for r in inventory['cases'] if r['status'] == 'accepted_original_pair_and_ordinary_followup']
    rejected = [r for r in inventory['cases'] if r['status'] == 'original_contract_rejected']
    assembly.need(all(r['typedContract']['originalContract']['passed'] and r['floorAnchorsChecked'] and
                  not r['rawFloorDifferences'] and r['wholeActualGuestReconstructed'] and r['noGuestStateInjection'] for r in accepted) and
                  all(not r['originalContract']['passed'] and r['originalContract']['errors'] and r['typedContract'] is None for r in rejected),
                  'Strictly typed actual pair/follow-up accepts and unchanged original rejected cases')
    units, units_path = proof('audit_v2889_native_cpu_start_pairs_units')
    assembly.need(units['candidate'] == assembly.NAME and units['acceptedFixturesTested'] == 9 and
                  units['actualOriginalCounterexamplesRejected'] == 180 and units['originalTypedContractsUnchanged'] and
                  units['mutationNonVacuityRequired'] and units['actualCapturesUnmodified'] and not units['gameBytesChanged'],
                  'All 180 actual CPU corruption tests rejected without changing captures or playable bytes')
    previous_cpu, previous_cpu_path = proof('audit_v2880_native_cpu_start_inventory_checked')
    previous_units, previous_units_path = proof('audit_v2882_native_cpu_start_pairs_units')
    assembly.need(previous_cpu['acceptedPairFixtures'] == 5 and previous_units['actualOriginalCounterexamplesRejected'] == 100,
                  'Earlier bounded sixteen-case CPU proof and actual rejection evidence preserved')

    guest, _, _, _, _ = assembly.expected()
    build = json.loads((ROOT / assembly.NAME / 'build-info.json').read_text(encoding='utf-8-sig'))
    earlier_misses = []
    for version, params in ((2864, [(p, 604, 264) for p in ('kano', 'sonya')]),
                            (2869, [(p, 604, age) for p in ('kano', 'sonya') for age in (265, 266, 267)])):
        for player, boot, age in params:
            leaf = f'audit_v2864_native_sonya_p2_cpu_human_{player}' if version == 2864 else f'audit_v2869_native_cpu_human_{player}_confirm{age}'
            folder = ROOT / leaf
            meta = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
            before = json.loads((folder / 'input_hashes_before.json').read_text(encoding='utf-8-sig'))
            assembly.need(meta['exit_code'] == 0 and meta['candidate'] == assembly.NAME and meta['player'] == player and
                          (meta['boot_frame'], meta['confirm_age']) == (boot, age) and meta['assistance'] == 'none' and
                          not meta['cheats_enabled'] and before == meta['input_hashes'] and
                          meta['executable_sha256'] == build['executable_sha256'] and
                          all(before.get(file) == wanted for file, wanted in build['input_hashes'].items()) and
                          (folder / 'guest_maincpu.bin').read_bytes() == guest, 'Earlier actual terminal natural CPU timing miss retained')
            for file, wanted in before.items():
                pin(file, wanted)
            log = (folder / 'run.log').read_text(encoding='utf-8-sig')
            cold = cpu.rows_prefix(log, 'MK2_P2CPU_COLD_LIVE ')
            assembly.need(len(cold) == 1 and cold[0]['cpu_id'] == 3 and not cpu.rows(log, 'ENTRY') and not cpu.rows(log, 'COMPLETE'),
                          'Baraka scenario miss must not be promoted to Kano/Sonya CPU coverage')
            for file in folder.rglob('*'):
                if file.is_file():
                    pin(file)
            earlier_misses.append(dict(case=leaf, actualCPU=3, accepted=False, scenarioMiss=True))
    control = ROOT / 'audit_v2870_native_cpu_noextra_guest_control'
    meta = json.loads((control / 'result.json').read_text(encoding='utf-8-sig'))
    before = json.loads((control / 'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    assembly.need(meta['exit_code'] == 0 and meta['candidate'] == assembly.NAME and meta['player'] == 'kano' and
                  (meta['boot_frame'], meta['confirm_age']) == (604, 264) and before == meta['input_hashes'] and
                  meta['assistance'] == 'none' and not meta['cheats_enabled'] and meta['executable_sha256'] == build['executable_sha256'] and
                  all(before.get(file) == wanted for file, wanted in build['input_hashes'].items()), 'Original unwrapped observer control terminal and matched')
    for file, wanted in before.items():
        pin(file, wanted)
    controlled = (control / 'run.log').read_text(encoding='utf-8-sig')
    wrapped = (ROOT / 'audit_v2864_native_sonya_p2_cpu_human_kano/run.log').read_text(encoding='utf-8-sig')
    events = lambda text: [line for line in text.splitlines() if line.startswith(('MK2_CPU_PAIR_', 'MK2_P2CPU_'))]
    assembly.need(events(controlled) == events(wrapped), 'Entire original CPU/UI chronology unchanged by extra read-only whole-guest observer')
    for file in control.rglob('*'):
        if file.is_file():
            pin(file)
    failures = []
    for leaf in ('audit_v2866_native_physical_p2_cpu_checked', 'audit_v2878_native_cpu_start_inventory_checked'):
        path = ROOT / leaf / 'report.json'
        value = json.loads(path.read_text())
        assembly.need(not value['passed'] and value['error'], 'Actual earlier diagnostic failure remains preserved')
        pin(path)
        failures.append(dict(report=str(path), error=value['error'], accepted=False))
    for file in ('run_native_cpu_timing_sweep_v2867.py', 'verify_native_physical_p2_cpu_v2865.py',
                 'verify_native_cpu_start_inventory_v2877.py', 'inspect_native_combat_differences_v2858.py'):
        pin(ROOT / 'tools' / file)
    for path, wanted in {
        'PLAY_MK2_KANO_SONYA.cmd': '631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
        'PLAY_CURRENT_V1836_CHECKED.cmd': 'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
        'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip': '994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
        'mame-mkp/src/mame/midway/midtunit_m.cpp': 'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        'mame-mkp/src/mame/midway/midtunit.cpp': '07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        'mame-mkp/src/mame/midway/midtunit.h': '256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
        'mame-mkp/mkport.exe': '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():
        pin(ROOT / path, wanted)
    pin(PREVIOUS)
    pin(__file__)
    pin(cpu.__file__)
    print('Revalidating fresh relevant combat/CPU files:', len(fresh), flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file, wanted), actual in zip(fresh.items(), pool.map(assembly.sha, fresh)):
            assembly.need(actual == wanted, 'Changed fresh actual source/evidence ' + file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS), previousGoalTurnClassification=prior['thisGoalTurnClassification'],
        immediatelyPreviousUserStatusTurnClassification='no progress: status response only; revalidated and resumed the next safe physical CPU action in this continuation',
        thisGoalTurnClassification='progress: twenty fresh native interruption/retry and KO/next-round contracts plus 31 unchanged original rejection methods accepted. Exact field differences inventoried without normalization: seven blade addresses still require allocator provenance. Original no-extra-guest CPU observer control proved exact unchanged chronology. Twenty-four actual normal coin/start timings captured, whole guest and roles/source/floors/opcodes independently bound; nine complete native CPU pairs and original ordinary follow-ups accepted (eight Kano, one Sonya), 180 actual corruptions rejected. Ten stock-opponent scenario misses and five original contract rejections retained unaccepted, plus eight earlier Baraka misses and two failed diagnostics. No playable bytes/public launcher/release changed; entire original natural-character goal remains unfinished.',
        candidateUnderTestFreshCombatRegressionReport=combat_path,
        candidateUnderTestFreshCombatFixtures=20, candidateUnderTestFreshCombatPairedFields=39266,
        candidateUnderTestFreshCombatUnitsReport=combat_units_path, candidateUnderTestFreshCombatRejectionMethods=31,
        candidateUnderTestFreshCombatDifferenceReport=str(difference_path),
        candidateUnderTestSevenBladeAllocationAddressDifferences=changed,
        candidateUnderTestBladeAllocationAddressProvenanceAccepted=False,
        candidateUnderTestPhysicalP2CPUInventoryReport=inventory_path,
        candidateUnderTestPhysicalP2CPUCaptureCount=24,
        candidateUnderTestBoundedPhysicalP2CPUAcceptedFixtures=accepted,
        candidateUnderTestBoundedPhysicalP2CPUAcceptedCount=9,
        candidateUnderTestBoundedPhysicalP2CPUAcceptedByActualCPU={'kano': 8, 'sonya': 1},
        candidateUnderTestPhysicalP2CPURejectedFixtures=rejected,
        candidateUnderTestPhysicalP2CPUStockOpponentMisses=10,
        candidateUnderTestPhysicalP2CPUUnitsReport=units_path,
        candidateUnderTestPhysicalP2CPUActualCounterexamplesRejected=180,
        candidateUnderTestPhysicalP2CPUEarlierInventoryReport=previous_cpu_path,
        candidateUnderTestPhysicalP2CPUEarlierUnitsReport=previous_units_path,
        candidateUnderTestEarlierCPUConfirmationTimingMisses=earlier_misses,
        candidateUnderTestNoExtraGuestCPUControl=dict(case=control.name, terminalExit=0,
            entireOriginalNativeChronologyExact=True, naturallySelectedCPU=3, gameplayPairAccepted=False),
        preservedCurrentCPUInventoryDiagnosticFailures=failures,
        candidateUnderTestPhysicalP2CPUSonyaMirrorAccepted=False,
        candidateUnderTestAllCPUAccepted=False,
        candidatePromotionGates=[
            'Broader affected move/morph/ordinary-combat/CPU/KO/overlap regressions after shared allocator/reset routing change: native UI, 52 human states, blade blood, repeated Kano bubble lifecycle, twenty interruption/KO cases and nine P2 CPU pairs accepted. Seven blade child-address allocation causes and rejected/missing CPU signature/repeated/KO paths remain open.',
            'Fresh full original Friendship audible PCM/tail/overlap checks, including actual randomized Sonya variants and matched samples-off controls'],
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False, revalidatedFreshRelevantFilePins=len(fresh),
        gameSourceAndPlayableBytesChangedThisTurn=False, publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False, oldBuildFoldersDeletedThisTurn=0,
        nativeDifficultyHealthAIPositionStageRNGModified=False, actualEndingsAccepted=False,
        fullPortAcceptance=False, finishedRelease=False, goalStatus='active',
        nextAction='Keep v2753 isolated. Source-bind seven changed blade child addresses to original pool allocation/attachment/cleanup; add fresh read-only provenance for rejected real signature-after-pair or subsequent-pair contexts without relabeling them ordinary. Obtain actual Sonya CPU mirror and broader CPU/morph/KO/overlap proof, plus full original Friendship audible PCM/tail/overlap with matched samples-off controls. Retain all five original remaining groups: arena/victim/mirror/stage effects/audio/move-phase/grounding/floor shadows/other finishers/morphs/secrets/cinematics/natural full Kintaro/Shao match clears/own endings/attract/final integration/obsolete dependency cleanup/refreshed ZIP. Promote no launcher or final release before those gates pass.',
        inputHashes=inherited)
    return prior


if __name__ == '__main__':
    assembly.need(not OUT.exists(), 'Immutable full-scope native combat/CPU checkpoint')
    value = save()
    OUT.mkdir()
    (OUT / 'checkpoint.json').write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(dict(goalStatus=value['goalStatus'], publicCandidate=value['currentCandidate'],
        candidateUnderTest=value['candidateUnderTest'], freshCombatFixtures=20, freshCombatPairedFields=39266,
        actualPhysicalP2CPUFixtures=24, actualAcceptedCPUPairs=9, acceptedByActualCPU={'kano':8,'sonya':1},
        actualCPUCorruptionsRejected=180, sevenBladeAddressCausesAccepted=False,
        remainingCandidateGates=len(value['candidatePromotionGates']), fullPortAcceptance=False,
        finishedRelease=False, revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']), indent=2), flush=True)
