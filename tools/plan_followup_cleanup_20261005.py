"""Plan requested removal of obsolete builds and failed-campaign recordings."""
import json
import os
import re
from pathlib import Path
import inventory_requested_cleanup_v3274 as space
from plan_requested_cleanup_v3275 import sha

ROOT = space.ROOT.resolve()
OUT = ROOT / 'workspace_cleanup_followup_2026-10-05'
FRONTIERS = [
    ROOT / 'audit_v3288_current_cpu_square_full_scope_checkpoint/checkpoint.json',
    ROOT / 'audit_v3269_current_native_cpu_square_hit/input_hashes_before.json',
    ROOT / 'audit_v3297_current_cpu_bicycle_launch_response/input_hashes_before.json',
    ROOT / 'audit_v3308_current_cpu_bicycle_launch_jump/input_hashes_before.json',
]

def plan():
    destination = OUT / 'deletion_plan.json'
    if destination.exists():
        raise ValueError('Never overwrite a cleanup plan')
    inventory = json.loads((OUT / 'inventory.json').read_text())
    pinned = set()
    protected = {'diagnostic_v1836_ball_register_boundary',
                 'diagnostic_v2753_native_friendship_palette',
                 'diagnostic_v3172_native_morph_shadow',
                 'release_v1863_current_playtest'}
    for frontier in FRONTIERS:
        record = json.loads(frontier.read_text(encoding='utf-8-sig'))
        pinned.add(frontier)
        for value in record.get('inputHashes', record):
            path = Path(value)
            if path.is_absolute() and path.is_relative_to(ROOT):
                pinned.add(path)
                protected.add(path.relative_to(ROOT).parts[0].casefold())
    old_plan = json.loads((ROOT / 'workspace_cleanup_requested_2026-10-05/deletion_plan.json').read_text())
    guards = {path: sha(path) for path in old_plan['preservedHashes'] if Path(path).exists()}
    for frontier in FRONTIERS:
        guards[str(frontier)] = sha(frontier)
    guards[str(ROOT / 'tools/plan_followup_cleanup_20261005.py')] = sha(__file__)
    outer = Path('C:/Users/kando/Documents/Codex/2026-08-30/continue-the-mk2-kano-sonya-port/PLAY_MK2_KANO_SONYA.cmd')
    guards[str(outer)] = sha(outer)
    targets = []
    for row in inventory['groups']:
        name = row['name']
        if name.casefold() in protected:
            continue
        obsolete = bool(re.fullmatch(r'v\d+[a-z]?_[A-Za-z0-9_-]+', name))
        obsolete |= bool(re.fullmatch(r'diagnostic_v(?:\d+[a-z]?|native)_[A-Za-z0-9_-]+', name))
        obsolete |= name == 'release_v1743_current_playtest'
        if obsolete:
            targets.append((ROOT / name, 'folder', 'superseded early build/test output'))
    recovery = ROOT / 'audit_v3262_obsolete_workspace_zstd_recovery/obsolete_470_folders_complete_recovery.tar.zst'
    # The checkpoint pins this as cleanup-history recovery, not as a game/build
    # dependency. This renewed request explicitly discards the obsolete history.
    retired = [str(recovery)] if recovery in pinned else []
    targets.append((recovery, 'file', 'archive of previously discarded obsolete builds'))
    # Retire only raw mixes from failed historical boss/campaign trials. Their
    # logs, summaries, images and source snapshots stay; no successful ending or
    # campaign audio acceptance exists. Arena/finisher audio stays untouched.
    for row in inventory['largestFiles']:
        path = Path(row['path'])
        parts = path.relative_to(ROOT).parts
        match = re.fullmatch(r'audit_v(\d+)_[A-Za-z0-9_]+', parts[0])
        if len(parts) == 2 and parts[1] == 'native_mix.wav' and match:
            if 2110 <= int(match[1]) < 2600 and parts[0].endswith(('_campaign', '_extended')):
                targets.append((path, 'file', 'raw recording from superseded failed boss trial'))
                if path in pinned:
                    retired.append(str(path))
    identities = {}
    rows = []
    for target, kind, reason in targets:
        target = target.resolve(strict=True)
        if target == ROOT or not target.is_relative_to(ROOT):
            raise ValueError('Exact descendant required')
        for ancestor in [target, *target.parents]:
            if ancestor == ROOT:
                break
            if ancestor.lstat().st_file_attributes & 0x400:
                raise ValueError('No reparse target or ancestor')
        leaves = [target] if kind == 'file' else []
        directories = 0
        if kind == 'folder':
            for base, dirs, files in os.walk(target, followlinks=False):
                directories += 1
                for name in dirs:
                    if (Path(base) / name).lstat().st_file_attributes & 0x400:
                        raise ValueError('Linked directory in target')
                leaves.extend(Path(base) / name for name in files)
        logical = 0
        for leaf in leaves:
            stat = leaf.lstat()
            if stat.st_file_attributes & 0x400:
                raise ValueError('Linked file in target')
            logical += stat.st_size
            key = (stat.st_dev, stat.st_ino)
            if key not in identities:
                identities[key] = [0, stat.st_nlink, space.allocated(leaf)]
            identities[key][0] += 1
        rows.append(dict(path=str(target), kind=kind, reason=reason,
                         files=len(leaves), directories=directories, logicalBytes=logical))
    folder_targets = {target for target, kind, _ in targets if kind == 'folder'}
    file_targets = {target for target, kind, _ in targets if kind == 'file'}
    def under_target(pin):
        return pin in file_targets or any(parent in folder_targets for parent in pin.parents)
    for pin in pinned:
        if str(pin) in retired:
            continue
        if under_target(pin):
            raise ValueError(f'Active dependency under removal target: {pin}')
    for value in guards:
        pin = Path(value)
        if under_target(pin):
            raise ValueError(f'Playable/source guard under target: {pin}')
    preserved = {}
    for pin in pinned:
        if str(pin) not in retired:
            stat = pin.stat()
            preserved[str(pin)] = dict(size=stat.st_size, mtime=stat.st_mtime_ns)
    result = dict(root=str(ROOT), targets=rows, preservedHashes=guards,
                  retainedActiveInputStats=preserved, retiredHistoricalEvidencePins=retired,
                  reclaimableAllocatedBytes=sum(v[2] for v in identities.values() if v[0] == v[1]),
                  permanentlyDiscarded=True, noNewRecoveryArchive=True,
                  sourceCurrentBuildsROMsSettingsReleasePreserved=True,
                  fullPortAcceptance=False)
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(folders=sum(r['kind']=='folder' for r in rows),
                         individualFiles=sum(r['kind']=='file' for r in rows),
                         GiB=round(result['reclaimableAllocatedBytes']/2**30, 2),
                         retiredHistoricalAudioPins=len(retired)), indent=2), flush=True)

if __name__ == '__main__':
    plan()
