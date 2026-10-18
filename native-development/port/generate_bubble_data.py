"""Separate native Death Orb animation/palette DATA, not a flame-kiss alias."""
import json
import struct
import zipfile
import import_character_art as art

HERE=art.HERE

def main():
    out=HERE/'generated_bubble'
    assert not out.exists()
    intro=[0xff83fda0,0xff83fde0,0xff83fe20,0xff83fe60,0xff83fea0,0xff83fee0,0xff83ff20]
    loop=[0xff83ff60,0xff83ffa0,0xff83ffe0,0xff840020]
    burst=[0xff840060,0xff8400a0,0xff8400e0]
    imported=(HERE/'generated_packed/SONYAART.ASM').read_text()
    refs={f'ks_sonya_pose_{g:08x}' for g in intro+loop+burst}
    assert all('.def '+r+'\n' in imported for r in refs)
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        data=bytearray(1048576);data[::2]=z.read('mk321u54.bin');data[1::2]=z.read('mk321u63.bin')
        gfx=bytearray(0x1200000)
        for bank in range(5):
            for lane in range(4):
                chip=133-bank*4-lane
                raw=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
                start=bank*0x400000+lane;gfx[start:start+len(raw)*4:4]=raw
    assert art.sha(data)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    address=0xff83f6f0;at=art.parser.stock_file(address)
    assert art.parser.u16(data,at)==32
    colors=list(struct.unpack_from('<32H',data,at+2));colors[0]=0
    peaks={}
    for group in intro+loop+burst:
        peak=0
        for frame in art.parser.frame_group(data,group,*art.parser.SONYA_BLOCK):
            w,h,x,y,sag,ctrl=struct.unpack_from('<4hIH',data,art.parser.stock_file(frame))
            raw,bits=art.bitstream(gfx,sag,w,h,ctrl)
            cursor=0;bpp=(ctrl>>12)&7 or 8
            def take(n):
                nonlocal cursor
                value=(int.from_bytes(raw[cursor//8:cursor//8+3],'little')>>(cursor&7))&((1<<n)-1)
                cursor+=n;return value
            for _ in range(h):
                if ctrl&0x80:
                    skip=take(8);pre=(skip&15)<<((ctrl>>8)&3);post=(skip>>4)<<((ctrl>>10)&3)
                else:pre=post=0
                for _ in range(max(0,w-pre-post)):peak=max(peak,take(bpp))
            assert cursor==bits
        assert peak<32,(hex(group),peak)
        peaks[hex(group)]=peak
    lines=['; Original Death Orb composites and palette, named native DATA.',
           '        .data']+['        .ref '+r for r in sorted(refs)]
    for label,groups in [('ks_bubble_intro',intro),('ks_bubble_loop',loop),('ks_bubble_burst',burst)]:
        lines += ['        .def '+label,label]
        lines += [f'        .long ks_sonya_pose_{g:08x}' for g in groups]+['        .long 0']
    lines += ['        .def ks_bubble_palette','ks_bubble_palette','        .word 32']
    for i in range(0,32,8):lines.append('        .word '+','.join(art.word(c) for c in colors[i:i+8]))
    source=('\n'.join(lines)+'\n').encode()
    out.mkdir();(out/'KSBUANI.ASM').write_bytes(source)
    report=dict(sourceSHA256=art.sha(source),inputProgramSHA256=art.sha(data),
                intro=[hex(g) for g in intro],loop=[hex(g) for g in loop],burst=[hex(g) for g in burst],
                paletteSource=hex(address),paletteColors=32,pixelPeaks=peaks,
                allPixelsFitPalette=True,additionalGraphicsBytes=0,runtimeVerified=False)
    (out/'BUBBLE_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
