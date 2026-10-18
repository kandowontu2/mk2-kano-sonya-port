"""Render donor roll/square-wave poses for explicit native script selection."""
import json
import sys
import zipfile
from PIL import Image,ImageDraw
import import_character_art as art
sys.path.insert(0,str(art.ROOT/'tools'))
from audit_animation_poses import render_group
from upgrade_ksui_previews import donor_palette
p=art.parser

def main():
    projectile='--projectiles' in sys.argv
    out=art.HERE/('projectile_pose_review' if projectile else 'special_pose_review')
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
    result={}
    roles=[
        ('kano',p.KANO_MAIN,p.KANO_SPECIAL,p.KANO_BLOCK,26,'main'),
        ('sonya',p.SONYA_MAIN,p.SONYA_SPECIAL,p.SONYA_BLOCK,3,'special')]
    if projectile:
        roles=[(fighter,root,special,block,index,'main')
               for fighter,root,special,block in [
                   ('kano',p.KANO_MAIN,p.KANO_SPECIAL,p.KANO_BLOCK),
                   ('sonya',p.SONYA_MAIN,p.SONYA_SPECIAL,p.SONYA_BLOCK)]
               for index in (36,55)]
    for fighter,root,special,block,index,which in roles:
        spans=p.sequence_spans(data,root if which=='main' else special,block,(root,special))
        poses=p.group_references(data,*spans[index],*block)
        sheet=Image.new('RGB',(1280,((len(poses)+7)//8)*200),(35,35,35))
        draw=ImageDraw.Draw(sheet)
        for i,(_,address,frames) in enumerate(poses):
            image=render_group(data,gfx,donor_palette(data,fighter),frames)
            image.thumbnail((150,170),Image.Resampling.NEAREST)
            x=i%8*160;y=i//8*200
            sheet.paste(image,(x+(160-image.width)//2,y+20+170-image.height),image)
            draw.text((x+2,y+2),f'{i}: {address:08x}',fill='white')
        name=f'{fighter}_{index}' if projectile else fighter
        sheet.save(out/f'{name}.png')
        result[name]=dict(root=hex(root if which=='main' else special),index=index,poses=[hex(a) for _,a,_ in poses])
    (out/'poses.json').write_text(json.dumps(result,indent=2)+'\n')
    print(out)
if __name__=='__main__': main()
