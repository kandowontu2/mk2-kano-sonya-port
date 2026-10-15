"""Exact obsolete output targets, excluding current dependency frontiers and active assets."""
import hashlib
import json
import os
import re
from pathlib import Path
from collections import Counter
import inventory_requested_cleanup_v3274 as space

ROOT = space.ROOT.resolve()
OUT = space.OUT

def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest().upper()

def main():
    output = OUT / 'deletion_plan.json'
    if output.exists():
        raise ValueError('Never overwrite an executed cleanup plan')
    frontiers = [ROOT / 'audit_v3260_cleanup_and_adversity_full_scope_checkpoint/checkpoint.json',
                 ROOT / 'audit_v3264_current_native_cpu_square_hit/input_hashes_before.json',
                 ROOT / 'audit_v3269_current_native_cpu_square_hit/input_hashes_before.json']
    protected = set()
    guard = {}
    for frontier in frontiers:
        record = json.loads(frontier.read_text(encoding='utf-8-sig'))
        paths = record.get('inputHashes', record)
        guard[str(frontier)] = sha(frontier)
        for value in paths:
            path = Path(value)
            if path.is_absolute() and path.is_relative_to(ROOT):
                protected.add(path.relative_to(ROOT).parts[0].casefold())
    # Latest in-progress verification's historical trajectory reference is retained.
    for name in ('verify_current_cpu_square_v3265.py', 'current_cpu_capture_contract_v3270.py',
                 'run_current_cpu_square_v3268.ps1'):
        script = ROOT / 'tools' / name
        if script.exists():
            guard[str(script)] = sha(script)
            for value in re.findall(r'(?:audit|diagnostic|release)_v\d+_[a-zA-Z0-9_]+', script.read_text()):
                protected.add(value.casefold())
    protected.update(('diagnostic_v1836_ball_register_boundary',
                      'diagnostic_v2753_native_friendship_palette',
                      'diagnostic_v3172_native_morph_shadow'))
    inventory_path = OUT / 'inventory.json'
    guard[str(inventory_path)] = sha(inventory_path)
    inventory = json.loads(inventory_path.read_text())
    names = []
    for row in inventory['groups']:
        name = row['name']
        match = re.fullmatch(r'(audit|diagnostic|regression|control|trace|pilot|reference)_v(\d+)_[a-zA-Z0-9_]+', name)
        if match and int(match[2]) < 3200 and name.casefold() not in protected:
            names.append(name)
    if '_archive' in protected:
        raise ValueError('Legacy archive is a current dependency; do not discard it')
    names += ['_archive/legacy_evidence_v284', 'mame-mkp/build/mingw-gcc']
    compiler = ROOT / 'mame-mkp/build/mingw-gcc'
    checkpoint = json.loads(frontiers[0].read_text())
    if any(Path(value).is_relative_to(compiler) for value in checkpoint['inputHashes']):
        raise ValueError('Compiler output contains a required checkpoint dependency')
    critical = [ROOT / 'PLAY_MK2_KANO_SONYA.cmd', ROOT / 'PLAY_CURRENT_V1836_CHECKED.cmd',
                ROOT / 'tools/check_ball_register_playtest_v1849.ps1',
                ROOT / 'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                ROOT / 'diagnostic_v1836_ball_register_boundary/build-info.json',
                ROOT / 'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata',
                ROOT / 'diagnostic_v3172_native_morph_shadow/mkport_candidate.exe',
                ROOT / 'diagnostic_v3172_native_morph_shadow/roms/mk2ks/mk2ks.mdata',
                ROOT / 'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip']
    critical += list((ROOT / 'samples/mk2ks').glob('*.wav'))
    for relative in ('src/devices/cpu/tms34010/tms34010.cpp', 'src/devices/cpu/tms34010/tms34010.h',
                     'src/frontend/mame/mame.cpp', 'src/frontend/mame/ui/slider.h',
                     'src/mame/mame.lst', 'src/mame/midway/midtunit.cpp',
                     'src/mame/midway/midtunit.h', 'src/mame/midway/midtunit_m.cpp',
                     'src/mame/midway/midtunit_v.cpp', 'src/mame/midway/midtunit_v.h',
                     'src/osd/modules/lib/osdlib.h', 'src/osd/modules/monitor/monitor_module.h',
                     'src/mame/midway/mk2ks_native_picture.h'):
        critical.append(ROOT / 'mame-mkp' / relative)
    guard.update({str(path): sha(path) for path in critical})
    rows, identities = [], {}
    for index, name in enumerate(names):
        folder = (ROOT / name).resolve(strict=True)
        if not folder.is_relative_to(ROOT) or folder == ROOT:
            raise ValueError('Exact child target required')
        for ancestor in (folder, *folder.parents):
            if ancestor == ROOT:
                break
            if ancestor.lstat().st_file_attributes & 0x400:
                raise ValueError('No linked target or ancestor')
        files = directories = logical = 0
        for base, dirs, leaves in os.walk(folder, followlinks=False):
            directories += 1
            for leaf in [*dirs, *leaves]:
                path = Path(base) / leaf
                meta = path.lstat()
                if meta.st_file_attributes & 0x400:
                    raise ValueError('No reparse entries anywhere in removal targets')
                if leaf in dirs:
                    continue
                files += 1
                logical += meta.st_size
                key = (meta.st_dev, meta.st_ino)
                if key not in identities:
                    identities[key] = [0, meta.st_nlink, space.allocated(path)]
                identities[key][0] += 1
        rows.append(dict(path=str(folder), files=files, directories=directories, logicalBytes=logical))
        if index % 500 == 0:
            print('Validated obsolete folders:', index + 1, '/', len(names), flush=True)
    result = dict(root=str(ROOT), targets=rows, preservedHashes=guard,
                  protectedTopLevelFolders=len(protected), dependencyFrontiers=[str(p) for p in frontiers],
                  reclaimableAllocatedBytes=sum(r[2] for r in identities.values() if r[0] == r[1]),
                  hardlinkedIdentitiesKeptElsewhere=sum(r[0] < r[1] for r in identities.values()),
                  recovery='Obsolete test outputs and legacy archive history are intentionally discarded. Compiler cache can be regenerated from preserved source. No new recovery archive is created.',
                  sourceAndPlayableArtifactsRemoved=False)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(targetFolders=len(rows), files=sum(r['files'] for r in rows),
                         reclaimableGiB=round(result['reclaimableAllocatedBytes']/2**30, 2),
                         protectedFolders=len(protected)), indent=2), flush=True)

if __name__ == '__main__':
    main()
