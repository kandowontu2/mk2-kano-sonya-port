"""Read-only original MK3 small-component contact sheets for head-art routing."""
import argparse
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image,ImageDraw
import upgrade_ksui_previews as ui

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('Preserve existing inspection')
    args.output.mkdir()
    program=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();gfx=ui.load_gfx(ROOT/'mk3')
    report={'program_sha256':hashlib.sha256(program).hexdigest().upper(),'fighters':{}}
    # All small components inside the original fighter descriptor banks,
    # not crops or generated replacements. Labels retain the original address.
    for name,first,last in(('kano',0xffc96000,0xfffffe00),):
        palette=ui.donor_palette(program,name);frames=[]
        for address in range(first,last,16):
            offset=(address-0xff800000)//8
            w,h,x,y,source,cmd=struct.unpack_from('<4hIH',program,offset)
            if not(8<=w<=65 and 10<=h<=65 and -256<=x<=256 and -256<=y<=256 and
                   cmd&0x7f in(0,2) and 1<=(cmd>>12)&7<=6 and 0<=source<len(gfx)*8-0x1000):continue
            try:
                if cmd&0x80:pic=ui.decode_component(gfx,palette,source,cmd,w,h)
                else:
                    pic=Image.new('RGBA',(w,h));bits=(cmd>>12)&7
                    for yy in range(h):
                        for xx in range(w):
                            index=ui.extract_bits(gfx,source+(yy*w+xx)*bits,(1<<bits)-1)
                            if index:pic.putpixel((xx,yy),palette[index])
            except (IndexError,ValueError):continue
            frames.append((address,pic,{'address':f'{address:08X}','width':w,'height':h,
                                      'xOffset':x,'yOffset':y,'source':f'{source:08X}','command':f'{cmd:04X}'}))
        report['fighters'][name]=[row for address,pic,row in frames]
        for page in range((len(frames)+79)//80):
            selected=frames[page*80:(page+1)*80]
            sheet=Image.new('RGB',(800,((len(selected)+9)//10)*85),(35,35,35));draw=ImageDraw.Draw(sheet)
            for i,(address,pic,row)in enumerate(selected):
                x=(i%10)*80;y=(i//10)*85
                sheet.paste(pic,(x+(80-pic.width)//2,y+20),pic)
                draw.text((x+2,y+2),f'{address&0xfffff:05X}',fill='white')
                draw.text((x+2,y+70),f'{pic.width}x{pic.height}',fill='yellow')
            sheet.save(args.output/f'{name}_small_components_{page}.png')
    (args.output/'inspection.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({name:len(data)for name,data in report['fighters'].items()}))

if __name__=='__main__':main()
