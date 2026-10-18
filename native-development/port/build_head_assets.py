"""Emit native direct-image head loops and stock Wolf graphics sockets."""
import hashlib
import json
from pathlib import Path
import sys

PORT = Path(__file__).resolve().parent
OUT = PORT/'generated_heads'
sha = lambda b: hashlib.sha256(b).hexdigest().upper()

def main(mode_override=None,prefix_path=None,output=None,emit_sockets=True):
    global OUT
    assert mode_override in (None,'head','decap','drain')
    decap = '--decap' in sys.argv if mode_override is None else mode_override=='decap'
    drain = '--drain' in sys.argv if mode_override is None else mode_override=='drain'
    assert not (decap and drain)
    if not decap and not drain:
        OUT=PORT/'generated_heads'
    if decap:
        OUT = PORT/'generated_decap'
    if drain:
        OUT = PORT/'generated_drain'
    if output is not None:
        OUT=Path(output)
    assert not OUT.exists() or '--refresh-generated' in sys.argv
    mode='drain' if drain else ('decap' if decap else 'head')
    source = PORT/('assets/heads' if mode=='head' else 'assets/'+mode)
    manifest = json.loads((source/(mode.upper()+'_SOURCE.json')).read_text())
    assert manifest['format'] == 'MK2KS-'+mode.upper()+'-PALETTE-INDEX-PGM-1'
    previous='generated_decap/fighter_ui_finish_decap_graphics.bin' if drain else ('generated_heads/fighter_ui_finish_heads_graphics.bin' if decap else 'generated_backbreak/fighter_ui_finish_backbreak_graphics.bin')
    prefix=(Path(prefix_path) if prefix_path is not None else PORT/previous).read_bytes()
    packed = bytearray(prefix)
    lines = ['; Authored head image DATA, no imported executable words.',
             '        .include mainequ.asm',
             '        .ref ks_kano_primary_palette,ks_sonya_primary_palette', '        .data']
    records = {}
    for actor in ('kano', 'sonya'):
        records[actor] = []
        frames = manifest['actors'][actor]['frames']
        assert [f['phase'] for f in frames] == list(range(3 if drain else 7))
        for frame in frames:
            raw = (source/frame['file']).read_bytes()
            assert sha(raw) == frame['fileSHA256']
            words = ' '.join(line.split('#', 1)[0] for line in raw.decode('ascii').splitlines()).split()
            assert words[0] == 'P2'
            w, h, maximum = map(int, words[1:4])
            indices = bytes(map(int, words[4:]))
            assert (w, h, maximum) == (frame['width'], frame['height'], 63)
            assert len(indices) == w*h and max(indices) <= 63
            assert sha(indices) == frame['indexSHA256']
            payload = bytearray((w*h*6+7)//8)
            for i, value in enumerate(indices):
                bit = i*6
                at, shift = divmod(bit, 8)
                payload[at] |= value << shift & 255
                if shift > 2:
                    payload[at+1] |= value >> (8-shift)
            # Separate bitstream decoder must recover every palette index.
            accumulator = int.from_bytes(payload, 'little')
            decoded = bytes((accumulator >> (i*6)) & 63 for i in range(w*h))
            assert decoded == indices
            offset = len(packed)
            packed.extend(payload)
            kind='dr' if drain else ('dc' if decap else 'hd')
            name = f'ks_{kind}_{actor}_frame{frame["phase"]}'
            lines += [f'        .def {name}', name,
                      f'        .word {w},{h},{frame["xOffset"]},{frame["yOffset"]}',
                      f'        .long 0{(0xc00000+offset)*8:08x}h',
                      '        .word 06000h', f'        .long ks_{actor}_primary_palette']
            if decap or drain:
                pose = f'ks_{kind}_{actor}_pose{frame["phase"]}'
                lines += [f'        .def {pose}', pose, f'        .long {name},0']
            records[actor].append(dict(frame, packedByteOffset=offset, packedSHA256=sha(payload)))
        root = f'ks_{actor}_decapfall' if decap else f'ks_{actor}_head'
        if drain:root=f'ks_{actor}_drain_shrink'
        lines += [f'        .def {root}', root]
        if drain:
            for section in ((0,1,2),(1,0,1,2)):
                lines += [f'        .long ks_dr_{actor}_pose{i}' for i in section]
                lines += ['        .long 0']
        elif decap:
            for section in ((0,1,2),(3,2,3,2,3,2),(3,4,5,6)):
                lines += [f'        .long ks_dc_{actor}_pose{i}' for i in section]
                lines += ['        .long 0']
        else:
            lines += [f'        .long ks_hd_{actor}_frame{i}' for i in range(7)]
            lines += [f'        .long ani_jump,{root}']
    assert packed[:len(prefix)] == prefix and len(packed) < 0x600000
    OUT.mkdir(exist_ok=True)
    asmname='KSDRART.ASM' if drain else ('KSDCART.ASM' if decap else 'KSHDART.ASM')
    binname='fighter_ui_finish_drain_graphics.bin' if drain else ('fighter_ui_finish_decap_graphics.bin' if decap else 'fighter_ui_finish_heads_graphics.bin')
    (OUT/asmname).write_text('\n'.join(lines)+'\n')
    (OUT/binname).write_bytes(packed)
    region = packed+bytes(0x600000-len(packed))
    rebuilt = bytearray(0x600000)
    sockets = {}
    for bank, size in ((0, 0x100000), (1, 0x80000)):
        for lane in range(4):
            chip = 121-bank*4-lane
            name = f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start = bank*0x400000+lane
            payload = region[start:start+size*4:4]
            assert len(payload) == size
            if emit_sockets:
                (OUT/name).write_bytes(payload)
            rebuilt[start:start+size*4:4] = payload
            sockets[name] = sha(payload)
    assert rebuilt == region
    report = dict(records=records, prefixSHA256=sha(prefix), prefixBytes=len(prefix),
                  appendedBytes=len(packed)-len(prefix), totalGraphicsBytes=len(packed),
                  independentIndexDecodeVerified=True, stockSocketRoundTripVerified=True,
                  sockets=sockets, directImageDescriptorLoop=not (decap or drain),
                  visualAcceptance=False, runtimeVerified=False, fullPortVerified=False)
    (OUT/('DRAIN_DATA.json' if drain else ('DECAP_DATA.json' if decap else 'HEAD_DATA.json'))).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('records', 'sockets')}))

if __name__ == '__main__':
    main()
