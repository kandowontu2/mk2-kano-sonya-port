"""Native single-image baby descriptors and original compressed pixels."""
import json
import struct
import zipfile
import import_character_art as art

HERE=art.HERE

def main(emit_sockets=True,reuse_generated=False):
    out=HERE/'generated_baby'
    assert not out.exists() or reuse_generated,'Never overwrite generated evidence'
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        data=bytearray(1048576)
        data[::2]=z.read('mk321u54.bin');data[1::2]=z.read('mk321u63.bin')
        gfx=bytearray(0x1200000)
        for bank in range(5):
            for lane in range(4):
                chip=133-bank*4-lane
                raw=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
                start=bank*0x400000+lane;gfx[start:start+len(raw)*4:4]=raw
    assert art.sha(data)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    prefix=(HERE/'generated_kiss/fighter_ui_finish_kiss_graphics.bin').read_bytes()
    packed=bytearray(prefix)
    lines=['; Original compressed baby pixels and typed native image/palette DATA.','        .data']
    records={}
    for donor_id,(name,frame,wanted) in enumerate([('kano',0xffc7e7a0,(27,44)),('sonya',0xffc7e950,(35,54))]):
        assert art.parser.u32(data,art.parser.stock_file(0xffa2a5b0)+donor_id*4)==frame
        w,h,x,y,sag,ctrl,palette=struct.unpack_from('<HHhhIHI',data,art.parser.stock_file(frame))
        assert (w,h)==wanted and (x,y)==(0,0) and (ctrl>>12)&7==5
        raw,bits=art.bitstream(gfx,sag,w,h,ctrl)
        offset=len(packed);packed.extend(raw)
        pal_at=art.parser.stock_file(palette)
        count=art.parser.u16(data,pal_at)
        assert 1<count<=32
        colors=list(struct.unpack_from(f'<{count}H',data,pal_at+2));colors[0]=0
        lines += [f'        .def ks_{name}_baby',f'ks_{name}_baby',f'        .word {w},{h},{x},{y}',
                  f'        .long 0{(0xc00000+offset)*8:08x}h',f'        .word {art.word(ctrl)}',
                  f'        .long ks_{name}_baby_pal',f'ks_{name}_baby_pal',f'        .word {count}']
        for i in range(0,count,8):lines.append('        .word '+','.join(art.word(c) for c in colors[i:i+8]))
        records[name]=dict(sourceFrame=hex(frame),width=w,height=h,paletteSource=hex(palette),
                           paletteColors=count,packedByteOffset=offset,bits=bits,compressedSHA256=art.sha(raw))
    assert packed[:len(prefix)]==prefix and len(packed)<0x600000
    source=('\n'.join(lines)+'\n').encode()
    out.mkdir(exist_ok=reuse_generated);(out/'KSBABART.ASM').write_bytes(source)
    (out/'fighter_ui_finish_baby_graphics.bin').write_bytes(packed)
    region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(0x600000);sockets={}
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
    report=dict(sourceSHA256=art.sha(source),inputProgramSHA256=art.sha(data),records=records,
                prefixBytes=len(prefix),prefixSHA256=art.sha(prefix),appendedBytes=len(packed)-len(prefix),
                totalGraphicsBytes=len(packed),stockSocketRoundTripVerified=True,
                originalCompressedPixelsPreserved=True,sockets=sockets,runtimeVerified=False)
    (out/'BABY_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='sockets'},indent=2))

if __name__=='__main__':main()
