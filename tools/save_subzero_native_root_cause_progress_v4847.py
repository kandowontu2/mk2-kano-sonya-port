"""Additive full-scope progress, never a source-only runtime/release claim."""
import hashlib, json, subprocess
from pathlib import Path
import save_jax_evasion_and_subzero_overrun_progress_v4815 as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
BASE = previous.BASE
PARENTS = previous.PARENTS + [previous.OUT / 'progress.json']
OUT = ROOT / 'audit_v4848_subzero_native_root_cause_progress'

def main():
    need(not OUT.exists(), 'Fresh additive journal')
    base = json.loads(BASE.read_text())
    inherited = dict(base['inputHashes'])
    for parent in PARENTS:
        for path, digest in json.loads(parent.read_text())['newInputHashes'].items():
            need(path not in inherited or inherited[path] == digest, 'Consistent inherited source/evidence')
            inherited[path] = digest
    need(all(sha(path) == digest for path, digest in inherited.items()), 'Inherited full-scope evidence unchanged')
    pins = {}
    def pin(path, wanted=None):
        path = Path(path).resolve(); key = str(path); digest = sha(path)
        need(wanted is None or wanted == digest, 'Exact actual input hash')
        need(key not in inherited or inherited[key] == digest, 'Inherited immutable bytes')
        need(key not in pins or pins[key] == digest, 'Consistent new immutable bytes')
        if key not in inherited:
            pins[key] = digest
    for path in [BASE, *PARENTS, Path(__file__).resolve(), Path(previous.__file__).resolve()]:
        pin(path)
    reports = {}
    for key, relative in {
        'trace': 'audit_v4836_sonya_subzero_cache_trace_observed/report.json',
        'cause': 'audit_v4839_native_subzero_victim_offset_qualified/report.json',
        'source': 'audit_v4846_native_subzero_offset_staged_source_checked/report.json',
        'observer': 'audit_v4834_sonya_subzero_cache_trace_source_checked/report.json',
    }.items():
        path = ROOT / relative
        reports[key] = json.loads(path.read_text()); pin(path)
        for input_path, digest in reports[key].get('inputHashes', {}).items():
            pin(input_path, digest)
    cause, source = reports['cause'], reports['source']
    need(cause['passed'] and cause['actualNativeTraceRows'] == 915 and cause['firstBadFrame'] == 108255,
         'Actual independently bound original native corruption route')
    need(len(cause['actualFaultsRejected']) == 8 and source['passed'] and
         len(source['actualSourceFaultsRejected']) == 6, 'Actual native/source fault rejection retained')
    need(cause['expectedRepairedGuestSHA256'] == source['expectedGuestSHA256'] and
         not cause['compiledFixAccepted'] and not source['compiledFixAccepted'],
         'Source initializer equals qualified whole guest; compilation still pending')
    failed = ROOT / 'tools/qualify_native_subzero_offset_staged_source_v4842.py'
    try:
        compile(failed.read_text(), str(failed), 'exec')
    except SyntaxError as error:
        need(error.lineno == 48 and 'never closed' in str(error), 'Preserved actual failed checker')
    else:
        raise ValueError('Executed parse-failed checker changed')
    pin(failed)
    for relative in (
        'tools/qualify_native_subzero_offset_staged_source_v4845.py',
        'tools/inspect_sonya_subzero_cache_trace_v4830.py',
        'tools/inspect_sonya_subzero_cache_trace_v4837.py',
        'audit_v4829_sonya_subzero_cache_trace_observed/report.json',
        'workspace_cleanup_followup_2026-10-05/verified_summary.json',
        'WORKSPACE_CLEANUP_CURRENT.md',
    ):
        pin(ROOT / relative)
    cleanup = json.loads((ROOT / 'workspace_cleanup_followup_2026-10-05/verified_summary.json').read_text())
    need(cleanup['passed'] and cleanup['currentCMDBootPassed'], 'Existing cleanup retained; no new space-reclaim claim')
    report = dict(
        schema=1, baseFullScopeCheckpoint=str(BASE), parentAdditiveJournals=[str(p) for p in PARENTS],
        mergeRule='Additive to4557 and every parent; preserve all five original requirements and finite prior results. The real corruption is now root-caused, not fixed in a tested binary. Do not promote a source-only repair or transport-only pass.',
        remaining=base['remaining'], goalStatus='active', fullPortAcceptance=False, finishedRelease=False,
        newInputHashes=pins,
        thisGoalTurnClassification='progress: native corruption reproduced twice on original physical policy. The first observer failed because A15 is not an exposed CPU state; actual SP register and explicit callback-error handling corrected in fresh source. Corrected native trace produced915 actual records bound to original guest instructions and payload. Native Sub-Zero action0616 reads ID18 beyond12-word victim-offset table, obtains2B90 from adjacent shatter pointer, advances valid ownmain40 into FFFFFFFF, and native cache overwrites physical globals. Qualified guarded initialized-ROM table extension preserves17 existing words and adds separate true17/18 zero-offset rows;39 guest bytes change, no runtime identity/cache/task fix. Correct source4844 is based on actual compiled3836 bytes, not dirty checkout. Fresh4845 source proof passes6 actual faults; preserved4842 parse failure not edited.',
        actualNativeRootCause=cause['actualNativeRootCause'], actualNativeCauseReport=str(ROOT / 'audit_v4839_native_subzero_victim_offset_qualified/report.json'),
        nativeDefect=dict(firstFrame=108255, actualTraceRows=915, action='0616', rootCauseQualified=True,
            ordinaryFreezeVersusFinisherDistinguished=True, actualVictimIdentity=18, stableAllContextsContradicted=True),
        stagedRepair=dict(source=source['stagedSource'], sourceSHA256=source['stagedSourceSHA256'],
            actualCompiledBaseSHA256=source['baseCompiledSourceSHA256'], expectedGuestSHA256=source['expectedGuestSHA256'],
            initializedGuestByteDelta=39, originalNativeInstructionsAndTasksPreserved=True,
            earlierDirtyBaselineStagesNotBuildEligible=True, compiledFixAccepted=False, nativeRuntimeAccepted=False),
        preservedFailures=dict(firstObserver='A15 nil; records1/trace0, despite transport terminal0. Not a trace acceptance.',
            failedSourceChecker=str(failed), earlierStages='4840 extra EOF and dirty baseline;4841 dirty baseline. Do not build either.'),
        remainingSubzeroFinisher='Later body lookup clamps17/18 to11/Jax. Requires dedicated own-character shatter body art/data and actual native rendering/cleanup/audio proof; table overrun fix alone does not complete this finisher.',
        currentDirtyCheckoutAndPublicChanged=False, newBuilds=0, rawMediaFilesWritten=0, newlyDeletedFiles=0,
        cleanupAccounting=dict(priorCleanupVerified=True, priorReclaimedAllocatedBytes=cleanup['reclaimedAllocatedBytes'],
            priorReclaimedGiB=cleanup['reclaimedGiB'], newlyReclaimedAllocatedBytes=0,
            policy='Retain current playable/release/source and necessary evidence. RAM-only raw guest/media; compressed small new source and digest reports. Never regenerate retired evidence.'),
        nextAction='Compile source4844 against actual3836 frozen driver/header/other native inputs, preserving dirty checkout and installed/public executables with exact backups/restoration. Existing compiler objects/makefiles are present. Canonical current driver/header/machine differ from actual3836, CPU gfx/ops match; do not compile dirty baseline accidentally. Verify actual new initialized whole guest33018F... then same original physical controls/native action0616 without global overrun. Complete own shatter-body art/data separately. All five full-port requirements remain open.'
    )
    need(len(report['remaining']) == 5 and all(sha(p) == h for p, h in pins.items()), 'Original five groups and new whole evidence unchanged')
    OUT.mkdir()
    need(subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(OUT)], capture_output=True).returncode == 0, 'Compression before writes')
    (OUT / 'progress.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(journal=str(OUT / 'progress.json'), newPins=len(pins),
        nativeRootCauseQualified=True, stagedSourceQualified=True, compiledFixAccepted=False,
        fullPortAcceptance=False, newBuilds=0, newlyDeletedFiles=0), indent=2), flush=True)

if __name__ == '__main__':
    main()
