"""Independent native table/stream/descriptor/packed-pixel contract, v597.

This proves bounded asset integrity, not art quality, a whole campaign, or that
the actual native scene has executed. Caller supplies frozen input payloads.
"""
import hashlib
import struct

SOURCE_SHA = '82fe153fb56b46a6f9d42f493451ac3d59ad61713433714aca7704e2881f8951'
BASE = 0xFE800000
HEADER, END = 0x130000, 0x160000
TABLE, PIXELS, GFX = 0x130100, 0x134000, 0x1E80000
STOCK_TABLE_AT = (0xFF85E6B0 - 0xFF800000) // 8


def check(ok, message):
    if not ok:
        raise ValueError(message)


def u32(data, at):
    check(0 <= at <= len(data)-4, 'Out-of-range word')
    return struct.unpack_from('<I', data, at)[0]


def verify(payload, source, stock):
    check(len(payload) == len(source) == 0x200000, 'Payload size')
    check(hashlib.sha256(source).hexdigest() == SOURCE_SHA, 'Wrong base candidate')
    check(payload[:HEADER] == source[:HEADER] and payload[END:] == source[END:], 'Unrelated payload modified')
    check(payload[HEADER:HEADER+4] == b'KPT1', 'Missing dedicated Pit header')
    header = struct.unpack_from('<8I', payload, HEADER+4)
    check(header == (PIXELS, 128356, GFX, BASE+TABLE*8, BASE+0x130200*8,
                     BASE+0x130240*8, 19, 12), 'Header allocations/identities')
    check(payload[TABLE:TABLE+17*4] == stock[STOCK_TABLE_AT:STOCK_TABLE_AT+17*4], 'Original rows changed')
    groups, frames, allocated = [], [], []
    for fighter in range(2):
        sequence = 0x130200 + fighter * 0x40
        address = BASE+sequence*8
        check(u32(payload, TABLE+(17+fighter)*4) == address, 'Added identity aliases another stream')
        words = struct.unpack_from('<10I', payload, sequence)
        check(words[5:8] == (1, address, 0) and words[9] == 0, 'Native loop/phase separators')
        for phase in range(6):
            group = 0x130400 + (fighter*6+phase)*8
            frame = 0x130800 + (fighter*6+phase)*16
            check(words[phase if phase<5 else 8] == BASE+group*8, 'Wrong own phase composite')
            check(struct.unpack_from('<2I', payload, group) == (BASE+frame*8, 0), 'Unbounded/wrong composite')
            width, height, xo, yo, source_bits, command = struct.unpack_from('<4hIH', payload, frame)
            check(command == 0x6000, 'Not native full-copy 6bpp')
            check(40 <= width <= 160 and 80 <= height <= 145, 'Frame geometry outside cinematic scale')
            check(abs(xo)<=100 and abs(yo)<=10, 'Cinematic origin shifted')
            check(source_bits%8 == 0, 'Unaligned graphics source')
            graphics_at = source_bits//8
            byte_count = (width*height*6+7)//8
            check(GFX <= graphics_at and graphics_at+byte_count <= GFX+header[1], 'Graphics range overflow')
            packed_at = PIXELS + graphics_at-GFX
            raw = payload[packed_at:packed_at+byte_count]
            values = []
            for pixel in range(width*height):
                bit = pixel*6
                pair = int.from_bytes(raw[bit//8:bit//8+2], 'little')
                values.append((pair >> (bit%8)) & 63)
            check(0 in values and len(set(values)) >= 15, 'Transparent/costume pixels absent')
            check(sum(v != 0 for v in values) > width*height//4, 'Body mostly empty')
            groups.append(BASE+group*8);frames.append(BASE+frame*8)
            allocated.append((graphics_at, graphics_at+byte_count))
    check(len(set(groups)) == len(set(frames)) == 12, 'Cross-fighter proxy data')
    for previous, current in zip(allocated, allocated[1:]):
        check(previous[1] <= current[0], 'Overlapping image streams')
    return dict(passed=True, fighters=2, frames=12, pixel_bytes=header[1],
                scope='native_asset_integrity_not_cinematic_or_visual_acceptance', fullPortAcceptance=False)
