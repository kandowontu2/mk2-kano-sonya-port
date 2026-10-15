"""Full-scope checkpoint after exact native blade allocation lifetime proof.

Retain every original unfinished natural-character requirement. Original
address differences are NOT normalized and their exact hardware/RNG cause is
not claimed. Their actual native allocation/attachment/reclamation is now
proved on both builds. No public executable, CMD, ZIP or user source changes.
"""
import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT = assembly.ROOT
PREVIOUS = ROOT / 'audit_v2891_native_combat_cpu_full_scope_checkpoint/checkpoint.json'
OUT = ROOT / 'audit_v2916_blade_allocation_full_scope_checkpoint'


def save():
    prior = json.loads(PREVIOUS.read_text())
    inherited, fresh = dict(prior['inputHashes']), {}
    assembly.need(prior['goalStatus'] == 'active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and
                  len(prior['remaining']) == 5 and len(prior['currentSourceBoundBossCampaigns']) == 70 and
                  prior['currentRealShaoKahnMatchClears'] == 0 and not prior['actualEndingsAccepted'] and
                  prior['candidateUnderTestFreshCombatFixtures'] == 20 and
                  prior['candidateUnderTestBoundedPhysicalP2CPUAcceptedCount'] == 9 and
                  not prior['candidateUnderTestAllCPUAccepted'] and not prior['candidateUnderTestPhysicalP2CPUSonyaMirrorAccepted'] and
                  len(prior['candidatePromotionGates']) == 2 and not prior['candidateUnderTestBladeAllocationAddressProvenanceAccepted'],
                  'Retain whole natural-character goal and all accepted/rejected/uncovered prior CPU/combat requirements')

    def pin(path, wanted=None):
        path = Path(path)
        key = str((path if path.is_absolute() else ROOT/path).absolute())
        wanted = assembly.sha(key) if wanted is None else wanted
        assembly.need(key not in fresh or fresh[key] == wanted, 'Consistent fresh native allocation dependency '+key)
        assembly.need(key not in inherited or inherited[key] == wanted, 'Immutable prior source/evidence '+key)
        fresh[key] = wanted

    def proof(leaf):
        path = ROOT/leaf/'report.json'
        value = json.loads(path.read_text())
        pin(path)
        assembly.need(value['passed'] and not value.get('fullPortAcceptance', False), 'Actual bounded terminal proof '+leaf)
        for file, wanted in value['inputHashes'].items():
            pin(file, wanted)
        return value, str(path)

    allocation, allocation_path = proof('audit_v2912_blade_allocation_checked')
    assembly.need(allocation['candidate'] == assembly.NAME and allocation['control'] == assembly.prior.NAME and
                  allocation['actualFixtures'] == 14 and allocation['actualBladeLifetimes'] == 88 and len(allocation['cases']) == 7 and
                  allocation['allSevenChangedBladeAddressesSourceBound'] and allocation['noAddressNormalization'] and
                  allocation['originalPhysicalInputStrategiesUnchanged'] and allocation['wholeActualGuestReconstructedForBothBuilds'] and
                  allocation['originalNativeChronologyExactForEveryFixture'] and not allocation['exactHardwareRNGCauseAccepted'] and
                  not allocation['fullRendererOrAudioAccepted'] and not allocation['allCPUOrMorphsAccepted'],
                  'All actual changed-address fixtures have complete original allocator/attachment/retirement provenance, not universal claims')
    cases = {}
    for key, pair in allocation['cases'].items():
        assembly.need(pair['actualAddressDifferences'] and all(r['actual'] != r['previous'] for r in pair['actualAddressDifferences']),
                      'All raw current/control allocation address differences reproduced without masking')
        for build in ('new', 'old'):
            value = pair[build]
            assembly.need(value['passed'] and value['allocationAddressProvenanceAccepted'] and
                          value['allActualAllocationAttachmentRetirementSourceBound'] and value['originalNativeChronologyExact'] and
                          value['wholeActualGuestReconstructed'] and value['rawStackTopNotAcceptedAsReturnAddress'] and
                          not value['exactHardwareRNGCauseAccepted'] and all(r['attached'] == r['start'] < r['detached'] and
                          r['nativePopSequence'] < r['nativePopFinalSequence'] < r['nativePushSequence'] < r['nativePushFinalSequence'] and
                          r['detachedFields'] == 2 and r['addressUnnormalized'] for r in value['contexts']),
                          'Original full-width native store transactions, actual lifetimes, detach and preserved raw addresses')
        cases[key] = dict(actualAddressDifferences=pair['actualAddressDifferences'],
                         newCase=pair['new']['case'], originalControlCase=pair['old']['case'],
                         currentLifetimes=pair['new']['contexts'], originalControlLifetimes=pair['old']['contexts'],
                         actualAllocationAddressProvenanceAccepted=True, exactHardwareRNGCauseAccepted=False)
    assembly.need(sum(len(r['actualAddressDifferences']) for r in cases.values()) == 18,
                  'All eighteen actual unequal allocation pairs across seven differing fixtures source-bound')
    units, units_path = proof('audit_v2914_blade_allocation_units')
    assembly.need(units['candidate'] == assembly.NAME and units['control'] == assembly.prior.NAME and
                  units['actualFixturesTested'] == 14 and units['actualCounterexamplesRejected'] == 330 and
                  units['mutationNonVacuityRequired'] and units['actualCapturesUnmodified'] and
                  units['originalCombatContractsUnchanged'] and not units['gameBytesChanged'],
                  'All 330 actual native allocation/attachment/phase/retirement/reuse corruptions rejected')
    failures = []
    for version in (2900, 2902, 2904, 2906, 2910):
        path = ROOT/f'audit_v{version}_blade_allocation_checked/report.json'
        value = json.loads(path.read_text())
        assembly.need(not value['passed'] and value['error'], 'Preserved real predecessor parser/invariant diagnostic failure')
        pin(path)
        failures.append(dict(report=str(path), error=value['error'], accepted=False))
    for version in (2899, 2901, 2903, 2905, 2909, 2911):
        pin(ROOT/f'tools/verify_blade_allocation_v{version}.py')
    pin(ROOT/'tools/test_blade_allocation_v2907.py')
    pin(ROOT/'mk2ks_blade_allocation_v2892.lua')
    pin(ROOT/'tools/run_blade_allocation_v2893.ps1')
    pin(ROOT/'tools/run_blade_allocation_dispatch_v2896.py')
    pin(PREVIOUS)
    pin(__file__)
    for path, wanted in {
        'PLAY_MK2_KANO_SONYA.cmd': '631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
        'PLAY_CURRENT_V1836_CHECKED.cmd': 'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
        'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip': '994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
        'mame-mkp/src/mame/midway/midtunit_m.cpp': 'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        'mame-mkp/src/mame/midway/midtunit.cpp': '07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        'mame-mkp/src/mame/midway/midtunit.h': '256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
        'mame-mkp/mkport.exe': '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    }.items():
        pin(ROOT/path, wanted)
    print('Revalidating fresh relevant native blade files:', len(fresh), flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file, wanted), actual in zip(fresh.items(), pool.map(assembly.sha, fresh)):
            assembly.need(actual == wanted, 'Changed fresh actual native proof file '+file)
    inherited.update(fresh)
    prior.update(previousCheckpoint=str(PREVIOUS), previousGoalTurnClassification=prior['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: fourteen fresh physical interruption/retry and KO/next-round candidate/original-control fixtures reproduced all eighteen unequal blade allocation pairs across the seven recorded differing cases. Every one of 88 actual blade lifetimes independently source-bound to original full 32-bit free-head pop, live owning Main attachment, native body/descriptor/list phases, original retirement/full-width free-list push and detach, including exact new allocation under another Main on immediate interrupted-blade address reuse. Complete original native combat chronology and all mode transitions unchanged on both builds. 330 actual corruptions rejected. Earlier parser, overstrict persistent-free, incomplete half-store, later zero-fill and live-mode-only diagnostics preserved; immutable successors model original native branches with source-bound stores rather than alter game. Public bytes/CMD/ZIP untouched. Full original natural-character scope remains active and unfinished.',
        candidateUnderTestBladeAllocationAddressProvenanceAccepted=True,
        candidateUnderTestBladeAllocationProvenanceReport=allocation_path,
        candidateUnderTestBladeAllocationFixtures=14, candidateUnderTestBladeAllocationLifetimes=88,
        candidateUnderTestBladeAllocationUnequalAddressPairs=18,
        candidateUnderTestBladeAllocationCases=cases,
        candidateUnderTestBladeAllocationOriginalChronologyExact=True,
        candidateUnderTestBladeAllocationExactHardwareRNGCauseAccepted=False,
        candidateUnderTestBladeAllocationUnitsReport=units_path,
        candidateUnderTestBladeAllocationActualCounterexamplesRejected=330,
        preservedBladeAllocationDiagnosticFailures=failures,
        candidatePromotionGates=[
            'Broader affected move/morph/ordinary-combat/CPU/KO/overlap regressions after shared allocator/reset routing change. Native UI, 52 human states, blade blood, repeated Kano bubble lifecycle, twenty interruption/KO cases, nine P2 CPU pairs and all seven differing blade allocation lifetimes accepted. Rejected/missing CPU signature/repeated/KO/mirror paths and morph/other overlapping effects remain open.',
            'Fresh full original Friendship audible PCM/tail/overlap checks, including actual randomized Sonya variants and matched samples-off controls'],
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False, revalidatedFreshRelevantFilePins=len(fresh),
        gameSourceAndPlayableBytesChangedThisTurn=False, publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False, oldBuildFoldersDeletedThisTurn=0,
        nativeDifficultyHealthAIPositionStageRNGModified=False, actualEndingsAccepted=False,
        fullPortAcceptance=False, finishedRelease=False, goalStatus='active',
        nextAction='Keep v2753 isolated. Seven recorded blade-address differences now have source-bound actual allocation/attachment/reclamation/reuse provenance without address normalization; do not claim an independently proved exact hardware/RNG cause. Next fresh CPU signature-after-pair/subsequent-pair/KO/overlap/morph and actual Sonya CPU mirror coverage, plus full original Friendship audible PCM/tail/overlap with matched samples-off controls. Retain all five original remaining groups: arena/victim/mirror/stage effects/audio/move phases/grounding/floor shadows/other finishers/morphs/secrets/cinematics/natural full Kintaro/Shao match clears/own endings/attract/final integration/obsolete dependency cleanup/refreshed ZIP. No public promotion or finished-release claim before required gates pass.',
        inputHashes=inherited)
    return prior


if __name__ == '__main__':
    assembly.need(not OUT.exists(), 'Immutable full-scope native allocation checkpoint')
    value = save()
    OUT.mkdir()
    path = OUT/'checkpoint.json'
    path.write_text(json.dumps(value, indent=2)+'\n')
    # Lossless NTFS compression only on the new exact artifact, no deletion.
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    assembly.need(result.returncode == 0, 'Compress new checkpoint without modifying logical bytes')
    print(json.dumps(dict(goalStatus=value['goalStatus'], publicCandidate=value['currentCandidate'],
        candidateUnderTest=value['candidateUnderTest'], actualFixtures=14, actualBladeLifetimes=88,
        actualUnequalAllocationPairs=18, actualCorruptionsRejected=330, sevenRecordedDifferenceCasesProven=True,
        exactHardwareRNGCauseAccepted=False, remainingCandidateGates=len(value['candidatePromotionGates']),
        fullPortAcceptance=False, finishedRelease=False, revalidatedFreshRelevantFilePins=value['revalidatedFreshRelevantFilePins']), indent=2), flush=True)
