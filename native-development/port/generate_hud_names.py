"""Compose native HUD glyph pixels, preserving SCORE_P indices and shadows."""
from collections import Counter
import json
import re
import sys
import zipfile
from PIL import Image
import import_character_art as art

HERE=art.HERE
SRC=HERE.parent/'baseline/mk2-rebuild-main/srcp'

def main(emit_sockets=True,reuse_generated=False):
    out=HERE/'generated_names'
    assert not out.exists() or reuse_generated or '--refresh-generated' in sys.argv
    gfx=bytearray(0xc00000)
    with zipfile.ZipFile(art.ROOT/'roms/mk2.zip') as z:
        for bank,(first,second) in enumerate([(14,19),(16,20),(17,22)]):
            for lane,(letter,socket) in enumerate([('ug',first),('uj',first),('ug',second),('uj',second)]):
                raw=z.read(f'l1_mortal_kombat_ii_game_rom_{letter}{socket}.{letter}{socket}')
                start=bank*0x400000+lane;gfx[start:start+len(raw)*4:4]=raw
    def decode(sag,w,h,bpp):
        pixels=[]
        for i in range(w*h):
            bit=sag+i*bpp;at=bit//8
            pixels.append((int.from_bytes(gfx[at:at+2],'little')>>(bit&7))&((1<<bpp)-1))
        image=Image.new('L',(w,h));image.putdata(pixels);return image
    kang=decode(0x4122e42,65,10,4)
    scorpion=decode(0x412386a,68,10,4)
    glyphs={'K':kang.crop((28,0,36,10)),'A':kang.crop((37,0,46,10)),
            'N':kang.crop((47,0,56,10)),'S':scorpion.crop((0,0,8,10)),
            'O':scorpion.crop((19,0,27,10))}
    # R starts immediately at source column27: do not copy its first column
    # as O's shadow. Reconstruct only O's one-pixel native shadow at that edge.
    old_o=glyphs['O'];new_o=Image.new('L',(9,10))
    for y in range(9):
        for x in range(8):
            if old_o.getpixel((x,y)) not in (0,2):new_o.putpixel((x+1,y+1),2)
    for y in range(10):
        for x in range(8):
            value=old_o.getpixel((x,y))
            if value not in (0,2):new_o.putpixel((x,y),value)
    glyphs['O']=new_o
    # Native MK2 FONT7Y, adapted to the lifebar's nine-pixel face height.
    mask=decode(0x40038ee,6,8,1).resize((7,9),Image.Resampling.NEAREST)
    yy=Image.new('L',(8,10))
    for y in range(9):
        for x in range(7):
            if mask.getpixel((x,y)):yy.putpixel((x+1,y+1),2)
    for y in range(9):
        colors=Counter(v for v in kang.crop((37,y,45,y+1)).getdata() if v not in (0,2))
        color=colors.most_common(1)[0][0] if colors else 1
        for x in range(7):
            if mask.getpixel((x,y)):yy.putpixel((x,y),color)
    glyphs['Y']=yy
    palette_text=(SRC/'IMGPAL6.ASM').read_text().split('SCORE_P:',1)[1]
    words=[]
    for line in palette_text.splitlines():
        if '.word' not in line:continue
        words.extend(int(v[:-1],16) if v.lower().endswith('h') else int(v) for v in line.split('.word',1)[1].strip().split(','))
        if len(words)>=65:break
    assert words[0]==64
    rgb=[]
    for c in words[1:65]:rgb.extend([((c>>10)&31)*255//31,((c>>5)&31)*255//31,(c&31)*255//31])
    rgb+=([0]*(768-len(rgb)))
    prefix=(HERE/'generated_baby/fighter_ui_finish_baby_graphics.bin').read_bytes()
    packed=bytearray(prefix);lines=['; Native HUD image DATA, original SCORE_P indices.','        .data'];names={}
    out.mkdir(exist_ok=True)
    for name in ['KANO','SONYA']:
        width=sum(glyphs[c].width for c in name)+len(name)-1
        image=Image.new('L',(width,10));x=0
        for c in name:
            image.paste(glyphs[c],(x,0));x+=glyphs[c].width+1
        pixels=list(image.getdata());assert max(pixels)<16 and 2 in pixels
        raw=bytes(pixels[i]|((pixels[i+1] if i+1<len(pixels) else 0)<<4) for i in range(0,len(pixels),2))
        offset=len(packed);packed.extend(raw)
        label='ks_bar_'+name.lower()
        lines += [f'        .def {label}',label,f'        .word {width},10,0,0',
                  f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 04000h']
        indexed=image.convert('P');indexed.putpalette(rgb)
        indexed.resize((width*8,80),Image.Resampling.NEAREST).save(out/f'{name}.png')
        names[name]=dict(width=width,height=10,packedByteOffset=offset,pixelSHA256=art.sha(bytes(pixels)),
                         shadowIndex=2,yGlyph='native FONT7Y resized nearest 6x8 to 7x9' if 'Y' in name else None)
    source=('\n'.join(lines)+'\n').encode();(out/'KSNAMES.ASM').write_bytes(source)
    (out/'fighter_ui_finish_names_graphics.bin').write_bytes(packed)
    region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(0x600000);sockets={}
    for bank,size in [(0,0x100000),(1,0x80000)]:
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane;raw=region[start:start+size*4:4]
            if emit_sockets:
                (out/name).write_bytes(raw)
            rebuilt[start:start+size*4:4]=raw;sockets[name]=art.sha(raw)
    assert rebuilt==region and packed[:len(prefix)]==prefix
    report=dict(names=names,sourceSHA256=art.sha(source),prefixSHA256=art.sha(prefix),
                appendedBytes=len(packed)-len(prefix),stockSocketRoundTripVerified=True,
                sockets=sockets,runtimeVerified=False)
    (out/'NAMES_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(names,indent=2))

if __name__=='__main__':main()
