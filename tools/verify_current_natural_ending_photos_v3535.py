"""Current3172 natural P1 endings: original-ROM visible photo pixel gate.

Use the already accepted natural campaign captures, never rerun combat or
recreate retired photo-oracle/audio folders. Decode original donor graphics
in memory. Frame overpaint, font pixels, cinematics and audio remain separate
gates; an exact visible photograph is not full ending/port acceptance.
"""
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
import build_native_ending_reference as original
import decode_native_picture as decoder
import upgrade_ksui_previews as graphics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_v3536_current_natural_ending_photos_checked'
CANDIDATE = ROOT / 'diagnostic_v3172_native_morph_shadow'
EXE = '1835D8E05A25E193D0934560115A8C77B2F15C92B8BA3FF1BA06AA0C7D59BD24'
PAYLOAD = 'ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3'
GUEST = '65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7'
CASES = {
    'kano': ('audit_v3516_current_kano_natural_knife_retreat_campaign',
             'audit_v3521_current_kano_knife_campaign_checked/report.json', 17),
    'sonya': ('audit_v3490_current_sonya_natural_ring_retreat_campaign',
              'audit_v3494_current_sonya_ring_campaign_checked/report.json', 18),
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def rows(log, tag):
    prefix = 'MK2_NAT_CAMPAIGN_' + tag + ' '
    return [dict(re.findall(r'(\w+)=([^\s]+)', line))
            for line in log.splitlines() if line.startswith(prefix)]


def rgb_record(data):
    width, height, frames, count = struct.unpack_from('<4H', data)
    need(frames == 1 and count == 256 and len(data) == 520 + width * height,
         'Complete original-derived photo record, including full palette')
    palette = np.frombuffer(data, dtype='<u2', count=count, offset=8)
    rgb5 = np.stack(((palette >> 10) & 31, (palette >> 5) & 31, palette & 31), axis=1)
    rgb = ((rgb5 << 3) | (rgb5 >> 2)).astype(np.uint8)
    return rgb[np.frombuffer(data, dtype=np.uint8, offset=520).reshape(height, width)]


def photo_gate(image, photo, page):
    # Preserve the previously established native visible crop. Do not call
    # the original frame's overpaint pixels matched to photo artwork.
    visible = photo[1:, :-1] if page == 1 else photo[1:, 2:]
    x, y = (30, 42) if page == 1 else (58, 20)
    need(image.shape == (254, 400, 3), 'Actual native 400x254 scanout')
    height, width = visible.shape[:2]
    need(np.array_equal(image[y:y + height, x:x + width], visible),
         'Every visible original-ROM photo pixel exact at native page position')
    return dict(position=[x, y], visiblePhotoPixels=width * height,
                originalPhotoPixels=int(photo.shape[0] * photo.shape[1]),
                overpaintPixelsExcluded=int(photo.shape[0] * photo.shape[1] - width * height))


def qualified_faults(image, photo, other, page):
    x, y = (30, 42) if page == 1 else (58, 20)
    trials = []
    changed = image.copy()
    changed[y + 17, x + 19, 0] ^= 1
    trials.append(('one_actual_visible_photo_pixel_changed', changed, photo))
    changed = image.copy()
    visible = photo[1:, :-1] if page == 1 else photo[1:, 2:]
    h, w = visible.shape[:2]
    changed[y:y + h, x:x + w] = np.roll(visible, 1, axis=1)
    trials.append(('actual_photo_shifted_one_pixel', changed, photo))
    trials.append(('other_fighters_original_photo', image, other))
    reversed_photo = photo[::-1].copy()
    trials.append(('original_photo_row_direction_reversed', image, reversed_photo))
    rejected = []
    for label, actual, expected in trials:
        need(not np.array_equal(actual, image) or not np.array_equal(expected, photo),
             'Non-vacuous original-photograph fault')
        try:
            photo_gate(actual, expected, page)
        except ValueError as error:
            need(str(error) == 'Every visible original-ROM photo pixel exact at native page position',
                 'Photo fault rejected by intended pixel invariant')
            rejected.append(dict(name=label, rejectedBy=str(error)))
        else:
            raise ValueError('Accepted actual photo fault: ' + label)
    photo_gate(image, photo, page)
    return rejected


def main():
    need(not OUT.exists(), 'Immutable fresh ending evidence')
    pins = {}
    proofs = {}
    def pin(path, expected=None):
        key = str(Path(path).resolve())
        actual = sha(path)
        need(expected is None or actual == expected, 'Existing accepted input unchanged: ' + key)
        need(key not in pins or pins[key] == actual, 'Consistent actual byte pin')
        pins[key] = actual

    for fighter, (folder_name, proof_name, identity) in CASES.items():
        path = ROOT / proof_name
        proof = json.loads(path.read_text())
        need(proof['passed'] and proof['unassisted_clear_proven'] and
             proof['current3172WholeGuestAndCampaignAccepted'] and proof['player'] == fighter and
             proof['human_slot'] == 1 and not proof['fullPortAcceptance'],
             'Previously accepted current true-character natural P1 clear')
        proofs[fighter] = {str(Path(k).resolve()): v for k, v in proof['inputHashes'].items()}
        pin(path)
    def accepted(path, fighter):
        key = str(Path(path).resolve())
        need(key in proofs[fighter], 'Actual file was pinned by whole campaign verifier: ' + key)
        pin(path, proofs[fighter][key])

    pin(CANDIDATE / 'mkport_candidate.exe', EXE)
    pin(CANDIDATE / 'roms/mk2ks/mk2ks.mdata', PAYLOAD)
    machine = CANDIDATE / 'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
    accepted(machine, 'kano')
    accepted(machine, 'sonya')
    source = machine.read_text()
    need('0x0c00000 + (fighter ? 0x1000000 : 0x103599a)' in source and
         'constexpr unsigned scene_width = 238, scene_left = 21;' in source and
         'unsigned const source_x = (fighter ? 4 : 149) + x * 94 / width;' in source,
         'Actual compiled native photo source/crop/contain layout, not canonical restored source')
    rom_dir = ROOT / 'roms/mk2ks'
    for _, chips in graphics.GFX_BANKS:
        for chip in chips:
            path = rom_dir / f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            accepted(path, 'kano')
            accepted(path, 'sonya')
    gfx = graphics.load_gfx(rom_dir)
    photos = {}
    for fi, fighter in enumerate(CASES):
        for page in (1, 2):
            record, _, provenance = original.reference(gfx, fi, page - 1)
            photos[fighter, page] = (rgb_record(record), provenance,
                                      hashlib.sha256(record).hexdigest().upper())

    cases = {}
    for fighter, (folder_name, _, identity) in CASES.items():
        folder = ROOT / folder_name
        for relative in ('run.log', 'result.json', 'guest_maincpu.bin'):
            accepted(folder / relative, fighter)
        need(sha(folder / 'guest_maincpu.bin') == GUEST, 'Current whole guest, no masked photo-only projection')
        guest = (folder / 'guest_maincpu.bin').read_bytes()
        log = (folder / 'run.log').read_text(encoding='utf-8-sig')
        starts, ends = rows(log, 'ENDING_START'), rows(log, 'ENDING_COMPLETED')
        pictures, texts, snaps = rows(log, 'PICTURE'), rows(log, 'TEXT'), rows(log, 'PAGE_SNAP')
        need(len(starts) == len(ends) == 1 and len(pictures) == 2 and len(texts) == 6 and len(snaps) == 4,
             'One actual natural ending, two complete photo/text pages, four scheduled scanouts')
        need(starts[0]['roster'] == str(identity) and starts[0]['winner'] == '1' and
             ends[0]['pictures'] == '1,1' and ends[0]['texts'] == '3,3', 'Own native ending route')
        sampled = []
        for page in (1, 2):
            photo_rows = [r for r in pictures if r['page'] == str(page)]
            need(len(photo_rows) == 1, 'Exactly one actual original native photo dispatch')
            dispatch = photo_rows[0]
            frame = int(dispatch['frame'])
            index = 50 + (identity - 17) * 2 + page - 1
            entry = 0xff800000 + (0xf4900 + index * 4) * 8
            pointer = struct.unpack_from('<I', guest, 0xf4900 + index * 4)[0]
            need(int(dispatch['entry'], 16) == entry and int(dispatch['value'], 16) == pointer & 0xffff and
                 dispatch['pc'] == 'FF8447E0' and dispatch['mask'] == 'FFFF' and
                 dispatch['roster'] == str(identity) and int(starts[0]['frame']) < frame < int(ends[0]['frame']),
                 'Actual own guest pointer dispatched by original native renderer in chronology')
            story = [r for r in texts if r['page'] == str(page)]
            need(len(story) == 3 and {r['segment'] for r in story} == {'0', '1', '2'}, 'Three original own text table reads')
            for row in story:
                offset = (0xf4a00 if page == 1 else 0xf4b00) + (identity * 3 + int(row['segment'])) * 4
                need(int(row['entry'], 16) == 0xff800000 + offset * 8 and
                     int(row['value'], 16) == struct.unpack_from('<H', guest, offset)[0] and
                     row['frame'] == dispatch['frame'] and row['roster'] == str(identity),
                     'Own native guest story table dispatch, not text pixel acceptance')
            photo, provenance, record_sha = photos[fighter, page]
            other = photos['sonya' if fighter == 'kano' else 'kano', page][0]
            for late, age in (('', 60), ('_late', 180)):
                filename = f'ending_page{page}{late}_{frame}.png'
                events = [r for r in snaps if r['file'] == filename]
                need(len(events) == 1 and int(events[0]['frame']) == frame + age,
                     'Actual native early/late snapshot chronology')
                path = folder / 'snap' / filename
                accepted(path, fighter)
                image = np.asarray(Image.open(path).convert('RGB'))
                result = photo_gate(image, photo, page)
                faults = qualified_faults(image, photo, other, page)
                sampled.append(dict(file=str(path), frame=frame + age, page=page,
                    **result, originalSource=provenance, inMemoryOriginalRecordSHA256=record_sha,
                    actualQualifiedPhotoFaults=faults, samePathOriginalPositiveAccepted=True))
        cases[fighter] = dict(actualNaturalEndingStart=int(starts[0]['frame']),
            actualNaturalEndingComplete=int(ends[0]['frame']), ownID=identity, physicalSlot=1, snapshots=sampled)

    for module in (original, decoder, graphics):
        pin(module.__file__)
    pin(__file__)
    report = dict(passed=True, candidate=CANDIDATE.name, cases=cases,
        actualNativeP1EndingScanouts=8,
        exactVisibleOriginalROMPhotoPixels=sum(s['visiblePhotoPixels'] for c in cases.values() for s in c['snapshots']),
        actualQualifiedPhotoFaults=32, bothNaturalP1EndingVisiblePhotosAccepted=True,
        frameOverpaintAllTextPixelsCinematicsAudioOrAllContextsAccepted=False,
        newRuntimeBuildROMRawAudioOrPhotoOracleCopies=0, fullPortAcceptance=False,
        scope='Both existing current3172 natural true-ID P1 ending pages, early/late original-ROM visible photo pixels at native positions and own native guest table/snapshot chronology. Not frame-overpaint/font pixels/audio/P2/all cinematics or full port.',
        inputHashes=pins)
    OUT.mkdir()
    path = OUT / 'report.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    digest = sha(path)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(path) == digest, 'Lossless compact evidence')
    print(json.dumps({k: v for k, v in report.items() if k not in ('inputHashes', 'cases')}, indent=2))


if __name__ == '__main__':
    main()
