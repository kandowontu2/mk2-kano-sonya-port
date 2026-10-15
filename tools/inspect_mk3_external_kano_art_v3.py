"""Locate original external Kano composites; diagnostic art, no ROM changes."""
import argparse,json,struct
from pathlib import Path
from PIL import Image,ImageDraw
import build_mk2ks_mk3 as b
import upgrade_ksui_previews as ui
from audit_animation_poses import render_group

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    if args.output.exists(): raise ValueError('Never overwrite evidence')
    args.output.mkdir(parents=True)
    program=(args.workspace/'mk3/mk3-maincpu.bin').read_bytes()
    graphics=ui.load_gfx(args.workspace/'roms_v22_clean/mk2ks')
    palette=ui.donor_palette(program,'kano')
    records=[]
    for offset in range(0x10000,len(program)-4,2):
        pointer=b.u32(program,offset)
        if not (0xff800000<=pointer<=0xffffffff and pointer&15==0): continue
        if not b.looks_like_frame(program,b.stock_file(pointer)): continue
        group=b.frame_group(program,b.stock_address(offset),0xff800000,0xffffffff)
        if not group or len(group)<2: continue
        specs=[ui.component_spec(program,frame)for frame in group]
        if any(s[0]>=0x005199b0 or s[0]<0 or ((s[1]>>12)&7)!=6 for s in specs): continue
        left=min(-s[4]for s in specs);top=min(-s[5]for s in specs)
        right=max(-s[4]+s[2]for s in specs);bottom=max(-s[5]+s[3]for s in specs)
        if not (45<=right-left<=160 and 85<=bottom-top<=180):continue
        records.append({'group':f'{b.stock_address(offset):08X}','bounds':[left,top,right,bottom],
            'frames':[f'{f:08X}'for f in group]})
    for page in range((len(records)+39)//40):
        sheet=Image.new('RGB',(1200,1000),(40,42,48));draw=ImageDraw.Draw(sheet)
        for index,row in enumerate(records[page*40:(page+1)*40]):
            pose=render_group(program,graphics,palette,[int(f,16)for f in row['frames']])
            x,y=(index%8)*150,(index//8)*200
            sheet.paste(pose,(x+(150-pose.width)//2,y+20),pose)
            draw.text((x+3,y+3),row['group'],fill='yellow')
        sheet.save(args.output/f'kano_{page}.png')
    (args.output/'groups.json').write_text(json.dumps(records,indent=2)+'\n')
    print(f'{len(records)} original external candidates')

if __name__=='__main__':main()
