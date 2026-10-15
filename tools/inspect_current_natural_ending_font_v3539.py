"""Read-only original native glyph/layout probe against saved natural endings."""
import json
import struct
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def off(address):
    return (address - 0xff800000) // 8


def glyph(program, graphics, char):
    descriptor = struct.unpack_from('<I', program, off(0xffa20790) + (ord(char) - 33) * 4)[0]
    width, height, xo, yo, source, command = struct.unpack_from('<4hIH', program, off(descriptor))
    assert (xo, yo, command) == (0, 0, 0x1000)
    bit = source - 0x04000000
    assert 0 <= bit and bit + width * height <= len(graphics) * 8
    pixels = np.array([(graphics[(bit + n) // 8] >> ((bit + n) % 8)) & 1
                       for n in range(width * height)], dtype=bool).reshape(height, width)
    return pixels, descriptor


def main():
    program = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    graphics = bytearray(0x400000)
    for lane, name in enumerate(('ug17', 'uj17', 'ug22', 'uj22')):
        raw = (ROOT / 'mk2' / f'l1_mortal_kombat_ii_game_rom_{name}.{name}').read_bytes()
        graphics[lane:lane + len(raw) * 4:4] = raw
    palette = struct.unpack_from('<64H', program, off(0xffafe5a0) + 2)
    def rgb(pen):
        color = palette[pen]
        return tuple((((color >> shift) & 31) << 3) | (((color >> shift) & 31) >> 2) for shift in (10, 5, 0))
    results = []
    for fighter, folder, frames, identity in (
        ('kano', 'audit_v3516_current_kano_natural_knife_retreat_campaign', (83157, 83942), 17),
        ('sonya', 'audit_v3490_current_sonya_natural_ring_retreat_campaign', (117194, 117980), 18)):
        guest = (ROOT / folder / 'guest_maincpu.bin').read_bytes()
        for page in (1, 2):
            image = np.asarray(Image.open(ROOT / folder / 'snap' / f'ending_page{page}_late_{frames[page - 1]}.png').convert('RGB'))
            face, shadow = np.zeros((254, 400), dtype=bool), np.zeros((254, 400), dtype=bool)
            strings = []
            for segment in range(3 if page == 1 else 2):
                table = (0xf4a00 if page == 1 else 0xf4b00) + (identity * 3 + segment) * 4
                pointer = struct.unpack_from('<I', guest, table)[0]
                header = struct.unpack_from('<6I', guest, off(pointer))
                font, spacing, xy, color, renderer, speed = header
                assert (font, spacing, color, renderer, speed) == (0xffa20790, 2, 0x0e0e0000, 0xffa29920, 0)
                x, y = xy & 65535, xy >> 16
                start_x = x
                text = guest[off(pointer) + 24:].split(bytes(1), 1)[0].decode('ascii')
                strings.append(dict(segment=segment, text=text, header=[hex(v) for v in header]))
                for char in text.replace('\\n', '\r'):
                    if char == '\r':
                        x, y = start_x, y + 16
                    elif char == ' ':
                        x += 6
                    else:
                        pixels, _ = glyph(program, graphics, char)
                        h, w = pixels.shape
                        face[y:y + h, x:x + w] |= pixels
                        shadow[y + 1:y + 1 + h, x + 1:x + 1 + w] |= pixels
                        x += w + spacing
            shadow &= ~face
            actual_face = np.all(image == rgb(14), axis=2)
            actual_shadow = np.all(image == rgb(15), axis=2)
            missing_face = int(np.count_nonzero(face & ~actual_face))
            missing_shadow = int(np.count_nonzero(shadow & ~actual_shadow))
            results.append(dict(fighter=fighter, page=page, facePen=rgb(14), shadowPen=rgb(15),
                                nativeFacePixels=int(np.count_nonzero(face)), nativeShadowPixels=int(np.count_nonzero(shadow)),
                                mismatchedFacePixels=missing_face, mismatchedShadowPixels=missing_shadow, scripts=strings))
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
