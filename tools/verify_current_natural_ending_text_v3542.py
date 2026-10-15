"""Original-ROM native story glyph, spacing, punctuation and shadow gate.

Existing unassisted current3172 P1 ending captures only. Original native font
data and glyph pixels are the oracle, never screenshot-extracted letters.
Frame/background/other cinematics/audio/P2 remain separate acceptance gates.
"""
import json
import re
import struct
import subprocess
import hashlib
import zipfile
import zlib
from pathlib import Path

import numpy as np
from PIL import Image
import verify_current_natural_ending_photos_v3535 as photos

ROOT, need, sha = photos.ROOT, photos.need, photos.sha
OUT = ROOT / 'audit_v3543_current_natural_ending_text_checked'
ROM_SHA = '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
STORIES = (
    ("KANO SEES HIS CHANCE\\nTO PLUNDER OUTWORLD\\nAS SHAO KAHN FALLS.",
     "HE ENTERS THE RUINS\\nOF THE EMPEROR'S\\nABANDONED ARMORY.",
     "BUT KAHN'S DEFEAT\\nHAS FREED THE SOULS\\nHE HELD CAPTIVE.",
     "THE SPIRITS OF KANO'S VICTIMS\\nSURROUND HIM. THERE IS NO ESCAPE.\\n",
     "THE BLACK DRAGON'S DREAM OF AN EMPIRE\\nENDS AS THE SOULS CLAIM THEIR REVENGE.\\nKANO'S VICTORY HAS A TERRIBLE PRICE."),
    ("SONYA BREAKS FREE\\nAS SHAO KAHN'S EMPIRE\\nCOLLAPSES.",
     "SHE FINDS JAX ALIVE\\nBEHIND OUTWORLD'S\\nLAST OPEN GATE.",
     "THE SPECIAL FORCES\\nCLOSE THE PORTALS\\nBEFORE EARTH FALLS.",
     "BACK HOME, SONYA WARNS HER COMMANDERS\\nOF THE THREAT FROM OUTWORLD.\\n",
     "SONYA HELPS FORM AN AGENCY TO STUDY\\nOUTWORLD AND DEFEND EARTH. THE SPECIAL\\nFORCES WILL BE READY FOR ITS RETURN."),
)


def off(address):
    need(0xff800000 <= address < 0x100000000 and address % 8 == 0, 'Actual native ROM byte pointer')
    return (address - 0xff800000) // 8


def u32(program, address):
    return struct.unpack_from('<I', program, off(address))[0]


