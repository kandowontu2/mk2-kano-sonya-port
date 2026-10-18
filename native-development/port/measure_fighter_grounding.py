"""Measure opaque stance soles, rather than copying descriptor heights."""
import json
import sys
import zipfile
from pathlib import Path
import import_character_art as art
sys.path.insert(0,str(art.ROOT/'tools'))
from audit_animation_poses import render_group
from upgrade_ksui_previews import component_spec
p=art.parser
def program(z,low,high):
    a=z.read(low);b=z.read(high);out=bytearray(len(a)+len(b));out[::2]=a;out[1::2]=b;return out
def main():
    transparent=[(0,0,0,0)]+[(255,255,255,255)]*255
    report={}
    for game in ('mk2','mk3'):
        path=art.ROOT/('roms/mk2.zip' if game=='mk2' else 'mk3.zip')
        with zipfile.ZipFile(path) as z:
            if game=='mk2':
                data=program(z,'l3.1_mortal_kombat_ii_game_rom_uj12.uj12','l3.1_mortal_kombat_ii_game_rom_ug12.ug12')
                gfx=bytearray(0xc00000)
                for bank,(first,second) in enumerate([(14,19),(16,20),(17,22)]):
                    for lane,(side,chip) in enumerate([('g',first),('j',first),('g',second),('j',second)]):
                        b=z.read(f'l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}')
                        a=bank*0x400000+lane;gfx[a:a+len(b)*4:4]=b
                names=['kung_lao','liu','johnny_cage','baraka','kitana','mileena','shang_tsung','raiden','sub_zero','reptile','scorpion','jax']
                offsets=[140,133,140,140,133,133,129,140,131,131,131,139]
                actors=[]
                for index,(name,offset) in enumerate(zip(names,offsets)):
                    root=p.u32(data,p.MK2_MAIN_TABLE+index*4)
                    special=p.u32(data,p.MK2_SPECIAL_TABLE+index*4)
                    actors.append((name,root,special,(root,0xff9a5b00),offset))
            else:
                data=program(z,'mk321u54.bin','mk321u63.bin');gfx=bytearray(0x1200000)
                for bank in range(5):
                    for lane in range(4):
                        chip=133-bank*4-lane;b=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
                        a=bank*0x400000+lane;gfx[a:a+len(b)*4:4]=b
                actors=[('kano',p.KANO_MAIN,p.KANO_SPECIAL,p.KANO_BLOCK,None),('sonya',p.SONYA_MAIN,p.SONYA_SPECIAL,p.SONYA_BLOCK,None)]
        for name,root,special,block,baseline in actors:
            span=p.sequence_spans(data,root,block,(root,special))[0]
            groups=p.group_references(data,*span,*(block if game=='mk3' else (0xff800000,0xffffffff)))
            assert groups,(game,name)
            entries=[]
            for _,address,frames in groups:
                specs=[component_spec(data,a) for a in frames]
                top=min(-s[5] for s in specs)
                image=render_group(data,gfx,transparent,frames);bounds=image.getbbox();assert bounds
                entries.append(dict(pose=f'{address:08x}',opaqueSoleExclusiveY=top+bounds[3],
                                    descriptorBottom=max(-s[5]+s[3] for s in specs)))
            soles=[min(x['opaqueSoleExclusiveY'] for x in entries),max(x['opaqueSoleExclusiveY'] for x in entries)]
            report[name]=dict(poses=entries,opaqueSoleRange=soles,baselineNativeGroundOffset=baseline,
                             renderedSoleRelativeToGround=[x-baseline for x in soles] if baseline is not None else None)
    (art.HERE/'GROUNDING_MEASUREMENTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:{n:v for n,v in r.items() if n!='poses'} for k,r in report.items()},indent=2))
if __name__=='__main__':main()
