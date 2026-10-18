"""Exercise the published native patcher from an isolated temporary CWD."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile
from inspect_normal_runtime import PORT, sha
from refresh_special_videos import FLAGS


def main():
    root = PORT.parents[1]
    checkout = root / 'public_source_mk2ks_20261015'
    source = checkout / 'native-rom'
    def command(args, cwd=checkout):
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                              check=True, timeout=60, creationflags=FLAGS)
    commit = command(['git', 'rev-parse', 'HEAD']).stdout.strip()
    remote = command(['git', 'ls-remote', 'origin', 'HEAD']).stdout.split()[0]
    assert commit == remote
    assert not command(['git', 'status', '--porcelain', '--', 'native-rom']).stdout.strip()
    pins = json.loads((source / 'FILES.json').read_text())
    assert len(pins) + 1 == 121
    assert all(sha(source / name) == digest for name, digest in pins.items())
    manifest = json.loads((source / 'PATCH_MANIFEST.json').read_text())
    assert not manifest['customDriver'] and not manifest['releaseReady']
    expected = {r['target']: r['targetSHA256'] for r in manifest['chips']}
    assert len(expected) == 26
    environment = os.environ.copy()
    environment.pop('PYTHONPATH', None)
    environment['PYTHONNOUSERSITE'] = '1'
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    with tempfile.TemporaryDirectory(prefix='public-native-roundtrip-', dir=PORT / 'development_patches') as temporary:
        work = Path(temporary).resolve()
        assert work.is_relative_to((PORT / 'development_patches').resolve())
        output = work / 'roms/mk3.zip'
        result = subprocess.run([sys.executable, str(source / 'patch_native_roms.py'),
            '--mk2', str(root / 'roms/mk2.zip'), '--mk3', str(root / 'mk3.zip'),
            '--output', str(output)], cwd=work, env=environment, capture_output=True,
            text=True, check=True, timeout=60, creationflags=FLAGS)
        patched = json.loads(result.stdout)
        assert patched['chips'] == 26 and not patched['customDriver']
        with zipfile.ZipFile(output) as archive:
            assert archive.testzip() is None
            assert len(archive.namelist()) == 26
            import hashlib
            assert {n: hashlib.sha256(archive.read(n)).hexdigest().upper() for n in archive.namelist()} == expected
        reference = PORT / 'development_patches/roundtrip/roms/mk3.zip'
        assert sha(output) == patched['SHA256'] == sha(reference)
        digest = sha(output)
        tests = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(source),
            '-p', 'test_ips_codec.py', '-q'], cwd=work, env=environment, capture_output=True,
            text=True, check=True, timeout=60, creationflags=FLAGS)
        test_summary = tests.stderr.strip()
    assert not work.exists(), 'Temporary ROM output must be removed after verification'
    report = dict(scope='Published checkout patcher CLI roundtrip from isolated CWD',
        sourceCommit=commit, remoteHEADMatched=True, snapshotFileHashesVerified=121,
        patchedChipsVerified=26, exactTestedROMArchiveSHA256=digest,
        publishedCodecTests=test_summary, temporaryROMOutputRemoved=True,
        fullGameplayAcceptance=False, releaseReady=False,
        pins={str(source / name): sha(source / name) for name in
              ('FILES.json', 'PATCH_MANIFEST.json', 'patch_native_roms.py', 'ips_codec.py')})
    (PORT / 'PUBLIC_NATIVE_SNAPSHOT_QUALIFICATION.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Published native CLI rebuilt the exact tested26-chip archive; codec tests passed; temporary ROM removed.')


if __name__ == '__main__':
    main()
