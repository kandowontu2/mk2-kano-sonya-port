"""Save scoped native progress, preserving the complete unfulfilled objective."""
import ast
import json
import shutil
from pathlib import Path
import verify_rolling_heads_v1014 as heads
import verify_rolling_head_regressions_v1013 as regression

ROOT=heads.ROOT
OUT=ROOT/'audit_v1017_owned_rolling_heads_checkpoint'


def main():
    if OUT.exists():raise ValueError('Never replace a checkpoint')
    previous=json.loads((ROOT/'audit_v995_owned_torso_blood_checkpoint/checkpoint.json').read_text())
    for filename,wanted in previous['inputHashes'].items():
        assert heads.digest(Path(filename))==wanted,'Previous scoped evidence changed: '+filename
    reports=[heads.verify(),regression.verify()]
    assert all(r['passed'] for r in reports)
    units=json.loads((ROOT/'audit_v1015_rolling_head_corruption_units/unit-results.json').read_text())
    assert units['passed'] and units['testMethods']==5 and units['fixtureAndCorruptionChecks']==34 and not units['errors'] and not units['failures']
    review=json.loads((ROOT/'audit_v1011_owned_rolling_head_visual_review/manual-review.json').read_text())
    assert review['normalDeadPoolBarakaOwnedRollingHeadPresentationAccepted'] and not review['fullPortAccepted']
    installed=ROOT/'mame-mkp/mkport.exe'
    assert heads.digest(installed)=='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'
    pins=previous['inputHashes'].copy()
    for r in reports:pins.update(r['inputHashes'])
    rejected=[]
    for name in ('kano','sonya'):
        for side in (1,2):
            directory=ROOT/f'audit_v1003_baraka_{name}_p{side}_owned_rolling_head'
            result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
            text=(directory/'run.log').read_text(encoding='utf-8-sig')
            rows=heads.records(text,'MK2_STOCK_HEAD_V921')
            assert result['exit_code']==0 and result['target_gap']==34
            assert not any(t in ('ACTION','WRAP','CACHE_OVERWRITE') for t,r in rows)
            stop=next(r for t,r in rows if t=='RESULT')
            assert stop['action']==stop['wrap']=='-1' and stop['damage']=='322' and stop['wins']=='2'
            rejected.append(directory.name)
            for filename in ('result.json','run.log'):
                path=directory/filename;pins[str(path)]=heads.digest(path)
    sources={
        'tools/build_rolling_head_order_v1001.py','tools/assemble_rolling_head_candidate_v1002.py',
        'tools/prepare_rolling_head_references_v998.py','tools/verify_rolling_heads_v1014.py',
        'tools/verify_rolling_head_regressions_v1013.py','tools/review_rolling_heads_v1011.py',
        'tools/test_rolling_head_proof_v1015.py','tools/save_rolling_heads_checkpoint_v1017.py',
        'tools/run_rolling_head_v1003.ps1','tools/run_cage_torso_v979.ps1',
        'tools/run_native_inflation_v939.ps1','tools/run_reptile_death_grounding_v904.ps1',
        'mk2ks_rolling_head_display_v1003.lua','mk2ks_stock_head_victim_v921.lua',
        'mk2ks_cage_torso_display_v979.lua','mk2ks_native_inflation_display_v939.lua',
        'mk2ks_reptile_death_grounding_v904.lua','mk2ks_reptile_victim_v887.lua',
        'mame-mkp/src/mame/midway/midtunit_m.cpp','mame-mkp/src/mame/midway/midtunit_v.cpp',
        'mame-mkp/src/mame/midway/midtunit.cpp','STATUS_2026-10-02_CURRENT_ROLLING_HEADS.md',
        'diagnostic_v1002_owned_rolling_head_order/build-info.json'}
    queue=[ROOT/name for name in sources if name.endswith('.py')];seen=set()
    while queue:
        path=queue.pop()
        if path in seen:continue
        seen.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8-sig'))):
            modules=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) else []
            for module in modules:
                local=ROOT/'tools'/((module or '').split('.')[0]+'.py')
                if local.is_file():sources.add(local.relative_to(ROOT).as_posix());queue.append(local)
    (OUT/'input_sources').mkdir(parents=True)
    for relative in sorted(sources):
        path=ROOT/relative;destination=OUT/'input_sources'/relative
        destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,destination)
        pins[str(path)]=pins[str(destination)]=heads.digest(path)
    for folder in ('art_native_rolling_heads_v998','audit_v997_native_rolling_head_references',
                   'audit_v1000_owned_rolling_head_encoding','audit_v1001_owned_rolling_head_encoding',
                   'audit_v1007_owned_rolling_head_runtime_checked','audit_v1009_owned_rolling_head_runtime_checked',
                   'audit_v1010_owned_rolling_head_runtime_checked','audit_v1011_owned_rolling_head_visual_review',
                   'audit_v1012_rolling_head_corruption_units','audit_v1013_current_death_paths_after_rolling_heads_checked',
                   'audit_v1014_owned_rolling_head_position_checked','audit_v1015_rolling_head_corruption_units'):
        for path in (ROOT/folder).rglob('*'):
            if path.is_file():pins[str(path)]=heads.digest(path)
    prior=ROOT/'audit_v995_owned_torso_blood_checkpoint/checkpoint.json';pins[str(prior)]=heads.digest(prior)
    for filename,wanted in pins.items():assert heads.digest(Path(filename))==wanted,filename
    dmas=sum(c['ownedDMAs'] for c in reports[0]['cases'].values())
    data=dict(candidate=heads.CANDIDATE,executableSHA256=heads.EXE,payloadSHA256=heads.PAYLOAD,
              driverSHA256=heads.digest(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'),
              scope='16 normal Dead Pool real-input cases; Baraka all own head/body poses and unchanged Cage/Kitana/Reptile regressions',
              normalPhysicalCases=16,barakaPhysicalCases=4,otherDeathPathRegressionCases=12,
              normalBarakaOwnedRollingHeadPresentationAccepted=True,
              barakaOwnedDMAs=dmas,barakaGroundedBodyDMAs=sum(c['groundedBodyDMAs'] for c in reports[0]['cases'].values()),
              barakaHardwarePaletteDumps=56,barakaSelectedActualPNGs=300,
              actualHeadCloseupsReviewed=28,actualSceneReviewImages=64,
              minimumPresentedNativePixelMatch=min(m['score'] for c in reports[0]['cases'].values() for m in c['pixelMatches']),
              exactNativeDMAImageLocationsChecked=56,unchangedOtherDeathPathPNGs=reports[1]['selectedActualPNGs'],
              unitTestMethods=5,fixtureAndCorruptionChecks=34,
              priorCheckpointPinsRevalidated=len(previous['inputHashes']),rejectedUnreachableInputCases=rejected,
              allNativeStreamsAndPriorPixelsPreserved=True,bothUprightHeadsPreserved=True,
              naturalAlternateSelectionAccepted=False,rollingHeadAlternateColorsAccepted=False,
              allAlternateCostumesAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,
              fullTowerAccepted=False,finalCombinedGameplayAndUIPassAccepted=False,fullPortAccepted=False,
              installedExecutableUnchanged=True,existingLaunchersNotUpdated=True,releaseZipNotUpdated=True,
              oldBuildCleanupComplete=False,evidencePins=len(pins),inputHashes=dict(sorted(pins.items())))
    (OUT/'checkpoint.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='inputHashes'},indent=2))


if __name__=='__main__':main()
