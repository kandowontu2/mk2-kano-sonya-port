"""Whole earned Tomb scene followed by ordinary paid rejoin and native scanouts.

Keep the earlier independent one-base scene model intact. Later rasters bind
to their own native display latch/VRAM/palette, never seed that earlier model.
No game-state/health/RNG writes, emulation rebuild or raw recordings on disk.
"""
import argparse
import code
import copy
import gzip
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
import numpy as np
import run_native_current_cross_tomb_render as previous
import verify_native_floor_display_v602 as display

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
RAM = {}
PREFIX = 'audit_native_tomb_transition_rejoin'
LUA = tuple(ROOT / ('mk2ks_native_tomb_rejoin_' + name + '.lua')
            for name in ('driver', 'provenance', 'display'))
once = previous.prepared.original.once


def paths(fighter, side):
    need(fighter in ('kano', 'sonya') and side in (1, 2), 'Actual requested fighter and physical slot')
    leaf = f'{PREFIX}_{fighter}_p{side}'
    return ROOT / (leaf + '_ram'), ROOT / (leaf + '_checked')


def initialize(fighter, side):
    source = inspect.getsource(previous.initialize)
    source = once(source, 'audit_native_current_cross_tomb_', PREFIX + '_')
    scope = dict(vars(previous), __file__=__file__, RAM=RAM)
    exec(compile(source, __file__ + '::whole_fresh_current_initializer', 'exec'), scope)
    return scope['initialize'](fighter, side)


def extension_source_guard():
    need(all(p.is_file() for p in LUA), 'All actual extended passive observers and physical driver present')
    driver, provenance, observer = (p.read_text() for p in LUA)
    need('local join_css,join_at,admitted,completed={},nil,nil,nil' in driver,
         'Separate later actual paid-input clock initially absent')
    need(driver.count('once(') == 8 and provenance.count('once(') == 3 and observer.count('once(') == 5,
         'Exact declared whole-original source adaptations')
    need(not re.search(r':write_u\d+|\.value\s*=(?!=)|load_?state', driver + provenance + observer),
         'No game/register/state writes in extended physical/passive wrapper')
    need("local age=(frame-join_at)%300" in driver and "alive_fields=" in driver and
         "MK2_TOMB_POST_BUFFER" in observer and "MK2_TOMB_POST_PIXELS" in observer,
         'Real coin/start policy, owned admission and separate later raster transport')
    baseline = ROOT / 'audit_native_current_cross_tomb_kano_p1_render_checked/report.json'
    report = json.loads(baseline.read_text())
    need(report['passed'] and report['sampledFrames'] == 537 and
         all(sha(p) == h for p, h in report['inputHashes'].items()),
         'Earlier entire current one-base scene outcome remains frozen')
    return {str(p): sha(p) for p in (*LUA, Path(__file__), baseline)}


def physical_extension(log, old, physical):
    """Only the actual terminal frame moves; every earlier earned control is exact."""
    lhs = [s for s in log.splitlines() if s.startswith(physical)]
    rhs = [s for s in old.splitlines() if s.startswith(physical)]
    a = [s for s in lhs if s.startswith('MK2_STAGE_RESULT ')]
    b = [s for s in rhs if s.startswith('MK2_STAGE_RESULT ')]
    need(len(a) == len(b) == 1, 'One actual terminal and one frozen earlier actual terminal')
    row = lambda s: dict(re.findall(r'(\w+)=([^\s]+)', s))
    ar, br = row(a[0]), row(b[0])
    af, bf = int(ar.pop('frame')), int(br.pop('frame'))
    need(ar == br and af > bf, 'Only terminal frame extends, original earned counters/source action identical')
    need([s for s in lhs if s not in a] == [s for s in rhs if s not in b],
         'All earlier actual physical inputs/HP/selection/window/command records byte-identical')


def post_line(line):
    if not line.startswith('MK2_TOMB_POST_STATE '):
        return
    row = dict(re.findall(r'(\w+)=([^\s]+)', line))
    hexadecimal = {'start', 'control', 'tap', 'actor1', 'main1', 'owner1', 'actor2', 'main2', 'owner2'}
    row = {k: int(v, 16 if k in hexadecimal else 10) if k != 'assistance' else v
           for k, v in row.items()}
    need(row['writes'] == 0 and row['assistance'] == 'none', 'Later fields remain passive')
    if RAM['post_states']:
        need(row['frame'] == RAM['post_states'][-1]['frame'] + 1, 'No missing or repeated later native field')
    else:
        need(row['frame'] == row['retired'] + 31, 'First later raster immediately after original verified window')
    RAM['post_states'].append(row)


