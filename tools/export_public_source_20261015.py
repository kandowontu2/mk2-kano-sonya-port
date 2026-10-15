"""Export code only, never ROMs/assets/logs/binaries or Git credentials.

One auditable source snapshot, not fabricated development commit history.
Writes only a fresh exact output directory and a code/hash manifest.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'public_source_mk2ks_20261015'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
EXT={'.py','.ps1','.lua','.cpp','.h','.cs','.inc','.cmd'}
SECRET=re.compile(rb'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY|AKIA[0-9A-Z]{16}')

def main():
    assert not OUT.exists(),'Fresh code-only export required'
    upstream=ROOT/'mame-mkp'
    base=subprocess.run(['git','-C',str(upstream),'rev-parse','HEAD'],check=True,capture_output=True,text=True).stdout.strip()
    assert base=='914d2c29749a0ca612d92b1fc69cd62d94e1468d'
    build=json.loads((ROOT/'diagnostic_native_selector_layers_long/build-info.json').read_text())
    compiled=build['canonical_source_hashes_at_compile'];assert len(compiled)==15
    sources={}
    def add(source,target):
        assert source.is_file() and not source.is_symlink()
        raw=source.read_bytes();assert b'\0' not in raw and not SECRET.search(raw),'Non-text or credential-like material: '+str(source)
        assert len(raw)<5*1024**2,'Unexpected code size'
        sources[Path(target).as_posix()]=(source,raw)
    for path,pin in compiled.items():
        source=Path(path);assert sha(source)==pin
        add(source,Path('mame-overlay')/source.relative_to(upstream))
    for source in (ROOT/'tools').iterdir():
        if source.is_file() and source.suffix in EXT:add(source,source.relative_to(ROOT))
    for source in ROOT.iterdir():
        if source.is_file() and source.suffix in {'.py','.ps1','.lua','.cmd'}:add(source,Path('development')/source.name)
        if source.is_file() and source.name.startswith('STATUS_') and source.suffix=='.md':add(source,Path('history')/source.name)
        if source.is_dir() and source.name.endswith('_preparation'):
            for child in source.iterdir():
                if child.is_file() and child.suffix in EXT:add(child,Path('controllers')/source.name/child.name)
    for name in ('MK2_KANO_SONYA_MOVES.txt','CURRENT_PLAYTEST_STATUS.md','FINISHLINE_2026-10-15.txt'):
        if (ROOT/name).is_file():add(ROOT/name,Path('docs')/name)
    add(upstream/'COPYING','MAME_COPYING')
    for source in (upstream/'docs/legal').iterdir():
        if source.is_file():add(source,Path('licenses')/source.name)
    OUT.mkdir()
    inventory=[]
    for target,(source,raw) in sorted(sources.items()):
        dest=OUT/target;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        inventory.append(dict(path=target,bytes=len(raw),sha256=sha(dest)))
    patch=subprocess.run(['git','-C',str(upstream),'diff','--no-ext-diff','--binary','HEAD','--','src'],check=True,capture_output=True).stdout
    assert not SECRET.search(patch) and b'GIT binary patch' not in patch
    (OUT/'patches').mkdir();(OUT/'patches/native-integration.patch').write_bytes(patch)
    # The new codec header is untracked upstream and therefore supplied in the
    # complete15-file overlay; do not pretend git diff includes that header.
    manifest=dict(upstream='https://github.com/Zoltan45/mame-mkp',upstreamCommit=base,canonicalCompileInputCount=15,codeFiles=inventory,codeFileCount=len(inventory),codeBytes=sum(x['bytes'] for x in inventory),patchSHA256=sha(OUT/'patches/native-integration.patch'),currentEXESHA256=build['executable_sha256'],currentPayloadSHA256=build['payload_sha256'],romsIncluded=False,extractedGameAssetsIncluded=False,binariesIncluded=False,gameplayLogsIncluded=False,credentialPatternScanPassed=True,actualHistoricalGitHistory=False,scope='Current exact MAME overlay + retained top-level tooling, Lua development drivers, prepared controllers and technical status notes; single source snapshot, historical paths not automatically portable.')
    (OUT/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='codeFiles'},indent=2))

if __name__=='__main__':main()
