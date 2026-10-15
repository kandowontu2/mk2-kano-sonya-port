"""Preserve raw-capture-vs-qualified-receipt lookup mistake; no game booted."""
import gzip,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    out=ROOT/'audit_native_sonya_cpu_ui_preflight_failure'
    if out.exists():raise ValueError('Fresh first preflight failure archive')
    raw=json.loads((ROOT/'audit_native_current_ui_ram/kano_p2/result.json').read_text())
    qualified=json.loads((ROOT/'audit_native_current_ui_owned_checked/report.json').read_text())
    if not(not raw['passed'] and qualified['passed'] and not (ROOT/'audit_native_sonya_cpu_finisher').exists()):
        raise ValueError('Original rejected owner-assumption receipt, accepted same-run correction, no native test folder')
    paths=[ROOT/'tools/capture_native_sonya_cpu_finisher.py',ROOT/'mk2ks_native_sonya_cpu_finisher.lua']
    out.mkdir()
    with gzip.open(out/'original_preflight_sources.json.gz','wt',encoding='utf-8') as f:
        json.dump({str(p):dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest().upper(),text=p.read_text()) for p in paths},f)
    (out/'report.json').write_text(json.dumps(dict(passed=False,hostSession=98262,hostExit=1,nativeJobsStarted=0,
        observedError='ValueError: Entire actually accepted original P2 selection/ladder/first-combat input fixture unchanged',
        cause='Checked the retained raw capture rejected by an old idle-owner assumption, rather than its completed same-run owner/state/pixel qualification.',
        rawCaptureError=raw['error'],sameRunQualifiedReceipt='audit_native_current_ui_owned_checked/report.json',
        nativeGameFailure=False,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print('Original preflight failure preserved; no native game was started.')