def post_packet(binary, stream, log):
    header = binary.decode('ascii').strip()
    row = dict(re.findall(r'(\w+)=([^\s]+)', header))
    encoded = stream.readline().decode('ascii').strip()
    if binary.startswith(b'MK2_TOMB_POST_BUFFER '):
        raw = RAM['post_transport'].decode(row, encoded)
        RAM['post_raw'][row['file']] = raw
        log.write('MK2_TOMB_POST_BUFFER_CHECKED ' + header.split(' ', 1)[1] +
                  ' sha256=' + previous.previous.model.digest(raw) + '\n')
        return
    need(row['bytes'] == '406400' and row['width'] == '400' and row['height'] == '254' and
         row['encoding'] == 'u32le_numeric_hex' and len(encoded) == 812800,
         'Full original 400x254 later native raster')
    frame = int(row['frame'])
    state = RAM['post_states'][-1]
    need(state['frame'] == frame and len(RAM['post_records']) + 1 == len(RAM['post_states']),
         'One actual raster in the exact actual field')
    words = np.frombuffer(bytes.fromhex(encoded), dtype='>u4').reshape(254, 400)
    rgb = np.stack([(words >> n) & 255 for n in (16, 8, 0)], axis=2).astype(np.uint8)
    vram = RAM['post_raw'].pop(f'display_vram_{frame}.bin')
    palette = RAM['post_raw'].pop(f'display_palette_{frame}.bin')
    proof = display.check_latch(rgb, vram, palette, state['start'], state['control'], state['tap'])
    digest = previous.previous.model.digest
    record = dict(state, **proof, rgbSHA256=digest(rgb.tobytes()),
                  vramSHA256=digest(vram), paletteSHA256=digest(palette))
    RAM['post_records'].append(record)
    key = tuple(state[k] for k in ('mode', 'arena', 'state1', 'state2'))
    changed = key != RAM.get('post_last_key')
    RAM['post_last_key'] = key
    admitted = state['admitted']
    keep = changed or frame % 120 == 0 or frame-state['action'] in (800, 1100, 1101, 1140) or (
        admitted >= 0 and frame-admitted in (0, 1, 40, 80, 120, 180))
    if keep:
        need(len(RAM['post_images']) < 64, 'Bounded native later-screen review, no raw disk files')
        RAM['post_images'][frame] = rgb.copy()
    log.write('MK2_TOMB_POST_PIXELS_CHECKED ' + header.split(' ', 1)[1] +
              ' sha256=' + record['rgbSHA256'] + '\n')
    if len(RAM['post_records']) % 120 == 0:
        print(f"Later scanout {frame}: mode={state['mode']} states={state['state1']},{state['state2']} "
              f"ids={state['id1']},{state['id2']}; every native pixel bound", flush=True)


def functions(current):
    guard = extension_source_guard()
    # Clone the whole previously executed factory, exposing its generated body.
    factory = inspect.getsource(previous.functions)
    factory = once(factory, '    return namespace', "    namespace['run'].source = body\n    return namespace")
    context = dict(vars(previous), __file__=__file__, RAM=RAM, paths=paths)
    exec(compile(factory, __file__ + '::whole_original_current_transport_factory', 'exec'), context)
    original = context['functions'](current)
    body = original['run'].source
    body = once(body, '    CASE,OUT=paths(fighter,side)',
                '    CASE,OUT=paths(fighter,side)\n    extension_source_guard()')
    body = once(body, '    files.update(Path(p)for p in graphics_pins)',
                '    files.update(LUA)\n    files.update(Path(p)for p in graphics_pins)')
    before = "                if binary.startswith((b'MK2_TOMB_RAM_BUFFER ',b'MK2_TOMB_RAM_PIXELS ')):"
    body = once(body, before,
                "                if binary.startswith((b'MK2_TOMB_POST_BUFFER ',b'MK2_TOMB_POST_PIXELS ')):\n"
                "                    try:post_packet(binary,process.stdout,log)\n"
                "                    except Exception as error:\n"
                "                        if not errors:errors.append(dict(header=binary.decode('ascii').strip(),error=repr(error),traceback=traceback.format_exc()))\n"
                "                    continue\n" + before)
    body = once(body, "                    line=binary.decode('utf-8')",
                "                    line=binary.decode('utf-8')\n"
                "                    try:post_line(line)\n"
                "                    except Exception as error:\n"
                "                        if not errors:errors.append(dict(line=line.strip(),error=repr(error),traceback=traceback.format_exc()))")
    body = once(body, "    stderr=(CASE/'stderr.log').read_text()",
                "    stderr=(CASE/'stderr.log').read_text()\n"
                "    (CASE/'post_scene_records.json').write_text(json.dumps(RAM['post_records'],indent=2)+'\\n')\n"
                "    (CASE/'post_buffer_digests.json').write_text(json.dumps(RAM['post_transport'].records,indent=2)+'\\n')\n"
                "    (CASE/'post_state_records.json').write_text(json.dumps(RAM['post_states'],indent=2)+'\\n')")
    contract = previous.previous.contract_source
    check = "    need([line for line in log.splitlines()if line.startswith(physical)]==\n         [line for line in old.splitlines()if line.startswith(physical)],\n         'All original physical controls/earned damage/select/window/command/terminal records')"
    contract = once(contract, check, '    physical_extension(log,old,physical)')
    contract_scope = dict(previous.previous.scene_scope, physical_extension=physical_extension)
    exec(compile(contract, __file__ + '::whole_scene_only_actual_terminal_extension', 'exec'), contract_scope)
    model = previous.previous.model
    RAM.update(post_states=[], post_records=[], post_images={}, post_raw={}, post_transport=model.Transport(),
               extensionSourceHashes=guard)
    scope = dict(original, OBSERVER=LUA[-1], scene_contract=contract_scope['scene_contract'],
                 post_packet=post_packet, post_line=post_line, LUA=LUA,
                 extension_source_guard=extension_source_guard)
    exec(compile(body, __file__ + '::whole_original_scene_then_later_physical_test', 'exec'), scope)
    return scope


