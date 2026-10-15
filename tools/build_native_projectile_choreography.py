"""Transactional, character-owned release/startup/full-flight payload upgrade.

This is asset preparation, not proof of runtime choreography. The native action
must create Kano's child after three fields, hold all six intro poses for three
fields, then travel at eight pixels/field with ten one-field rotations. Sonya
creates her ring after the complete fifteen-field body release and immediately
travels, with four three-field poses. No stationary Sonya intro is invented.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

import build_mk2ks_mk3 as animation
import build_native_projectile_impacts as impact
import build_native_projectiles as flight
import upgrade_ksui_previews as decoder

BASE = animation.DONOR_TMS_BASE
HEADER, META_END = 0x1C2000, 0x1C4000
BODY_SEQUENCES = (0x1C2100, 0x1C2140)
CHILD_SEQUENCES = (0x1C2180, 0x1C21E0)
FRAMES, INTRO_GROUPS, FLIGHT_GROUPS = 0x1C2400, 0x1C2800, 0x1C2900
PIXELS, END = 0x1F4000, 0x200000
GFX_DEST, GFX_END = 0x1E60000, 0x2000000
SOURCE_SHA256 = 'c846a1a8a58fa8133d514a2ea831448d017b93fcb4d8cdb7b1b6908801c4d10c'
BODY_GROUPS = {
    'kano': (0xFF82F400, 0xFF82F460, 0xFF82F4C0, 0xFF82F520,
             0xFF82F580, 0xFF82F5E0, 0xFF82F640, 0xFF82F6A0),
    'sonya': (0xFF83DBE0, 0xFF83DC40, 0xFF83DCA0, 0xFF83DD00, 0xFF83DEC0),
}
INTRO_SOURCE_GROUPS = (0xFF82EC40, 0xFF82ECA0, 0xFF82ECE0,
                       0xFF82ED40, 0xFF82EDC0, 0xFF82EE20)
FLIGHT_SOURCE_GROUPS = {
    'kano': tuple(range(0xFF82EE80, 0xFF82F100, 0x40)),
    'sonya': tuple(range(0xFF83E100, 0xFF83E200, 0x40)),
}
TIMING = {
    'kano': dict(body_holds=[3]*7+[4], recovery_fields=24, child_spawn_age=3,
                 intro_holds=[3]*6, first_flight_age=22, flight_hold=1, speed=8,
                 intro_origin=[-100,-72], flight_origin=[-12,-40]),
    'sonya': dict(body_holds=[3]*5, recovery_fields=35, child_spawn_age=15,
                  intro_holds=[], first_flight_age=16, flight_hold=3, speed=8,
                  flight_origin=[0,0]),
}


def address(at: int) -> int:
    return BASE + at*8


def verify_body(payload: bytes, program: bytes, group: int) -> list[int]:
    """Require the existing complete donor body groups, not partial clones."""
    frames = animation.frame_group(program, group, 0xFF800000, 0xFFFFFFFF)
    if not frames:
        raise ValueError('original release body composite missing')
    at = animation.stock_file(group)
    native = [animation.relocate_pointer(f) for f in frames]
    if struct.unpack_from(f'<{len(frames)+1}I', payload, at) != (*native,0):
        raise ValueError('existing release body composite changed')
    for frame in frames:
        at = animation.stock_file(frame)
        expected = bytearray(program[at:at+18])
        struct.pack_into('<I', expected, 8, animation.u32(program,at+8)+animation.GFX_REBASE)
        struct.pack_into('<I', expected, 14, animation.relocate_pointer(animation.u32(program,at+14)))
        if payload[at:at+18] != expected:
            raise ValueError('existing release body frame changed')
    return native


def build(payload: bytearray, program: bytes, gfx_directory: Path) -> dict:
    if len(payload) != END:
        raise ValueError('wrong choreography payload size')
    if any(v != 255 for v in payload[HEADER:META_END]) or any(v != 255 for v in payload[PIXELS:END]):
        raise ValueError('native choreography allocation occupied')
    # Exact predecessor protects all of the accepted collision/impact assets.
    if hashlib.sha256(payload).hexdigest() != SOURCE_SHA256:
        raise ValueError('choreography predecessor changed')
    original, output = bytes(payload), bytearray(payload)
    gfx = decoder.load_gfx(gfx_directory)
    converted, components, intro_groups, pointer_cells = {}, [], [], []
    frame_cursor, group_cursor, pixel_cursor = FRAMES, INTRO_GROUPS, PIXELS
    for source_group in INTRO_SOURCE_GROUPS:
        frames = animation.frame_group(program,source_group,0xFF800000,0xFFFFFFFF)
        if not frames:
            raise ValueError('original knife intro composite missing')
        native_frames = []
        for frame in frames:
            if frame not in converted:
                spec = decoder.component_spec(program,frame)
                indices = impact.decode_indices(gfx,spec)
                if max(indices) >= 24:
                    raise ValueError('knife intro exceeds original palette')
                packed = impact.pack_indices(indices)
                if frame_cursor+20 > INTRO_GROUPS or pixel_cursor+len(packed) > END:
                    raise ValueError('choreography asset overflow')
                w,h,xo,yo = spec[2:]
                native = address(frame_cursor)
                # The same converter pivot as existing knife flight records;
                # creating the stationary child at (-100,-72) cancels it.
                struct.pack_into('<4hIHI',output,frame_cursor,w,h,xo-100,yo-72,
                                 (GFX_DEST+pixel_cursor-PIXELS)*8,0x6000,address(flight.PALETTES[0]))
                output[pixel_cursor:pixel_cursor+len(packed)] = packed
                converted[frame] = native
                components.append(dict(source=f'{frame:08x}',native=f'{native:08x}',width=w,height=h,
                                       x_offset=xo-100,y_offset=yo-72,
                                       pixel_sha256=hashlib.sha256(indices).hexdigest()))
                frame_cursor += 20
                pixel_cursor = (pixel_cursor+len(packed)+3)&~3
            native_frames.append(converted[frame])
        if group_cursor+(len(native_frames)+1)*4 > FLIGHT_GROUPS:
            raise ValueError('choreography intro group overflow')
        native_group = address(group_cursor)
        struct.pack_into(f'<{len(native_frames)+1}I',output,group_cursor,*native_frames,0)
        group_cursor += (len(native_frames)+1)*4
        intro_groups.append(dict(source=f'{source_group:08x}',native=f'{native_group:08x}',components=native_frames))

    report, group_cursor, flight_index = {}, FLIGHT_GROUPS, 0
    for index,fighter in enumerate(('kano','sonya')):
        body = []
        for source_group in BODY_GROUPS[fighter]:
            native_frames = verify_body(original,program,source_group)
            body.append(dict(source=f'{source_group:08x}',native=f'{animation.relocate_pointer(source_group):08x}',
                             components=native_frames))
        struct.pack_into(f'<{len(body)+1}I',output,BODY_SEQUENCES[index],
                         *(int(g['native'],16) for g in body),0)
        travelling = []
        for source_group in FLIGHT_SOURCE_GROUPS[fighter]:
            source_frames = animation.frame_group(program,source_group,0xFF800000,0xFFFFFFFF)
            if not source_frames or len(source_frames) != 1:
                raise ValueError('original travelling composite changed')
            frame_at = flight.FRAMES + 20*flight_index
            spec = decoder.component_spec(program,source_frames[0])
            w,h,xo,yo = spec[2:]
            expected_pivot = (xo-100,yo-72) if fighter == 'kano' else (xo,yo)
            nw,nh,nxo,nyo,pixels,cmd,palette = struct.unpack_from('<4hIHI',original,frame_at)
            if (nw,nh,nxo,nyo,cmd,palette) != (w,h,*expected_pivot,0x6000,address(flight.PALETTES[index])):
                raise ValueError('existing full travelling frame changed')
            expected_pixels = impact.pack_indices(impact.decode_indices(gfx,spec))
            pixel_at = flight.PIXELS+(pixels//8-flight.GFX_DEST)
            flight_end = flight.PIXELS+animation.u32(original,flight.HEADER+8)
            if pixels&7 or not flight.PIXELS <= pixel_at < flight_end or pixel_at+len(expected_pixels) > flight_end or original[pixel_at:pixel_at+len(expected_pixels)] != expected_pixels:
                raise ValueError('existing travelling pixels changed')
            native = address(frame_at)
            struct.pack_into('<II',output,group_cursor,native,0)
            travelling.append(dict(source=f'{source_group:08x}',native=f'{address(group_cursor):08x}',components=[native]))
            group_cursor += 8
            flight_index += 1
        # Sonya's one-pose bootstrap exists only for the native object allocator.
        # Its custom task must skip it immediately; it is not a held intro.
        intro = intro_groups if fighter == 'kano' else []
        bootstrap = [int(g['native'],16) for g in intro] or [int(travelling[0]['native'],16)]
        flight_at = CHILD_SEQUENCES[index]+4*(len(bootstrap)+1)
        words = [*bootstrap,0,*(int(g['native'],16) for g in travelling),1,address(flight_at),0]
        sequence_end = CHILD_SEQUENCES[index]+4*len(words)
        if sequence_end > (CHILD_SEQUENCES[index+1] if index == 0 else FRAMES):
            raise ValueError('choreography sequence overflow')
        struct.pack_into(f'<{len(words)}I',output,CHILD_SEQUENCES[index],*words)
        blocks = [animation.HYBRID_FILE_BASES[fighter]]+[b for n,b in animation.HYBRID_VARIANT_BASES.items() if n.startswith(fighter)]
        for block in blocks:
            for slot,target in ((38,BODY_SEQUENCES[index]),(39,CHILD_SEQUENCES[index])):
                cell = block+slot*4
                prior = animation.u32(original,cell)
                if not address(block) <= prior < address(block+0x4000):
                    raise ValueError('unexpected prior own projectile dispatch')
                struct.pack_into('<I',output,cell,address(target))
                pointer_cells.append(cell)
        report[fighter] = dict(body=body,intro=intro,flight=travelling,timing=TIMING[fighter],
                               body_sequence=f'{address(BODY_SEQUENCES[index]):08x}',
                               child_sequence=f'{address(CHILD_SEQUENCES[index]):08x}',
                               flight_sequence=f'{address(flight_at):08x}',bootstrap_is_held=False)
    if len(converted) != 12 or flight_index != 14 or group_cursor > META_END:
        raise ValueError('incomplete original choreography assets')
    struct.pack_into('<4s9I',output,HEADER,b'KPJ1',PIXELS,pixel_cursor-PIXELS,GFX_DEST,
                     address(BODY_SEQUENCES[0]),address(BODY_SEQUENCES[1]),
                     address(CHILD_SEQUENCES[0]),address(CHILD_SEQUENCES[1]),len(converted),flight_index)
    if GFX_DEST+pixel_cursor-PIXELS > GFX_END:
        raise ValueError('choreography graphics overflow')
    allowed = set(range(HEADER,META_END))|set(range(PIXELS,END))
    allowed.update(cell+j for cell in pointer_cells for j in range(4))
    if any(a != b and i not in allowed for i,(a,b) in enumerate(zip(original,output))):
        raise ValueError('choreography upgrade changed unrelated payload bytes')
    payload[:] = output
    report.update(scope='assets_only_native_runtime_not_yet_verified',component_count=len(converted),
                  intro_components=components,pixel_bytes=pixel_cursor-PIXELS,pointer_cells=pointer_cells,
                  source_sha256=hashlib.sha256(original).hexdigest(),payload_sha256=hashlib.sha256(output).hexdigest())
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser();parser.add_argument('source',type=Path);parser.add_argument('output',type=Path)
    args = parser.parse_args();root = Path(__file__).resolve().parents[1]
    if args.output.exists() or args.output.with_suffix('.choreography.json').exists():
        raise SystemExit('Refusing to overwrite payload or evidence')
    payload = bytearray(args.source.read_bytes())
    report = build(payload,(root/'mk3/mk3-maincpu.bin').read_bytes(),root/'mk3')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(payload)
    args.output.with_suffix('.choreography.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
