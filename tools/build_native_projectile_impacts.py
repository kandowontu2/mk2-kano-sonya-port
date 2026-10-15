"""Import complete MK3 knife/ring impact composites into unused payload space.

This upgrades an existing payload without rebuilding or changing its prior
assets. Native MKII animation/DMA render these groups; there is no host drawing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

import build_mk2ks_mk3 as animation
import upgrade_ksui_previews as decoder

BASE = 0xFE800000
HEADER, META_END = 0x1C1000, 0x1C4000
PALETTES = (0x1C1100, 0x1C1200)
SEQUENCES = (0x1C1300, 0x1C1340)
FRAMES, GROUPS = 0x1C1400, 0x1C1800
PIXELS, END = 0x1E6000, 0x200000
GFX_DEST, GFX_END = 0x1E50000, 0x2000000
SOURCE_GROUPS = {
    "kano": (0xFF82F100, 0xFF82F140, 0xFF82F180, 0xFF82F1C0, 0xFF82F200, 0xFF82F260),
    "sonya": (0xFF83E200, 0xFF83E240, 0xFF83E280, 0xFF83E340, 0xFF83E440, 0xFF83E520, 0xFF83E5C0),
}


def decode_indices(gfx: bytes, spec: tuple) -> bytearray:
    source, command, width, height, *_ = spec
    bits, cursor = (command >> 12) & 7, source
    if bits != 6 or width <= 0 or height <= 0:
        raise ValueError("unexpected impact component format")
    result = bytearray(width * height)
    for y in range(height):
        pre = post = 0
        if command & 0x80:
            skip = decoder.extract_bits(gfx, cursor, 255); cursor += 8
            pre = (skip & 15) << ((command >> 8) & 3)
            post = (skip >> 4) << ((command >> 10) & 3)
        for x in range(pre, max(pre, width - post)):
            value = decoder.extract_bits(gfx, cursor, 63); cursor += 6
            if x < width:
                result[y * width + x] = value
    return result


def pack_indices(indices: bytes) -> bytes:
    result = bytearray((len(indices) * 6 + 7) // 8)
    for pixel, value in enumerate(indices):
        bit = pixel * 6
        result[bit // 8] |= (value << (bit & 7)) & 255
        if bit & 7 > 2:
            result[bit // 8 + 1] |= value >> (8 - (bit & 7))
    return bytes(result)


def build(payload: bytearray, program: bytes, gfx_directory: Path) -> dict:
    if len(payload) != END or any(v != 255 for v in payload[HEADER:META_END]) or any(v != 255 for v in payload[PIXELS:END]):
        raise ValueError("native impact allocation occupied or absent")
    gfx = decoder.load_gfx(gfx_directory)
    original = bytes(payload)
    output = bytearray(payload)  # Commit only after every guard succeeds.
    frame_cursor, group_cursor, pixel_cursor = FRAMES, GROUPS, PIXELS
    converted, report, pointer_cells = {}, {}, []
    for fighter_index, fighter in enumerate(("kano", "sonya")):
        palette_source = 0xFFC96600 if fighter == "kano" else 0xFFC973C0
        at = animation.stock_file(palette_source)
        count = animation.u16(program, at)
        if count != (24 if fighter == "kano" else 5):
            raise ValueError("original projectile impact palette changed")
        palette = list(struct.unpack_from(f"<{count}H", program, at + 2))
        palette[0] = 0
        struct.pack_into("<H64H", output, PALETTES[fighter_index], 64, *(palette + [0] * (64 - count)))
        groups, components, used = [], [], set()
        for source_group in SOURCE_GROUPS[fighter]:
            frames = animation.frame_group(program, source_group, 0xFF800000, 0xFFFFFFFF)
            if not frames:
                raise ValueError("original impact composite missing")
            native_group = BASE + group_cursor * 8
            native_frames = []
            for frame in frames:
                if frame not in converted:
                    spec = decoder.component_spec(program, frame)
                    indices = decode_indices(gfx, spec)
                    if max(indices) >= count:
                        raise ValueError("impact pixel exceeds its original palette")
                    packed = pack_indices(indices)
                    if frame_cursor + 20 > GROUPS or pixel_cursor + len(packed) > END or GFX_DEST + pixel_cursor - PIXELS + len(packed) > GFX_END:
                        raise ValueError("native impact storage overflow")
                    w, h, xo, yo = spec[2:]
                    native = BASE + frame_cursor * 8
                    struct.pack_into("<4hIHI", output, frame_cursor, w, h, xo, yo,
                                     (GFX_DEST + pixel_cursor - PIXELS) * 8, 0x6000,
                                     BASE + PALETTES[fighter_index] * 8)
                    output[pixel_cursor:pixel_cursor + len(packed)] = packed
                    converted[frame] = native
                    components.append(dict(source=f"{frame:08x}", native=f"{native:08x}", width=w, height=h,
                                           x_offset=xo, y_offset=yo, pixel_sha256=hashlib.sha256(indices).hexdigest()))
                    used.update(indices)
                    frame_cursor += 20
                    pixel_cursor = (pixel_cursor + len(packed) + 3) & ~3
                native_frames.append(converted[frame])
            if group_cursor + (len(native_frames) + 1) * 4 > META_END:
                raise ValueError("native impact composite storage overflow")
            struct.pack_into(f"<{len(native_frames)+1}I", output, group_cursor, *native_frames, 0)
            group_cursor += (len(native_frames) + 1) * 4
            groups.append(dict(source=f"{source_group:08x}", native=f"{native_group:08x}", components=native_frames))
        sequence = BASE + SEQUENCES[fighter_index] * 8
        struct.pack_into(f"<{len(groups)+1}I", output, SEQUENCES[fighter_index],
                         *(int(g["native"], 16) for g in groups), 0)
        blocks = [animation.HYBRID_FILE_BASES[fighter]] + [b for name,b in animation.HYBRID_VARIANT_BASES.items() if name.startswith(fighter)]
        special_offset = animation.stock_file(animation.LIU_SPECIAL) - animation.stock_file(animation.LIU_MAIN)
        for block in blocks:
            cell = block + special_offset + 4  # special animation 1, impact only
            prior = animation.u32(output, cell)
            if not BASE + block * 8 <= prior < BASE + (block + 0x4000) * 8:
                raise ValueError("unexpected pre-existing impact dispatch")
            struct.pack_into("<I", output, cell, sequence)
            pointer_cells.append(cell)
        report[fighter] = dict(palette_colors=count, used_indices=sorted(used), groups=groups, components=components,
                               sequence=f"{sequence:08x}", pose_fields=4)
    struct.pack_into("<4sIIIIII", output, HEADER, b"KPI1", PIXELS, pixel_cursor-PIXELS, GFX_DEST,
                     BASE + SEQUENCES[0]*8, BASE + SEQUENCES[1]*8, len(converted))
    allowed = set(range(HEADER, META_END)) | set(range(PIXELS, END))
    allowed.update(at+j for at in pointer_cells for j in range(4))
    if any(before != after and i not in allowed for i,(before,after) in enumerate(zip(original,output))):
        raise ValueError("impact upgrade changed an unrelated payload byte")
    payload[:] = output
    report.update(pixel_bytes=pixel_cursor-PIXELS, component_count=len(converted), pointer_cells=pointer_cells,
                  payload_sha256=hashlib.sha256(payload).hexdigest())
    return report


if __name__ == "__main__":
    parser=argparse.ArgumentParser();parser.add_argument("source",type=Path);parser.add_argument("output",type=Path)
    args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    if args.output.exists():raise SystemExit("Refusing to overwrite payload")
    payload=bytearray(args.source.read_bytes());report=build(payload,(root/"mk3/mk3-maincpu.bin").read_bytes(),root/"mk3")
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(payload)
    args.output.with_suffix(".impact.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
