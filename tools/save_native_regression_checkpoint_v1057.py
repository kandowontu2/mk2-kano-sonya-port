"""Preserve twenty current native regressions without broadening acceptance."""
import json
import shutil
from pathlib import Path
import verify_native_regressions_v1056 as proof

ROOT = proof.ROOT
OUT = ROOT / 'audit_v1057_native_regression_checkpoint'


def main():
    if OUT.exists():
        raise ValueError('Preserve checkpoint evidence')
    previous_path = ROOT / 'audit_v1054_native_arm_rip_checkpoint/checkpoint.json'
    previous = json.loads(previous_path.read_text())
    pins = dict(previous['inputHashes'])
    for filename, wanted in pins.items():
        assert proof.digest(Path(filename)) == wanted, filename
    report_path = ROOT / 'audit_v1056_native_regressions_checked/report.json'
    report = json.loads(report_path.read_text())
    assert report['passed'] and report['newNativeArmRipRegressionsAccepted']
    assert not report['fullPortAccepted'] and len(report['cases']) == 20
    units_path = ROOT / 'audit_v1058_native_regression_proof_units/unit-results.json'
    units = json.loads(units_path.read_text())
    assert units['passed'] and units['corruptionChecks'] == 3
    assert not units['evidenceFilesModified'] and not units['sourceFilesModified']
    expected = {case for killer in ('jax', 'baraka', 'cage', 'kitana', 'reptile')
                for case in proof.cases(killer)}
    assert set(report['cases']) == expected
    for filename, wanted in report['inputHashes'].items():
        assert proof.digest(Path(filename)) == wanted, filename
        if filename in pins:
            assert pins[filename] == wanted, filename
        pins[filename] = wanted

    # Transfer earlier manual reviews by exact images, not build similarity.
    identical_pictures = {}
    for killer, version, suffix in (
            ('jax', 1029, 'clap_grounding'),
            ('baraka', 1034, 'jax_clap_grounding_regression')):
        count = 0
        for name in ('kano', 'sonya'):
            for side in (1, 2):
                baseline = ROOT / f'audit_v{version}_{killer}_{name}_p{side}_{suffix}/snap'
                current = ROOT / f'audit_v1055_{killer}_{name}_p{side}_arm_regression/snap'
                a = {str(p.relative_to(baseline)): p for p in baseline.rglob('*.png')}
                b = {str(p.relative_to(current)): p for p in current.rglob('*.png')}
                assert a and a.keys() == b.keys()
                for relative, path in b.items():
                    assert path.read_bytes() == a[relative].read_bytes(), str(path)
                    count += 1
                    pins[str(path)] = proof.digest(path)
        identical_pictures[killer] = count
    identical_pictures.update({killer: sum(
        row['actualIdenticalPNGs'] for row in report['cases'].values()
        if row['killer'] == killer) for killer in ('cage', 'kitana', 'reptile')})
    assert proof.digest(ROOT / 'mame-mkp/mkport.exe') == (
        '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891')
    for case in sorted(expected):
        for path in (ROOT / case).rglob('*'):
            if path.is_file():
                pins[str(path)] = proof.digest(path)
    for path in (previous_path, report_path, units_path):
        pins[str(path)] = proof.digest(path)

    OUT.mkdir()
    for filename in (
            'tools/run_native_regressions_v1055.ps1',
            'tools/verify_native_regressions_v1056.py',
            'tools/test_native_regressions_v1058.py',
            'tools/save_native_regression_checkpoint_v1057.py',
            'STATUS_2026-10-03_CURRENT_NATIVE_REGRESSIONS.md'):
        path = ROOT / filename
        frozen = OUT / 'input_sources' / filename
        frozen.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, frozen)
        pins[str(path)] = proof.digest(path)
        pins[str(frozen)] = proof.digest(frozen)
    data = {
        'candidate': proof.CANDIDATE,
        'scope': report['scope'],
        'historicalPinsRevalidated': len(previous['inputHashes']),
        'currentRegressionCases': 20,
        'regressionProofCorruptionChecks': 3,
        'actualPNGsIdenticalToPriorVerifiedCases': identical_pictures,
        'jaxGroundedBodyDMAs': sum(row['ownedBodyDMAs'] for row in report['cases'].values()
                                  if row['killer'] == 'jax'),
        'barakaOwnedDMAs': sum(row['ownedDMAs'] for row in report['cases'].values()
                              if row['killer'] == 'baraka'),
        'nativeGameSourceChangesThisTurn': False,
        'artworkChangesThisTurn': False,
        'newCandidateRegressionsAccepted': True,
        'previousArmRipScopePreserved': previous['scope'],
        'installedExecutableUnchanged': True,
        'existingLaunchersNotUpdated': True,
        'releaseZipNotUpdated': True,
        'naturalAlternateSelectionAccepted': False,
        'allStockFatalitiesAccepted': False,
        'allArenasAccepted': False,
        'fullTowerAccepted': False,
        'finalCombinedGameplayAndUIAccepted': False,
        'fullPortAccepted': False,
        'evidencePins': len(pins),
        'inputHashes': pins,
    }
    (OUT / 'checkpoint.json').write_text(json.dumps(data, indent=2) + '\n')
    for filename, wanted in pins.items():
        assert proof.digest(Path(filename)) == wanted, filename
    print(json.dumps({k: v for k, v in data.items() if k != 'inputHashes'}, indent=2))


if __name__ == '__main__':
    main()
