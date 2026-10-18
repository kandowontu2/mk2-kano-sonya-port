"""Content-keyed test ROM archives; per-run hard links avoid duplicate storage."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

def file_sha(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):digest.update(block)
    return digest.hexdigest().upper()

def prepare_archive(base,replacements,cache,output):
    base,cache,output=map(Path,(base,cache,output))
    assert not output.exists(),'Never replace an existing run input'
    request={'baseSHA256':file_sha(base),
             'replacementSHA256':{name:hashlib.sha256(data).hexdigest().upper() for name,data in sorted(replacements.items())}}
    key=hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest().upper()
    folder=cache/key
    folder.mkdir(parents=True,exist_ok=True)
    archive=folder/'mk3.zip';manifest=folder/'manifest.json'
    reused=archive.exists()
    if reused:
        record=json.loads(manifest.read_text())
        if record['request']!=request or file_sha(archive)!=record['archiveSHA256']:
            raise ValueError('Cached ROM archive failed content verification')
    else:
        with tempfile.NamedTemporaryFile(dir=folder,suffix='.partial',delete=False) as temporary:
            temporary_path=Path(temporary.name)
        try:
            with zipfile.ZipFile(base) as original,zipfile.ZipFile(temporary_path,'w',zipfile.ZIP_DEFLATED) as target:
                for name in original.namelist():
                    if not name.endswith('/'):
                        target.writestr(name,replacements[name] if name in replacements else original.read(name))
            record={'request':request,'archiveSHA256':file_sha(temporary_path)}
            temporary_path.replace(archive)
            manifest.write_text(json.dumps(record,indent=2)+'\n')
        finally:
            if temporary_path.exists():temporary_path.unlink()
    output.parent.mkdir(parents=True,exist_ok=True)
    try:
        os.link(archive,output)
        hard_link=True
    except FileExistsError:
        raise
    except OSError:
        # Filesystems without hard-link support retain bounded, correct behavior.
        with archive.open('rb') as source,output.open('xb') as destination:
            shutil.copyfileobj(source,destination,1048576)
        hard_link=False
    return {'key':key,'archiveSHA256':record['archiveSHA256'],
            'cacheReused':reused,'hardLinked':hard_link}
