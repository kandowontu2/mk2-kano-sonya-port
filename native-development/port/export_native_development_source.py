"""Source-only developer snapshot; deliberately excludes ROMs, assets and run dumps."""
import hashlib
import json
from pathlib import Path
from inspect_normal_runtime import PORT, BASE


def main():
    checkout = PORT.parents[1] / 'public_source_mk2ks_20261015'
    destination = (checkout / 'native-development').resolve()
    assert (checkout / '.git').is_dir() and not destination.exists()
    inputs = []
    inputs += [(p, 'port/' + p.name) for p in PORT.iterdir() if p.is_file() and p.suffix.lower() in ('.py', '.md', '.ps1', '.cmd')]
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
    for name, data in files.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(data)
        assert target.read_bytes() == data
    print('Source files', len(files), 'bytes', sum(map(len, files.values())))


if __name__ == '__main__':
    main()
