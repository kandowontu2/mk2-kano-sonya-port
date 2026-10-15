"""Add explicit new video support sources to the code-only public snapshot."""
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'public_source_mk2ks_20261015'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
TOOLS=['seal_showcase_delivery_20261015.py','cleanup_failed_sonya_early_video_20261015.ps1','prepare_sonya_kitana_leg_video_bench_20261015.py','run_sonya_kitana_leg_video_bench_20261015.py','sync_public_video_sources_20261015.py']

def main():
    manifest=OUT/'SOURCE_MANIFEST.json';data=json.loads(manifest.read_text())
    rows={r['path']:r for r in data['codeFiles']}
    targets=[(ROOT/'tools'/name,Path('tools')/name) for name in TOOLS]
    for name in ('campaign.lua','preparation.json'):
        # Only Lua source belongs in the public controller set, not the
        # private runtime preparation receipt with original workspace paths.
        if name.endswith('.lua'):targets.append((ROOT/'video_sonya_kitana_leg_bench_20261015_preparation'/name,Path('controllers/video_sonya_kitana_leg_bench_20261015_preparation')/name))
    for source,relative in targets:
        raw=source.read_bytes();assert b'\0' not in raw and len(raw)<1024**2
        assert not re.search(rb'gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',raw)
        dest=OUT/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        rows[relative.as_posix()]=dict(path=relative.as_posix(),bytes=len(raw),sha256=sha(dest))
    data['codeFiles']=sorted(rows.values(),key=lambda r:r['path']);data['codeFileCount']=len(rows);data['codeBytes']=sum(r['bytes'] for r in rows.values())
    manifest.write_text(json.dumps(data,indent=2)+'\n')
    print('Added explicit code-only video support sources',len(targets))

if __name__=='__main__':main()
