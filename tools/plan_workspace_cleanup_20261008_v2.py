"""Exact, dependency-aware plan for the renewed old-output cleanup request."""
import json, os, re
from pathlib import Path
from collections import deque
from functools import lru_cache
from plan_requested_cleanup_v3275 import sha
from inventory_current_port_storage_v4200 import allocated

ROOT = Path(__file__).resolve().parent.parent.resolve()
OUT = ROOT / 'workspace_cleanup_2026-10-08'
FRONTIER = ROOT / 'audit_v5825_current_held_tomb_full_scene_matrix_progress/progress.json'

@lru_cache(maxsize=None)
def existing_path(value):
    p = Path(value)
    return p.resolve() if p.is_file() else None

def paths(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from paths(key)
            yield from paths(item)
    elif isinstance(value, list):
        for item in value:
            yield from paths(item)
    elif isinstance(value, str) and re.match(r'^[A-Za-z]:[\\/]', value):
        p = existing_path(value)
        if p is not None:
            yield p

def main():
    destination = OUT / 'deletion_plan.json'
    if destination.exists():
        raise ValueError('Never overwrite an executed cleanup plan')
    record = json.loads(FRONTIER.read_text())
    assert record['passed'] and record['goalStatus'] == 'active'
    protected, visited, queue = set(), set(), deque([FRONTIER])
    while queue:
        path = queue.popleft()
        if path in visited:
            continue
        visited.add(path)
        if len(visited) % 100 == 0:
            print('Dependency graph:', len(visited), 'JSON files;', len(protected), 'protected files; queue', len(queue), flush=True)
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        for dependency in paths(data):
            protected.add(dependency)
            if dependency.suffix.lower() == '.json' and dependency not in visited:
                queue.append(dependency)
    print('Inspected current dependency graph:', len(visited), 'JSON files;', len(protected), 'protected files', flush=True)
    guards = dict(record['newInputHashes'])
    guards[str(FRONTIER)] = sha(FRONTIER)
    previous = json.loads((ROOT/'workspace_cleanup_followup_2026-10-05/deletion_plan.json').read_text())
    for name in previous['preservedHashes']:
        p = Path(name)
        if p.is_file():
            guards[str(p)] = sha(p)
            protected.add(p.resolve())
    targets, skipped = [], []
    cache = ROOT/'mame-mkp/build/mingw-gcc'
    if cache.is_dir():
        targets.append((cache, 'folder', 'regenerable compiler objects/libraries, not the playable executable'))
    for prefix in ('audit_v2347_', 'audit_v2611_', 'audit_v2633_'):
        for folder in ROOT.glob(prefix+'*campaign'):
            mix, result = folder/'native_mix.wav', folder/'result.json'
            if not mix.is_file() or not result.is_file():
                continue
            status = json.loads(result.read_text(encoding='utf-8-sig'))
            if status.get('passed') is not False or status.get('unassisted_clear_proven') is not False:
                skipped.append(str(mix)+' (not a confirmed obsolete failed campaign)')
                continue
            if status.get('candidate') != 'diagnostic_v1836_ball_register_boundary':
                skipped.append(str(mix)+' (unexpected build)')
                continue
            targets.append((mix, 'file', 'raw mix from superseded failed campaign; logs/results/source retained'))
    for name in (
        'audit_v2430_unreferenced_old_build_recovery/six_unreferenced_builds_complete_recovery.zip',
        'audit_v2486_next_old_build_solid_recovery/ten_unreferenced_builds_complete_recovery.tar.xz',
        'audit_v2518_remaining_old_build_recovery/remaining_68_builds_complete_recovery.tar.xz',
        'audit_v3254_obsolete_workspace_parallel_recovery/obsolete_470_folders_complete_recovery.tar.xz',
    ):
        p = ROOT/name
        if p.is_file():
            targets.append((p, 'file', 'recovery archive containing already retired old builds; inventory retained'))
    rows, identities = [], {}
    for target, kind, reason in targets:
        target = target.resolve(strict=True)
        assert target != ROOT and target.is_relative_to(ROOT)
        affected = [p for p in protected if p == target or target in p.parents]
        if affected:
            skipped.append(dict(path=str(target), reason='current transitive dependency', protected=[str(p) for p in affected]))
            continue
        for ancestor in (target, *target.parents):
            if ancestor == ROOT:
                break
            assert not ancestor.lstat().st_file_attributes & 0x400
        leaves = []
        if kind == 'file':
            leaves = [target]
        else:
            for base, dirs, files in os.walk(target, followlinks=False):
                for name in dirs:
                    assert not (Path(base)/name).lstat().st_file_attributes & 0x400
                leaves.extend(Path(base)/name for name in files)
        entries = []
        for leaf in leaves:
            stat = leaf.lstat()
            assert not stat.st_file_attributes & 0x400
            amount = allocated(leaf)
            key = (stat.st_dev, stat.st_ino)
            if key not in identities:
                identities[key] = [0, stat.st_nlink, amount]
            identities[key][0] += 1
            entries.append(dict(path=str(leaf), bytes=stat.st_size, mtimeNS=stat.st_mtime_ns,
                                SHA256=sha(leaf), allocatedBytes=amount, links=stat.st_nlink))
        rows.append(dict(path=str(target), kind=kind, reason=reason, files=entries))
    for name, digest in guards.items():
        assert sha(name) == digest, name
    plan = dict(root=str(ROOT), targets=rows, preservedHashes=guards,
                dependencyFrontier=str(FRONTIER), transitiveJSONFilesInspected=len(visited),
                transitiveProtectedFiles=len(protected), skipped=skipped,
                reclaimableAllocatedBytes=sum(v[2] for v in identities.values() if v[0] == v[1]),
                retiredHistoricalEvidencePins=[r['path'] for r in rows if r['kind']=='file'],
                noNewRecoveryArchive=True, sourceAndPlayableArtifactsRemoved=False,
                fullPortAcceptance=False)
    destination.write_text(json.dumps(plan, indent=2)+'\n')
    print(json.dumps(dict(targets=len(rows), files=sum(len(r['files']) for r in rows),
                         reclaimableGiB=round(plan['reclaimableAllocatedBytes']/2**30, 3),
                         selected=[dict(path=r['path'],reason=r['reason']) for r in rows],
                         skipped=skipped), indent=2), flush=True)

if __name__ == '__main__':
    main()