def source_contract(guest, original):
    spans = ((0xffa29600, 0xffa2b660), (0xffa2c540, 0xffa2c5a0),
             (0xffa2c8f0, 0xffa2cb30), (0xffa2ea20, 0xffa2eac0),
             (0xff809f10, 0xff809fa0), (0xff80a490, 0xff80a610))
    for lo, hi in spans:
        need(guest[off(lo):off(hi)] == original[off(lo):off(hi)],
             'Entire original native font/header/drawing/spacing/newline/shadow/offset code unchanged')
    need(guest[off(0xffafe5a0):off(0xffafe5a0) + 130] == original[off(0xffafe5a0):off(0xffafe5a0) + 130],
         'Whole original native text palette unchanged')
    return [dict(first=hex(lo), endExclusive=hex(hi), bytes=(hi - lo) // 8) for lo, hi in spans]


def glyph(program, graphics, char):
    table = 0xffa20790 + (ord(char) - 33) * 32
    descriptor = u32(program, table)
    width, height, xo, yo, source, command = struct.unpack_from('<4hIH', program, off(descriptor))
    need(command == 0x1000 and width > 0 and height > 0 and descriptor != 0xffc0b570,
         'Observed original one-bit glyph, no unmodeled special advance descriptor')
    bit = source - 0x04000000
    need(0 <= bit and bit + width * height <= len(graphics) * 8, 'Complete original native glyph source bits')
    pixels = np.array([(graphics[(bit + n) // 8] >> ((bit + n) % 8)) & 1
                       for n in range(width * height)], dtype=bool).reshape(height, width)
    return pixels, dict(character=char, table=hex(table), descriptor=hex(descriptor),
                        width=width, height=height, xOffset=xo, yOffset=yo, source=hex(source), command=hex(command))


def model(guest, original, graphics, identity, page):
    face, shadow = np.zeros((254, 400), dtype=bool), np.zeros((254, 400), dtype=bool)
    glyphs, scripts = {}, []
    # Original FFA2CA20 indexes table entry27h, the H descriptor, to derive
    # half-width space and height+half-height line advance. Never infer either
    # metric by trying positions against an image.
    metric_pointer = u32(original, 0xffa20790 + 0x27 * 32)
    metric_w, metric_h = struct.unpack_from('<2H', original, off(metric_pointer))
    space = metric_w // 2
    line = metric_h + metric_h // 2
    need((metric_w, metric_h, space, line) == (7, 11, 3, 16), 'Actual original H-based native text metrics')
    for segment in range(3):
        at = (0xf4a00 if page == 1 else 0xf4b00) + (identity * 3 + segment) * 4
        pointer = struct.unpack_from('<I', guest, at)[0]
        if page == 2 and segment == 2:
            need(pointer == 0, 'Original two-script page2 null third segment')
            continue
        header = struct.unpack_from('<6I', guest, off(pointer))
        stock_table = (0xff8f5550 if page == 1 else 0xff8f59d0) + (8 * 3 + segment) * 32
        stock_script = u32(original, stock_table)
        need(guest[off(pointer):off(pointer) + 24] == original[off(stock_script):off(stock_script) + 24],
             'Entire genuine stock ending font/style/position/renderer header preserved')
        font, spacing, xy, color, renderer, speed = header
        need((font, spacing, color, renderer, speed) == (0xffa20790, 2, 0x0e0e0000, 0xffa29920, 0),
             'Native original ending font/shader/shadow renderer and zero per-character sleep')
        text = guest[off(pointer) + 24:].split(bytes(1), 1)[0].decode('ascii')
        expected = STORIES[identity - 17][segment + (3 if page == 2 else 0)]
        need(text == expected, 'Complete own independent story script, no proxy/truncation/wrong wording')
        x, y = xy & 65535, xy >> 16
        start_x = x
        for char in text.replace('\\n', '\r'):
            if char == '\r':
                x, y = start_x, y + line
            elif char == ' ':
                x += space + spacing
            else:
                pixels, record = glyph(original, graphics, char)
                table, descriptor = int(record['table'], 16), int(record['descriptor'], 16)
                need(guest[off(table):off(table) + 4] == original[off(table):off(table) + 4] and
                     guest[off(descriptor):off(descriptor) + 14] == original[off(descriptor):off(descriptor) + 14],
                     'Every actual used native glyph table pointer and full descriptor unchanged')
                h, w = pixels.shape
                xx, yy = x - record['xOffset'], y - record['yOffset']
                need(0 <= xx and xx + w + 1 <= 400 and 0 <= yy and yy + h + 1 <= 254,
                     'Every original native glyph and its shadow fully inside actual viewport')
                face[yy:yy + h, xx:xx + w] |= pixels
                shadow[yy + 1:yy + 1 + h, xx + 1:xx + 1 + w] |= pixels
                glyphs[char] = record
                x += w + spacing
        scripts.append(dict(segment=segment, nativePointer=hex(pointer), preservedStockHeader=hex(stock_script),
                            startPosition=[xy & 65535, xy >> 16], story=text))
    shadow &= ~face  # Original black copy behind white faces, including overlap.
    palette = struct.unpack_from('<64H', original, off(0xffafe5a0) + 2)
    need(struct.unpack_from('<H', original, off(0xffafe5a0))[0] == 64, 'Original native sixteen-bit palette count')
    def rgb(pen):
        word = palette[pen]
        return tuple((((word >> s) & 31) << 3) | (((word >> s) & 31) >> 2) for s in (10, 5, 0))
    need(rgb(14) == (231, 231, 231) and rgb(15) == (0, 0, 0), 'Actual native white/black original text pens')
    domain = np.zeros_like(face)
    if page == 1:
        domain[13:241, 185:376] = True
    else:
        domain[163:244, 24:372] = True
    need(not np.any((face | shadow) & ~domain), 'Full own story including final line and shadow lies in the native panel interior')
    return dict(face=face, shadow=shadow, domain=domain, faceRGB=rgb(14), shadowRGB=rgb(15),
                scripts=scripts, glyphs=glyphs, nativeSpaceWidth=space + 2, nativeLineAdvance=line)


def pixel_gate(image, expected):
    need(image.shape == (254, 400, 3), 'Actual native 400x254 ending scanout')
    actual_face = np.all(image == expected['faceRGB'], axis=2)
    actual_shadow = np.all(image == expected['shadowRGB'], axis=2)
    need(np.all(actual_face[expected['face']]), 'Every original native glyph face pixel and color exact')
    need(np.all(actual_shadow[expected['shadow']]), 'Every original native one-pixel black shadow pixel exact')
    need(np.array_equal(actual_face[expected['domain']], expected['face'][expected['domain']]),
         'No extra original-white glyph face pixels anywhere in native text panel interior')
    return dict(exactGlyphFacePixels=int(np.count_nonzero(expected['face'])),
                exactBlackShadowPixels=int(np.count_nonzero(expected['shadow'])),
                extraWhiteGlyphSearchPixels=int(np.count_nonzero(expected['domain'])),
                panelBackgroundAllPixelsOrEveryExtraBlackPenAccepted=False)


def faults(image, expected):
    trials = []
    sy, sx = np.argwhere(expected['face'])[0]
    changed = image.copy(); changed[sy, sx, 0] ^= 1
    trials.append(('one_actual_native_letter_pixel_changed', changed,
                   'Every original native glyph face pixel and color exact'))
    sy, sx = np.argwhere(expected['shadow'])[0]
    changed = image.copy(); changed[sy, sx] = [33, 33, 33]
    trials.append(('one_actual_black_shadow_pixel_removed', changed,
                   'Every original native one-pixel black shadow pixel exact'))
    sy, sx = np.argwhere(expected['domain'] & ~expected['face'] & ~expected['shadow'])[0]
    changed = image.copy(); changed[sy, sx] = expected['faceRGB']
    trials.append(('extra_white_letter_pixel_in_panel', changed,
                   'No extra original-white glyph face pixels anywhere in native text panel interior'))
    changed = image.copy(); changed[expected['face']] = [239, 239, 239]
    trials.append(('wrong_original_native_text_palette', changed,
                   'Every original native glyph face pixel and color exact'))
    rejected = []
    for label, changed, invariant in trials:
        need(not np.array_equal(changed, image), 'Non-vacuous actual original-glyph pixel fault')
        try:
            pixel_gate(changed, expected)
        except ValueError as error:
            need(str(error) == invariant, 'Actual font fault rejected by intended invariant')
            rejected.append(dict(name=label, rejectedBy=str(error)))
        else:
            raise ValueError('Accepted actual native text fault: ' + label)
    pixel_gate(image, expected)
    return rejected


def main():
    need(not OUT.exists(), 'Immutable fresh native text proof')
    previous_path = photos.OUT / 'report.json'
    prior = json.loads(previous_path.read_text())
    need(prior['passed'] and prior['bothNaturalP1EndingVisiblePhotosAccepted'] and not prior['fullPortAcceptance'],
         'Accepted current native natural photo captures used, not a new assisted campaign')
    inherited = {str(Path(k).resolve()): v for k, v in prior['inputHashes'].items()}
    pins = {}
    def pin(path, wanted=None):
        key = str(Path(path).resolve())
        wanted = wanted or inherited.get(key)
        digest = sha(path)
        need(wanted is None or digest == wanted, 'Actual accepted source/capture byte unchanged: ' + key)
        pins[key] = digest
    pin(previous_path)
    original_path = ROOT / 'mk2/mk2-maincpu.bin'
    pin(original_path, ROM_SHA)
    original = original_path.read_bytes()
    driver_path = photos.CANDIDATE / 'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    build = json.loads((photos.CANDIDATE / 'build-info.json').read_text(encoding='utf-8-sig'))
    declared = {str(Path(k).resolve()): v for k, v in build['input_hashes'].items()}
    need(str(driver_path.resolve()) in declared, 'Actual compiled driver retained in build input bindings')
    pin(driver_path, declared[str(driver_path.resolve())])
    declaration = driver_path.read_text().split('ROM_START( mk2ks )', 1)[1].split('ROM_END', 1)[0]
    pattern = r'ROM_LOAD32_BYTE\(\s*"([^"]+)"\s*,\s*(0x[0-9a-f]+)\s*,\s*(0x[0-9a-f]+)\s*,\s*CRC\(([0-9a-f]+)\)\s*SHA1\(([0-9a-f]+)\)'
    graphics = bytearray(0x400000)
    archive = ROOT / 'roms/mk2.zip'; pin(archive)
    chips = []
    with zipfile.ZipFile(archive) as package:
        for filename, start, length, crc, digest in re.findall(pattern, declaration):
            start, length = int(start, 16), int(length, 16)
            if not 0x800000 <= start < 0xc00000:
                continue
            path = ROOT / 'mk2' / filename
            raw = path.read_bytes(); pin(path)
            need(len(raw) == length and zlib.crc32(raw) == int(crc, 16) and
                 hashlib.sha1(raw).hexdigest() == digest and package.read(filename) == raw,
                 'Every original native font bank chip matches actual MAME parent and declared CRC/SHA1')
            at = start - 0x800000
            graphics[at:at + length * 4:4] = raw
            chips.append(dict(file=str(path), regionLane=hex(start), SHA1=digest))
    need(len(chips) == 4, 'Complete original four-chip font graphics bank')
    pin(photos.CANDIDATE / 'mkport_candidate.exe', photos.EXE)
    pin(photos.CANDIDATE / 'roms/mk2ks/mk2ks.mdata', photos.PAYLOAD)
    cases = {}
    for fighter, (folder_name, _, identity) in photos.CASES.items():
        folder = ROOT / folder_name
        guest_path = folder / 'guest_maincpu.bin'; pin(guest_path, photos.GUEST)
        guest = guest_path.read_bytes()
        source = source_contract(guest, original)
        records = []
        for page in (1, 2):
            expected = model(guest, original, graphics, identity, page)
            captures = [s for s in prior['cases'][fighter]['snapshots'] if s['page'] == page]
            need(len(captures) == 2, 'Both actual early/late complete-story scanouts from natural campaign')
            for capture in captures:
                path = Path(capture['file']); pin(path)
                image = np.asarray(Image.open(path).convert('RGB'))
                result = pixel_gate(image, expected)
                records.append(dict(file=str(path), frame=capture['frame'], page=page, **result,
                    nativeScripts=expected['scripts'], sourceGlyphDescriptors=list(expected['glyphs'].values()),
                    nativeSpaceWidth=expected['nativeSpaceWidth'], nativeLineAdvance=expected['nativeLineAdvance'],
                    actualQualifiedPixelFaults=faults(image, expected), samePathOriginalPositiveAccepted=True))
        cases[fighter] = dict(actualIdentity=identity, physicalSlot=1, originalNativeCodeSpans=source, snapshots=records)
    for path in (Path(__file__), Path(photos.__file__), ROOT / 'tools/inspect_current_natural_ending_font_v3539.py',
                 ROOT / 'tools/inspect_current_natural_ending_font_v3540.py', ROOT / 'tools/inspect_current_natural_ending_font_v3541.py'):
        pin(path)
    report = dict(passed=True, candidate=photos.CANDIDATE.name, cases=cases,
        originalFontBankChips=chips, actualNaturalP1EarlyLateStoryScanouts=8,
        exactOriginalNativeGlyphFacePixels=sum(s['exactGlyphFacePixels'] for c in cases.values() for s in c['snapshots']),
        exactOriginalNativeBlackTextShadowPixels=sum(s['exactBlackShadowPixels'] for c in cases.values() for s in c['snapshots']),
        actualQualifiedTextPixelFaults=32, bothNaturalP1StoryGlyphSpacingPunctuationAndBlackShadowsAccepted=True,
        initialProbePunctuationOffsetAndSpaceWidthAssumptionsNotAccepted=True,
        allFrameBackgroundPixelsCinematicsAudioP2OrAllContextsAccepted=False,
        newRuntimeBuildROMRawAudioOrRecoveredOracleCopies=0, fullPortAcceptance=False,
        scope=__doc__, inputHashes=pins)
    OUT.mkdir(); path = OUT / 'report.json'
    path.write_text(json.dumps(report, indent=2) + '\n'); digest = sha(path)
    compressed = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(compressed.returncode == 0 and sha(path) == digest, 'Lossless compact native text evidence')
    print(json.dumps({k: v for k, v in report.items() if k not in ('cases', 'inputHashes', 'originalFontBankChips')}, indent=2))


if __name__ == '__main__':
    main()
