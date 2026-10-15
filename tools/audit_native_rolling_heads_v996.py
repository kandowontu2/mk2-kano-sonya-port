"""Decode original seven MKII rolling-head poses; never modify ROMs/artwork."""
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image, ImageDraw
import audit_animation_poses as poses
import audit_native_inflation_references_v931 as native
import upgrade_ksui_previews as ui

ROOT = native.ROOT
OUT = ROOT/'audit_v996_native_rolling_head_references'
FRAMES = (0xffb4a4b0,0xffb4a540,0xffb4a5b0,0xffb4a620,0xffb4a690,0xffb4a700,0xffb4a770)


def main():
    if OUT.exists():
        raise ValueError('Preserve original reference evidence')
    program=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    assert native.digest(program)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
    gfx=bytearray(0xc00000)
    pins={'mk2/mk2-maincpu.bin':native.digest(program)}
    for base,pair in enumerate(((14,19),(16,20),(17,22))):
        for lane,(side,chip) in enumerate((('g',pair[0]),('j',pair[0]),('g',pair[1]),('j',pair[1]))):
            name=f'mk2/l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}'
            data=(ROOT/name).read_bytes()
            assert len(data)==0x100000
            pins[name]=native.digest(data)
            gfx[base*0x400000+lane:base*0x400000+lane+len(data)*4:4]=data
    OUT.mkdir()
    sheet=Image.new('RGBA',(1120,180),(35,35,40,255))
    draw=ImageDraw.Draw(sheet)
    records=[]
    for index,frame in enumerate(FRAMES):
        palette_pointer=struct.unpack_from('<I',program,native.off(frame)+14)[0]
        palette=native.palette(program,palette_pointer)
        spec=ui.component_spec(program,frame)
        image=poses.render_group(program,gfx,palette,(frame,))
        image.save(OUT/f'liu-head-{index}.png')
        scaled=image.resize((image.width*4,image.height*4),Image.Resampling.NEAREST)
        sheet.alpha_composite(scaled,(index*160+(160-scaled.width)//2,170-scaled.height))
        draw.text((index*160+3,3),f'head {index}: {frame:08X}',fill='white')
        draw.text((index*160+3,17),f'offset {spec[4:]}',fill='white')
        records.append(dict(pose=index,descriptor=f'{frame:08X}',spec=spec,palette=f'{palette_pointer:08X}',size=list(image.size)))
    sheet.save(OUT/'liu-seven-heads-native-order.png')
    (OUT/'reference.json').write_text(json.dumps(dict(scope='original seven native head poses and anchors only',inputHashes=pins,frames=records,romWrites=0),indent=2)+'\n')
    print(json.dumps(dict(poses=7,romWrites=0,output=str(OUT))))


if __name__=='__main__':
    main()
