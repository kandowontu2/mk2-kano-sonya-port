"""Typed finisher image/composite data; never copy donor executable code.

Append missing fatality pixels after the accepted fighter/UI graphics prefix.
Existing frame addresses and all stock Wolf socket sizes remain unchanged.
This prepares assets, not finisher actions or runtime acceptance.
"""
import json
import struct
import import_character_art as art
import zipfile

HERE=art.HERE
p=art.parser
GROUPS={
    'kano_extract': [0xff9b24f0,0xff9b2550,0xff9b25b0,0xff9b2610,0xff9b2670,
                     0xff9b26d0,0xff9b2730,0xff9b2790,0xff9b2810,
                     0xff9b29b0,0xff9b2a30,0xff9b2ab0,0xff9b2b30,0xff9b2b70,0xff9b2bb0],
    'kano_skeleton': [0xff9b22d0,0xff9b2310,0xff9b2350,0xff9b23d0,0xff9b2430,0xff9b2490],
    'kano_burn_victim': [0xff9b2d10,0xff9b2db0,0xff9b2e50,0xff9b2ef0,0xff9b2f70,0xff9b2fb0],
    'kano_torn_victim': [0xff9b3110,0xff9b3190,0xff9b3210,0xff9b3290,0xff9b32f0,0xff9b3330],
    'sonya_burn': [0xff9b0ae0,0xff9b0b20,0xff9b0b60,0xff9b0ba0,0xff9b0be0,
                   0xff9b0c20,0xff9b0c60,0xff9b0ca0,0xff9b0ce0,0xff9b0d40,
                   0xff9b0da0,0xff9b0e00,0xff9b0e60,0xff9b0ec0,0xff9b0f20],
}