def verify_rejoin(text, records, states, ids):
    rows = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in text.splitlines()
                        if line.startswith('MK2_TOMB_REJOIN_' + tag + ' ')]
    need(not rows('DEADLINE') and not re.search(r'LUA ERROR|stack traceback|RENDER_DEADLINE', text, re.I),
         'No failed deadline or native observer errors')
    admission, complete = rows('ADMITTED'), rows('COMPLETE')
    need(len(admission) == len(complete) == 1, 'One actual physical paid-rejoin admission and terminal completion')
    af, cf = int(admission[0]['frame']), int(complete[0]['frame'])
    need(int(complete[0]['admitted']) == af and int(complete[0]['alive_fields']) >= 180 and cf-af >= 180,
         'At least 180 real resumed fields after actual admission')
    need(admission[0]['ids'] == ','.join(map(str, ids)), 'Actual admitted character IDs, no proxy')
    need(len(states) == len(records) > 180 and [r['frame'] for r in records] ==
         list(range(records[0]['retired']+31, records[-1]['frame']+1)) and records[-1]['frame'] >= cf,
         'Entire later transition is consecutive and includes actual terminal')
    need(all(s == {k:r[k] for k in s} and r['passed'] and r['pixels'] == 101600
             for s,r in zip(states,records)), 'All later native states and full pixels tied to exact native buffers')
    inputs = rows('INPUT')
    for slot, identity in enumerate(ids, 1):
        for button in ('Coin', 'Start'):
            need(any(int(r['frame']) < af and int(r['slot']) == slot and r['button'] == button for r in inputs),
                 'Ordinary paid coin/start actually pressed in both slots')
        selected = [r for r in rows('SELECT_ID') if int(r['slot']) == slot and int(r['frame']) < af]
        need(selected and all(int(r['actual']) == int(r['target']) == identity for r in selected),
             'Both actual native character selections independently confirmed')
    need(any(r['mode'] == 4 for r in records if r['frame'] < af), 'Actual later character-select screen observed')
    live = [r for r in records if af <= r['frame'] <= cf]
    need([r['frame'] for r in live] == list(range(af, cf+1)), 'Every resumed gameplay field retained')
    for r in live:
        need(r['mode'] == 2 and r['admitted'] == af and all(
            r[f'actor{s}'] == r[f'owner{s}'] and r[f'actor{s}'] != 0 and r[f'main{s}'] != 0 and
            r[f'id{s}'] == r[f'roster{s}'] == ids[s-1] and r[f'state{s}'] == 1 for s in (1, 2)),
            'True native owned Kano/Sonya bodies remain playable through resumed window')
    for slot, button in ((1,'Right'),(2,'Left'),(1,'Up'),(2,'High_Punch'),(1,'Block'),(1,'Low_Kick')):
        need(any(af < int(r['frame']) < cf and int(r['slot']) == slot and r['button'] == button for r in inputs),
             'Actual ordinary movement/jump/punch/block/kick inputs present')
    return dict(passed=True, admitted=af, completed=cf, resumedConsecutiveFields=len(live),
                laterConsecutiveNativeFields=len(records), laterNativeBoundRGBPixels=len(records)*101600,
                truePhysicalIDs=ids, ordinaryCoinStartAndNativeSelection=True,
                laterFullIndependentRendererModel=False, visibleClearingIndividuallyReviewed=False,
                fullPortAcceptance=False)


