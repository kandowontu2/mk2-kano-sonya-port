"""Seal actual failed provenance and release only its original RAM parent."""
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

import capture_native_sonya_raiden_cache_cause as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT / 'audit_native_sonya_raiden_cache_cause_preserved'
RETIRED = ROOT / 'audit_native_sonya_raiden_cache_cause_retirement'
PARENT, GAME = 145372, 190268


def prepare(ram):
    need(os.getpid() == PARENT and not OUT.exists(), 'Original retained forensic parent only')
    terminal = json.loads((capture.OUT / 'native_terminal.json').read_text())
    proof = json.loads((capture.OUT / 'guest_memory_proof.json').read_text())
    failed = json.loads((capture.OUT / 'current_capture_failure.json').read_text())
    repair = ROOT / 'audit_native_paired_stumble_table_bounded_source/report.json'
    qualified = json.loads(repair.read_text())
    before = json.loads((capture.OUT / 'input_hashes_before.json').read_text())
    need(terminal['nativeExit'] == 0 and terminal['identity']['ProcessId'] == GAME and
         terminal['identity']['ParentProcessId'] == PARENT and not failed['passed'] and
         proof['everyActualByteComparedInRAM'] and
         hashlib.sha256(ram['guest']).hexdigest().upper() == proof['sha256'] and
         qualified['passed'] and qualified['actualRootCauseSourceMatched'] and
         qualified['actualGlobalDecoderStores'] == 146 and
         all(sha(p) == h for p, h in before.items()) and
         all(sha(p) == h for p, h in qualified['inputHashes'].items()),
         'Actual failed current guest/whole trace and independently qualified source cause')
    scope, host = capture.prior.prior.prior.functions(ram['scope']['native'])
    need(scope['capture'].__code__.co_code == ram['scope']['capture'].__code__.co_code,
         'Whole actually executed host reconstructed without invoking gameplay')
    raw, rendered = ram['scope']['RAM_RAW'], ram['scope']['RAM_IMAGES']
    need(len(raw) == len(rendered) == 1, 'Original bounded selection buffers only')
    OUT.mkdir()
    with gzip.open(OUT / 'original_executed_sources.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump(dict(wholeExecutedHost=host, files={p: dict(sha256=h, text=Path(p).read_text())
            for p, h in before.items() if Path(p).suffix.lower() in ('.py', '.lua', '.cpp', '.h', '.cmd')}), stream)
    pins = dict(before)
    for path in [Path(__file__), repair, *capture.OUT.rglob('*'), *capture.SOURCE.rglob('*'),
                 *capture.INIT.rglob('*'), OUT / 'original_executed_sources.json.gz']:
        if path.is_file():
            pins[str(path.resolve())] = sha(path)
    report = dict(passed=False, preservationPassed=True, nativeGameplayAcceptance=False,
        exactNativeGame=GAME, exactRAMParent=PARENT, nativeExit=0,
        confirmedRealGlobalCacheCorruption=True, actualGlobalStores=146,
        completeNativeProvenanceRows=1800, actualCause=qualified['actualCause'],
        originalRawRasterInventory={name: dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest().upper())
                                    for name, data in raw.items()},
        originalPILBufferCount=len(rendered), individuallyViewedInThisTrial=False,
        imageNotUsedToInferGameplayAcceptance=True, allOriginalInputsPreserved=True,
        proposedFixOnlySourceAccepted=True, inputHashes=pins,
        originalNaturalIntegrationRequirements=qualified['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=qualified['originalRemainingWorkGroups'],
        newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
        publicPlayableChanged=False, fullPortAcceptance=False, goalStatus='active')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(preserved=True, nativeFailureStillFalse=True,
                         originalRawBuffersToRelease=len(raw), originalPILBuffersToRelease=len(rendered))), flush=True)


def retire():
    need(not RETIRED.exists(), 'Fresh exact forensic retirement')
    report = json.loads((OUT / 'report.json').read_text())
    need(report['preservationPassed'] and not report['passed'] and
         all(sha(p) == h for p, h in report['inputHashes'].items()), 'Full failed outcome and originals retained')
    command = f'Get-CimInstance Win32_Process -Filter "ProcessId={PARENT} OR ProcessId={GAME}" | Select-Object ProcessId | ConvertTo-Json -Compress'
    query = subprocess.run(['powershell.exe', '-NoProfile', '-Command', command], capture_output=True, text=True)
    need(query.returncode == 0 and not query.stdout.strip() and not query.stderr.strip(),
         'Both exact original producers absent, no review server was created')
    RETIRED.mkdir()
    (RETIRED / 'report.json').write_text(json.dumps(dict(passed=True, failedNativeOutcomePreserved=True,
        exactNativeGameRetired=GAME, exactRAMParentRetired=PARENT, originalRawBuffersReleased=1,
        originalPILBuffersReleased=1, noReviewServerCreated=True,
        inputHashes={str(Path(__file__).resolve()): sha(__file__), str(OUT / 'report.json'): sha(OUT / 'report.json')},
        fullPortAcceptance=False, goalStatus='active'), indent=2) + '\n')
    print(json.dumps(dict(retired=True, originalFailureAndCausePreserved=True)), flush=True)


if __name__ == '__main__':
    retire()
