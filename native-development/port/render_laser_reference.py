"""Bounded original-ROM laser victim pixel preview, not gameplay evidence."""
from PIL import Image
import json
import struct
import zipfile
import import_character_art as art

def main():
    out=art.HERE/'laser_reference'
    out.mkdir(exist_ok=True)
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        data=bytearray(1048576);data[::2]=z.read('mk321u54.bin');data[1::2]=z.read('mk321u63.bin')
        gfx=bytearray(0x1200000)
        for bank in range(5):
            for lane in range(4):
                chip=133-bank*4-lane
                raw=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
                start=bank*0x400000+lane;gfx[start:start+len(raw)*4:4]=raw
    assert art.sha(data)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    result={}
    for name,frame,palette_at in [('kano',0xffb19c00,0x92bbc),('sonya',0xffb276c0,0x92cf2)]:
        w,h,x,y,sag,ctrl=struct.unpack_from('<4hIH',data,art.parser.stock_file(frame))
        raw,bits=art.bitstream(gfx,sag,w,h,ctrl)
        cursor=0;bpp=(ctrl>>12)&7 or 8
        def take(n):
            nonlocal cursor
            value=(int.from_bytes(raw[cursor//8:cursor//8+3],'little')>>(cursor&7))&((1<<n)-1)
            cursor+=n;return value
        colors=[0]+list(struct.unpack_from('<64H',data,palette_at+4))
        pixels=Image.new('RGBA',(w,h))
        for row in range(h):
            skip=take(8) if ctrl&0x80 else 0
            pre=(skip&15)<<((ctrl>>8)&3);post=(skip>>4)<<((ctrl>>10)&3)
            for column in range(pre,max(pre,w-post)):
                index=take(bpp)
                assert index<len(colors)
                c=colors[index]
                if column<w and index:
                    pixels.putpixel((column,row),(((c>>10)&31)*255//31,((c>>5)&31)*255//31,(c&31)*255//31,255))
        assert cursor==bits
        path=out/f'{name}_laser_victim.png'
        pixels.resize((w*3,h*3),Image.Resampling.NEAREST).save(path)
        result[name]=dict(frame=hex(frame),width=w,height=h,origin=[x,y],path=str(path))
    (out/'REFERENCE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
