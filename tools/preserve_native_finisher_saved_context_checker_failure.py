"""Freeze a failed immutable-player-owner assumption before adding child provenance."""
import gzip,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
if __name__=='__main__':
    source=ROOT/'tools/qualify_native_cpu_finisher_spacing.py'
    run=ROOT/'audit_native_cpu_finisher_spacing'
    out=ROOT/'audit_native_cpu_finisher_saved_context_checker_failure'
    if out.exists():raise ValueError('Fresh original checker failure')
    meta=json.loads((run/'result.json').read_text())
    text=gzip.open(run/'run.log.gz','rt',encoding='utf-8').read()
    fields=[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith('MK2_FINISH_SPACING_FIELD ')]
    borrowed=[r for r in fields if 1<=int(r['age'])<=231 and r['k_owner']!=r['k_actor']]
    if not(meta['nativeExit']==0 and not meta['nativeCacheOverrunObserved'] and
           len(borrowed)==48 and [int(r['age']) for r in borrowed]==list(range(84,132))):
        raise ValueError('Actual saved-context discrepancy preserved, not invented gameplay failure')
    out.mkdir()
    with gzip.open(out/'failed_executed_checker.json.gz','wt',encoding='utf-8') as f:
        json.dump(dict(path=str(source),sha256=sha(source),text=source.read_text()),f)
    (out/'report.json').write_text(json.dumps(dict(passed=False,checkerFailure=True,nativeExit=0,
        nativeGameFailure=False,nativeCacheOverrunObserved=False,
        observedError='ValueError: Continuous actual physical identities/owners/health and native ground actors remain stable',
        borrowedSavedA8Fields=borrowed,actualEntryGap=79,
        cause='Checker equated main-task saved A8 with player identity during an attached-object coroutine.',
        independentChildLinkStillRequired=True,originalCheckerSHA256=sha(source),
        actualRunInputHashes={str(p):sha(p) for p in run.iterdir() if p.is_file()},
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(preserved=True,nativeExit=0,actualBorrowedFields=48,childProvenancePending=True)))
