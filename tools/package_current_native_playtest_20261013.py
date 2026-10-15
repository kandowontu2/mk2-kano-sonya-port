"""Stream one requested current-state ZIP; no staging tree or emulator recording."""
import hashlib
import json
from pathlib import Path
import zipfile
import verify_native_source_sync as sync


def digest(reader):
    h = hashlib.sha256()
    while chunk := reader.read(1024*1024):
        h.update(chunk)
    return h.hexdigest().upper()


def main():
    sync.verify()
    root, build = sync.ROOT, sync.BUILD
    out = root/'release_current_native_playtest_20261013'
    assert not out.exists(), 'Never overwrite an executed package'
    info = json.loads((build/'build-info.json').read_text())
    files = {'PLAY.cmd':root/'PLAY_CURRENT_NATIVE_CHECKED.cmd',
             'README.txt':root/'tools/CURRENT_PLAYTEST_README.txt',
             'tools/check_current_native_playtest.ps1':root/'tools/check_current_native_playtest.ps1',
             'COPYING':root/'mame-mkp/COPYING',
             'artwork/mk2ks/default.lay':root/'artwork/mk2ks/default.lay',
             'roms/mk2.zip':root/'roms/mk2.zip',
             'roms/mk2ks.zip':root/'roms/mk2ks.zip'}
    for name in ('mkport_candidate.exe', 'build-info.json', 'roms/mk2ks/mk2ks.mdata'):
        files[build.name+'/'+name] = build/name
    voices = {}
    for path, wanted in info['input_hashes'].items():
        if path.lower().endswith('.wav'):
            leaf = Path(path.replace('\\','/')).name
            assert leaf not in voices or voices[leaf] == wanted
            voices[leaf] = wanted
    assert len(voices) == 23
    for leaf, wanted in voices.items():
        path = build/'samples/mk2ks'/leaf
        if not path.is_file():
            path = root/'samples/mk2ks'/leaf
        assert sync.sha(path) == wanted
        files[build.name+'/samples/mk2ks/'+leaf] = path
    for path, wanted in info['canonical_source_hashes_at_compile'].items():
        source = Path(path)
        assert sync.sha(source) == wanted
        files['source/'+source.relative_to(root/'mame-mkp').as_posix()] = source
    hashes = {name:sync.sha(path) for name,path in files.items()}
    manifest = dict(build=build.name, releaseStatus='UNFINISHED CURRENT PLAYTEST',
                    fullPortAccepted=False, files=hashes)
    payload = json.dumps(manifest, indent=2).encode()
    out.mkdir()
    archive = out/'MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013.zip'
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name,path in files.items():
            z.write(path, 'MK2_Kano_Sonya_Playtest/'+name)
        z.writestr('MK2_Kano_Sonya_Playtest/RELEASE.json', payload)
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == len(files)+1
        assert z.testzip() is None
        for name,wanted in hashes.items():
            with z.open('MK2_Kano_Sonya_Playtest/'+name) as reader:
                assert digest(reader) == wanted
    assert all(sync.sha(path) == hashes[name] for name,path in files.items())
    report = dict(passedArchiveIntegrity=True, zip=str(archive),
                  zipBytes=archive.stat().st_size, zipSHA256=sync.sha(archive),
                  files=len(files), soundAssets=len(voices), newBuilds=0,
                  stagingTrees=0, portableRuntimeCheckPending=True,
                  fullPortAccepted=False)
    (out/'package-report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
