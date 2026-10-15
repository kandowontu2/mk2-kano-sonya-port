"""Preserve Kano's original blade-swipe trail as a separate MKII effect.

The body composites remain imported character art. Only the ten single-frame
trail objects are converted, with their own original palette and origin. The
runtime copies these descriptors into program ROM for MKII's single-frame
animation helper, whose pointer validator requires addresses >= FF800000.
"""
from __future__ import annotations

import struct
from pathlib import Path

import build_mk2ks_mk3 as animation
import upgrade_ksui_previews as decoder

BASE = 0xFE800000
HEADER = 0x1D0000
PALETTE = 0x1D0100
FRAMES = 0x1D0400
PIXELS = 0x1D4000
END = 0x1E0000
GFX_DEST = 0x1E08000
SOURCE_PALETTE = 0xFFC96600
GROUPS = tuple(0xFF830000 + index * 0x40 for index in range(10))
SOURCE_FRAMES = (0xFFB182D0, 0xFFB18360, 0xFFB183D0, 0xFFB18440,
                 0xFFB184B0, 0xFFB18520, 0xFFB18590, 0xFFB18600,
                 0xFFB18670, 0xFFB186E0)
BODY_GROUPS = tuple(0xFE82FC40 + index * 0x60 for index in range(10))
X_ADVANCES = (0, 8, 8, 8, 11, 11, 11, 0, 0, 0)
POSE_FIELDS = (2, 2, 2, 2, 2, 4, 4, 12, 4, 4)


def build(payload: bytearray, program: bytes, gfx_directory: Path) -> dict:
    if len(payload) < END or any(value != 0xFF for value in payload[HEADER:END]):
        raise ValueError("native blade payload allocation is occupied or absent")
    gfx = decoder.load_gfx(gfx_directory)
    palette_offset = animation.stock_file(SOURCE_PALETTE)
    count = animation.u16(program, palette_offset)
    if count != 24:
        raise ValueError("unexpected original blade palette")
    colors = list(struct.unpack_from(f"<{count}H", program, palette_offset + 2))
    colors[0] = 0  # MKII's explicit transparent pen, not a body-palette alias.
    colors += [0] * (64 - count)
    converted = bytearray(b"\xff" * (END - HEADER))
    struct.pack_into("<H64H", converted, PALETTE - HEADER, 64, *colors)
    pixel_cursor, records = PIXELS, []
    for index, (group, expected_frame) in enumerate(zip(GROUPS, SOURCE_FRAMES)):
        frame, terminator = struct.unpack_from("<II", program, animation.stock_file(group))
        if (frame, terminator) != (expected_frame, 0):
            raise ValueError(f"unexpected blade component group {group:08x}")
        source, command, width, height, xo, yo = decoder.component_spec(program, frame)
        bits, cursor = (command >> 12) & 7, source
        indices = bytearray(width * height)
        for y in range(height):
            pre = post = 0
            if command & 0x80:
                skip = decoder.extract_bits(gfx, cursor, 0xFF)
                cursor += 8
                pre = (skip & 15) << ((command >> 8) & 3)
                post = (skip >> 4) << ((command >> 10) & 3)
            for x in range(pre, max(pre, width - post)):
                value = decoder.extract_bits(gfx, cursor, (1 << bits) - 1)
                cursor += bits
                if value >= count:
                    raise ValueError("blade pixel exceeds its original palette")
                if x < width:
                    indices[y * width + x] = value
        packed = bytearray((len(indices) * 6 + 7) // 8)
        for pixel, value in enumerate(indices):
            bit = pixel * 6
            packed[bit // 8] |= (value << (bit & 7)) & 0xFF
            if (bit & 7) > 2:
                packed[bit // 8 + 1] |= value >> (8 - (bit & 7))
        if pixel_cursor + len(packed) > END:
            raise ValueError("native blade pixels exceed allocation")
        start = pixel_cursor - HEADER
        converted[start:start + len(packed)] = packed
        # Unlike the travelling knife, this is already relative to Kano's
        # origin. In particular, do not apply the knife's -100 X adjustment.
        frame_offset = FRAMES + index * 20
        struct.pack_into("<4hIHI", converted, frame_offset - HEADER,
                         width, height, xo, yo,
                         (GFX_DEST + pixel_cursor - PIXELS) * 8,
                         0x6000, BASE + PALETTE * 8)
        records.append(dict(source=f"{frame:08x}", group=f"{group:08x}",
                            descriptor_offset=frame_offset, width=width, height=height,
                            x_offset=xo, y_offset=yo, used_indices=sorted(set(indices))))
        pixel_cursor = (pixel_cursor + len(packed) + 3) & ~3
    struct.pack_into("<4sIIII", converted, 0, b"KBL1", PIXELS,
                     pixel_cursor - PIXELS, GFX_DEST, len(records))
    payload[HEADER:END] = converted
    return dict(frames=records, palette_colors=count, pixel_bytes=pixel_cursor - PIXELS,
                body_groups=[f"{value:08x}" for value in BODY_GROUPS],
                x_advances=X_ADVANCES, pose_fields=POSE_FIELDS)
