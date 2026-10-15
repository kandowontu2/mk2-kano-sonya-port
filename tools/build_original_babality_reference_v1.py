"""Decode MK3's actual baby dispatch records; never writes a playable ROM."""
from pathlib import Path
import argparse
import hashlib
import json
import struct
from PIL import Image
import upgrade_ksui_previews as ui

BASE = 0xFF800000
TABLE = 0xFFA2A5B0
FRAMES = {"kano": 0xFFC7E7A0, "sonya": 0xFFC7E950}


def offset(address):
    assert BASE <= address < 0x100000000 and address % 16 == 0
    return (address - BASE) // 8


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    assert not args.output.exists(), "Do not overwrite reference evidence"
    program_path = args.root / "mk3/mk3-maincpu.bin"
    program = program_path.read_bytes()
    assert len(program) == 0x100000
    # Original instructions load the actual victim ID, shift five and index
    # this table before single-frame construction (FFA2A350..FFA2A3C0).
    instructions = program[offset(0xFFA2A350):offset(0xFFA2A3F0)]
    expected = struct.pack("<10H", 0xB505, 0x01F0, 0x24A5, 0x0B25,
                           0xA5B0, 0xFFA2, 0x86A5, 0x0D5F, 0xCA80, 0xFF95)
    assert instructions == expected
    gfx = ui.load_gfx(args.root / "mk3")
    inputs = [program_path]
    inputs.extend(args.root / "mk3" / f"l1_mortal_kombat_3_u{chip}_game_rom.u{chip}"
                  for _, chips in ui.GFX_BANKS for chip in chips)
    report = {"source": "original_mk3_2_1", "table": TABLE,
              "victim_dispatch_instructions": instructions.hex(), "records": {},
              "input_hashes": {str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in inputs}, "fullPortAcceptance": False}
    args.output.mkdir(parents=True)
    for index, (name, frame) in enumerate(FRAMES.items()):
        assert struct.unpack_from("<I", program, offset(TABLE) + 4 * index)[0] == frame
        raw = program[offset(frame):offset(frame) + 18]
        width, height, xoff, yoff, source, command, palette_ptr = struct.unpack("<HHhhIHI", raw)
        assert (width, height) == ((27, 44) if name == "kano" else (35, 54))
        assert xoff == yoff == 0 and (command >> 12) & 7 == 5
        pal_off = offset(palette_ptr)
        count = struct.unpack_from("<H", program, pal_off)[0]
        assert 1 < count <= 32
        words = struct.unpack_from(f"<{count}H", program, pal_off + 2)
        palette = [(0, 0, 0, 0)] + [(*ui.xrgb555(value), 255) for value in words[1:]]
        palette.extend([(0, 0, 0, 0)] * (256 - len(palette)))
        picture = ui.decode_component(gfx, palette, source, command, width, height)
        picture.save(args.output / f"{name}_baby.png")
        picture.resize((width * 6, height * 6), Image.Resampling.NEAREST).save(
            args.output / f"{name}_baby_zoom.png")
        report["records"][name] = dict(original_id=index, frame=frame,
            descriptor_hex=raw.hex(), width=width, height=height, source_bits=source,
            command=command, palette_pointer=palette_ptr, palette_count=count,
            palette_hex=program[pal_off:pal_off + 2 + count * 2].hex(),
            rgba_sha256=hashlib.sha256(picture.tobytes()).hexdigest())
    (args.output / "reference.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["records"], indent=2))


if __name__ == "__main__":
    main()
