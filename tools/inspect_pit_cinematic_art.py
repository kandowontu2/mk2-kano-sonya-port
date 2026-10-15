"""Read-only native Pit II and donor reaction geometry/art inspection."""
import argparse
import json
from pathlib import Path
import build_mk2ks_mk3 as b
import upgrade_ksui_previews as ui
from audit_leg_victims import stock_gfx, stock_palette, write_sheet

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Never overwrite evidence')
    args.output.mkdir(parents=True)
    native = (args.workspace/'mk2/mk2-maincpu.bin').read_bytes()
    groups = [b.u32(native, b.stock_file(0xff85edb0)+i*4) for i in range(5)] + [0xff85f1d0]
    report = {'native_liu': write_sheet(native, stock_gfx(args.workspace), stock_palette(native, 1),
        [(str(i),g) for i,g in enumerate(groups)], 'native Pit II Liu', args.output/'native_liu.png')}
    donor = (args.workspace/'mk3/mk3-maincpu.bin').read_bytes()
    gfx = ui.load_gfx(args.workspace/'roms_v22_clean/mk2ks')
    for fighter, root, special, block in [('kano', b.KANO_MAIN,b.KANO_SPECIAL,b.KANO_BLOCK),
                                         ('sonya',b.SONYA_MAIN,b.SONYA_SPECIAL,b.SONYA_BLOCK)]:
        spans = b.sequence_spans(donor, root, block, (root,special))
        groups = []
        for index in (30,35,48,63):
            for phase,group in enumerate(dict((g,f) for _,g,f in b.group_references(donor,*spans[index],*block))):
                groups.append((f'{index}/{phase}', group))
        report[fighter] = write_sheet(donor,gfx,ui.donor_palette(donor,fighter),groups,
            f'donor {fighter}', args.output/f'{fighter}.png')
    (args.output/'art_geometry.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__ == '__main__':
    main()