def main(emit_sockets=True,reuse_generated=False):
    out=HERE/'generated_finishers'
    assert not out.exists() or reuse_generated, 'Never silently replace an asset evidence set'
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        lo=z.read('mk321u54.bin');hi=z.read('mk321u63.bin')
        donor=bytearray(len(lo)*2);donor[::2]=lo;donor[1::2]=hi
        gfx=bytearray(0x1200000)
        for bank in range(5):
            for lane in range(4):
                chip=133-bank*4-lane
                raw=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
                base=bank*0x400000+lane
                gfx[base:base+len(raw)*4:4]=raw
    assert art.sha(donor)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    prefix=(HERE/'generated_ui_packed/fighter_and_ui_graphics.bin').read_bytes()
    packed=bytearray(prefix)
    poses={}
    for groups in GROUPS.values():
        for group in groups:
            frames=p.frame_group(donor,group,group,group+0x200)
            assert frames,hex(group)
            poses[group]=frames
    frames=sorted({frame for values in poses.values() for frame in values})
    palettes={};records=[];streams={};pins=[]
    for frame in frames:
        at=p.stock_file(frame)
        assert p.looks_like_frame(donor,at)
        width,height,x,y,sag,control=struct.unpack_from('<HHHHIH',donor,at)
        raw,bits=art.bitstream(gfx,sag,width,height,control)
        key=(bits,art.sha(raw))
        if key not in streams:
            streams[key]=len(packed);packed.extend(raw)
        offset=streams[key]
        assert packed[offset:offset+len(raw)]==raw
        tail=p.u32(donor,at+14)
        if 0xff800000<=tail<=0xffffffff and not tail&15:
            pat=p.stock_file(tail);count=p.u16(donor,pat)
            assert 1<=count<=256,(hex(frame),hex(tail),count)
            colors=struct.unpack_from(f'<{count}H',donor,pat+2)
            palettes[tail]=colors
            palette=f'ks_finish_palette_{tail:08x}'
        else:
            # Explicit body palettes only; never treat adjacent descriptor data
            # as a pointer or copy an opaque block into executable program space.
            palette='ks_sonya_primary_palette' if frame in {
                f for g in GROUPS['sonya_burn'] for f in poses[g]
            } else 'ks_kano_primary_palette'
        label=f'ks_finish_frame_{frame:08x}'
        records += [label,f'        .word {width},{height},{p.signed(x)},{p.signed(y)}',
                    f'        .long 0{(0xc00000+offset)*8:08x}h',
                    f'        .word {art.word(control)}',f'        .long {palette}']
        pins.append(dict(frame=hex(frame),bits=bits,sourceBitAddress=hex(sag),
                         packedByteOffset=offset,SHA256=art.sha(raw),palette=palette))
    assert len(packed)<=0x600000
    lines=['; Generated typed image/palette/composite DATA, not executable donor code.',
           '        .ref ks_kano_primary_palette,ks_sonya_primary_palette','        .data']
    for address,colors in sorted(palettes.items()):
        label=f'ks_finish_palette_{address:08x}'
        lines += [f'        .def {label}',label,f'        .word {len(colors)}']
        for i in range(0,len(colors),8):
            lines.append('        .word '+','.join(art.word(c) for c in colors[i:i+8]))
    lines += records
    for group,values in sorted(poses.items()):
        label=f'ks_finish_pose_{group:08x}'
        lines += [f'        .def {label}',label]
        lines += [f'        .long ks_finish_frame_{f:08x}' for f in values]
        lines.append('        .long 0')
    source=('\n'.join(lines)+'\n').encode()
    out.mkdir(exist_ok=reuse_generated)
    (out/'KSFART.ASM').write_bytes(source)
    (out/'fighter_ui_finish_graphics.bin').write_bytes(packed)
    region=packed+bytes(0x600000-len(packed));sockets={}
    reconstructed=bytearray(0x600000)
    for bank,size in [(0,0x100000),(1,0x80000)]:
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane
            raw=region[start:start+size*4:4]
            assert len(raw)==size
            if emit_sockets:
                (out/name).write_bytes(raw)
            sockets[name]=art.sha(raw)
            reconstructed[start:start+size*4:4]=raw
    assert reconstructed==region
    assert packed[:len(prefix)]==prefix
    # A bounded, known performer sequence ends at its first zero. The donor
    # dispatch span also contains adjacent composites and must not be copied whole.
    kiss=[0xff8402c0,0xff840340,0xff8403c0,0xff840440,0xff8404c0,0xff840540,
          0xff8405c0,0xff840640,0xff8406c0,0xff840740,0xff8407a0]
    at=p.stock_file(p.u32(donor,p.stock_file(p.SONYA_SPECIAL)+2*4))
    assert list(struct.unpack_from('<12I',donor,at))==kiss+[0]
    existing=(HERE/'generated_packed/SONYAART.ASM').read_text()
    script=['; Native Sonya kiss performer control DATA; timing belongs to its action.',
            '        .data','        .def ks_finish_sonya_kiss','ks_finish_sonya_kiss']
    refs=[]
    for group in kiss:
        label=f'ks_sonya_pose_{group:08x}'
        assert '.def '+label+'\n' in existing
        refs.append('        .ref '+label);script.append('        .long '+label)
    script.append('        .long 0');script[1:1]=refs
    control=('\n'.join(script)+'\n').encode()
    (out/'KSFANI.ASM').write_bytes(control)
    report=dict(inputProgramSHA256=art.sha(donor),sourceSHA256=art.sha(source),
                animationSourceSHA256=art.sha(control),compositePoses=len(poses),frameRecords=len(frames),
                palettes=len(palettes),groups={k:[hex(a) for a in v] for k,v in GROUPS.items()},
                originalGraphicsPrefixBytes=len(prefix),originalGraphicsPrefixSHA256=art.sha(prefix),
                appendedBytes=len(packed)-len(prefix),totalGraphicsBytes=len(packed),capacity=0x600000,
                compressedStreamsVerified=True,stockSocketRoundTripVerified=True,
                originalGraphicsPrefixPreserved=True,sockets=sockets,framePins=pins,
                finisherActionsImplemented=False,runtimeVerified=False,releaseReady=False)
    (out/'FINISHER_ASSETS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('framePins','sockets','groups')},indent=2))

if __name__=='__main__':main()
