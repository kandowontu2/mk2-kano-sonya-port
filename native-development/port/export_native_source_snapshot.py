"""Export only the qualified native development package into the source checkout."""
import json
from pathlib import Path
import zipfile
import subprocess
from inspect_normal_runtime import PORT, sha


def verify_staged(destination):
    destination = Path(destination).resolve()
    pins = json.loads((destination / 'FILES.json').read_text())
    paths = [*pins, 'FILES.json']
    prefix = destination.name + '/'
    flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0) | getattr(subprocess, 'BELOW_NORMAL_PRIORITY_CLASS', 0)
    tracked = subprocess.run(['git', 'ls-files', '-z', '--', destination.name], cwd=destination.parent,
        check=True, capture_output=True, creationflags=flags).stdout.decode().split('\0')
    assert set(filter(None, tracked)) == {prefix + name for name in paths}
    for name in paths:
        staged = subprocess.run(['git', 'show', ':' + prefix + name], cwd=destination.parent,
            check=True, capture_output=True, creationflags=flags).stdout
        assert staged == (destination / name).read_bytes(), 'Git transformed snapshot bytes: ' + name
    print('Verified all', len(paths), 'staged native files byte-for-byte')


def export(destination):
    destination = Path(destination).resolve()
    assert not destination.exists(), 'Never overwrite a source snapshot'
    assert (destination.parent / '.git').is_dir(), 'Expected existing source checkout'
    package = PORT / 'development_patches/MK2KS_NATIVE_DEVELOPMENT_IPS.zip'
    qualification = json.loads((package.parent / 'PACKAGE_QUALIFICATION.json').read_text())
    assert qualification['packageSHA256'] == sha(package)
    assert qualification['sourceDiffAppliedAndMatchedCurrent']
    assert qualification['ownASMModulesMatched'] == 59
    prefix = 'MK2KS_NATIVE_DEVELOPMENT/'
    with zipfile.ZipFile(package) as archive:
        assert archive.testzip() is None
        files = {}
        for name in archive.namelist():
            assert name.startswith(prefix)
            relative = name[len(prefix):]
            target = (destination / relative).resolve()
            assert target.is_relative_to(destination) and relative not in files
            assert target.suffix.lower() in ('.py', '.asm', '.patch', '.json', '.txt', '.md', '.cmd', '.bat', '.ips')
            files[relative] = archive.read(name)
    pins = json.loads(files['FILES.json'])
    assert set(files) == set(pins) | {'FILES.json'}
    import hashlib
    assert all(hashlib.sha256(files[name]).hexdigest().upper() == digest for name, digest in pins.items())
    for relative, content in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(content)
        assert target.read_bytes() == content
    print('Exported', len(files), 'qualified native files;', sum(map(len, files.values())), 'bytes')


if __name__ == '__main__':
    export(PORT.parents[1] / 'public_source_mk2ks_20261015/native-rom')
