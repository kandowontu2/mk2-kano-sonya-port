"""Validate user archives and build an isolated stock-MAME ROM set from IPS."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from ips_codec import apply_patch

def sha(data): return hashlib.sha256(data).hexdigest().upper()

def manifest_status(manifest):
    """Lifecycle metadata is separate from the per-chip integrity checks below."""
    if manifest.get('format')!='MK2KS-NATIVE-IPS-1':
        raise ValueError('Unexpected native patch format')
    ready=manifest.get('releaseReady')
    if type(ready) is not bool:
        raise ValueError('releaseReady must be a boolean')
    development=manifest.get('developmentOnly',True)
    if type(development) is not bool or development==ready:
        raise ValueError('Inconsistent development/release status')
    if ready:
        evidence=manifest.get('releaseEvidenceSHA256','')
        if not isinstance(evidence,str) or len(evidence)!=64 or any(c not in '0123456789abcdefABCDEF' for c in evidence):
            raise ValueError('Release manifest lacks its evidence binding')
    return ready
def read_chip(archive,name):
    entries=[entry for entry in archive.infolist() if entry.filename==name]
    if len(entries)!=1 or entries[0].file_size>0x200000:
        raise ValueError('Missing, duplicate or oversized source chip: '+name)
    return archive.read(entries[0])

def build(mk2,mk3,package,output):
    if output.exists(): raise FileExistsError('Refusing to overwrite '+str(output))
    manifest=json.loads((package/'PATCH_MANIFEST.json').read_text())
    release_ready=manifest_status(manifest)
    chips={}
    with zipfile.ZipFile(mk2) as a,zipfile.ZipFile(mk3) as b:
        archives={'mk2':a,'mk3':b}
        for record in manifest['chips']:
            name=record['target']
            if Path(name).name!=name or '/' in name or '\\' in name or name in chips:
                raise ValueError('Unsafe or duplicate target name')
            source=read_chip(archives[record['sourceArchive']],record['source'])
            if len(source)!=record['sourceBytes'] or sha(source)!=record['sourceSHA256']:
                raise ValueError('Wrong source revision/hash: '+record['source'])
            if record['operation']=='copy': target=source
            elif record['operation']=='ips':
                relative=Path(record['patch'])
                if relative.is_absolute() or relative.parts[0]!='patches' or '..' in relative.parts:
                    raise ValueError('Unsafe patch path')
                delta=(package/relative).read_bytes()
                if sha(delta)!=record['patchSHA256']: raise ValueError('Patch checksum failed: '+name)
                target=apply_patch(source,delta)
            else: raise ValueError('Unknown patch operation')
            if len(target)!=record['targetBytes'] or sha(target)!=record['targetSHA256']:
                raise ValueError('Patched chip checksum failed: '+name)
            chips[name]=target
    if len(chips)!=26: raise ValueError('Incomplete Wolf ROM socket set')
    # Validate every source and result BEFORE creating any output.
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('xb') as destination:
        with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
            for name,data in sorted(chips.items()):
                entry=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0))
                entry.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(entry,data)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert {n:sha(archive.read(n)) for n in archive.namelist()}=={n:sha(d) for n,d in chips.items()}
    return dict(output=str(output),chips=len(chips),SHA256=sha(output.read_bytes()),
        stockMAME=True,customDriver=False,developmentOnly=not release_ready,
        releaseReady=release_ready,fullPortVerified=False)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mk2',type=Path,required=True)
    parser.add_argument('--mk3',type=Path,required=True)
    parser.add_argument('--package',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(build(args.mk2,args.mk3,args.package,args.output),indent=2))

if __name__=='__main__': main()