def faults(text, records, states, ids):
    rejected = []
    for name, replace in (
        ('missing coin', lambda t: re.sub(r'^MK2_TOMB_REJOIN_INPUT .*button=Coin\n', '', t, flags=re.M)),
        ('missing start', lambda t: re.sub(r'^MK2_TOMB_REJOIN_INPUT .*button=Start\n', '', t, flags=re.M)),
        ('missing confirmations', lambda t: re.sub(r'^MK2_TOMB_REJOIN_SELECT_ID .*\n', '', t, flags=re.M)),
        ('missing completion', lambda t: re.sub(r'^MK2_TOMB_REJOIN_COMPLETE .*\n', '', t, flags=re.M)),
        ('failed deadline', lambda t: t+'\nMK2_TOMB_REJOIN_DEADLINE frame=0\n'),
        ('short survival', lambda t: re.sub(r'alive_fields=\d+', 'alive_fields=179', t)),
    ):
        try: verify_rejoin(replace(text), records, states, ids)
        except ValueError: rejected.append(name)
        else: raise ValueError('Actual later-window fault admitted: '+name)
    af = int(re.search(r'MK2_TOMB_REJOIN_ADMITTED frame=(\d+)', text)[1])
    for name, mutate in (
        ('missing field', lambda r,s: (r.pop(),s.pop())),
        ('duplicate field', lambda r,s: (r.append(r[-1]),s.append(s[-1]))),
        ('wrong actual character', lambda r,s: next(v for v in r if v['frame']==af).__setitem__('id1',1)),
        ('wrong actual owner', lambda r,s: next(v for v in r if v['frame']==af).__setitem__('owner2',0)),
        ('wrong native roster', lambda r,s: next(v for v in r if v['frame']==af).__setitem__('roster2',1)),
        ('wrong native pixel binding', lambda r,s: r[-1].__setitem__('pixels',101599)),
    ):
        r,s = copy.deepcopy(records),copy.deepcopy(states)
        mutate(r,s)
        try: verify_rejoin(text,r,s,ids)
        except ValueError: rejected.append(name)
        else: raise ValueError('Actual later-state fault admitted: '+name)
    verify_rejoin(text, records, states, ids)
    return rejected


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fighter', choices=('kano','sonya'), required=True)
    parser.add_argument('--side', type=int, choices=(1,2), required=True)
    args = parser.parse_args()
    folder, output = paths(args.fighter,args.side)
    need(not folder.exists() and not output.exists(), 'Fresh immutable actual extended scene case')
    try:
        current = initialize(args.fighter,args.side)
        scope = functions(current)
        base = scope['run'](args.fighter,args.side)
        with gzip.open(folder/'run.log.gz','rt') as reader: text = reader.read()
        post = verify_rejoin(text,RAM['post_records'],RAM['post_states'],base['truePhysicalIDs'])
        post['actualSemanticFaultsRejected'] = faults(text,RAM['post_records'],RAM['post_states'],base['truePhysicalIDs'])
        report = dict(base, laterNativeTransitionAndPhysicalRejoin=post,
                      extensionSourceHashes=RAM['extensionSourceHashes'],
                      originalNaturalIntegrationRequirements=RAM['matrix']['originalNaturalIntegrationRequirements'],
                      originalRemainingWorkGroups=RAM['matrix']['originalRemainingWorkGroups'],goalStatus='active')
        RAM['report'] = report
    except Exception as error:
        report = dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                      fullPortAcceptance=False,goalStatus='active')
        print(json.dumps(report),flush=True)
    need(not output.exists(), 'Never overwrite actual extended trial outcome')
    output.mkdir()
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    if report['passed']:
        print(json.dumps(report['laterNativeTransitionAndPhysicalRejoin'],indent=2),flush=True)
    if RAM.get('images') or RAM.get('post_images'):
        RAM['review_images'] = dict(RAM.get('images',{}),**{})
        RAM['review_images'].update(RAM.get('post_images',{}))
        RAM['server'] = previous.review.start(RAM['review_images'],folder)
    code.interact(banner='Exact native transition trial; bounded original rasters held only in RAM.',local=dict(RAM=RAM))
