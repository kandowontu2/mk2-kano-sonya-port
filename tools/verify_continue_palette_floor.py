"""Bounded v471 Courtyard shadow verification, NOT full natural-port acceptance.

The body/ROM model is selected solely using the frozen v456 baseline. It is
never selected from the corrected image. Jump-pose decoder correlation remains
diagnostic; acceptance restricts changes rather than claiming complete decoding.
"""
import json
from functools import lru_cache
import numpy as np
import inspect_dynamic_continue as d
import inspect_ground_presentation as p
from verify_ko_round_floor_shadows import digest, need, rgb

NAME = 'diagnostic_v471_owned_palette_floor_shadow'
EXE = '5A33F3368E1AD975ED5FF72EC2E0C6EA74F2BF5BCB4CCD7B2F8338E24E22F01F'
OLD = 'diagnostic_v456_ko_round_floor_shadow'
OLD_EXE = '2731D2D965477251F19E1E8496480588C59BA521DDC3DD4AE55C3FD14D7DDB0A'
PAYLOAD = '82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951'
TAGS = ('FIELD', 'PART', 'INPUT', 'HEALTH', 'CODE', 'SELECT', 'OUTSIDE',
        'SNAP', 'RESULT', 'RE_READY', 'RE_LIVE', 'RESELECT_EXIT')

def matched(folder, current, inputs):
    result = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    name, exe = (NAME, EXE) if current else (OLD, OLD_EXE)
    need(result['exit_code'] == 0 and result['candidate'] == name and
         result['assistance'] == 'none', 'Complete unassisted matched run')
    need(result['executable_sha256'] == exe and result['payload_sha256'] == PAYLOAD,
         'Run executable/payload identity')
    build = json.loads((p.ROOT/name/'build-info.json').read_text(encoding='utf-8-sig'))
    need(build['executable_sha256'] == exe and build['payload_sha256'] == PAYLOAD,
         'Build identity')
    need(digest(p.ROOT/name/'mkport_candidate.exe') == exe, 'Executable bytes')
    need(digest(p.ROOT/name/'roms/mk2ks/mk2ks.mdata') == PAYLOAD, 'Payload bytes')
    manifest = json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    need(manifest == result['input_hashes'], 'Run input manifests agree')
    for path, sha in manifest.items():
        actual = p.ROOT/path
        if digest(actual) != sha:
            # The older v469 observer ran before the video source edit. Accept
            # ONLY an original named build source with an exact frozen copy;
            # never substitute arbitrary logs, observers or images by basename.
            need(build['input_hashes'].get(path) == sha,
                 'Changed non-build-source run input: '+path)
            actual = p.ROOT/name/'input_sources'/actual.name
        need(digest(actual) == sha, 'Frozen run input changed: '+path)
        inputs[str(actual)] = sha
    for path, sha in build['input_hashes'].items():
        actual = p.ROOT/path
        if digest(actual) != sha:
            actual = p.ROOT/name/'input_sources'/actual.name
        need(digest(actual) == sha, 'Matched frozen build source: '+path)
        inputs[str(actual)] = sha
    for file in (folder/'result.json', folder/'input_hashes_before.json', folder/'run.log',
                 p.ROOT/name/'build-info.json', p.ROOT/name/'mkport_candidate.exe',
                 p.ROOT/name/'roms/mk2ks/mk2ks.mdata'):
        inputs[str(file)] = digest(file)

def preserve_records(before, after, tags=TAGS):
    for tag in tags:
        need(p.rows(before, tag) == p.rows(after, tag), 'Actual '+tag+' records changed')

def check_pixels(before, after, body, opaque, shadow):
    need(before.shape == after.shape == body.shape, 'Pixel dimensions')
    expected = shadow & ~opaque
    need(int(expected.sum()) > 100, 'Nontrivial expected projected silhouette')
    need(not np.any(after[expected]), 'Missing, shifted or incorrectly colored floor shadow')
    difference = np.any(before != after, axis=2)
    restored = (opaque & np.all(before == 0, axis=2) &
                np.all(after == body, axis=2) & np.any(body != 0, axis=2))
    need(not np.any(difference & ~(expected | restored)),
         'Change outside independently expected shadow or restoration of erased body pixels')
    need(not np.any(difference & opaque & ~restored), 'Fighter recolored/erased')
    return {'expectedShadowPixels': int(expected.sum()),
            'restoredBodyPixels': int(restored.sum()), 'changedPixels': int(difference.sum())}

