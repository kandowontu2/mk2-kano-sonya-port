"""Build minimal final native bundles and independently patch from their bytes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile
from inspect_normal_runtime import PORT
from audit_stock_mame_distribution import main as audit_distribution, player_member, EMULATOR_SHA
from build_native_player_playtest import isolated_launcher, digest_stream
from prepare_native_release_evidence import digest, main as collect_evidence
from refresh_special_videos import FLAGS


def encoded(data):
    return (json.dumps(data, indent=2)+'\n').encode()


def write_checked(destination, files):
    assert not destination.exists(), 'Never overwrite a release artifact'
    pins = {name: digest(data) if isinstance(data, Path) else __import__('hashlib').sha256(data).hexdigest().upper()
            for name, data in sorted(files.items())}
    files = dict(files, **{'FILES.json': encoded(pins)})
    partial = destination.with_suffix('.zip.partial')
    assert not partial.exists()
    with partial.open('xb') as output, zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            with archive.open(info, 'w') as target:
                if isinstance(data, Path):
                    with data.open('rb') as source:
                        shutil.copyfileobj(source, target, 65536)
                else:
                    target.write(data)
    with zipfile.ZipFile(partial) as archive:
        assert len(archive.infolist()) == len(files) and set(archive.namelist()) == set(files)
        for name, expected in pins.items():
            with archive.open(name) as stream:
                assert digest_stream(stream) == expected, name
    os.link(partial, destination)
    partial.unlink()
    return dict(file=destination.name, bytes=destination.stat().st_size, SHA256=digest(destination),
                members=len(files), allMemberHashesVerified=True)


def verify_patching(archive_path, expected_rom):
    with tempfile.TemporaryDirectory(prefix='final-patch-check-', dir=archive_path.parent) as folder:
        work = Path(folder)
        with zipfile.ZipFile(archive_path) as archive:
            for name in archive.namelist():
                if player_member(name) or name == 'RELEASE_EVIDENCE.json':
                    target = work/name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.read(name))
        environment = os.environ.copy()
        environment.pop('PYTHONPATH', None)
        environment['PYTHONNOUSERSITE'] = '1'
        environment['PYTHONDONTWRITEBYTECODE'] = '1'
        root = PORT.parents[1]
        result = subprocess.run([sys.executable, str(work/'patch_native_roms.py'),
            '--mk2', str(root/'roms/mk2.zip'), '--mk3', str(root/'mk3.zip'),
            '--output', str(work/'roms/mk3.zip')], cwd=work, env=environment,
            capture_output=True, text=True, creationflags=FLAGS, timeout=60)
        assert result.returncode == 0, result.stdout+result.stderr
        assert digest(work/'roms/mk3.zip') == expected_rom
    assert not work.exists()


def main():
    out = PORT/'native_release'
    out.mkdir(exist_ok=True)
    assert not list(out.glob('*.zip')), 'Review existing release before building another'
    collect_evidence()
    audit_distribution()
    evidence = json.loads((PORT/'NATIVE_RELEASE_EVIDENCE_CANDIDATE.json').read_text())
    # Approval is emitted separately only AFTER both completed ZIPs patch correctly.
    evidence['scope'] = 'Finite gameplay/rebuild/media evidence; final ZIP qualification is a separate receipt'
    evidence.pop('releaseApproved')
    evidence.pop('finalPlayerPackageVerified')
    evidence_bytes = encoded(evidence)
    import hashlib
    evidence_sha = hashlib.sha256(evidence_bytes).hexdigest().upper()
    with zipfile.ZipFile(PORT/'development_patches/MK2KS_NATIVE_DEVELOPMENT_IPS.zip') as archive:
        source = {name.removeprefix('MK2KS_NATIVE_DEVELOPMENT/'): archive.read(name)
                  for name in archive.namelist()}
    source.pop('FILES.json')
    manifest = json.loads(source['PATCH_MANIFEST.json'])
    manifest.update(developmentOnly=False, releaseReady=True, releaseEvidenceSHA256=evidence_sha)
    source['PATCH_MANIFEST.json'] = encoded(manifest)
    source['RELEASE_EVIDENCE.json'] = evidence_bytes
    source['README_PATCHING.txt'] = (PORT/'RELEASE_README.txt').read_bytes()
    source['PLAY.cmd'] = isolated_launcher(source['PLAY.cmd'])
    player = {name: data for name, data in source.items() if player_member(name)}
    assert len(player) == 21
    player['RELEASE_EVIDENCE.json'] = evidence_bytes
    distribution = json.loads((PORT/'STOCK_MAME_DISTRIBUTION_0289.json').read_text())
    assert distribution['correspondingSourceAsset']['presentAndHashVerified']
    mame = PORT.parents[1].parent/'mame0289'
    for record in distribution['verifiedMembers']:
        player[record['member']] = mame/record['member']
    assert digest(player['mame.exe']) == EMULATOR_SHA
    expected_rom = digest(PORT/'development_patches/roundtrip/roms/mk3.zip')
    records = []
    for name, files in [('MK2KS_NATIVE_SOURCE_AND_IPS.zip', source),
                        ('MK2KS_NATIVE_WITH_STOCK_MAME.zip', player)]:
        record = write_checked(out/name, files)
        verify_patching(out/name, expected_rom)
        record.update(isolatedPatcherReproducedExactTestedROM=True, temporaryGeneratedROMRemoved=True)
        records.append(record)
    receipt = dict(scope='Both distributed native ZIPs verified from their own bytes',
        releaseApproved=True, gameROMsIncluded=False, customDriver=False,
        patchedROMArchiveSHA256=expected_rom, releaseEvidenceSHA256=evidence_sha,
        stockMAMESHA256=EMULATOR_SHA, artifacts=records,
        sourceDistributionRequiredAsset='mame0289s.exe', publicationVerified=False)
    (out/'RELEASE_QUALIFICATION.json').write_bytes(encoded(receipt))
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
