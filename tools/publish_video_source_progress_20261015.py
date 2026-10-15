"""Export the next explicit video support sources; do not publish game/media."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'public_source_mk2ks_20261015'
NAMES=['qualify_sonya_kitana_video_bench_20261015.py','prepare_sonya_complete_video_bench_20261015.py','publish_video_source_progress_20261015.py','qualify_sonya_complete_video_bench_20261015.py','prepare_sonya_late_leg_video_bench_20261015.py','prepare_sonya_raiden_leg_video_bench_20261015.py','prepare_sonya_shao_counter_video_bench_20261015.py','prepare_sonya_final_video_20261015.py','cleanup_failed_showcase_media_20261015.ps1']

def main():
    path=OUT/'SOURCE_MANIFEST.json';manifest=json.loads(path.read_text());rows={r['path']:r for r in manifest['codeFiles']}
    files=[(ROOT/'tools'/name,Path('tools')/name) for name in NAMES]
    for case in ('video_sonya_complete_bench_20261015_preparation','video_sonya_late_leg_bench_20261015_preparation','video_sonya_raiden_leg_bench_20261015_preparation','video_sonya_shao_counter_bench_20261015_preparation','video_sonya_final_20261015_preparation'):
        folder=ROOT/case
        files += [(folder/name,Path('controllers')/folder.name/name) for name in ('campaign.lua','run.py')]
    for original,relative in files:
        raw=original.read_bytes();assert b'\0' not in raw and len(raw)<1024**2
        target=OUT/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        rows[relative.as_posix()]=dict(path=relative.as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper())
    manifest['codeFiles']=sorted(rows.values(),key=lambda x:x['path']);manifest['codeFileCount']=len(rows);manifest['codeBytes']=sum(x['bytes'] for x in rows.values())
    path.write_text(json.dumps(manifest,indent=2)+'\n')
    print('Exported',len(files),'new source files; no game/media data')

if __name__=='__main__':main()
