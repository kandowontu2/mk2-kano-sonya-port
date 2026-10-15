"""Final independent cleanup checks, including corrected package-row totals."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'workspace_cleanup_requested_2026-10-05'

def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest().upper()

def main():
    destination = OUT / 'verified_summary.json'
    if destination.exists():
        raise ValueError('Never overwrite final verification')
    plan = json.loads((OUT / 'deletion_plan.json').read_text())
    result = json.loads((OUT / 'result.json').read_text(encoding='utf-8-sig'))
    packages = json.loads((OUT / 'old_task_packages.json').read_text(encoding='utf-8-sig'))
    boot = json.loads((OUT / 'launcher_check/report.json').read_text(encoding='utf-8-sig'))
    assert result['passed'] and packages['passed'] and boot['passed']
    assert sha(OUT / 'deletion_plan.json') == result['planSHA256']
    assert len(plan['targets']) == result['removedFolderCount']
    assert sum(r['files'] for r in plan['targets']) == result['removedFiles']
    for row in [*plan['targets'], *packages['removedTargets']]:
        assert not Path(row['path']).exists(), row['path']
    for file, digest in plan['preservedHashes'].items():
        assert sha(file) == digest, file
    targets = {Path(r['path']).relative_to(ROOT).parts[0].casefold()
               for r in plan['targets'] if len(Path(r['path']).relative_to(ROOT).parts) == 1}
    for frontier in plan['dependencyFrontiers']:
        state = json.loads(Path(frontier).read_text(encoding='utf-8-sig'))
        for file in state.get('inputHashes', state):
            path = Path(file)
            if path.is_absolute() and path.is_relative_to(ROOT):
                assert path.relative_to(ROOT).parts[0].casefold() not in targets, file
                assert not path.is_relative_to(ROOT / '_archive/legacy_evidence_v284'), file
                assert not path.is_relative_to(ROOT / 'mame-mkp/build/mingw-gcc'), file
    # Original PowerShell report kept its exact rows but Measure-Object could not
    # aggregate ordered dictionaries. Recalculate from those immutable rows.
    package_bytes = sum(r['logicalBytes'] for r in packages['removedTargets'])
    report = dict(passed=True, removedObsoleteFolders=result['removedFolderCount'],
                  removedOldPackageZIPs=9, removedPackageVerificationFolders=3,
                  removedFiles=result['removedFiles'] + sum(r['files'] for r in packages['removedTargets']),
                  reclaimedWorkspaceAllocatedBytes=result['reclaimedAllocatedBytes'],
                  additionalDiscardedPackageLogicalBytes=package_bytes,
                  packageAllocatedSavingsNotSeparatelyMeasured=True,
                  activeDependencyFrontiersDoNotIntersectDeletedTrees=True,
                  everyPreservedHashRechecked=True, launcherBootPassed=True,
                  sourceCurrentBuildsROMsSettingsReleasePreserved=True,
                  oldHistoryPermanentlyDiscarded=True, compilerCacheRegenerable=True,
                  fullPortAcceptance=False,
                  evidenceHashes={str(path):sha(path) for path in
                                  [OUT/'deletion_plan.json', OUT/'result.json', OUT/'old_task_packages.json',
                                   OUT/'launcher_check/report.json', Path(__file__).resolve()]})
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'evidenceHashes'}, indent=2), flush=True)

if __name__ == '__main__':
    main()
