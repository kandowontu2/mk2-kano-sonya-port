"""Decode original poses as references; no original sprites/ROMs are edited."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw
import build_mk2ks_mk3 as b
import upgrade_ksui_previews as ui
from audit_animation_poses import render_group

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('Preserve reference evidence')
    args.output.mkdir()
    original=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();gfx=ui.load_gfx(ROOT/'mk3')
    report={'originalProgramSHA256':hashlib.sha256(original).hexdigest().upper(),'fighters':{}}
    for name,root,special,bounds in(('kano',b.KANO_MAIN,b.KANO_SPECIAL,b.KANO_BLOCK),
                                    ('sonya',b.SONYA_MAIN,b.SONYA_SPECIAL,b.SONYA_BLOCK)):
        spans=b.sequence_spans(original,root,bounds,(root,special))
        sheet=Image.new('RGBA',(1120,760),(32,32,32,255));draw=ImageDraw.Draw(sheet)
        records=[];palette=ui.donor_palette(original,name)
        for row,anim in enumerate((37,28,35,30)):
            groups=list(dict((group,frames)for _,group,frames in
                             b.group_references(original,*spans[anim],*bounds)).items())
            for index,(group,frames)in enumerate(groups[:7]):
                image=render_group(original,gfx,palette,frames)
                x=index*160;y=row*190
                draw.text((x+2,y+3),f'{name} a{anim}/{index}',fill='white')
                draw.text((x+2,y+16),f'{group:08X}',fill='yellow')
                sheet.alpha_composite(image,(x+(160-image.width)//2,y+40+145-image.height))
                image.save(args.output/f'{name}_a{anim}_pose{index}.png')
                records.append({'animation':anim,'pose':index,'group':f'{group:08X}',
                                'frames':[f'{f:08X}'for f in frames],'size':image.size})
        sheet.save(args.output/f'{name}_original_death_pose_reference.png')
        report['fighters'][name]=records
    (args.output/'reference.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({name:len(data)for name,data in report['fighters'].items()}))

if __name__=='__main__':main()
