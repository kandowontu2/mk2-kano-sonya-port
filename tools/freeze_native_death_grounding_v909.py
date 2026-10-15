"""Freeze the current narrow native-art proof; never mark the port complete."""
import hashlib
import json
import shutil
from pathlib import Path
import verify_native_death_grounding_v907 as proof

ROOT = proof.ROOT
OUTPUT = ROOT / 'audit_v909_owned_death_grounding_checkpoint'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    if OUTPUT.exists():
        raise ValueError('Preserve checkpoint evidence')
    report = proof.verify()
    units = json.loads((ROOT / 'audit_v908_owned_death_grounding_units/result.json').read_text())
    if not report['passed'] or not units['passed'] or units['methods'] != 25:
        raise ValueError('Current native runtime and corruption gate required')
    installed = ROOT / 'mame-mkp/mkport.exe'
    if digest(installed) != '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':
        raise ValueError('Production executable changed')
    sources = [ROOT / name for name in (
        'mame-mkp/src/mame/midway/midtunit_m.cpp',
        'tools/build_native_death_art_v900.py', 'tools/verify_native_death_grounding_v907.py',
        'tools/test_native_death_grounding_v908.py', 'tools/run_reptile_death_grounding_v904.ps1',
        'mk2ks_reptile_victim_v887.lua', 'mk2ks_reptile_death_grounding_v904.lua',
        'STATUS_2026-10-02_CURRENT_OWNED_DEATH_ART.md', 'tools/freeze_native_death_grounding_v909.py')]
    paths = set(Path(path) for path in report['inputHashes'])
    paths.update(sources)
    paths.add(installed)
    for directory in ('art_native_death_v893', 'audit_v900_native_death_grounding_encoding',
                      'audit_v907_owned_death_grounding_checked', 'audit_v908_owned_death_grounding_units'):
        paths.update(path for path in (ROOT / directory).rglob('*') if path.is_file())
    paths.update(ROOT.glob('PLAY*.cmd'))
    OUTPUT.mkdir()
    archive = OUTPUT / 'input_sources'
    archive.mkdir()
    for source in sources:
        shutil.copy2(source, archive / source.name)
    checkpoint = {'scope': 'four true-ID stock Reptile normal-costume native death-art and floor cases',
                  'candidate': 'diagnostic_v901_native_death_grounding',
                  'nativeOwnedDeathArtRuntimeAccepted': True, 'reptileDeadPoolGroundingAccepted': True,
                  'normalCostumeCases': 4, 'nativeBodyDMAs': 1950, 'nativeHeadDMAs': 104,
                  'actualSnapshots': 124, 'corruptionTestMethods': 25,
                  'fullNativeDeathArtAccepted': False, 'fullPortAccepted': False,
                  'alternatePaletteRuntimeAccepted': False, 'fullTowerAccepted': False,
                  'installedExecutableUnchanged': True, 'existingLaunchersNotUpdated': True,
                  'inputHashes': {str(path): digest(path) for path in sorted(paths)}}
    (OUTPUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({key: value for key, value in checkpoint.items() if key != 'inputHashes'}))
    print('Frozen input/artifact pins:', len(checkpoint['inputHashes']))


if __name__ == '__main__':
    main()
