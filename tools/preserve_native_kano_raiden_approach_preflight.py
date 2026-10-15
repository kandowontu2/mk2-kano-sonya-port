"""Capture the exact original preboot filename-guard failure, no native replay."""
import hashlib
import json
import os
from pathlib import Path
import native_process_census_v6647 as census

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_kano_raiden_paired_victim_approach_preflight_failure'


def preserve(ram, failure):
    if not (os.getpid() == 22536 and not OUT.exists() and not ram and not census.census() and
            not failure['passed'] and failure['error'] == "ValueError('Whole existing native cache observer, one driver leaf only')" and
            all(not (ROOT / ('audit_native_kano_raiden_paired_victim_approach_' + suffix)).exists()
                for suffix in ('ram', 'source', 'initializer', 'previous_initializer'))):
        raise ValueError('Same exact original source-only failure before any native boot or initializer')
    paths = [Path(__file__).resolve(), ROOT / 'tools/run_native_kano_raiden_paired_victim_approach.py',
             ROOT / 'tools/run_native_kano_raiden_paired_victim.py',
             *[ROOT / ('mk2ks_native_kano_raiden_victim_approach_' + suffix + '.lua')
               for suffix in ('driver', 'cache', 'provenance')]]
    report = dict(passed=False, phase='source_only_cache_leaf_preflight', originalFailure=failure,
                  nativeBootOccurred=False, originalRAMWasEmpty=True, actualRAMHost=22536,
                  diagnosis='Whole guard retained an obsolete exact driver filename after the declared leaf change.',
                  inputHashes={str(path): hashlib.sha256(path.read_bytes()).hexdigest().upper() for path in paths},
                  newBuilds=0, newROMCopies=0, newRawMedia=0, fullPortAcceptance=False, goalStatus='active')
    OUT.mkdir()
    (OUT / 'failure.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Exact original source-only failure preserved; no native game ran.', flush=True)
    return report
