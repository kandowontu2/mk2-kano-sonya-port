"""Assemble the exact qualified additive successor and frozen build contract.

Mechanically creates only three required native source files, not a repository
copy. No emulator, ROM, game data, public executable or launcher is changed.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / 'source_native_paired_stumble_table'
STAGE = ROOT / 'source_native_shang_owned_drain'
OUT = ROOT / 'audit_native_shang_drain_build_source'
QUALIFIED = ROOT / 'audit_native_shang_drain_native_opcode_source/report.json'
BUILD = ROOT / 'tools/build_native_shang_drain_ps7.ps1'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def need(value, reason):
    if not value:
        raise ValueError(reason)


def main():
    need(not STAGE.exists() and not OUT.exists(), 'Never overwrite assembled source or executed qualification')
    proof = json.loads(QUALIFIED.read_text())
    native = json.loads((ROOT / 'audit_native_shang_drain_reservation_native/report.json').read_text())
    generation_path = ROOT / 'source_native_shang_drain_compare/generation-report.json'
    generation = json.loads(generation_path.read_text())
    need(proof['passed'] and proof['sourceOnlyAccepted'] and proof['actualCppInitializerExit'] == 0 and
         len(proof['actualCppFaultsRejected']) == 50 and proof['helperInstructionModelCases'] == 2052 and
         proof['exactFourNativeCMPIInstructionsAccepted'] and proof['actualPredecessorANDIOpcodeRejected'] and
         not proof['predecessorSourceQualificationAccepted'] and not proof['nativeRepairAccepted'] and
         not proof['fullPortAcceptance'] and native['passed'] and native['nativeReservationAccepted'],
         'Complete corrected source and actual native free-storage prerequisites')
    for report in (proof, native, generation):
        need(all(sha(p) == h for p, h in report['inputHashes'].items()), 'Every executed prerequisite source/art/reference pin intact')
    fragment_path = ROOT / 'source_native_shang_drain_compare/native_shang_owned_drain.inc'
    need(sha(fragment_path) == generation['fragmentSHA256'], 'Exact corrected CMPI fragment, not the failed ANDI predecessor')
    lead = (ROOT / 'tools/native_shang_owned_reaction.inc').read_text()
    fragment = fragment_path.read_text()
    before = (PRIOR / 'midtunit_m.cpp').read_text()
    anchor = '\t// PAIRED_STUMBLE_TABLE_END\n'
    need(before.count(anchor) == 1 and 'SHANG_OWNED_DRAIN_BEGIN' not in before, 'One additive source anchor on unchanged actual current driver')
    addition = lead + '\n' + fragment
    after = before.replace(anchor, anchor + addition, 1)
    need(after.replace(addition, '', 1) == before and
         hashlib.sha256(after.encode()).hexdigest().upper() == proof['additiveWholeDriverSHA256'],
         'Byte-identical complete normalized driver from the actual qualified initializer source')
    need(len(proof['originalNaturalIntegrationRequirements']) == 14 and
         len(proof['originalRemainingWorkGroups']) == 6, 'Original natural integration scope preserved')
    STAGE.mkdir()
    # Build artifacts are mechanical derivations; original source is never edited.
    (STAGE / 'midtunit_m.cpp').write_bytes(after.encode())
    for name in ('midtunit.cpp', 'midtunit.h'):
        (STAGE / name).write_bytes((PRIOR / name).read_bytes())
        need(sha(STAGE / name) == sha(PRIOR / name), 'No unrelated native registration/audio/header changes')
    staged = {name: sha(STAGE / name) for name in ('midtunit.cpp', 'midtunit.h', 'midtunit_m.cpp')}
    need(staged['midtunit_m.cpp'] == proof['additiveWholeDriverSHA256'], 'Physical assembled driver exactly equals qualified source')
    pins = dict(proof['inputHashes'])
    for p in (Path(__file__), BUILD, QUALIFIED, generation_path,
              ROOT / 'tools/build_native_ai_response.ps1',
              ROOT / 'diagnostic_native_paired_stumble_table_ps7/build-info.json',
              *(PRIOR / n for n in staged), *(STAGE / n for n in staged)):
        pins[str(p.resolve())] = sha(p)
    need(all(sha(p) == h for p, h in pins.items()), 'All old and new required build inputs frozen')
    OUT.mkdir()
    report = dict(passed=True, sourceOnlyAccepted=True, bothQualifiedFragmentsApplied=True,
                  sourceStage=str(STAGE), stagedSourceHashes=staged,
                  sourceQualification=str(QUALIFIED), sourceQualificationSHA256=sha(QUALIFIED),
                  actualCppFaultsRejected=proof['actualCppFaultsRejected'], helperInstructionModelCases=2052,
                  exactFourNativeCMPIInstructionsAccepted=True, actualPredecessorANDIOpcodeRejected=True,
                  proposedGuestSHA256=proof['wholeProposedGuestSHA256'],
                  expectedOwnedWindowSHA256=proof['wholeProposedOwnedWindowSHA256'],
                  expectedGraphicsReservationSHA256=proof['proposedGraphicsReservationSHA256'],
                  initializedGuestByteDelta=proof['changedHighGuestBytes'],
                  initializedOwnedByteDelta=proof['changedOwnedBytes'],
                  immutablePhysicalPayloadUnchanged=True, ownedDataChangesAtInitializationOnly=True,
                  everyPriorSourceByteConservedOutsideBothAdditiveFragments=True,
                  originalNaturalIntegrationRequirements=proof['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=proof['originalRemainingWorkGroups'], inputHashes=pins,
                  previousGoalTurnClassification='progress: encoded six shrinking poses and qualified complete corrected source/data',
                  thisGoalTurnClassification='progress: assembled exact complete successor and qualified guarded build inputs',
                  nativeRuntimeAccepted=False, nativeRepairAccepted=False, fullPortAcceptance=False,
                  newEmulatorBuilds=0, newROMCopies=0, newRawGameplayMedia=0, newZIPs=0,
                  publicPlayableChanged=False, goalStatus='active')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=True, sourceStage=str(STAGE), stagedSourceHashes=staged,
                         proposedGuestSHA256=report['proposedGuestSHA256'], nativeRepairAccepted=False)))


if __name__ == '__main__':
    main()
