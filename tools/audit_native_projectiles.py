"""Render the exact native projectile payload (not the donor preview path)."""
import argparse
import json
import struct
from pathlib import Path
from PIL import Image, ImageDraw
from build_native_projectiles import BASE, GFX_DEST, PIXELS
from upgrade_ksui_previews import extract_bits, xrgb555

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("build", type=Path)
args = parser.parse_args()
payload = (args.build / "mk2ks.mdata").read_bytes()
report = json.loads((args.build / "mk2ks-build-report.json").read_text())
sheet = Image.new("RGB", (800, 240), (45, 45, 45))
draw = ImageDraw.Draw(sheet)
for row, fighter in enumerate(("kano", "sonya")):
    for slot, frame in enumerate(report["native_projectiles"][fighter]["frames"]):
        address = int(frame["native"], 16)
        width, height, xo, yo, source, command, palette = struct.unpack_from("<4hIHI", payload, (address - BASE) // 8)
        colors = struct.unpack_from("<64H", payload, (palette - BASE) // 8 + 2)
        for y in range(height):
            for x in range(width):
                index = extract_bits(payload, PIXELS * 8 + source - GFX_DEST * 8 + (y * width + x) * 6, 63)
                if index:
                    sheet.putpixel((slot * 80 + x, row * 120 + 25 + y), xrgb555(colors[index]))
        draw.text((slot * 80, row * 120 + 5), f"{fighter} {slot}", fill="white")
sheet.save(args.build / "native_projectiles.png")
