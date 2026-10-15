"""Preserve a manual digest transcription failure; no native test failure."""
import gzip,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    source=ROOT/'tools/journal_native_cpu_finisher_spacing_progress.py'
    out=ROOT/'audit_native_cpu_finisher_view_digest_journal_failure'
    if out.exists():raise ValueError('Fresh failure archive required')
    actual=json.loads((ROOT/'audit_native_cpu_finisher_repair_regression_checked/report.json').read_text())
    out.mkdir()
    with gzip.open(out/'failed_executed_journal.json.gz','wt',encoding='utf-8') as f:
        json.dump(dict(path=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest().upper(),
                       text=source.read_text()),f)
    (out/'report.json').write_text(json.dumps(dict(passed=False,hostExit=1,nativeGameFailure=False,
        observedError='ValueError: All six actual native RAM fields displayed as800x834 atlas and visually inspected',
        cause='Three copied summary digests contained additional digits; original authoritative native records unchanged.',
        actualNativeRGBScenes=actual['actualNativeRGBScenes'],nativeExit=0,
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print('Failed journal preserved; original native raster callback digests retained.')
