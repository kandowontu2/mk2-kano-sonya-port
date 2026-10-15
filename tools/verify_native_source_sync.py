"""Read-only verification of source sync and explicitly relocated historical pins.

This does not rerun gameplay/audio acceptance and never rewrites old reports.
Only the three exact pre-sync source paths can resolve to preserved old bytes.
Current canonical sources must independently match the actual compiled inputs.
"""
import hashlib
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / 'diagnostic_native_selector_layers_long'
BACKUP = ROOT / 'audit_native_source_sync'
OLD = {
    'midtunit.cpp': '07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
    'midtunit_m.cpp': 'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
    'midtunit.h': '256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
}
NEW = {
    'midtunit.cpp': 'F35CD66B766835203BE4D9AF19ED4096F79947F65310868DE8138CB82BFD1C7D',
    'midtunit_m.cpp': 'A32C860194808831589A7D06F47A564708162B723391801EC5A310113767ACDD',
    'midtunit.h': '4995B72D7492C4AB45DEEC21212E5B5D60F94495F10078F081A8D082D9683232',
}
FIXED = {
    BUILD / 'build-info.json': 'F06150835A253E079449F6C1234509F3640B25A81284900C84B912EE45B309F1',
    BUILD / 'mkport_candidate.exe': 'EBDFEB6CCA3617308F1448A4A0F6778E3E787420CACF3D11E9B4F40358C87F6A',
    BUILD / 'roms/mk2ks/mk2ks.mdata': 'A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3',
    ROOT / 'audit_current_launcher_routing/PLAY_LATEST_KANO_SONYA_before_current.cmd': 'D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5',
    ROOT / 'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip': '4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C',
}
REPORTS = {
    ROOT / 'audit_native_selector_cpu_startup_ring_audio_checked/report.json': 'C5A9858649C2DCA47A645EC8B2D60B4E76CC5D63CB4B01ED1A28DB63BD8EC8FD',
    ROOT / 'audit_native_selector_exit_stock_comparison_saved_checked/report.json': '191746B0FA250DB293081DE943ACF774C6899DB9BFDF2009792FF6995DCB8D6C',
}
RETIRED_ARCHIVE = ROOT / 'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
RETIRED_ARCHIVE_SHA256 = '4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C'
RETIREMENT_RECEIPT = ROOT / 'audit_requested_old_release_retirement_20261015/deletion_receipt.json'
RETIREMENT_RECEIPT_SHA256 = '94F645C7328D8EAAABBB520CFD0EF59A506950DEABA27FA4D142DC0DD06A2199'


def need(value, message):
    if not value:
        raise AssertionError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest().upper()


def validate_archive_retirement(path, expected, receipt, receipt_digest, archive_present):
    """One explicit removed distribution artifact, never missing source bytes."""
    need(Path(path).resolve() == RETIRED_ARCHIVE.resolve(), 'Exact archival retirement path')
    need(expected == RETIRED_ARCHIVE_SHA256, 'Exact historical archive digest')
    need(receipt_digest == RETIREMENT_RECEIPT_SHA256, 'Pinned executed retirement receipt')
    need(not archive_present, 'Retired archive must actually be absent')
    need(receipt.get('userAuthorizedOldReleaseRemoval') is True, 'Explicit user archive removal')
    need(receipt.get('currentRebuildPreserved') is True, 'Retirement preserved current rebuild')
    need(receipt.get('archiveCreated') is False and receipt.get('noPolicyBypassAttempted') is True,
         'No replacement archive or policy bypass')
    need(receipt.get('oldArchiveBytesStillVerifiableAfterDeletion') is False,
         'Never claim deleted archive bytes freshly checked')
    entries = [row for row in receipt.get('removedFiles', [])
               if Path(row['path']).resolve() == RETIRED_ARCHIVE.resolve()]
    need(len(entries) == 1 and entries[0].get('removed') is True and
         entries[0].get('SHA256') == expected and entries[0].get('bytes') == 57592947,
         'Exact successfully removed archival artifact')
    latest = Path(receipt['latestZIP']).resolve()
    need(latest.is_relative_to(ROOT.resolve()) and latest != RETIRED_ARCHIVE.resolve(),
         'Latest player release retained inside workspace')
    return dict(originalPath=str(RETIRED_ARCHIVE), historicalSHA256=expected,
                retirementReceipt=str(RETIREMENT_RECEIPT), retirementReceiptSHA256=receipt_digest,
                oldArchiveBytesFreshlyRevalidated=False, currentRebuildDependency=False,
                latestRetainedPlayerZIP=str(latest), latestSHA256=receipt['latestSHA256'])


