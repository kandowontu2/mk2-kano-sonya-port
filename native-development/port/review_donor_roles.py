"""Bounded visual inventory for explicitly mapping throw/victim animations."""
import json
import sys
import zipfile
from pathlib import Path
from PIL import Image,ImageDraw
import import_character_art as art
sys.path.insert(0,str(art.ROOT/'tools'))
from audit_animation_poses import render_group
from upgrade_ksui_previews import donor_palette
p=art.parser
def main():
    out=art.HERE/'donor_role_review'
    assert not out.exists()
    out.mkdir()
    gfx=bytearray(0x1200000)
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        lo=z.read('mk321u54.bin');hi=z.read('mk321u63.bin')
        for bank in range(5):
            for lane in range(4):
                chip=133-bank*4-lane
                b=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
                start=bank*0x400000+lane;gfx[start:start+len(b)*4:4]=b
    data=bytearray(len(lo)+len(hi));data[::2]=lo;data[1::2]=hi
    report={}
    for fighter,root,special,block in [('kano',p.KANO_MAIN,p.KANO_SPECIAL,p.KANO_BLOCK),('sonya',p.SONYA_MAIN,p.SONYA_SPECIAL,p.SONYA_BLOCK)]:
        palette=donor_palette(data,fighter)
        spans=p.sequence_spans(data,root,block,(root,special))
        sheet=Image.new('RGB',(1760,800),(35,35,35));draw=ImageDraw.Draw(sheet)
        entries={}
        for cell,index in enumerate(range(33,65)):
            x=(cell%8)*220;y=(cell//8)*200
            if index not in spans:
                draw.text((x+4,y+4),f'{index}: no span',fill='red');continue
            groups=p.group_references(data,*spans[index],*block)
            groups=list({address:frames for _,address,frames in groups}.items())
            draw.text((x+4,y+4),f'{fighter} main {index} | {len(groups)} poses',fill='white')
            entries[index]=dict(span=list(spans[index]),poses=[hex(a) for a,_ in groups])
            if not groups: continue
            for slot,pos in enumerate((0,len(groups)//2,len(groups)-1)):
                address,frames=groups[pos]
                image=render_group(data,gfx,palette,frames)
                assert image.width<800 and image.height<800
                image.thumbnail((70,156),Image.Resampling.NEAREST)
                sheet.paste(image,(x+slot*72+(70-image.width)//2,y+22+156-image.height),image)
                draw.text((x+slot*72,y+182),f'{address&0xfffff:05x}',fill='yellow')
        sheet.save(out/f'{fighter}_main_33_64.png')
        report[fighter]=entries
    (out/'roles.json').write_text(json.dumps(report,indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
