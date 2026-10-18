"""Sonya flame-kiss original compressed orb, performer/outro and burn DATA."""
import json
import struct
import zipfile
import import_character_art as art

HERE=art.HERE
FRAMES=[0xffb263f0,0xffb26460,0xffb264d0,0xffb26540,
        0xffb265b0,0xffb26620,0xffb26690,0xffb26700]

def main(emit_sockets=True,reuse_generated=False):
    out=HERE/'generated_kiss'
    assert not out.exists() or reuse_generated
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        data=bytearray(1048576);data[::2]=z.read('mk321u54.bin');data[1::2]=z.read('mk321u63.bin')
        gfx=bytearray(0x1200000)
        for bank in range(5):
            for lane in range(4):
                chip=133-bank*4-lane
                raw=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
                start=bank*0x400000+lane;gfx[start:start+len(raw)*4:4]=raw
    assert art.sha(data)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    prefix=(HERE/'generated_finishers/fighter_ui_finish_graphics.bin').read_bytes()
    packed=bytearray(prefix)
    lines=['; Native typed DATA; original compressed fire-orb pixels, no executable blobs.',
           '        .data','        .def ks_kiss_orb_frames,ks_kiss_orb_palette','ks_kiss_orb_frames']
    lines += [f'        .long ks_kiss_orb_{i}' for i in range(8)]
    pins=[]
    for i,frame in enumerate(FRAMES):
        at=art.parser.stock_file(frame)
        assert art.parser.looks_like_frame(data,at)
        w,h,x,y,sag,control=struct.unpack_from('<HHHHIH',data,at)
        assert control&0x80 and (control>>12)&7==5
        raw,bits=art.bitstream(gfx,sag,w,h,control)
        offset=len(packed);packed.extend(raw)
        assert packed[offset:offset+len(raw)]==raw
        lines += [f'ks_kiss_orb_{i}',f'        .word {w},{h},{art.parser.signed(x)},{art.parser.signed(y)}',
                  f'        .long 0{(0xc00000+offset)*8:08x}h',f'        .word {art.word(control)}',
                  '        .long ks_kiss_orb_palette']
        pins.append(dict(frame=hex(frame),width=w,height=h,sourceBitAddress=hex(sag),
                         packedByteOffset=offset,bits=bits,SHA256=art.sha(raw)))
    assert art.parser.u16(data,0x9990c)==31
    colors=list(struct.unpack_from('<32H',data,0x9990e));colors[0]=0
    colors += [0]*32
    lines+=['ks_kiss_orb_palette','        .word 64']
    for i in range(0,64,8):lines.append('        .word '+','.join(art.word(c) for c in colors[i:i+8]))
    outro=[0xff83d500,0xff83d560,0xff83d5a0,0xff83d600,0xff83d660,0xff83d6a0,0xff83d700,0xff83d760]
    imported=(HERE/'generated_packed/SONYAART.ASM').read_text()
    refs=[f'ks_sonya_pose_{g:08x}' for g in outro]
    assert all('.def '+r+'\n' in imported for r in refs)
    burn=json.loads((HERE/'generated_finishers/FINISHER_ASSETS.json').read_text())['groups']['sonya_burn']
    groups=[f'ks_finish_pose_{int(g,16):08x}' for g in burn]
    sequence=groups+groups[8:15]+groups[8:15]
    assert len(sequence)==29
    refs+=groups
    lines[1:1]=['        .ref '+r for r in refs]
    lines+=['        .def ks_kiss_burn,ks_kiss_outro,ks_kiss_outro_counts','ks_kiss_burn']
    lines += ['        .long '+r for r in sequence]
    lines += ['ks_kiss_outro']+['        .long '+r for r in refs[:8]]
    lines += ['ks_kiss_outro_counts','        .word 1,1,4,1,1,1,1,1']
    source=('\n'.join(lines)+'\n').encode()
    assert len(packed)<=0x600000 and packed[:len(prefix)]==prefix
    out.mkdir(exist_ok=reuse_generated);(out/'KSKSANI.ASM').write_bytes(source)
    (out/'fighter_ui_finish_kiss_graphics.bin').write_bytes(packed)
    region=packed+bytes(0x600000-len(packed));sockets={};rebuilt=bytearray(0x600000)
    for bank,size in [(0,0x100000),(1,0x80000)]:
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane;raw=region[start:start+size*4:4]
            assert len(raw)==size
            if emit_sockets:
                (out/name).write_bytes(raw)
            sockets[name]=art.sha(raw)
            rebuilt[start:start+size*4:4]=raw
    assert rebuilt==region
    report=dict(sourceSHA256=art.sha(source),inputProgramSHA256=art.sha(data),
                frames=pins,prefixBytes=len(prefix),prefixSHA256=art.sha(prefix),
                appendedBytes=len(packed)-len(prefix),totalGraphicsBytes=len(packed),
                compressedPixelsPreserved=True,stockSocketRoundTripVerified=True,sockets=sockets,
                outro=[hex(g) for g in outro],burn=sequence,runtimeVerified=False)
    (out/'KISS_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('frames','sockets','burn','outro')},indent=2))

if __name__=='__main__':main()
