"""Freeze scoped real evidence; the complete natural-character goal stays active."""
import ast
import hashlib
import json
import shutil
from pathlib import Path
import verify_native_torso_art_v980 as cage
import verify_cage_alt_blood_v985 as alternate
import verify_native_inflation_art_v989 as inflation
import verify_native_death_grounding_v990 as reptile

ROOT = cage.ROOT
OUT = ROOT / 'audit_v994_owned_torso_blood_checkpoint'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    if OUT.exists():
        raise ValueError('Never replace a checkpoint')
    reports = [cage.verify(), alternate.verify(), inflation.verify(), reptile.verify()]
    if not all(r['passed'] for r in reports):
        raise ValueError('Fresh current native evidence must pass')
    for folder, filename, field, count in (
            ('audit_v982_owned_torso_blood_corruption_units','unit-results.json','testsRun',23),
            ('audit_v991_current_inflation_corruption_units','result.json','tests',39),
            ('audit_v992_current_reptile_corruption_units','result.json','methods',25)):
        result = json.loads((ROOT/folder/filename).read_text())
        if not result['passed'] or result[field] != count or result['errors'] or result['failures']:
            raise ValueError('Current corruption rejection methods must pass')
    for folder, field in (
            ('audit_v986_owned_torso_blood_visual_review','ownedNormalCageTorsoPresentationAccepted'),
            ('audit_v984_controlled_alt_blood_visual_review','controlledNativeAlternateBloodBranchPresentationAccepted')):
        review = json.loads((ROOT/folder/'manual-review.json').read_text())
        if not review[field] or review['fullPortAccepted'] or review['naturalAlternateSelectionAccepted']:
            raise ValueError('Scoped reviewed actual pictures required; no natural-alt/full-port claim')
    installed = ROOT/'mame-mkp/mkport.exe'
    expected = '413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    if digest(installed) != expected:
        raise ValueError('Installed executable changed')
    pins = {}
    for report in reports:
        pins.update(report.get('inputHashes',report.get('pins',{})))
    previous = json.loads((ROOT/'audit_v947_owned_inflation_checkpoint/checkpoint.json').read_text())
    for filename in ('PLAY_CURRENT_V786_TEST_BUILD.cmd','PLAY_LATEST_TEST_BUILD.cmd','PLAY_MK2_KANO_SONYA.cmd'):
        path = ROOT/filename
        previous_hash = next(value for key,value in previous['inputHashes'].items() if Path(key).name == filename)
        if digest(path) != previous_hash:
            raise ValueError('Existing launcher unexpectedly changed')
        pins[str(path)] = previous_hash
    pins[str(installed)] = expected
    sources = {
        'mame-mkp/src/mame/midway/midtunit_m.cpp',
        'diagnostic_v978_owned_torso_invariant_blood/build-info.json',
        'STATUS_2026-10-02_CURRENT_STOCK_FATALITY_PATHS.md',
        'mk2ks_stock_head_victim_v921.lua','mk2ks_cage_torso_display_v979.lua',
        'mk2ks_cage_alt_palette_v983.lua','mk2ks_native_inflation_display_v939.lua',
        'mk2ks_reptile_death_art_v904.lua',
        'tools/run_cage_torso_v979.ps1','tools/run_cage_alt_palette_v983.ps1',
        'tools/run_native_inflation_v939.ps1','tools/run_reptile_death_grounding_v904.ps1',
        'tools/review_native_torso_v986.py','tools/review_cage_alt_blood_v984.py',
        'tools/test_native_torso_art_v982.py','tools/test_native_inflation_art_v991.py',
        'tools/test_native_death_grounding_v992.py','tools/save_owned_torso_blood_checkpoint_v994.py',
        'tools/verify_native_torso_art_v980.py','tools/verify_cage_alt_blood_v985.py',
        'tools/verify_native_inflation_art_v989.py','tools/verify_native_death_grounding_v990.py'}
    # Include the complete local Python import closure used to reconstruct ROM
    # references and assets, not just the four top-level green-check scripts.
    queue = [ROOT/path for path in sources if path.endswith('.py')]
    seen = set()
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8-sig'))):
            modules = [a.name for a in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) else []
            for module in modules:
                local = ROOT/'tools'/((module or '').split('.')[0]+'.py')
                if local.is_file():
                    sources.add(local.relative_to(ROOT).as_posix())
                    queue.append(local)
    (OUT/'input_sources').mkdir(parents=True)
    for relative in sorted(sources):
        path = ROOT/relative
        if not path.is_file():
            raise ValueError('Missing checkpoint source: '+relative)
        destination = OUT/'input_sources'/relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,destination)
        pins[str(path)] = pins[str(destination)] = digest(path)
    references = [
        'diagnostic_v936_owned_inflation_art/roms/mk2ks/mk2ks.mdata',
        'diagnostic_v958_owned_cage_torso_grounding/roms/mk2ks/mk2ks.mdata',
        'audit_v934_pre_owned_inflation/input_sources/mk2ks.mdata',
        'audit_v947_owned_inflation_checkpoint/checkpoint.json']
    for reference in references:
        pins[str(ROOT/reference)] = digest(ROOT/reference)
    for name in ('kano','sonya'):
        for side in (1,2):
            folder = ROOT/f'audit_v904_{name}_p{side}_native_death_grounding'
            for file in ('run.log','guest_maincpu.bin'):
                pins[str(folder/file)] = digest(folder/file)
            for path in (folder/'snap').glob('*.png'):
                pins[str(path)] = digest(path)
    folders = (
        'art_native_torso_v951','art_native_torso_blood_v976','art_native_inflation_v933',
        'audit_v977_owned_torso_blood_encoding','audit_v980_owned_torso_blood_runtime_checked',
        'audit_v981_actual_presented_torso_blood_pixels_checked','audit_v982_owned_torso_blood_corruption_units',
        'audit_v984_controlled_alt_blood_visual_review','audit_v985_controlled_native_alt_blood_checked',
        'audit_v986_owned_torso_blood_visual_review','audit_v989_current_inflation_after_blood_checked',
        'audit_v990_current_reptile_after_blood_checked','audit_v991_current_inflation_corruption_units',
        'audit_v992_current_reptile_corruption_units','audit_v935_owned_inflation_encoding')
    for folder in folders:
        for path in (ROOT/folder).rglob('*'):
            if path.is_file():
                pins[str(path)] = digest(path)
    for file,wanted in pins.items():
        if digest(Path(file)) != wanted:
            raise ValueError('Evidence changed while checkpointing: '+file)
    data = dict(
        scope='12 unassisted normal-costume native Dead Pool cases, plus two separately labeled controlled Kano alternate Cage palette diagnostics',
        candidate='diagnostic_v978_owned_torso_invariant_blood',
        executableSHA256=cage.PROFILES['current'][3],payloadSHA256=cage.PROFILES['current'][4],
        driverSHA256=digest(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'),
        normalCagePhysicalCases=4,normalKitanaPhysicalCases=4,normalReptilePhysicalCases=4,
        separatelyAssistedAlternateDiagnosticCases=2,explicitAlternateFlagWrites=2,
        normalOwnedCageTorsoPresentationAccepted=True,cageBloodEncodingCostumeInvariant=True,
        controlledKanoNativeAlternateBloodBranchAccepted=True,
        cageOwnedSectionDMAs=8944,inflationOwnedDMAs=700,reptileOwnedBodyDMAs=1950,reptileOwnedHeadDMAs=104,
        controlledAlternateOwnedSectionDMAs=4472,cageGroundedLowerDMAs=4368,cageGroundedUpperDMAs=3644,
        selectedNormalRuntimePNGs=660,selectedControlledAlternateRuntimePNGs=134,
        normalHardwarePaletteDumps=72,controlledAlternateHardwarePaletteDumps=24,
        currentCorruptionTestMethods=87,
        naturalAlternateSelectionAccepted=False,fullAlternateCostumeAccepted=False,
        otherDeathPathsAlternateBloodAccepted=False,unusedCagePose4RuntimeAccepted=False,
        rollingHeadArtworkAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,
        fullTowerAccepted=False,fullNativeDeathArtAccepted=False,fullPortAccepted=False,
        installedExecutableUnchanged=True,existingLaunchersNotUpdated=True,releaseZipNotUpdated=True,
        oldBuildCleanupComplete=False,evidencePins=len(pins),inputHashes=dict(sorted(pins.items())))
    (OUT/'checkpoint.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k != 'inputHashes'},indent=2))


if __name__ == '__main__':
    main()
