"""Controlled alternate palette evidence, explicitly not natural selection."""
import json
import re
import struct
from pathlib import Path
import numpy as np
import verify_native_arm_blood_v1064 as normal

ROOT = normal.ROOT
OUT = ROOT / 'audit_v1065_arm_alternate_palette_diagnostic_checked'
CASES = tuple(f'audit_v1063_jax_kano_p{side}_controlled_alternate_blood' for side in (1, 2))


def verify():
    guest, graphics, assets = normal.reconstruct()
    errors, pins, summaries = [], {}, {}
    donor = (ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    normal_palette = normal.colors.palette(donor, 0x92bbc)
    alternate_palette = normal.colors.palette(donor, 0x92c3e)
    info = json.loads((ROOT / normal.CANDIDATE / 'build-info.json').read_text(encoding='utf-8-sig'))
    def need(ok, label):
        if not ok:
            errors.append(label)
    for case in CASES:
        folder = ROOT / case
        result = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
        side = result['victim_slot']
        need(result['exit_code'] == 0 and result['candidate'] == normal.CANDIDATE
             and result['executable_sha256'] == info['executable_sha256']
             and result['payload_sha256'] == info['payload_sha256'], 'Exact diagnostic build ' + case)
        need(result['assistance'] == 'controlled_alt_flag' and not result['natural_alternate_selection_verified']
             and not result['cheats_enabled'] and result['player'] == 'kano'
             and result['killer'] == 'jax' and result['command'] == 'bbbb_lp'
             and result['target_gap'] == 96, 'Explicit controlled scope ' + case)
        for filename, wanted in result['input_hashes'].items():
            need(normal.digest(Path(filename)) == wanted, 'Changed diagnostic input ' + filename)
            pins[filename] = wanted
        text = (folder / 'run.log').read_text(encoding='utf-8-sig')
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation', text, re.I), 'No runtime error ' + case)
        stock = normal.prior.rows(text, 'MK2_STOCK_HEAD_V921')
        art = normal.prior.rows(text, 'MK2_ROLLING_HEAD_V1003')
        controlled = normal.prior.rows(text, 'MK2_ARM_ALT_V1063')
        entries = lambda tag: [r for t, r in stock if t == tag]
        action, wrap, stop = entries('ACTION'), entries('WRAP'), entries('RESULT')
        assists = [r for t, r in controlled if t == 'ASSIST']
        ends = [r for t, r in controlled if t == 'RESULT']
        need(len(action) == len(wrap) == len(stop) == len(assists) == len(ends) == 1,
             'One explicit assist and native completion ' + case)
        if len(action) != 1 or len(assists) != 1:
            continue
        action, assist = action[0], assists[0]
        start = int(action['frame'])
        need(assist['actor'] == action['victim_actor'] and assist['id'] == '17'
             and assist['side'] == str(side) and int(assist['frame']) < start
             and int(assist['new'], 16) == int(assist['old'], 16) | 0x40
             and assist['writes'] == '1' and assist['assistance'] == 'controlled_alt_flag'
             and assist['natural_selection_verified'] == 'false'
             and ends[0]['applied'] == ends[0]['writes'] == '1', 'Exactly one known flag-6 write ' + case)
        need(all(r['writes'] == '0' and r['assistance'] == 'none' for _, r in stock + art),
             'Other observers and physical driver unchanged ' + case)
        live = entries('FIRST_LIVE')
        need(len(live) == 1 and live[0]['ids'] == '11,17'
             and live[0]['victim'] == action['victim_actor'], 'Actual Kano/Jax selection ' + case)
        need(action['variant'] == '2' and action['address'] == 'FF8BE240'
             and action['damage'] == '322' and wrap[0]['age'] == '147'
             and int(wrap[0]['frame']) == start + 147 and stop[0]['frame'] == '5198'
             and stop[0]['damage'] == '322' and stop[0]['wins'] == '2'
             and not entries('CACHE_OVERWRITE'), 'Native action/timing and safe continuation ' + case)
        need((folder / 'guest_maincpu.bin').read_bytes() == guest, 'Whole native guest ' + case)
        need((folder / 'native_arm_rip_gfx.bin').read_bytes() == graphics, 'Actual native packed pixels ' + case)
        own = {g: a for g, a in assets.items() if a['fighter'] == 'kano'}
        dumps = {int(r['source'], 16): r for t, r in art if t == 'PALETTE_DUMP'}
        dmas = [r for t, r in art if t == 'DMA' and int(r['source'], 16) in own]
        queues = {(r['frame'], r['cursor'], r['source']): r for t, r in art if t == 'QUEUE'}
        matches, mismatched_arm_pens = [], set()
        for tag, snap in art:
            source = int(snap.get('source', '0'), 16)
            if tag != 'POSE_SNAPSHOT' or source not in own:
                continue
            asset = own[source]
            dma = next((r for r in dmas if r['frame'] == snap['queued_frame']
                        and int(r['source'], 16) == source
                        and r['fifo_actor'] == snap['actor_pose'].split('_')[0]), None)
            need(dma is not None, 'Actual native snapshot DMA ' + case)
            if dma is None:
                continue
            queue = queues[(dma['frame'], dma['cursor'], dma['source'])]
            if asset['kind'] == 'body':
                need(queue['id'] == '17' and queue['actor'] == action['victim_actor']
                     and int(queue['body'], 16) & 0x40 != 0
                     and queue['y'] == queue['floor'], 'Owned alternate body ' + case)
            path = folder / dumps[source]['file']
            raw = np.array(struct.unpack('<64I', path.read_bytes()), dtype=np.uint32)
            palette = np.stack(((raw >> 16) & 255, (raw >> 8) & 255, raw & 255), axis=1)
            used = np.unique(asset['indices']);used = used[used != 0]
            expected = alternate_palette if asset['kind'] == 'body' else normal_palette
            need(np.max(np.abs(palette[used].astype(int) - expected[used].astype(int))) <= 1,
                 'Measured body/prop hardware palette ' + case)
            if asset['bloodMask'].any():
                pens = np.unique(asset['indices'][asset['bloodMask']])
                need(set(pens).issubset({48, 46, 63}) and np.max(
                    np.abs(palette[pens].astype(int) - alternate_palette[pens].astype(int))) <= 1,
                    'Every classified blood pixel remains native red ' + case)
            if asset['kind'] == 'arms':
                different = used[np.max(np.abs(normal_palette[used].astype(int)
                                              - alternate_palette[used].astype(int)), axis=1) > 5]
                mismatched_arm_pens.update(map(int, different))
            picture = folder / 'snap' / f"head_pose_{snap['actor_pose']}_{snap['frame']}.png"
            score, count = normal.pixel_score(picture, asset['indices'], palette, dma)
            matches.append({'kind': asset['kind'], 'pose': asset['pose'], 'score': score,
                            'visibleChromaticPixels': count, 'picture': str(picture)})
            for path in (path, picture):
                pins[str(path)] = normal.digest(path)
        need({(m['kind'], m['pose']) for m in matches if m['score'] >= 0.5
              and m['visibleChromaticPixels'] >= 8} == {(k, p) for k in ('body', 'arms') for p in range(5)},
             'Actual pixels for all ten controlled poses ' + case)
        need(bool(mismatched_arm_pens), 'Expose native detached-arm alternate palette gap ' + case)
        summaries[case] = {'controlledFlagWrites': 1, 'nativeWrapAge': 147, 'ownedDMAs': len(dmas),
                           'pixelMatches': matches, 'bloodColourCorrectInMeasuredHardwarePalette': True,
                           'bodyUsesAlternatePalette': True, 'detachedArmsStillUseNormalPalette': True,
                           'mismatchedArmCostumePens': sorted(mismatched_arm_pens)}
        for filename in ('run.log', 'result.json', 'guest_maincpu.bin', 'native_arm_rip_gfx.bin'):
            pins[str(folder / filename)] = normal.digest(folder / filename)
    return {'passed': not errors, 'errors': sorted(set(errors)), 'cases': summaries, 'inputHashes': pins,
            'scope': 'two controlled flag-6 diagnostics ONLY; blood fix and detached-arm costume gap',
            'controlledBloodColourDiagnosticAccepted': not errors,
            'detachedArmAlternateCostumeFixStillRequired': True,
            'naturalAlternateSelectionAccepted': False, 'fullAlternateRuntimeAccepted': False,
            'allArenasAccepted': False, 'fullPortAccepted': False}


if __name__ == '__main__':
    if OUT.exists():
        raise ValueError('Preserve diagnostic evidence')
    report = verify()
    OUT.mkdir()
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('cases', 'inputHashes')}, indent=2))
    raise SystemExit(0 if report['passed'] else 1)
