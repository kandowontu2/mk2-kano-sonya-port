"""Read-only original friendship artwork oracle, including Kano's separate bubble.

No ROM, payload or driver is edited. Linear and skip-encoded native DMA sources
are decoded separately; never treat a linear bubble frame as a skip stream.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from PIL import Image,ImageDraw
import build_mk2ks_mk3 as animation
import upgrade_ksui_previews as ui

BASE=0xff800000
def off(address):return (address-BASE)//8
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def component(gfx,palette,source,command,width,height):
    bpp=(command>>12)&7
    if not 1<=bpp<=6:raise ValueError('Unsupported native bpp')
    image=Image.new('RGBA',(width,height))
    cursor=source
    for y in range(height):
        pre=post=0
        if command&0x80:
            skip=ui.extract_bits(gfx,cursor,255);cursor+=8
            pre=(skip&15)<<((command>>8)&3)
            post=(skip>>4)<<((command>>10)&3)
        for x in range(pre,max(pre,width-post)):
            value=ui.extract_bits(gfx,cursor,(1<<bpp)-1);cursor+=bpp
            if value:
                if value>=len(palette):raise ValueError('Pixel exceeds original palette')
                image.putpixel((x,y),palette[value])
    return image

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('Do not overwrite original-art evidence')
    program_path=args.root/'mk3/mk3-maincpu.bin'
    program=program_path.read_bytes()
    if len(program)!=0x100000:raise ValueError('Complete original program required')
    gfx=ui.load_gfx(args.root/'mk3')
    sources=[program_path,Path(__file__),Path(ui.__file__),Path(animation.__file__)]
    sources.extend(args.root/'mk3'/f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
                   for _,chips in ui.GFX_BANKS for chip in chips)
    specs={
      'kano':dict(stream=0xff9d1690,stream_words=43,bounds=(0xff9d1c30,0xff9d27d0),
                  primary_record=0xff991c50,original_id=0),
      'sonya':dict(stream=0xff9d27d0,stream_words=30,bounds=(0xff9d2b90,0xff9d3170),
                   primary_record=0xff98a620,original_id=1)}
    # Actual original friendship dispatch table, not a numerically equal pose ID.
    if struct.unpack_from('<2I',program,off(0xff9ccf80))!=(0xff9cd160,0xff9cd1d0):
        raise ValueError('Original true-ID friendship dispatch changed')
    bubble_palette=0xffcdf710
    count=struct.unpack_from('<H',program,off(bubble_palette))[0]
    if count!=16:raise ValueError('Original bubble palette changed')
    words=struct.unpack_from('<16H',program,off(bubble_palette)+2)
    bubble=[(0,0,0,0)]+[(*ui.xrgb555(word),255)for word in words[1:]]
    report={'source':'original MK3 2.1 native friendship records','records':{},
            'input_hashes':{str(path.resolve()):digest(path)for path in sources},
            'bubble_palette_pointer':bubble_palette,
            'bubble_palette_hex':program[off(bubble_palette):off(bubble_palette)+34].hex(),
            'fullPortAcceptance':False,'scope':'artwork oracle; does not certify native port choreography'}
    args.output.mkdir(parents=True)
    for fighter,spec in specs.items():
        stream=struct.unpack_from(f'<{spec["stream_words"]}I',program,off(spec['stream']))
        groups=[]
        for address in stream:
            if spec['bounds'][0]<=address<spec['bounds'][1]and address not in groups:groups.append(address)
        if len(groups)!=(25 if fighter=='kano'else 11):raise ValueError('Unexpected original scene group count')
        body_palette=ui.donor_palette(program,fighter)
        metadata=[]
        pictures=[]
        for address in groups:
            frames=animation.frame_group(program,address,*spec['bounds'])
            if not frames:raise ValueError('Malformed original component list')
            effect=fighter=='kano'and address>=0xff9d2610
            palette=bubble if effect else body_palette
            parts=[]
            for frame in frames:
                raw=program[off(frame):off(frame)+14]
                w,h,x,y,source,command=struct.unpack('<HHhhIH',raw)
                image=component(gfx,palette,source,command,w,h)
                parts.append((image,x,y))
            left=min(-x for image,x,y in parts);top=min(-y for image,x,y in parts)
            right=max(-x+image.width for image,x,y in parts);bottom=max(-y+image.height for image,x,y in parts)
            canvas=Image.new('RGBA',(right-left,bottom-top))
            for image,x,y in parts:canvas.alpha_composite(image,(-x-left,-y-top))
            name=f'{fighter}_{address:08x}.png'
            canvas.save(args.output/name)
            pictures.append((canvas,address,effect))
            metadata.append(dict(group=address,effect=effect,frames=frames,
                descriptors_hex=[program[off(frame):off(frame)+14].hex()for frame in frames],
                bounds=[left,top,right,bottom],file=name,rgba_sha256=hashlib.sha256(canvas.tobytes()).hexdigest()))
        sheet=Image.new('RGB',(220*6,190*((len(pictures)+5)//6)),(35,35,35))
        draw=ImageDraw.Draw(sheet)
        for index,(picture,address,effect)in enumerate(pictures):
            x=(index%6)*220;y=(index//6)*190
            sheet.paste(picture,(x+(220-picture.width)//2,y+20+(155-picture.height)//2),picture)
            draw.text((x+8,y+4),f'{address:08X}'+(' bubble'if effect else''),fill='white')
        sheet.save(args.output/f'{fighter}_contact_sheet.png')
        record=program[off(spec['primary_record']):off(spec['primary_record'])+44]
        masks,type_,gate,action=struct.unpack_from('<IIHII',record)[0:2],struct.unpack_from('<H',record,8)[0],struct.unpack_from('<I',record,10)[0],struct.unpack_from('<I',record,14)[0]
        if action!=0xff9ccce0 or type_!=6:raise ValueError('Not an original friendship command record')
        report['records'][fighter]=dict(original_id=spec['original_id'],native_action=(0xff9cd160 if fighter=='kano'else 0xff9cd1d0),
            stream=spec['stream'],stream_hex=program[off(spec['stream']):off(spec['stream'])+spec['stream_words']*4].hex(),
            primary_command_record=spec['primary_record'],command_record_hex=record.hex(),groups=metadata,
            command_gate=gate,input_masks=masks)
    (args.output/'reference.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'groups':{key:len(value['groups'])for key,value in report['records'].items()},
                      'fullPortAcceptance':False},indent=2))

if __name__=='__main__':main()
