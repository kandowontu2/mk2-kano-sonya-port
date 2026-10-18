"""Character-owned Friendship art as named native DATA; no donor action code."""
import json
import struct
import zipfile
import import_character_art as art

HERE=art.HERE
p=art.parser
KANO=[0xff9d1c30,0xff9d1c90,0xff9d1d10,0xff9d1d90,0xff9d1e10,0xff9d1e90,
      0xff9d1f10,0xff9d1f90,0xff9d2010,0xff9d20b0,0xff9d2150,0xff9d21f0,
      0xff9d2290,0xff9d2330,0xff9d23d0,0xff9d2470,0xff9d2510,0xff9d2590]
BUBBLE=[0xff9d2610,0xff9d2650,0xff9d2690,0xff9d26d0,0xff9d2710,0xff9d2750,0xff9d2790]
SONYA=[0xff9d2b90,0xff9d2bf0,0xff9d2c70,0xff9d2d10,0xff9d2db0,0xff9d2e50,
       0xff9d2ef0,0xff9d2f70,0xff9d2ff0,0xff9d3070,0xff9d30f0]

def main(emit_sockets=True,reuse_generated=False):
    out=HERE/'generated_friendship'
    assert not out.exists() or reuse_generated
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        donor=bytearray(1048576);donor[::2]=z.read('mk321u54.bin');donor[1::2]=z.read('mk321u63.bin')
        gfx=bytearray(0x1200000)
        for bank in range(5):
            for lane in range(4):
                chip=133-bank*4-lane;raw=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
                at=bank*0x400000+lane;gfx[at:at+len(raw)*4:4]=raw
    assert art.sha(donor)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    # Actual donor dispatch references, not an equal-looking animation index.
    assert struct.unpack_from('<2I',donor,p.stock_file(0xff9ccf80))==(0xff9cd160,0xff9cd1d0)
    poses={g:p.frame_group(donor,g,g,g+0x200) for g in KANO+BUBBLE+SONYA}
    assert all(poses.values())
    sonya_frames={f for g in SONYA for f in poses[g]}
    prefix=(HERE/'generated_names/fighter_ui_finish_names_graphics.bin').read_bytes()
    packed=bytearray(prefix);streams={};palettes={};records=[];pins=[]
    for frame in sorted({f for fs in poses.values() for f in fs}):
        at=p.stock_file(frame);assert p.looks_like_frame(donor,at)
        w,h,x,y,sag,ctrl=struct.unpack_from('<HHHHIH',donor,at)
        raw,bits=art.bitstream(gfx,sag,w,h,ctrl);key=(bits,art.sha(raw))
        if key not in streams:streams[key]=len(packed);packed.extend(raw)
        offset=streams[key];tail=p.u32(donor,at+14)
        if 0xff800000<=tail<=0xffffffff and not tail&15:
            pal=p.stock_file(tail);count=p.u16(donor,pal);assert 1<=count<=256
            palettes[tail]=struct.unpack_from(f'<{count}H',donor,pal+2)
            palette=f'ks_friend_palette_{tail:08x}'
        else:palette='ks_sonya_primary_palette' if frame in sonya_frames else 'ks_kano_primary_palette'
        label=f'ks_friend_frame_{frame:08x}'
        records += [label,f'        .word {w},{h},{p.signed(x)},{p.signed(y)}',
                    f'        .long 0{(0xc00000+offset)*8:08x}h',f'        .word {art.word(ctrl)}',f'        .long {palette}']
        pins.append(dict(sourceFrame=hex(frame),width=w,height=h,sourceBitAddress=hex(sag),
                         packedByteOffset=offset,bits=bits,compressedSHA256=art.sha(raw),palette=palette))
    lines=['; Native typed Friendship image/palette/composite DATA, no executable blobs.',
           '        .ref ks_kano_primary_palette,ks_sonya_primary_palette','        .data']
    for address,colors in sorted(palettes.items()):
        label=f'ks_friend_palette_{address:08x}'
        lines += [f'        .def {label}',label,f'        .word {len(colors)}']
        for i in range(0,len(colors),8):lines.append('        .word '+','.join(art.word(c) for c in colors[i:i+8]))
    lines+=records
    for group,frames in sorted(poses.items()):
        label=f'ks_friend_pose_{group:08x}'
        lines += [f'        .def {label}',label]+[f'        .long ks_friend_frame_{f:08x}' for f in frames]+['        .long 0']
    for label,groups in [('ks_friend_kano_body',KANO),('ks_friend_kano_bubbles',BUBBLE),
                         ('ks_friend_sonya_intro',SONYA[:7]),('ks_friend_sonya_poses',SONYA)]:
        lines += [f'        .def {label}',label]+[f'        .long ks_friend_pose_{g:08x}' for g in groups]+['        .long 0']
    source=('\n'.join(lines)+'\n').encode()
    assert packed[:len(prefix)]==prefix and len(packed)<0x600000
    out.mkdir(exist_ok=reuse_generated);(out/'KSFRART.ASM').write_bytes(source)
    (out/'fighter_ui_finish_friend_graphics.bin').write_bytes(packed)
    region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(0x600000);sockets={}
    for bank,size in [(0,0x100000),(1,0x80000)]:
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            at=bank*0x400000+lane;raw=region[at:at+size*4:4]
            assert len(raw)==size
            if emit_sockets:
                (out/name).write_bytes(raw)
            rebuilt[at:at+size*4:4]=raw;sockets[name]=art.sha(raw)
    assert rebuilt==region
    report=dict(inputProgramSHA256=art.sha(donor),sourceSHA256=art.sha(source),
                groups={k:[hex(g) for g in gs] for k,gs in [('kanoBody',KANO),('kanoBubble',BUBBLE),('sonyaBody',SONYA)]},
                compositePoses=len(poses),uniqueFrames=len(pins),framePins=pins,palettes=len(palettes),
                prefixBytes=len(prefix),prefixSHA256=art.sha(prefix),appendedBytes=len(packed)-len(prefix),
                totalGraphicsBytes=len(packed),stockSocketRoundTripVerified=True,sockets=sockets,
                nativeActionsImplemented=False,runtimeVerified=False,releaseReady=False)
    (out/'FRIEND_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('groups','framePins','sockets')},indent=2))

if __name__=='__main__':main()
