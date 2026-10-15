"""Decode original opposite split-half streams and selector grammar only."""
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image,ImageDraw
import audit_animation_poses as poses
import audit_native_inflation_references_v931 as native
import upgrade_ksui_previews as ui

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v1094_native_split_opposite_references'
SHA='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    if OUT.exists():raise ValueError('Preserve original reference evidence')
    path=ROOT/'mk2/mk2-maincpu.bin';program=path.read_bytes();assert digest(path)==SHA
    read=lambda at:struct.unpack_from('<I',program,native.off(at))[0]
    read16=lambda at:struct.unpack_from('<H',program,native.off(at))[0]
    gfx=bytearray(0xc00000);pins={str(path):SHA}
    for base,pair in enumerate(((14,19),(16,20),(17,22))):
        for lane,(side,chip) in enumerate((('g',pair[0]),('j',pair[0]),('g',pair[1]),('j',pair[1]))):
            path=ROOT/f'mk2/l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}'
            data=path.read_bytes();assert len(data)==0x100000;pins[str(path)]=digest(path)
            gfx[base*0x400000+lane:base*0x400000+lane+len(data)*4:4]=data
    OUT.mkdir();fighters={}
    for name,identity in (('liu',1),('kitana',4),('mileena',5)):
        table=read(0xff906150+identity*32);original=read(table);cursor=original;selectors=[]
        # Follow ONLY original token8/id16/pointer32 selectors exactly as the
        # real FF8CECF0..FF8CEDD0 parser does; preserve the unaligned ID word.
        while read(cursor)==8:
            wanted=read16(cursor+32);target=read(cursor+48)
            selectors.append({'tokenAddress':f'{cursor:08X}','idWord':wanted,'target':f'{target:08X}'})
            cursor+=48
            if identity==wanted:cursor=target;break
            cursor+=32
        words=[read(cursor+index*32) for index in range(9)]
        assert words[7]==1 and words[8]==cursor
        palette_address=read(0xff90c900+identity*64)
        palette=native.palette(program,palette_address)
        frames=[];sheet=Image.new('RGBA',(240*4,230*2),(35,35,40,255));draw=ImageDraw.Draw(sheet)
        for index,group in enumerate(words[:7]):
            components=[]
            for item in range(8):
                component=read(group+item*32)
                if component==0:break
                components.append(component)
            else:raise ValueError('Unbounded original composite')
            assert components
            specs=[ui.component_spec(program,c) for c in components]
            bounds=[min(-s[4]for s in specs),min(-s[5]for s in specs),
                    max(-s[4]+s[2]for s in specs),max(-s[5]+s[3]for s in specs)]
            picture=poses.render_group(program,gfx,palette,components)
            path=OUT/f'{name}-opposite-{index}.png';picture.save(path);pins[str(path)]=digest(path)
            scaled=picture.resize((picture.width*2,picture.height*2),Image.Resampling.NEAREST)
            if scaled.height>190 or scaled.width>230:scaled=picture
            x=index%4*240;y=index//4*230
            sheet.alpha_composite(scaled,(x+(240-scaled.width)//2,y+225-scaled.height))
            draw.text((x+3,y+3),f'{name} opposite {index}: {bounds}',fill='white')
            frames.append({'index':index,'pointer':f'{group:08X}','components':[f'{c:08X}'for c in components],
                           'specs':specs,'bounds':bounds,'file':path.name})
        path=OUT/f'{name}-opposite-reference.png';sheet.save(path);pins[str(path)]=digest(path)
        fighters[name]={'actualID':identity,'table':f'{table:08X}','originalSpecial0':f'{original:08X}',
                        'selectedStream':f'{cursor:08X}','originalSelectors':selectors,
                        'words':[f'{word:08X}'for word in words],'frames':frames}
    report={'scope':'immutable original opposite vertical split-half reference only',
            'romWrites':0,'replacementArtworkAccepted':False,'fighters':fighters,'inputHashes':pins}
    (OUT/'reference.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'output':str(OUT),'fighters':list(fighters),'romWrites':0}))


if __name__=='__main__':main()
