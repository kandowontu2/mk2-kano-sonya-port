"""Keep the actual storage-journal assertion failure before correcting it."""
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_native_secondary_reference_journal_failure'


def main():
    if OUT.exists():raise ValueError('Immutable actual journal failure already exists')
    source=ROOT/'tools/journal_native_secondary_finisher_reference_progress.py'
    run=subprocess.run([sys.executable,'-B',str(source)],cwd=ROOT,capture_output=True,text=True)
    if run.returncode!=1 or 'ValueError: No new ROM/build/raw-media evidence files'not in run.stderr:
        raise ValueError('Exact actual journal failure not reproduced')
    native_snapshots=[]
    for name in ('audit_native_secondary_kano_reference','audit_native_secondary_kano_raster_checked',
                 'audit_native_secondary_kano_command_checked','audit_native_secondary_kano_guarded_command'):
        path=ROOT/name/'snap/mk3/0000.png'
        native_snapshots.append(dict(path=str(path.resolve()),bytes=path.stat().st_size,
            sha256=hashlib.sha256(path.read_bytes()).hexdigest().upper()))
    OUT.mkdir()
    with gzip.open(OUT/'failed_executed_sources.json.gz','wt',encoding='utf-8')as stream:
        json.dump({str(path.resolve()):dict(source=path.read_text(),
            sha256=hashlib.sha256(path.read_bytes()).hexdigest().upper())for path in (source,Path(__file__))},stream)
    (OUT/'report.json').write_text(json.dumps(dict(passed=False,actualFailureConserved=True,
        actualExecutedExit=run.returncode,actualTraceback=run.stderr,
        diagnosis='Four older original games reaching -str180 automatically saved a terminal PNG. This continuation two games exited via their planned Lua action endpoint and wrote no raster files. Count and preserve prior native automatic snapshots; do not claim all prior evidence is raw-media-free.',
        olderActualNativeAutomaticSnapshots=native_snapshots,newGameRuns=0),indent=2)+'\n')
    print(json.dumps(dict(actualFailureConserved=True,olderSnapshots=len(native_snapshots),newGameRuns=0)))


if __name__=='__main__':main()
