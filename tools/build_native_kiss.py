"""Convert the observed MK3 Sonya fatality orb into native MKII effect data.

The original fire orb is a single-frame object with pose zero, not one of the
victim burn groups. Its seven descriptor changes were observed in
diagnostic_v122_mk3_sonya_orb_frames. This builder only imports assets;
runtime travel, impact and cleanup belong to the native finish action.
"""
from __future__ import annotations

import struct
from pathlib import Path

import build_mk2ks_mk3 as animation
import upgrade_ksui_previews as decoder

BASE = 0xFE800000
HEADER = 0x1E0000
PALETTE = 0x1E0100
FRAMES = 0x1E0400
FRAME_STRIDE = 0x20
PIXELS = 0x1E4000
END = 0x200000
GFX_DEST = 0x1E0C000
SOURCE_PALETTE_COUNT = 0x9990C
SOURCE_FRAMES = (
    0xFFB263F0, 0xFFB26460, 0xFFB264D0, 0xFFB26540,
    0xFFB265B0, 0xFFB26620, 0xFFB26690,
)


def build(payload: bytearray, program: bytes, gfx_directory: Path,
          *, include_arc_frame: bool = False) -> dict:
    if len(payload) != END or any(value != 0xFF for value in payload[HEADER:END]):
        raise ValueError("native kiss payload allocation is occupied or absent")
    if animation.u16(program, SOURCE_PALETTE_COUNT) != 31:
        raise ValueError("original kiss palette count changed")
    colors = list(struct.unpack_from("<32H", program, SOURCE_PALETTE_COUNT + 2))
    if colors[:4] != [0x0007, 0x7FFF, 0x7FFB, 0x7FF8]:
        raise ValueError("original kiss palette colors changed")
    colors[0] = 0  # Transparent MKII pen; the donor's index zero is not drawn.
    converted = bytearray(b"\xff" * (END - HEADER))
    struct.pack_into("<H64H", converted, PALETTE - HEADER, 64,
                     *(colors + [0] * 32))
    gfx = decoder.load_gfx(gfx_directory)
    pixel_cursor, records, used_indices = PIXELS, [], set()
    # The initial seven-frame capture missed the final ascent frame because
    # that old diagnostic did not advance the animation normally. A genuine
    # human-input trace shows FFB26700 before the 16-field homing return.
    frames = SOURCE_FRAMES + ((0xFFB26700,) if include_arc_frame else ())
    for index, frame in enumerate(frames):
        source, command, width, height, xo, yo = decoder.component_spec(program, frame)
        bits, cursor = (command >> 12) & 7, source
        if bits != 5 or not (command & 0x80):
            raise ValueError(f"unexpected original kiss frame format {frame:08X}")
        indices = bytearray(width * height)
        for y in range(height):
            skip = decoder.extract_bits(gfx, cursor, 0xFF)
            cursor += 8
            pre = (skip & 15) << ((command >> 8) & 3)
            post = (skip >> 4) << ((command >> 10) & 3)
            for x in range(pre, max(pre, width - post)):
                value = decoder.extract_bits(gfx, cursor, 31)
                cursor += 5
                if x < width:
                    indices[y * width + x] = value
                    used_indices.add(value)
        packed = bytearray((len(indices) * 6 + 7) // 8)
        for pixel, value in enumerate(indices):
            bit = pixel * 6
            packed[bit // 8] |= (value << (bit & 7)) & 0xFF
            if (bit & 7) > 2:
                packed[bit // 8 + 1] |= value >> (8 - (bit & 7))
        if pixel_cursor + len(packed) > END:
            raise ValueError("native kiss pixels exceed payload allocation")
        start = pixel_cursor - HEADER
        converted[start:start + len(packed)] = packed
        descriptor = FRAMES + index * FRAME_STRIDE
        struct.pack_into("<4hIHI", converted, descriptor - HEADER,
                         width, height, xo, yo,
                         (GFX_DEST + pixel_cursor - PIXELS) * 8,
                         0x6000, BASE + PALETTE * 8)
        records.append(dict(source=f"{frame:08x}",
                            descriptor=f"{BASE + descriptor * 8:08x}",
                            width=width, height=height, x_offset=xo,
                            y_offset=yo))
        pixel_cursor = (pixel_cursor + len(packed) + 3) & ~3
    struct.pack_into("<4sIIII", converted, 0, b"KKS2", PIXELS,
                     pixel_cursor - PIXELS, GFX_DEST, len(frames))
    payload[HEADER:END] = converted
    return dict(frames=records, palette_colors=32,
                used_indices=sorted(used_indices),
                pixel_bytes=pixel_cursor - PIXELS)
