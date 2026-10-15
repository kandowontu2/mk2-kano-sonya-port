"""Freeze eight current native cases, with art/full-port acceptance still false."""
import hashlib
import json
import shutil
from pathlib import Path
import verify_native_gore_victim_tables_v924 as gore
import verify_native_death_grounding_v928 as reptile

ROOT = gore.ROOT
OUTPUT = ROOT / 'audit_v930_stock_victim_state_checkpoint'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    if OUTPUT.exists():
        raise ValueError('Preserve checkpoint')
    first, second = gore.verify(), reptile.verify()
    units = [json.loads((ROOT / name / 'result.json').read_text()) for name in
             ('audit_v925_native_gore_victim_table_units', 'audit_v929_current_reptile_grounding_units')]
    if not first['passed'] or not second['passed'] or not all(unit['passed'] for unit in units):
        raise ValueError('Both current genuine runtime gates and corruption suites required')
    if units[0]['tests'] != 25 or units[1]['methods'] != 25:
        raise ValueError('Both full 25-method corruption gates required')
    installed = ROOT / 'mame-mkp/mkport.exe'
    if digest(installed) != '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':
        raise ValueError('Installed executable changed')
    launchers = {'PLAY_CURRENT_V786_TEST_BUILD.cmd': 'diagnostic_v786_native_fighter_fade_exclusions',
                 'PLAY_LATEST_TEST_BUILD.cmd': 'diagnostic_v737_native_babality_performers',
                 'PLAY_MK2_KANO_SONYA.cmd': 'diagnostic_v277_native_battle_photos'}
    for file, old_target in launchers.items():
        if old_target not in (ROOT / file).read_text(encoding='utf-8-sig'):
            raise ValueError('Existing launcher changed: ' + file)
    sources = [ROOT / name for name in (
        'mame-mkp/src/mame/midway/midtunit_m.cpp',
        'mk2ks_stock_head_victim_v921.lua', 'mk2ks_stock_head_display_v921.lua',
        'tools/run_stock_head_victim_v921.ps1', 'tools/verify_native_gore_victim_tables_v924.py',
        'tools/test_native_gore_victim_tables_v925.py', 'tools/verify_native_death_grounding_v928.py',
        'tools/test_native_death_grounding_v929.py', 'tools/run_reptile_death_grounding_v904.ps1',
        'mk2ks_reptile_victim_v887.lua', 'mk2ks_reptile_death_grounding_v904.lua',
        'tools/build_native_death_art_v900.py', 'tools/build_native_candidate_v2.ps1',
        'STATUS_2026-10-02_CURRENT_STOCK_FATALITY_PATHS.md',
        'STATUS_2026-10-02_CURRENT_OWNED_DEATH_ART.md', 'tools/freeze_native_gore_checkpoint_v930.py')]
    paths = {Path(path) for path in first['pins']} | {Path(path) for path in second['inputHashes']}
    paths.update(sources)
    paths.add(installed)
    paths.update(ROOT / file for file in launchers)
    paths.add(ROOT / 'audit_v904_sonya_p2_native_death_grounding/guest_maincpu.bin')
    for directory in ('audit_v924_native_gore_victim_tables_checked', 'audit_v925_native_gore_victim_table_units',
                      'audit_v928_current_reptile_grounding_checked', 'audit_v929_current_reptile_grounding_units',
                      'audit_v914_pre_kitana_victim_parameters', 'audit_v917_pre_gore_victim_tables'):
        paths.update(path for path in (ROOT / directory).rglob('*') if path.is_file())
    OUTPUT.mkdir()
    archive = OUTPUT / 'input_sources'
    archive.mkdir()
    for path in sources:
        shutil.copy2(path, archive / path.name)
    hashes = {str(path): digest(path) for path in sorted(paths)}
    checkpoint = {
        'scope': 'four true-ID Kitana native table stability cases plus four current Reptile art/grounding regressions',
        'candidate': 'diagnostic_v918_native_gore_victim_tables',
        'fiveNativeVictimTablesAccepted': True, 'kitanaNormalCostumePhysicalCases': 4,
        'currentReptileNormalCostumePhysicalCases': 4, 'reptileNativeBodyDMAs': 1950,
        'reptileNativeHeadDMAs': 104, 'actualSnapshots': 244 + 124, 'corruptionTestMethods': 50,
        'ownedInflationArtworkAccepted': False, 'cageTorsoArtworkAccepted': False,
        'fullNativeDeathArtAccepted': False, 'fullPortAccepted': False,
        'alternatePaletteRuntimeAccepted': False, 'allStockFatalitiesAccepted': False,
        'fullTowerAccepted': False, 'installedExecutableUnchanged': True,
        'existingLaunchersNotUpdated': True, 'inputHashes': hashes}
    (OUTPUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({key: value for key, value in checkpoint.items() if key != 'inputHashes'}))
    print('Frozen input/artifact pins:', len(hashes))


if __name__ == '__main__':
    main()
