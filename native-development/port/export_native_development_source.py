"""Source-only developer snapshot; deliberately excludes ROMs, assets and run dumps."""
import hashlib
import json
import sys
from pathlib import Path
from inspect_normal_runtime import PORT, BASE


def validate_previous(destination):
    """Refuse replacement of any unrecorded or locally changed developer file."""
    pins = json.loads((destination / 'FILES.json').read_text())
    actual = {p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}
    assert actual == set(pins) | {'FILES.json'}, 'Unrecorded snapshot files'
    for name, digest in pins.items():
        path = (destination / name).resolve()
        assert path.is_relative_to(destination.resolve()) and not path.is_symlink()
        assert hashlib.sha256(path.read_bytes()).hexdigest().upper() == digest, name
    return pins


def main():
    assert sys.argv[1:] in ([], ['--update'])
    checkout = PORT.parents[1] / 'public_source_mk2ks_20261015'
    destination = (checkout / 'native-development').resolve()
    assert (checkout / '.git').is_dir()
    updating = sys.argv[1:] == ['--update']
    previous = validate_previous(destination) if updating else {}
    assert updating or not destination.exists()
    inputs = []
    inputs += [(p, 'port/' + p.name) for p in PORT.iterdir() if p.is_file() and p.suffix.lower() in ('.py', '.md', '.ps1', '.cmd')]
    inputs += [(PORT/'RELEASE_README.txt', 'port/RELEASE_README.txt')]
    route=PORT/'KINTARO_SHORT_ROUTE.json'
    if route.exists():
        data=json.loads(route.read_text())
        assert len(data['actions'])==37 and data['fieldsPerAction']==120
        assert all(action in ('kick','punch','counter','knife','guard','away','backkick') for action in data['actions'])
        assert data['scope'].startswith('Planning candidate only;') and not data['campaignAcceptance']
        inputs.append((route,'port/'+route.name))
    for directory, suffix in (('diagnostics', '.lua'), ('asm', '.asm')):
        inputs += [(p, 'port/' + directory + '/' + p.name) for p in (PORT / directory).iterdir()
                   if p.is_file() and p.suffix.lower() == suffix]
    inputs += [(p, 'baseline/' + p.name) for p in BASE.glob('*.py') if p.is_file()]
    files = {}
    for source, relative in inputs:
        target = (destination / relative).resolve()
        assert target.is_relative_to(destination) and relative not in files
        assert source.stat().st_size < 5 * 1024 * 1024
        files[relative] = source.read_bytes()
    assert files and len(files) < 2000
    pins = {name: hashlib.sha256(data).hexdigest().upper() for name, data in sorted(files.items())}
    files['FILES.json'] = (json.dumps(pins, indent=2) + '\n').encode()
    assert not (set(previous) - set(files)), 'Source removal requires explicit review'
    for name, data in files.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('wb' if updating else 'xb') as stream:
            stream.write(data)
        assert target.read_bytes() == data
    print('Source files', len(files), 'bytes', sum(map(len, files.values())))


if __name__ == '__main__':
    main()
