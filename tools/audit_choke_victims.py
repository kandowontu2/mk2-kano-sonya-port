"""Render original neck-grab and own MKII pain poses for contact adaptation."""
import argparse
import json
from pathlib import Path

import build_mk2ks_mk3 as b
import upgrade_ksui_previews as ui
from audit_leg_victims import NAMES, stock_gfx, stock_palette, stock_phases, write_sheet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    stock = (args.workspace / "mk2/mk2-maincpu.bin").read_bytes()
    donor = (args.workspace / "mk3/mk3-maincpu.bin").read_bytes()
    sgfx = stock_gfx(args.workspace)
    dgfx = ui.load_gfx(args.workspace / "roms_v22_clean/mk2ks")
    report = {}
    for fighter, root in (("kano", b.KANO_MAIN), ("sonya", b.SONYA_MAIN)):
        pairs = b.choke_victim_operands(donor, fighter)
        groups = [(f"victim {i}", b.u32(donor, end)) for i, (_, end) in enumerate(pairs)]
        if fighter == "kano":
            groups += [(f"grabber {i}", pointer) for i, pointer in enumerate(
                (0xFF8304E0, 0xFF830540, 0xFF8305A0, 0xFF830600, 0xFF830660, 0xFF8306C0))]
        report[fighter] = write_sheet(donor, dgfx, ui.donor_palette(donor, fighter), groups,
            "choke_" + fighter, args.output / f"{fighter}_original.png", grid=True)
    for fighter_id, name in enumerate(NAMES[:12]):
        root = b.u32(stock, b.MK2_MAIN_TABLE + fighter_id * 4)
        groups = [(f"pain {i}", pointer) for i, pointer in enumerate(stock_phases(stock, root, 16, 1))]
        groups += [("fall 0", stock_phases(stock, root, 15, 1)[0])]
        report[name] = write_sheet(stock, sgfx, stock_palette(stock, fighter_id), groups,
            "choke_" + name, args.output / f"{name}_options.png", grid=True)
    (args.output / "pose-inventory.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Rendered {len(report)} original-pose sheets to {args.output}")


if __name__ == "__main__":
    main()
