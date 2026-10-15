"""Stage authentic eight-frame kiss art; this alone is NOT a playable release.

The current driver deliberately still requires its seven-frame payload. The
new file is input for the native trajectory implementation, not the launcher.
"""
import argparse
import hashlib
import json
from pathlib import Path

import build_native_kiss as kiss


def upgrade(current, program, gfx_directory):
    blank = bytearray(current)
    blank[kiss.HEADER:kiss.END] = b'\xff' * (kiss.END-kiss.HEADER)
    legacy = bytearray(blank)
    kiss.build(legacy, program, gfx_directory)
    if bytes(legacy) != current:
        raise ValueError('Current kiss section does not reproduce the seven-frame conversion')
    report = kiss.build(blank, program, gfx_directory, include_arc_frame=True)
    if blank[:kiss.HEADER] != current[:kiss.HEADER]:
        raise ValueError('Unrelated character payload was modified')
    # Palette and original seven descriptors/pixels must remain byte-for-byte.
    for first,last in ((kiss.PALETTE,kiss.PALETTE+130),
                       (kiss.FRAMES,kiss.FRAMES+7*kiss.FRAME_STRIDE)):
        if blank[first:last] != current[first:last]:
            raise ValueError('Existing kiss palette or descriptors changed')
    report['scope'] = 'staged_eight_frame_art_not_runtime_acceptance'
    return bytes(blank), report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('current',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    if args.output.exists():
        raise SystemExit('Refusing to overwrite staged payload evidence')
    original=(root/'mk3/mk3-maincpu.bin').read_bytes()
    current=args.current.read_bytes()
    result,report=upgrade(current,original,root/'mk3')
    args.output.mkdir(parents=True)
    (args.output/'mk2ks.mdata').write_bytes(result)
    report.update(input_sha256=hashlib.sha256(current).hexdigest(),
                  output_sha256=hashlib.sha256(result).hexdigest(),
                  original_rom_sha256=hashlib.sha256(original).hexdigest())
    (args.output/'asset_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
