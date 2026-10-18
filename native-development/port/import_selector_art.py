"""Bake the existing dedicated portraits into ordinary ROM image records.

No runtime C++ image conversion, overlays, borders or highlight graphics.
Native MKII selection and ladder code will own those behaviors.
"""
import hashlib
import json
from pathlib import Path
import struct
from PIL import Image
import import_character_art as art
HERE=art.HERE
ROOT=art.ROOT
OUT=HERE/'generated_ui_packed'
SOURCE=HERE/'assets/selector_source'
def sha(b):return hashlib.sha256(b).hexdigest().upper()
def word(v):return f'0{v:04x}h'
def rgb(v):return (((v>>10)&31)*255//31,((v>>5)&31)*255//31,(v&31)*255//31)
def main(reuse_generated=False):
    assert not OUT.exists() or reuse_generated
    manifest=json.loads((SOURCE/'SOURCE.json').read_text())
    assert manifest['format']=='MK2KS-SELECTOR-INDEXED-1'
    sw,sh,colors=manifest['width'],manifest['height'],manifest['colors']
    assert sw and sh and 0<colors<=128
    restored_ui=bytearray(b'KSU4'+bytes((sw,sh))+struct.pack('<H',colors))
    body=(HERE/'generated_packed/fighter_graphics.bin').read_bytes()
    packed=bytearray(body);lines=['; Dedicated native selector/ladder image DATA. No baked cursor/border.', '        .data']
    records={};OUT.mkdir(exist_ok=reuse_generated)
    for index,fighter in enumerate(('kano','sonya')):
        actor=manifest['actors'][fighter]
        raw=(SOURCE/actor['file']).read_bytes();assert sha(raw)==actor['fileSHA256']
        words=' '.join(line.split('#',1)[0] for line in raw.decode('ascii').splitlines()).split()
        assert words[:4]==['P2',str(sw),str(sh),str(colors-1)]
        pixels=bytes(map(int,words[4:]));assert len(pixels)==sw*sh and max(pixels)<colors
        assert sha(pixels)==actor['indicesSHA256']
        source_palette=actor['paletteRGB15'];assert len(source_palette)==colors
        restored_ui.extend(struct.pack(f'<{colors}H',*source_palette));restored_ui.extend(pixels)
        for style,width,height,bpp in [('selector',55,70,7),('ladder',35,45,6)]:
            resized=[pixels[(y*sh//height)*sw+x*sw//width] for y in range(height) for x in range(width)]
            frequency=[resized.count(i) for i in range(colors)]
            order=sorted(range(colors),key=lambda i:-frequency[i])
            count=1<<bpp
            palette=[0]+[source_palette[order[i]] if i<colors else source_palette[0] for i in range(count-1)]
            mapping={}
            for original,value in enumerate(source_palette):
                def distance(i):return sum((((value>>shift)&31)-((palette[i]>>shift)&31))**2 for shift in (0,5,10))
                mapping[original]=min(range(1,count),key=distance)
            indices=[mapping[v] for v in resized]
            payload=bytearray((len(indices)*bpp+7)//8)
            for pos,value in enumerate(indices):
                bit=pos*bpp;byte=bit//8;shift=bit&7
                payload[byte]|=(value<<shift)&255
                if shift+bpp>8:payload[byte+1]|=value>>(8-shift)
            start=0xc00000+len(packed);packed.extend(payload)
            label=f'ks_{fighter}_{style}'
            lines += [f'        .def {label}',label,f'        .word {width},{height},0,0',f'        .long 0{start*8:08x}h',f'        .word 0{bpp<<12:04x}h',f'        .long {label}_palette',f'{label}_palette',f'        .word {count}']
            for row in range(0,count,8):lines.append('        .word '+','.join(word(v) for v in palette[row:row+8]))
            if style=='selector':
                locked=f'ks_{fighter}_locked_palette'
                lines += [f'        .def {locked}',locked,f'        .word {count}']
                for row in range(0,count,8):lines.append('        .word '+','.join(word((v>>1)&0x3def) for v in palette[row:row+8]))
            image=Image.new('RGB',(width,height));image.putdata([rgb(palette[v]) for v in indices]);image.save(OUT/f'{label}.png')
            records[label]=dict(width=width,height=height,bpp=bpp,graphicsByteOffset=start,
                                paletteColors=count,opaquePixelIndices=True,encodedSHA256=sha(payload))
    assert packed[:len(body)]==body and len(packed)<=0x600000
    text=('\n'.join(lines)+'\n').encode();(OUT/'KSUI.ASM').write_bytes(text)
    (OUT/'fighter_and_ui_graphics.bin').write_bytes(packed)
    region=packed+bytes(0x600000-len(packed));sockets={}
    for bank,size in [(0,0x100000),(1,0x80000)]:
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            payload=region[bank*0x400000+lane:bank*0x400000+lane+size*4:4]
            assert len(payload)==size;(OUT/name).write_bytes(payload);sockets[name]=sha(payload)
    assert sha(restored_ui)==manifest['legacyPortraitPrefixSHA256']
    result=dict(inputPortraitContainerSHA256=sha(restored_ui),
                inputSourceManifestSHA256=sha((SOURCE/'SOURCE.json').read_bytes()),
                requiresLegacyReleaseZIP=False,
                fighterGraphicsPrefixUnchanged=True,graphicsBytes=len(packed),stockSocketCapacity=0x600000,
                sourceSHA256=sha(text),records=records,sockets=sockets,
                runtimeEmulatorConversion=False,bakedBorders=False,selectionIntegrationVerified=False)
    (OUT/'UI_IMPORT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('sockets','records')},indent=2))
if __name__=='__main__':main()
