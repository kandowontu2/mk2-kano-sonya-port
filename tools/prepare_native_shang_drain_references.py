"""Small ROM-art authoring references; no game/ROM writes or visual acceptance."""
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image, ImageDraw
import audit_animation_poses as poses
import build_mk2ks_mk3 as animation
import upgrade_ksui_previews as ui

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'art_reference_native_shang_drain'


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def main():
    if OUT.exists():
        raise ValueError('Never overwrite executed authoring references')
    stock_path, donor_path = ROOT / 'mk2/mk2-maincpu.bin', ROOT / 'mk3/mk3-maincpu.bin'
    stock, donor = stock_path.read_bytes(), donor_path.read_bytes()
    assert sha(stock) == '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
    assert sha(donor) == '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    pins = {str(stock_path): sha(stock), str(donor_path): sha(donor),
            str(Path(__file__)): sha(Path(__file__).read_bytes())}
    gfx = bytearray(0xc00000)
    for bank, pair in enumerate(((14, 19), (16, 20), (17, 22))):
        for lane, (side, chip) in enumerate((('g', pair[0]), ('j', pair[0]), ('g', pair[1]), ('j', pair[1]))):
            path = ROOT / 'mk2' / f'l1_mortal_kombat_ii_game_rom_u{side}{chip}.u{side}{chip}'
            raw = path.read_bytes()
            assert len(raw) == 0x100000
            pins[str(path)] = sha(raw)
            gfx[bank * 0x400000 + lane:bank * 0x400000 + lane + len(raw) * 4:4] = raw
    donor_gfx = ui.load_gfx(ROOT / 'mk3')
    for _, chips in ui.GFX_BANKS:
        for chip in chips:
            path = ROOT / 'mk3' / f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            pins[str(path)] = sha(path.read_bytes())
    images, records = {}, {}
    atlas = Image.new('RGBA', (720, 640), (32, 32, 38, 255))
    draw = ImageDraw.Draw(atlas)
    for row, (name, ident) in enumerate((('Liu native male', 1), ('Kitana native female', 4))):
        stream = animation.u32(stock, animation.stock_file(0xff9d7770) + ident * 4)
        groups = [animation.u32(stock, animation.stock_file(stream) + i * 4) for i in range(3)]
        assert animation.u32(stock, animation.stock_file(stream) + 12) == 0
        words = struct.unpack_from('<9I', stock, animation.stock_file(stream))
        assert words == (groups[0], groups[1], groups[2], 0,
                         groups[1], groups[0], groups[1], groups[2], 0)
        info = []
        for col, group in enumerate(groups):
            parts = animation.frame_group(stock, group, 0xff800000, 0xffffffff)
            assert parts
            palette_address = animation.u32(stock, animation.stock_file(parts[0]) + 14)
            at = animation.stock_file(palette_address)
            count = animation.u16(stock, at)
            assert 1 < count <= 256
            palette = [(*ui.xrgb555(animation.u16(stock, at + 2 + i * 2)), 255 if i else 0)
                       for i in range(count)]
            palette += [(0, 0, 0, 255)] * (256 - len(palette))
            im = poses.render_group(stock, gfx, palette, parts)
            specs = [ui.component_spec(stock, f) for f in parts]
            bounds = [min(-s[4] for s in specs), min(-s[5] for s in specs),
                      max(-s[4] + s[2] for s in specs), max(-s[5] + s[3] for s in specs)]
            scaled = im.resize((im.width * 2, im.height * 2), Image.Resampling.NEAREST)
            atlas.alpha_composite(scaled, (col * 240 + (240 - scaled.width) // 2,
                                          row * 320 + 40 + 260 - scaled.height))
            draw.text((col * 240 + 6, row * 320 + 8), f'{name} phase {col + 1}', fill='white')
            draw.text((col * 240 + 6, row * 320 + 23), f'Native size {im.size}; {group:08X}', fill='white')
            info.append(dict(group=f'{group:08X}', parts=[f'{f:08X}' for f in parts],
                             specs=specs, bounds=bounds, size=list(im.size), rgbaSHA256=sha(im.tobytes())))
        records[name] = dict(identity=ident, stream=f'{stream:08X}', phases=info,
                             scriptWords=[f'{v:08X}' for v in words])
    images['original-mk2-drain-phases.png'] = atlas
    for name, root, special, block in (('kano', animation.KANO_MAIN, animation.KANO_SPECIAL, animation.KANO_BLOCK),
                                       ('sonya', animation.SONYA_MAIN, animation.SONYA_SPECIAL, animation.SONYA_BLOCK)):
        atlas = Image.new('RGBA', (720, 360), (32, 32, 38, 255))
        draw = ImageDraw.Draw(atlas)
        spans = animation.sequence_spans(donor, root, block, (root, special))
        pal = ui.donor_palette(donor, name)
        info = []
        for col, (index, label) in enumerate(((0, 'normal body'), (37, 'dizzy body'), (28, 'recoil body'))):
            refs = animation.group_references(donor, *spans[index], *block)
            assert refs
            _, group, parts = refs[0]
            im = poses.render_group(donor, donor_gfx, pal, parts)
            scaled = im.resize((im.width * 2, im.height * 2), Image.Resampling.NEAREST)
            assert scaled.width < 232 and scaled.height < 320
            atlas.alpha_composite(scaled, (col * 240 + (240 - scaled.width) // 2,
                                          340 - scaled.height))
            draw.text((col * 240 + 6, 8), f'{name}: {label}', fill='white')
            draw.text((col * 240 + 6, 23), f'{group:08X}, native {im.size}', fill='white')
            info.append(dict(animation=index, group=f'{group:08X}', parts=[f'{f:08X}' for f in parts],
                             size=list(im.size), rgbaSHA256=sha(im.tobytes())))
        records[name] = info
        images[name + '-own-native-body.png'] = atlas
    assert all(sha(Path(p).read_bytes()) == h for p, h in pins.items())
    OUT.mkdir()
    files = {}
    for name, im in images.items():
        path = OUT / name
        im.save(path)
        files[str(path)] = sha(path.read_bytes())
    report = dict(passed=True, scope=__doc__, records=records, inputHashes=pins,
                  referenceImageHashes=files, gameWrites=0, nativeRuntimeAccepted=False,
                  artAccepted=False, fullPortAcceptance=False)
    (OUT / 'reference.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=True, referenceImages=list(files), gameWrites=0,
                         nativeRuntimeAccepted=False, artAccepted=False)))


if __name__ == '__main__':
    main()
