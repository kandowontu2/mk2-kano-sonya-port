"""Render native reference and own composite candidates; no ROM modification."""
import json
from pathlib import Path
import sys
import zipfile
from PIL import Image,ImageDraw
import import_character_art as art
sys.path.insert(0,str(art.ROOT/'tools'))
from audit_animation_poses import render_group
from upgrade_ksui_previews import donor_palette,component_spec,xrgb555

OUT=art.HERE/'backbreak_part_review'
assert not OUT.exists()
OUT.mkdir()
p=art.parser
sheet=Image.new('RGB',(1440,630),(35,35,35));draw=ImageDraw.Draw(sheet)
report={}
def row(actor,program,gfx,palette,groups,row):
    entries=[]
    for col,(address,frames) in enumerate(groups):
        pose=render_group(program,gfx,palette,frames)
        assert pose.width<180 and pose.height<175
        x=col*180;y=row*210
        sheet.paste(pose,(x+(180-pose.width)//2,y+185-pose.height),pose)
        draw.text((x+4,y+4),f'{actor} {address:08x}',fill='yellow')
        draw.text((x+4,y+194),f'{pose.width}x{pose.height}',fill='white')
        entries.append({'pose':f'{address:08x}','components':[{'frame':f'{frame:08x}','spec':list(component_spec(program,frame))} for frame in frames]})
    report[actor]=entries

program=(art.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
gfx=bytearray(0xc00000)
with zipfile.ZipFile(art.ROOT/'roms/mk2.zip') as z:
    for bank,(first,second) in enumerate(((14,19),(16,20),(17,22))):
        for lane,(letter,socket) in enumerate((('ug',first),('uj',first),('ug',second),('uj',second))):
            payload=z.read(f'l1_mortal_kombat_ii_game_rom_{letter}{socket}.{letter}{socket}')
            start=bank*0x400000+lane;gfx[start:start+len(payload)*4:4]=payload
offset=p.stock_file(0xffadc8b0)
count=p.u16(program,offset)
palette=[(0,0,0,0)]+[(*xrgb555(p.u16(program,offset+2+i*2)),255) for i in range(1,min(count,256))]
palette += [(255,255,255,255)]*(256-len(palette))
span=p.sequence_spans(program,p.LIU_MAIN,p.LIU_BLOCK,(p.LIU_MAIN,p.LIU_SPECIAL))[63]
groups=list({address:frames for _,address,frames in p.group_references(program,*span,*p.LIU_BLOCK)}.items())
assert len(groups)==3
row('native_Liu_reference',program,gfx,palette,groups,0)
program=(art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
gfx=bytearray(0x1400000)
with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
    for bank in range(5):
        for lane in range(4):
            chip=133-bank*4-lane;payload=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
            start=bank*0x400000+lane;gfx[start:start+len(payload)*4:4]=payload
for y,(actor,root,special,block) in enumerate((('kano',p.KANO_MAIN,p.KANO_SPECIAL,p.KANO_BLOCK),('sonya',p.SONYA_MAIN,p.SONYA_SPECIAL,p.SONYA_BLOCK)),1):
    spans=p.sequence_spans(program,root,block,(root,special))
    groups={address:frames for index in (30,38) for _,address,frames in p.group_references(program,*spans[index],*block)}
    candidates=list(groups.items())
    # Show the airborne/flat tail of knockdown and all four own rotation poses.
    chosen=candidates[2:5]+candidates[7:12]
    assert len(chosen)<=8
    row(actor,program,gfx,donor_palette(program,actor),chosen,y)
sheet.save(OUT/'backbreak_candidates.png')
(OUT/'COMPOSITE_PARTS.json').write_text(json.dumps({'actors':report,'authoredBackbreakArt':False,'runtimeVerified':False},indent=2)+'\n')
print(OUT)
