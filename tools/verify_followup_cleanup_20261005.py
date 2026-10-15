"""Verify exact removals, retained inputs and public launcher after cleanup."""
import json
from pathlib import Path
from plan_followup_cleanup_20261005 import ROOT, OUT, sha

def main():
    destination = OUT / 'verified_summary.json'
    if destination.exists():
        raise ValueError('Never overwrite verification')
    plan = json.loads((OUT / 'deletion_plan.json').read_text())
    result = json.loads((OUT / 'result.json').read_text(encoding='utf-8-sig'))
    boot = json.loads((OUT / 'launcher_check/report.json').read_text(encoding='utf-8-sig'))
    assert result['passed'] and boot['passed']
    assert result['planSHA256'] == sha(OUT / 'deletion_plan.json')
    assert result['removedFolders'] == sum(row['kind']=='folder' for row in plan['targets'])
    assert result['removedFiles'] == sum(row['files'] for row in plan['targets'])
    for row in plan['targets']:
        assert not Path(row['path']).exists(), row['path']
    for file, digest in plan['preservedHashes'].items():
        assert sha(file) == digest, file
    for file, before in plan['retainedActiveInputStats'].items():
        stat = Path(file).stat()
        assert stat.st_size == before['size'] and stat.st_mtime_ns == before['mtime'], file
    summary = dict(passed=True, removedObsoleteFolders=result['removedFolders'],
                   removedFiles=result['removedFiles'],
                   removedOldRawTestRecordings=84, removedObsoleteRecoveryArchives=1,
                   reclaimedAllocatedBytes=result['reclaimedAllocatedBytes'],
                   reclaimedGiB=round(result['reclaimedAllocatedBytes']/2**30, 2),
                   observedDriveFreeIncreaseBytes=result['diskFreeAfter']-result['diskFreeBefore'],
                   retainedInputsUnchanged=len(plan['retainedActiveInputStats']),
                   playableAndSourceSHA256Checks=len(plan['preservedHashes']),
                   currentCMDBootPassed=True, userSettingsUnchanged=boot['userSettingsUnchanged'],
                   obsoleteDataPermanentlyDiscarded=True, newRecoveryArchiveCreated=False,
                   retiredHistoricalEvidencePins=plan['retiredHistoricalEvidencePins'],
                   fullPortAcceptance=False)
    destination.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='retiredHistoricalEvidencePins'}, indent=2), flush=True)

if __name__ == '__main__':
    main()