def verify():
    # The inventory caches bytes only within this read-only run; a final fresh
    # census repeats every hash after the gate and effective counterexamples.
    hashes = {}
    requests = []
    migrations = []
    retirements = {}
    def check(path, expected, role):
        path = Path(path).resolve()
        key = str(path)
        if path == RETIRED_ARCHIVE.resolve():
            receipt = json.loads(RETIREMENT_RECEIPT.read_text(encoding='utf-8-sig'))
            record = validate_archive_retirement(path, expected, receipt, sha(RETIREMENT_RECEIPT),
                                                path.exists() or path.is_symlink())
            # Actual receipt/latest bytes use normal hash requests; deleted
            # archive bytes do not enter hashes under a fabricated digest.
            check(RETIREMENT_RECEIPT, RETIREMENT_RECEIPT_SHA256, 'executed archive retirement receipt')
            check(record['latestRetainedPlayerZIP'], record['latestSHA256'], 'retained current player release')
            retirements[key] = record
            return record
        if key not in hashes:
            hashes[key] = sha(path)
        requests.append((key, expected, role))

    for path, expected in {**FIXED, **REPORTS}.items():
        check(path, expected, 'immutable build/public/report')
    manifest = json.loads((BUILD / 'build-info.json').read_text())
    need(manifest['total_sample_channels'] == 19, 'Actual compiled nineteen channels')
    need(not manifest['public_build_promoted'] and not manifest['full_port_accepted'],
         'No full-port or release promotion inferred from source synchronization')
    compiled = manifest['canonical_source_hashes_at_compile']
    need(len(compiled) == 15, 'Entire tracked canonical compile-input inventory')
    canonical = ROOT / 'mame-mkp/src/mame/midway'
    relocated = {}
    for name, old_hash in OLD.items():
        current = canonical / name
        old = BACKUP / ('canonical_' + Path(name).stem + '_before_sync' + Path(name).suffix)
        snapshot = BUILD / 'input_sources/mame-mkp/src/mame/midway' / name
        need(compiled[str(current)] == NEW[name], 'Manifest independently pins actual source')
        check(current, NEW[name], 'current synchronized source')
        check(snapshot, NEW[name], 'immutable actual compiled snapshot')
        check(old, old_hash, 'exact preserved historical source')
        need(current.read_bytes() == snapshot.read_bytes(), 'Whole byte equality, not logical/EOL-only')
        relocated[str(current.resolve())] = (old, old_hash)
        migrations.append(dict(originalPath=str(current), oldSHA256=old_hash,
                               preservedPath=str(old), newSHA256=NEW[name],
                               compiledSnapshotPath=str(snapshot)))
    for path, expected in compiled.items():
        check(path, expected, 'whole current tracked compile-source inventory')
    # Original reports keep their old launcher hash. Resolve only this exact
    # known pin to preserved bytes; do not rewrite historical report claims.
    relocated[str((ROOT / 'PLAY_LATEST_KANO_SONYA.cmd').resolve())] = (
        ROOT / 'audit_current_launcher_routing/PLAY_LATEST_KANO_SONYA_before_current.cmd',
        'D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5')
    historical = []
    for path in REPORTS:
        report = json.loads(path.read_text())
        need(report['passed'] is True, 'Original report remains passed historically')
        pins = report['inputHashes']
        moved = []
        retired_pins = []
        for pin, expected in pins.items():
            original = str(Path(pin).resolve())
            if original in relocated:
                backup, old_hash = relocated[original]
                need(expected == old_hash, 'Only exact known old source pin may relocate')
                check(backup, expected, 'explicit historical pin relocation')
                moved.append(dict(originalPath=pin, preservedPath=str(backup), SHA256=expected))
            else:
                retired = check(pin, expected, 'unchanged historical input pin')
                if retired:
                    retired_pins.append(retired)
        historical.append(dict(report=str(path), SHA256=REPORTS[path],
                               originalInputPinCount=len(pins), explicitlyRelocatedPins=moved,
                               originalReportRewritten=False,
                               explicitlyRetiredArchivePins=retired_pins,
                               unchangedOriginalPathsGateStillValid=not moved and not retired_pins,
                               gameplayOrAudioRerun=False))

    def gate(observed):
        for path, expected, role in requests:
            need(observed.get(path) == expected, role + ': ' + path)
    gate(hashes)
    retirement_faults = []
    receipt = json.loads(RETIREMENT_RECEIPT.read_text(encoding='utf-8-sig'))
    for kind in ('wrong_path', 'wrong_archive_digest', 'wrong_receipt_digest', 'archive_present',
                 'not_removed', 'missing_authorization', 'rebuild_not_preserved'):
        altered = copy.deepcopy(receipt)
        path, expected, digest, present = RETIRED_ARCHIVE, RETIRED_ARCHIVE_SHA256, RETIREMENT_RECEIPT_SHA256, False
        if kind == 'wrong_path': path = BUILD / 'mkport_candidate.exe'
        if kind == 'wrong_archive_digest': expected = '0' * 64
        if kind == 'wrong_receipt_digest': digest = '0' * 64
        if kind == 'archive_present': present = True
        if kind == 'not_removed':
            next(row for row in altered['removedFiles'] if Path(row['path']).resolve() == RETIRED_ARCHIVE.resolve())['removed'] = False
        if kind == 'missing_authorization': altered['userAuthorizedOldReleaseRemoval'] = False
        if kind == 'rebuild_not_preserved': altered['currentRebuildPreserved'] = False
        try:
            validate_archive_retirement(path, expected, altered, digest, present)
        except AssertionError:
            retirement_faults.append(kind)
        else:
            raise AssertionError('Invalid archive retirement accepted: ' + kind)
    faults = []
    # Counterexamples affect the real checked path's digest, not an unused field.
    for path in [canonical / 'midtunit.cpp', canonical / 'midtunit_m.cpp',
                 canonical / 'midtunit.h',
                 *[Path(item['preservedPath']) for item in migrations],
                 BUILD / 'mkport_candidate.exe', BUILD / 'roms/mk2ks/mk2ks.mdata',
                 ROOT / 'audit_current_launcher_routing/PLAY_LATEST_KANO_SONYA_before_current.cmd',
                 RETIREMENT_RECEIPT, Path(receipt['latestZIP']), *REPORTS]:
        key = str(path.resolve())
        bad = dict(hashes)
        bad[key] = ('0' if hashes[key][0] != '0' else '1') + hashes[key][1:]
        try:
            gate(bad)
        except AssertionError as error:
            faults.append(dict(path=key, rejectedBy=str(error)))
        else:
            raise AssertionError('Effective provenance corruption accepted: ' + key)
    gate(hashes)
    need(all(sha(path) == digest for path, digest in hashes.items()),
         'Final fresh whole-file census after counterexamples')
    return dict(passed=True, goalStatus='active', classification='progress',
                synchronizedSources=migrations, trackedCanonicalCompileInputs=15,
                historicalEvidence=historical, checkedUniqueWholeFiles=len(hashes),
                retiredHistoricalArchivePins=list(retirements.values()),
                effectiveArchiveRetirementFaultsRejected=retirement_faults,
                effectiveFaultsRejected=faults,
                verifierSHA256=sha(__file__),
                exactNewlineFormatting='Original compiled per-line endings restored only after whole logical equality',
                metadataEmissionErrorDuringFormatting='PowerShell true token lacked dollar prefix; formatting and whole-file gates succeeded; corrected read-only verifier independently rechecks all bytes',
                freshCompilationPerformed=False, newNativeGames=0, newBuilds=0,
                publicPlayableChanged=True, releaseZIPChanged=False,
                historicalReportsRewritten=False, fullPortAcceptance=False,
                scope='Source/provenance synchronization with explicit legacy launcher-pin preservation; unversioned CMD aliases now route the current native playtest. All original fourteen requirements and six remaining groups stay active')


if __name__ == '__main__':
    try:
        print(json.dumps(verify(), indent=2))
    except Exception as error:
        print(json.dumps(dict(passed=False, error=repr(error), fullPortAcceptance=False)))
        raise
