"""Current actual ending pages after explicit fixtures, never a tower-clear gate."""
import argparse
import json
import re
import struct
import wave
from pathlib import Path
import numpy as np
from PIL import Image
from verify_native_boss_recovery_v680_v1 import ROOT, EXE, PAYLOAD, GUEST as GUEST_SHA, digest, parse as parse_native

GUEST = ROOT / 'audit_v684_pit_guest_rom_integrity/diagnostic_v680_native_pit_initial_cache/guest_maincpu.bin'
ORACLE = ROOT / 'audit_v702_original_photo_oracle'
CONTROL = ROOT / 'audit_v718_current_ending_stock_liu_p1'


def stock_control(check_hashes):
    result = json.loads((CONTROL/'result.json').read_text(encoding='utf-8-sig'))
    text = (CONTROL/'run.log').read_text(encoding='utf-8-sig')
    rows = parse(text); errors = []
    def need(ok, label):
        if not ok: errors.append('Stock control: ' + label)
    need(result['exit_code'] == 0 and result['player'] == 'liu_kang' and result['human_slot'] == 1 and
         result['assistance'] == 'stage16_combat_health_only' and result['executable_sha256'] == EXE and result['payload_sha256'] == PAYLOAD,
         'Actual same-candidate original-character assisted diagnostic')
    if check_hashes:
        for name, sha in result['input_hashes'].items(): need(digest(Path(name)) == sha, 'Executed input changed: ' + name)
    source = (CONTROL/'input_sources/mk2ks_current_ending_presentation_v680_v4.lua').read_text()
    need(re.findall(r'\bp:write_\w+\([^\n]*?\)', source) ==
         ['p:write_u16(0x01061b30,16)', 'p:write_u16(slots[opponent].hp,1)', 'p:write_u16(slots[side].hp,161)'] and
         not re.search(r'\bload\s*\(|\bdofile\s*\(', source), 'No stock actor/ID/art/ending manipulation')
    live = [r for r in rows if r['tag']=='LIVE']
    need(bool(live) and all(r['human']=='1:1' and r['cpu']=='13:13' for r in live), 'Actual original Liu Kang and Shao Kahn')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation', text, re.I), 'No runtime/observer errors')
    starts = [r for r in rows if r['tag']=='ENDING_START']; done = [r for r in rows if r['tag']=='ENDING_COMPLETED']
    finals = [r for r in rows if r['tag']=='ENDING_FIXTURE_RESULT']
    need(len(starts)==len(done)==len(finals)==1 and finals[0]['last_fixture']<starts[0]['frame'] and finals[0]['ending_writes']==0 and
         done[0]['pictures']=='1,1' and done[0]['texts']=='3,3', 'Own complete native ending with no ending assistance')
    guest = GUEST.read_bytes(); original = (ROOT/'mk2/mk2-maincpu.bin').read_bytes(); frames={}
    for page in (1,2):
        entries=[r for r in rows if r['tag']=='PICTURE' and r['page']==page]
        need(len(entries)==1, 'One actual own picture page')
        if len(entries)!=1:continue
        row=entries[0]; index=16+2+page-1
        current=struct.unpack_from('<I',guest,0xf4900+index*4)[0]
        stock=struct.unpack_from('<I',original,(0xff8f48f0-0xff800000)//8+index*4)[0]
        need(current==stock and row['entry']==0xff800000+(0xf4900+index*4)*8 and
             row['value']==current&0xffff and row['roster']==1 and row['pc']==0xff8447e0, 'Original unmodified photo pointer/native renderer dispatch')
        path=CONTROL/'snap'/f'ending_page{page}_{row["frame"]}.png'
        frames[page]=np.asarray(Image.open(path).convert('RGB'))
    return errors,frames


def parse(text):
    rows = parse_native(text)
    for row in rows:
        if row['tag'] in ('PICTURE', 'TEXT'):
            raw = dict(re.findall(r'(\w+)=([^\s]+)', text[row['event']:].splitlines()[0]))
            row['value'] = int(raw['value'], 16); row['mask'] = int(raw['mask'], 16)
    return rows


def photo_rgb(path):
    data = path.read_bytes(); width, height, _, colors = struct.unpack_from('<4H', data)
    if colors != 256 or len(data) != 520 + width * height: raise ValueError('Exact native photo record required')
    palette = np.frombuffer(data, dtype='<u2', count=256, offset=8)
    rgb5 = np.stack(((palette >> 10) & 31, (palette >> 5) & 31, palette & 31), axis=1)
    rgb = ((rgb5 << 3) | (rgb5 >> 2)).astype(np.uint8)
    return rgb[np.frombuffer(data, dtype=np.uint8, offset=520).reshape(height, width)]


def locate_photo(image, needle):
    """Find all exact full photo matches, not a partial/template score."""
    h, w = needle.shape[:2]; ih, iw = image.shape[:2]
    packed = needle[:, :, 0].astype(np.uint32) << 16 | needle[:, :, 1].astype(np.uint32) << 8 | needle[:, :, 2]
    colors, counts = np.unique(packed, return_counts=True)
    color = colors[np.argmin(counts)]
    ay, ax = np.argwhere(packed == color)[0]
    locations = np.argwhere(np.all(image == needle[ay, ax], axis=2))
    matches = []
    for sy, sx in locations:
        y, x = int(sy - ay), int(sx - ax)
        if 0 <= y <= ih - h and 0 <= x <= iw - w and np.array_equal(image[y:y+h, x:x+w], needle):
            matches.append([x, y])
    return matches


def verify(folder, check_hashes=True, text_override=None, image_override=None):
    result = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
    text = text_override if text_override is not None else (folder / 'run.log').read_text(encoding='utf-8-sig')
    errors = []
    def need(ok, label):
        if not ok and label not in errors: errors.append(label)
    side = result['human_slot']; identity = {'kano':17, 'sonya':18}[result['player']]
    v3 = result['assistance'] == 'stage16_combat_health_only'
    version = 3 if v3 else 2
    need(side in (1, 2) and result['cpu_slot'] == 3 - side, 'Actual physical slots')
    need(result['exit_code'] == 0 and result['assistance'] in ('stage16_combat_health_only', 'stage16_and_initial_cpu_health_each_round') and
         result['unassisted_clear_proven'] is False, 'Terminal explicitly assisted ending diagnostic, not a cleared tower')
    need(result['candidate'] == 'diagnostic_v680_native_pit_initial_cache' and result['executable_sha256'] == EXE and result['payload_sha256'] == PAYLOAD,
         'Actual unchanged matched candidate')
    if check_hashes:
        for name, sha in result['input_hashes'].items(): need(digest(Path(name)) == sha, 'Input changed: ' + name)
    source_path = folder / f'input_sources/mk2ks_current_ending_presentation_v680_v{version}.lua'
    source = source_path.read_text()
    writes = re.findall(r'\bp:write_\w+\([^\n]*?\)', source)
    expected = ['p:write_u16(0x01061b30,16)', 'p:write_u16(slots[opponent].hp,1)'] + (['p:write_u16(slots[side].hp,161)'] if v3 else [])
    need(writes == expected and not re.search(r'\bload\s*\(|\bdofile\s*\(', source), 'Only declared stage/combat-health assistance; no actor/ID/ending manipulation')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at', text, re.I), 'No runtime/observer errors')
    rows = parse(text); tags = lambda t: [r for r in rows if r['tag'] == t]
    need(all(r.get('observer_writes') == 0 and r.get('setup_assistance') == result['assistance'] and r.get('human_slot') == side and
             r.get('fighter') == result['player'] for r in rows), 'Every retained record declares actual diagnostic scope')
    stage, health, regen = (tags(t) for t in ('ENDING_FIXTURE_STAGE', 'ENDING_FIXTURE_HEALTH', 'ENDING_FIXTURE_REGEN'))
    starts, completed, finals = (tags(t) for t in ('ENDING_START', 'ENDING_COMPLETED', 'ENDING_FIXTURE_RESULT'))
    need(len(stage) == len(starts) == len(completed) == len(finals) == 1 and len(health) == 2, 'One stage fixture, two initial CPU-health fixtures, whole ending and terminal return')
    if not (len(stage) == len(starts) == len(completed) == len(finals) == 1 and len(health) == 2):
        return dict(passed=False, errors=errors, unassisted_clear_proven=False, fullPortAcceptance=False)
    stage, start, complete, final = stage[0], starts[0], completed[0], finals[0]
    need(stage['before'] == 0 and stage['after'] == 16 and stage['mode'] == 4 and stage['state'] == 4 and
         stage['own_roster'] == identity and stage['cpu_roster'] == 65535 and stage['field'] == 0x01061b30,
         'One fixture after true locked selection and before native boss construction')
    hp_fields = (0x010602f0, 0x01060ec0)
    for n, row in enumerate(health, 1):
        need(row['round'] == n and row['slot'] == 3 - side and row['field'] == hp_fields[2-side] and row['before'] == 161 and
             row['after'] == 1 and row['own_health'] == 161 and row['own_id'] == identity and row['cpu_id'] == 13 and
             stage['frame'] < row['frame'] < start['frame'], 'CPU-only initial full-health round fixture on true native Shao Kahn')
    for row in regen:
        need(v3 and row['slot'] == side and row['field'] == hp_fields[side-1] and 0 < row['before'] < 161 and row['after'] == 161 and
             row['cpu_health'] > 0 and row['mode'] == 2 and row['frame'] < start['frame'], 'Human health assistance confined to live combat, never presentation')
    live = tags('LIVE')
    need(bool(live) and all(r['stage'] == 16 and r['human'] == f'{identity}:{identity}' and r['cpu'] == '13:13' for r in live), 'True native human and Shao Kahn, no proxy')
    damage = [r for r in tags('HEALTH') if r['slot'] == 3-side and r['before'] == 1 and r['after'] == 0 and r['pc'] == 0xff836700]
    need(len(damage) == 2 and health[0]['frame'] < damage[0]['frame'] < health[1]['frame'] < damage[1]['frame'] < start['frame'],
         'Two actual native combat KO stores after fixtures, not direct death/winner writes')
    # Shao Kahn's final defeat enters its native destruction path rather than
    # reading the ordinary per-round winner announcement table a second time.
    wins = tags('WIN')
    need(len(wins) == 1 and wins[0]['slot'] == side and wins[0]['id'] == identity and wins[0]['pc'] == 0xff8296b0 and
         wins[0]['entry'] == 0xfffef800 + identity*32 and damage[0]['frame'] <= wins[0]['frame'] < health[1]['frame'],
         'Actual first-round native winner call before final boss destruction path')
    hps = tuple(map(int, start['health'].split(',')))
    need(start['stage'] == 16 and start['winner'] == side and start['roster'] == identity and start['actors'] == '00000000,00000000' and
         hps[side-1] > 0 and hps[2-side] == 0, 'Original actor retirement and owned winner into ending')
    fixtures = [stage] + health + regen
    need(final['stage_writes'] == 1 and final['cpu_health_writes'] == 2 and final['own_health_writes'] == len(regen) and
         final['last_fixture'] == max(r['frame'] for r in fixtures) < start['frame'] and final['ending_writes'] == 0,
         'All assistance ends before the actual ending/cinematic interval')
    need(digest(GUEST) == GUEST_SHA, 'Actual previously captured current guest program identity')
    original_guest = GUEST.read_bytes(); guest_word = lambda at: struct.unpack_from('<H', original_guest, (at-0xff800000)//8)[0]
    pictures, texts = tags('PICTURE'), tags('TEXT')
    need(len(pictures) == 2 and len(texts) == 6, 'Both own photo pages and all native text-table segments fetched')
    images = []
    control_errors, control_frames = stock_control(check_hashes)
    errors.extend(control_errors)
    for page in (1, 2):
        prs = [r for r in pictures if r['page'] == page]
        trs = [r for r in texts if r['page'] == page]
        entry = 0xff800000 + 0xf4900*8 + (50+(identity-17)*2+page-1)*32
        base = 0xff800000 + (0xf4a00 if page == 1 else 0xf4b00)*8 + identity*3*32
        need(len(prs) == 1 and len(trs) == 3 and {r['segment'] for r in trs} == {0,1,2}, 'Exactly one actual page and its three text records')
        if len(prs) != 1: continue
        photo = prs[0]
        need(photo['entry'] == entry and photo['value'] == guest_word(entry) and photo['mask'] == 0xffff and photo['pc'] == 0xff8447e0 and
             photo['roster'] == identity and start['frame'] < photo['frame'] < complete['frame'], 'Actual own native picture-table dispatch and chronology')
        for row in trs:
            at = base + row['segment']*32
            need(row['entry'] == at and row['value'] == guest_word(at) and row['mask'] == 0xffff and
                 row['roster'] == identity and row['frame'] == photo['frame'], 'Actual true-ID ending text pointer values and same native page')
        needle = photo_rgb(ORACLE / f'{result["player"]}_page_{page}.bin')
        # Bound the comparison to visible photograph pixels. These captures
        # have native frame/background overpaint on page1's top/right edge
        # and page2's top/left two columns. Do NOT call those hidden pixels
        # matched or claim this proves all native frame/layout fidelity.
        visible = needle[1:, :-1] if page == 1 else needle[1:, 2:]
        expected_position = [30, 42] if page == 1 else [58, 20]
        for late in ('', '_late'):
            filename = f'ending_page{page}{late}_{photo["frame"]}.png'
            path = folder / 'snap' / filename
            need(path.is_file(), 'Actual rendered page snapshot exists: ' + filename)
            if not path.is_file(): continue
            image = image_override[filename] if image_override and filename in image_override else np.asarray(Image.open(path).convert('RGB'))
            matches = locate_photo(image, visible)
            need(image.shape == (254, 400, 3) and matches == [expected_position], 'Every compared visible photo pixel matches original-derived record at retained layout: ' + filename)
            h,w=needle.shape[:2];yy,xx=np.indices((h,w))
            mask=(yy==0)|(xx==w-1) if page==1 else (yy==0)|(xx<2)
            x,y=(30,41) if page==1 else (56,19)
            need(page in control_frames and np.array_equal(image[y:y+h,x:x+w][mask],control_frames[page][y:y+h,x:x+w][mask]),
                 'Every frame-overpaint pixel matches actual original-character ending at same layout: '+filename)
            images.append(dict(file=filename, original_photo_pixels=int(needle.shape[0]*needle.shape[1]),
                               compared_visible_pixels=int(visible.shape[0]*visible.shape[1]),
                               frame_overpaint_pixels_not_compared_to_photo=int(needle.shape[0]*needle.shape[1]-visible.shape[0]*visible.shape[1]),
                               stock_frame_overpaint_pixels_compared=int(np.count_nonzero(mask)),
                               positions=matches, sha256=digest(path)))
    need(complete['pictures'] == '1,1' and complete['texts'] == '3,3' and complete['mode'] == 11 and complete['age'] == complete['frame']-start['frame'] > 1200 and
         tuple(map(int, complete['roster'].split(',')))[side-1] != identity, 'Native whole slideshow returns to attract with complete own pages')
    audio_info = None
    with wave.open(str(folder / 'audio.wav')) as audio:
        data = np.frombuffer(audio.readframes(audio.getnframes()), dtype='<i2')
        audio_info = dict(rate=audio.getframerate(), channels=audio.getnchannels(), frames=audio.getnframes(),
                          nonzero_samples=int(np.count_nonzero(data)), sha256=digest(folder/'audio.wav'),
                          audio_fidelity_accepted=False)
    need(audio_info['rate'] == 48000 and audio_info['channels'] == 2 and audio_info['nonzero_samples'] > 0, 'Actual nonempty audio capture, explicitly not exact audio fidelity')
    return dict(passed=not errors, errors=errors, player=result['player'], human_slot=side,
                assisted_setup=result['assistance'], human_health_restorations=len(regen), ending_start=start['frame'],
                ending_complete=complete['frame'], rendered_photos=images, audio=audio_info,
                text_visual_review_required=True, unassisted_clear_proven=False, fullPortAcceptance=False,
                scope='Visible own photo pixels and stock frame-overpaint/native page-text dispatch/return after explicit combat fixtures; not full layout, unassisted bosses, text pixel/audio fidelity or whole port')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('folder', type=Path); parser.add_argument('--output', type=Path)
    args = parser.parse_args(); report = verify(args.folder)
    if args.output:
        if args.output.exists(): raise ValueError('Do not overwrite evidence')
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2)); raise SystemExit(not report['passed'])