def verify_native(fighter, side, inputs):
    old = p.ROOT/f'audit_v472_dynamic_before_{fighter}_p{side}'
    new = p.ROOT/f'audit_v474_dynamic_after_{fighter}_p{side}'
    matched(old, False, inputs); matched(new, True, inputs)
    log, buffers, palettes, draws, caches = d.data(old)
    newlog = (new/'run.log').read_text(encoding='utf-8-sig')
    need('Lua error' not in log+newlog and 'Fatal error' not in log+newlog, 'Runtime error')
    preserve_records(log, newlog, TAGS+('DMA', 'DMA_CACHE', 'GFX', 'RE_PALETTE'))
    ready = p.rows(log, 'RE_READY')
    need(len(ready) == 1, 'One actual continued-fight ready event')
    ready = ready[0]['frame']
    need(0x400 in palettes and 0x500 in palettes, 'Actual continued-arena fighter banks')
    @lru_cache(maxsize=None)
    def model(frame):
        return d.raster(draws.get(frame, []), buffers, palettes, caches)
    records = []; preserved = 0
    live = p.rows(log, 'RE_LIVE')[0]['frame']
    for snap in p.rows(log, 'SNAP'):
        path_old, path_new = old/'snap'/snap['file'], new/'snap'/snap['file']
        before, after = rgb(path_old), rgb(path_new)
        inputs[str(path_old)] = digest(path_old); inputs[str(path_new)] = digest(path_new)
        if snap['frame'] < ready:
            # First fight, paid continue and reselect/VS images should remain
            # identical. Arena intro (mode 7) can legitimately restore shadows.
            if snap['scene'] in ('ground', 'continue', 'reselect'):
                need(np.array_equal(before, after), 'Pre-continued-arena image changed')
                preserved += 1
            continue
        best = None
        for frame in range(snap['frame']-4, snap['frame']+1):
            body, opaque, slots, shadow = model(frame)
            if opaque.sum() < 100: continue
            score = float(np.all(before[opaque] == body[opaque], axis=1).mean())
            if best is None or score > best[0]:
                best = (score, frame, body, opaque, slots, shadow)
        need(best is not None, 'Frozen baseline DMA provenance')
        score, frame, body, opaque, slots, shadow = best
        counts = check_pixels(before, after, body, opaque, shadow)
        feet = {str(n): int(np.where(mask)[0].max()) for n, mask in slots.items()}
        if snap['frame'] == ready:
            need(feet == {'1': 236, '2': 236}, 'Stationary soles align with native Kitana')
        records.append(dict(frame=snap['frame'], dmaFrame=frame, file=snap['file'],
                            baselineBodyCorrelation=score, feet=feet, **counts))
    need(len(records) == 18, 'Full 18-snapshot continued stance/walk/jump/landing sequence')
    need(sum(r['restoredBodyPixels'] for r in records) > 0, 'Erased feet restored')
    return dict(fighter=fighter, side=side, snapshots=records,
                unchangedEarlierSnapshots=preserved, continuedMatchFrame=live,
                actualFields=len(p.rows(log, 'FIELD')), fullPortAcceptance=False)

def verify_stock(side, inputs):
    old = p.ROOT/f'audit_v469_continue_cross_sub_zero_p{side}'
    version = 474 if side == 1 else 476
    new = p.ROOT/f'audit_v{version}_dynamic_after_sub_zero_p{side}'
    matched(old, False, inputs); matched(new, True, inputs)
    before = (old/'run.log').read_text(encoding='utf-8-sig')
    after = (new/'run.log').read_text(encoding='utf-8-sig')
    # v17->v18 only changes observer DMA filtering/slot/palette metadata.
    # Inputs and native game records, and ALL actual PNGs, must be identical.
    preserve_records(before, after)
    snapshots = p.rows(before, 'SNAP')
    need(len(snapshots) == 450, 'Complete stock control sequence')
    for snap in snapshots:
        a, b = old/'snap'/snap['file'], new/'snap'/snap['file']
        need(np.array_equal(rgb(a), rgb(b)), 'Stock control image changed: '+snap['file'])
        inputs[str(a)] = digest(a); inputs[str(b)] = digest(b)
    return dict(fighter='sub_zero', side=side, unchangedSnapshots=len(snapshots),
                actualFields=len(p.rows(before, 'FIELD')), fullPortAcceptance=False)

def verify():
    inputs = {}
    native = [verify_native(fighter, side, inputs)
              for fighter in ('kano', 'sonya') for side in (1, 2)]
    stock = [verify_stock(side, inputs) for side in (1, 2)]
    for file in ('tools/verify_continue_palette_floor.py', 'tools/inspect_dynamic_continue.py',
                 'tools/inspect_ground_presentation.py', 'tools/verify_ko_round_floor_shadows.py'):
        inputs[str(p.ROOT/file)] = digest(p.ROOT/file)
    return dict(passed=True, fullPortAcceptance=False, candidate=NAME,
                scope='Courtyard dynamic palette floor silhouettes after two-human paid continue; '
                      '72 stance/walk/jump/landing images and 900 unchanged stock-control images. '
                      'Not universal native row-DMA geometry, foreground, full selection UI, '
                      'CPU campaign, all-arena/moves/finishers/audio or release acceptance.',
                native=native, stock=stock, inputHashes=inputs)

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
