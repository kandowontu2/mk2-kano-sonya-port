"""Decode original split/arm-rip references; never synthesize replacement art."""
import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
import audit_animation_poses as poses
import audit_native_inflation_references_v931 as native
import upgrade_ksui_previews as ui

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_v1022_native_split_arm_references'
ROM_SHA = '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
TABLES = {
    'kung_lao_split_stream': (0xff8cf110, 0xff8cea70),
    'jax_arm_body_stream': (0xff9f57b0, 0xff8bf180),
    'jax_arm_body_position': (0xff8bef70, 0xff8bf2b0),
    'jax_detached_arm_stream': (0xff8bf790, 0xff8be5b0),
    'jax_head_clap_position': (0xff8c7ff0, 0xff8c7b50),
}

def sha(data):
    return hashlib.sha256(data).hexdigest().upper()

def main():
    if OUT.exists():
        raise ValueError('Never overwrite reference evidence')
    program = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    assert sha(program) == ROM_SHA
    read = lambda address: struct.unpack_from('<I', program, native.off(address))[0]
    gfx = bytearray(0xc00000)
    pins = {'mk2/mk2-maincpu.bin': sha(program)}
    for base, pair in enumerate(((14, 19), (16, 20), (17, 22))):
        for lane, (side, chip) in enumerate((('g', pair[0]), ('j', pair[0]), ('g', pair[1]), ('j', pair[1]))):
            name = f'mk2/l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}'
            data = (ROOT / name).read_bytes()
            assert len(data) == 0x100000
            pins[name] = sha(data)
            gfx[base*0x400000+lane:base*0x400000+lane+len(data)*4:4] = data
    report = {'scope': 'immutable_original_rom_reference_only', 'inputHashes': pins,
              'romWrites': 0, 'replacementArtworkAccepted': False, 'tables': {}, 'fighters': {}}
    for name, (table, operand) in TABLES.items():
        assert read(operand) == table
        report['tables'][name] = {'table': f'{table:08X}', 'operand': f'{operand:08X}',
            'originalIndexedWords0to18': [f'{read(table+index*32):08X}' for index in range(19)],
            'warning': 'Rows17/18 are adjacent data/code, not added-character definitions.'}
    OUT.mkdir()
    for name, identity in (('liu', 1), ('kitana', 4)):
        palette_address = read(0xff90c900+identity*64)
        palette = native.palette(program, palette_address)
        records = {}
        for kind, table_name, count in (('split', 'kung_lao_split_stream', 12),
                ('arm_body', 'jax_arm_body_stream', 6), ('detached_arm', 'jax_detached_arm_stream', 6)):
            stream = read(TABLES[table_name][0]+identity*32)
            words = [read(stream+index*32) for index in range(count)]
            if kind == 'split':
                assert words[3] == words[11] == 0
            else:
                assert words[5] == 0
            sheet = Image.new('RGBA', (240*6, 220*((count+5)//6)), (35,35,40,255))
            draw = ImageDraw.Draw(sheet)
            frames = []
            for index, group in enumerate(words):
                if not group:
                    continue
                components = [group] if kind == 'detached_arm' else []
                if kind != 'detached_arm':
                    for item in range(8):
                        value = read(group+item*32)
                        if not value:
                            break
                        components.append(value)
                    else:
                        raise ValueError('Unbounded original composite')
                specs = [ui.component_spec(program, component) for component in components]
                bounds = [min(-s[4] for s in specs),min(-s[5] for s in specs),
                          max(-s[4]+s[2] for s in specs),max(-s[5]+s[3] for s in specs)]
                image = poses.render_group(program,gfx,palette,components)
                filename = f'{name}-{kind}-{index}.png'
                image.save(OUT / filename)
                scaled = image.resize((image.width*2,image.height*2),Image.Resampling.NEAREST)
                if scaled.height>185 or scaled.width>230:
                    scaled=image
                x,y=index%6*240,index//6*220
                sheet.alpha_composite(scaled,(x+(240-scaled.width)//2,y+215-scaled.height))
                draw.text((x+3,y+3),f'{kind} {index}: {bounds}',fill='white')
                draw.text((x+3,y+17),f'{group:08X}',fill='white')
                frames.append({'index':index,'pointer':f'{group:08X}',
                    'components':[f'{v:08X}' for v in components],'specs':specs,
                    'bounds':bounds,'file':filename,'rgbaSHA256':sha(image.tobytes())})
            sheet.save(OUT/f'{name}-{kind}-reference.png')
            records[kind]={'stream':f'{stream:08X}','words':[f'{v:08X}' for v in words],
                           'palette':f'{palette_address:08X}','frames':frames}
        report['fighters'][name]=records
    (OUT/'reference.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'output':str(OUT),'reference_only':True,'rom_writes':0}))

if __name__ == '__main__':
    main()
