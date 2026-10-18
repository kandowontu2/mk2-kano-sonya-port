"""Bounded rendering of actual own throw poses/pivots before choreography."""
import json
from pathlib import Path
import sys
import zipfile
from PIL import Image,ImageDraw
import import_character_art as art
sys.path.insert(0,str(art.ROOT/'tools'))
from audit_animation_poses import render_group
from upgrade_ksui_previews import donor_palette,component_spec

out=art.HERE/'throw_pose_review'
assert not out.exists() or '--refresh-generated' in sys.argv
out.mkdir(exist_ok=True)
gfx=bytearray(0x1400000)
with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
    lo=z.read('mk321u54.bin');hi=z.read('mk321u63.bin')
    for bank in range(5):
        for lane in range(4):
            chip=133-bank*4-lane
            payload=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
            start=bank*0x400000+lane
            gfx[start:start+len(payload)*4:4]=payload
data=bytearray(len(lo)+len(hi));data[::2]=lo;data[1::2]=hi
p=art.parser
report={}
for actor,root,special,block in [('kano',p.KANO_MAIN,p.KANO_SPECIAL,p.KANO_BLOCK),('sonya',p.SONYA_MAIN,p.SONYA_SPECIAL,p.SONYA_BLOCK)]:
    span=p.sequence_spans(data,root,block,(root,special))[35]
    groups=list({address:frames for _,address,frames in p.group_references(data,*span,*block)}.items())
    assert len(groups)==(7 if actor=='kano' else 6)
    palette=donor_palette(data,actor)
    sheet=Image.new('RGB',(7*170,230),(35,35,35));draw=ImageDraw.Draw(sheet)
    records=[]
    for i,(address,frames) in enumerate(groups):
        pose=render_group(data,gfx,palette,frames)
        assert pose.width<170 and pose.height<190
        sheet.paste(pose,(i*170+(170-pose.width)//2,205-pose.height),pose)
        draw.text((i*170+5,5),f'{i}: {address:08x}',fill='yellow')
        draw.text((i*170+5,212),f'{pose.width}x{pose.height}',fill='white')
        records.append({'pose':f'{address:08x}','components':[{'frame':f'{a:08x}','spec':list(component_spec(data,a))} for a in frames]})
    sheet.save(out/f'{actor}_throw.png')
    report[actor]={'mainIndex':35,'span':list(span),'poses':records,'runtimeChoreographyVerified':False}
(out/'THROW_POSES.json').write_text(json.dumps(report,indent=2)+'\n')
print(out)
