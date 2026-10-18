"""Independent original-ROM oracle for slideshow and BATTLE photo records."""
from pathlib import Path
import argparse
import hashlib
import json
import struct
from decode_native_picture import decode
from upgrade_ksui_previews import load_gfx
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def reference(gfx,fighter,page):
    if fighter not in (0,1) or page not in (0,1,2):raise ValueError('Unknown fighter/photo kind')
    offset=0x1000000 if fighter else 0x103599a
    source,report=decode(gfx,offset)
    if source.size!=(256,128) or report['palette_count']!=255:
        raise ValueError('Unexpected original ROM photo')
    width,height=(138,158) if page==2 else ((280,119) if page else (124,163))
    original=source.tobytes()
    original_palette=struct.unpack_from('<255H',gfx,offset+8)
    black_index=original_palette.index(0)+1
    rows=[]
    for y in range(height):
        for x in range(width):
            if page==2:
                sx=(0 if fighter else 143)+x*108//138
                sy=4+y*124//158
                pixel=original[sy*256+sx]+1
            elif page:
                pixel=original[(y*128//119)*256+(x-21)*256//238]+1 if 21<=x<259 else black_index
            else:
                sx=(4 if fighter else 149)+x*94//124
                sy=4+y*124//163
                pixel=original[sy*256+sx]+1
            rows.append(pixel)
    pixels=bytes(rows)
    palette=bytes(2)+gfx[offset+8:offset+8+255*2]
    header=struct.pack('<4H',width,height,1,256)
    image=Image.frombytes('P',(width,height),pixels)
    image.putpalette([0,0,0]+source.getpalette()[:255*3])
    return header+palette+pixels,image,report

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    gfx=load_gfx(ROOT/'mk3')
    records=[]
    for fighter,name in enumerate(('kano','sonya')):
        for page in range(3):
            data,image,report=reference(gfx,fighter,page)
            stem=f'{name}_battle' if page==2 else f'{name}_page_{page+1}'
            (args.output/f'{stem}.bin').write_bytes(data)
            image.save(args.output/f'{stem}.png')
            records.append({'fighter':name,'kind':'battle' if page==2 else 'ending','page':None if page==2 else page+1,'file':f'{stem}.bin',
                            'sha256':hashlib.sha256(data).hexdigest(),'original':report})
    (args.output/'reference.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))

if __name__=='__main__':main()
