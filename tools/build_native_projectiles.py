"""Convert donor projectile frames to self-contained MKII DMA records.

No runtime drawing or global fighter palette is involved. The payload contains
ordinary full-copy 6-bpp pixels, 18-byte frames and native palette records.
"""
from __future__ import annotations

import struct
from pathlib import Path

HEADER = 0x1C0000
PALETTES = (0x1C0100, 0x1C0200)
FRAMES = 0x1C0400
PIXELS = 0x1C4000
GFX_DEST = 0x1E04000
BASE = 0xFE800000


def build(payload: bytearray, program: bytes, gfx_directory: Path) -> dict:
    # Imported here to keep the animation builder's module initialization acyclic.
    import build_mk2ks_mk3 as animation
    import upgrade_ksui_previews as decoder

    if any(value != 0xFF for value in payload[HEADER:]):
        raise ValueError("native projectile payload allocation is occupied")
    gfx = decoder.load_gfx(gfx_directory)
    frame_cursor, pixel_cursor = FRAMES, PIXELS
    replacements, report = {}, {}
    for fighter_index, fighter in enumerate(("kano", "sonya")):
        # Use a dedicated palette, never whichever fighter last occupied P1.
        # The first word is the count, followed by colors INCLUDING index zero.
        palette_source = 0xFFC96600 if fighter == "kano" else 0xFFC973C0
        palette_offset = animation.stock_file(palette_source)
        count = animation.u16(program, palette_offset)
        palette = list(struct.unpack_from(f"<{count}H", program, palette_offset + 2))
        palette[0] = 0
        palette += [0] * (64 - len(palette))
        struct.pack_into("<H64H", payload, PALETTES[fighter_index], 64, *palette)
        used_indices = set()
        records = []
        for group in animation.DONOR_SEQUENCE_GROUPS[fighter]["main", 55]:
            source_frame = animation.u32(program, animation.stock_file(group))
            if animation.u32(program, animation.stock_file(group) + 4) != 0:
                raise ValueError("travelling projectile must be a single component")
            source, command, width, height, xo, yo = decoder.component_spec(program, source_frame)
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
                    index = decoder.extract_bits(gfx, cursor, (1 << bits) - 1)
                    cursor += bits
                    if index >= 64:
                        raise ValueError("effect exceeds native 6-bpp palette")
                    if x < width:
                        indices[y * width + x] = index
                        used_indices.add(index)
            packed = bytearray((len(indices) * 6 + 7) // 8)
            for index, value in enumerate(indices):
                bit = index * 6
                packed[bit // 8] |= (value << (bit & 7)) & 0xFF
                if (bit & 7) > 2:
                    packed[bit // 8 + 1] |= value >> (8 - (bit & 7))
            if pixel_cursor + len(packed) > len(payload):
                raise ValueError("native projectile pixels exceed payload allocation")
            payload[pixel_cursor:pixel_cursor + len(packed)] = packed
            # MKII creates this object at the fighter origin. MK3's rotating
            # knife uses a separately positioned object. Preserve its rotation
            # pivot, then translate both axes to the MKII release hand; an X-only
            # translation draws the flight near the HUD instead of the hitbox.
            if fighter == "kano":
                xo -= 100
                yo -= 72
            struct.pack_into("<4hIHI", payload, frame_cursor, width, height, xo, yo,
                             (GFX_DEST + pixel_cursor - PIXELS) * 8, 0x6000,
                             BASE + PALETTES[fighter_index] * 8)
            replacements[animation.relocate_pointer(source_frame)] = BASE + frame_cursor * 8
            records.append({"source": f"{source_frame:08x}", "native": f"{BASE + frame_cursor * 8:08x}",
                            "width": width, "height": height, "x_offset": xo, "y_offset": yo})
            frame_cursor += 20
            pixel_cursor = (pixel_cursor + len(packed) + 3) & ~3
        report[fighter] = {"palette_colors": count, "used_indices": sorted(used_indices), "frames": records}

    changed = 0
    for block in (*animation.HYBRID_FILE_BASES.values(), *animation.HYBRID_VARIANT_BASES.values()):
        for offset in range(block, block + 0x4000 - 3, 4):
            value = animation.u32(payload, offset)
            if value in replacements:
                animation.put_u32(payload, offset, replacements[value])
                changed += 1
    struct.pack_into("<4sIII", payload, HEADER, b"KFX1", PIXELS, pixel_cursor - PIXELS, GFX_DEST)
    report.update(pointer_replacements=changed, pixel_bytes=pixel_cursor - PIXELS)
    return report
