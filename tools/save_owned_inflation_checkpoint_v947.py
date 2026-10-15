"""Freeze scoped current evidence, never declare the full natural port done."""
import hashlib
import json
import shutil
from pathlib import Path
import verify_native_inflation_art_v941 as inflation
import verify_native_death_grounding_v945 as reptile

ROOT = inflation.ROOT
OUT = ROOT / 'audit_v947_owned_inflation_checkpoint'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    if OUT.exists():
        raise ValueError('Refuse to replace checkpoint')
    a, b = inflation.verify(), reptile.verify()
    if not a['passed'] or not b['passed']:
        raise ValueError('Current runtime evidence does not pass')
    art = json.loads((ROOT / 'audit_v943_owned_inflation_visual_review/manual-review.json').read_text())
    if not art['ownedNormalCostumeInflationPresentationAccepted'] or art['fullPortAccepted']:
        raise ValueError('Scoped manual visual review required')
    installed = ROOT / 'mame-mkp/mkport.exe'
    expected = '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    if digest(installed) != expected:
        raise ValueError('Installed build changed')
    for folder, field, count in [('audit_v942_owned_inflation_corruption_units', 'tests', 39),
                                  ('audit_v946_current_reptile_after_inflation_units', 'methods', 25)]:
        r = json.loads((ROOT / folder / 'result.json').read_text())
        if not r['passed'] or r[field] != count:
            raise ValueError('Corruption rejection suite incomplete')
    (OUT / 'input_sources').mkdir(parents=True)
    sources = ['mame-mkp/src/mame/midway/midtunit_m.cpp',
               'diagnostic_v936_owned_inflation_art/build-info.json',
               'STATUS_2026-10-02_CURRENT_STOCK_FATALITY_PATHS.md',
               'mk2ks_stock_head_victim_v921.lua', 'mk2ks_native_inflation_display_v939.lua',
               'tools/build_native_inflation_art_v935.py', 'tools/run_native_inflation_v939.ps1',
               'tools/verify_native_inflation_art_v940.py', 'tools/verify_native_inflation_art_v941.py',
               'tools/test_native_inflation_art_v942.py', 'tools/verify_native_death_grounding_v945.py',
               'tools/test_native_death_grounding_v946.py', 'tools/save_owned_inflation_checkpoint_v947.py']
    pins = {**a['pins'], **b['inputHashes']}
    for source in sources:
        path = ROOT / source
        target = OUT / 'input_sources' / path.name
        shutil.copy2(path, target)
        pins[str(target)] = digest(target)
        pins[str(path)] = digest(path)
    folders = ['audit_v935_owned_inflation_encoding', 'audit_v941_owned_inflation_runtime_checked',
               'audit_v942_owned_inflation_corruption_units', 'audit_v943_owned_inflation_visual_review',
               'audit_v945_current_reptile_after_inflation_checked', 'audit_v946_current_reptile_after_inflation_units',
               'art_native_inflation_v933']
    for folder in folders:
        for path in (ROOT / folder).rglob('*'):
            if path.is_file(): pins[str(path)] = digest(path)
    pins[str(installed)] = expected
    for name in ['PLAY_CURRENT_V786_TEST_BUILD.cmd', 'PLAY_LATEST_TEST_BUILD.cmd', 'PLAY_MK2_KANO_SONYA.cmd']:
        pins[str(ROOT / name)] = digest(ROOT / name)
    for filename, value in pins.items():
        if digest(Path(filename)) != value:
            raise ValueError('Evidence changed during checkpoint: ' + filename)
    data = {'scope': 'normal Dead Pool owned six-pose inflation/explosion in four true-ID physical cases plus four current Reptile regressions',
            'candidate': 'diagnostic_v936_owned_inflation_art',
            'executableSHA256': inflation.EXE, 'payloadSHA256': inflation.PAYLOAD,
            'fiveNativeVictimTablesAccepted': True, 'ownedSixPoseInflationNativeRuntimeAccepted': True,
            'ownedNormalCostumeInflationPresentationAccepted': True,
            'kitanaNormalCostumePhysicalCases': 4, 'currentReptileNormalCostumePhysicalCases': 4,
            'inflationNativeOwnedDMAs': 700, 'reptileNativeBodyDMAs': 1950, 'reptileNativeHeadDMAs': 104,
            'periodicSnapshots': 368, 'actualSixPoseSnapshots': 24, 'hardwarePaletteDumps': 24,
            'actualSnapshots': 392, 'corruptionTestMethods': 64,
            'cageTorsoArtworkAccepted': False, 'rollingHeadArtworkAccepted': False,
            'fullNativeDeathArtAccepted': False, 'fullPortAccepted': False,
            'alternatePaletteRuntimeAccepted': False, 'allArenasAccepted': False,
            'allStockFatalitiesAccepted': False, 'fullTowerAccepted': False,
            'installedExecutableUnchanged': True, 'existingLaunchersNotUpdated': True,
            'releaseZipNotUpdated': True, 'oldBuildCleanupComplete': False,
            'evidencePins': len(pins), 'inputHashes': dict(sorted(pins.items()))}
    (OUT / 'checkpoint.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({key: value for key, value in data.items() if key != 'inputHashes'}, indent=2))


if __name__ == '__main__':
    main()
