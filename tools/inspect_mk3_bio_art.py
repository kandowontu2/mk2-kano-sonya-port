"""Read-only census of original MK3 biography and ending background records."""
from pathlib import Path
import struct
from upgrade_ksui_previews import load_gfx
from decode_native_picture import decode
import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()

root=Path(__file__).resolve().parents[1]
program=(root/'mk3/mk3-maincpu.bin').read_bytes()
gfx=load_gfx(root/'mk3')
def offset(a): return (a-0xff800000)//8
for scene in (13,19,20):
    flag,pointer=struct.unpack_from('<HI',program,offset(0xff928740)+scene*6)
    bank=flag*0x800000
    address=bank+(pointer-0x02000000)//8
    print(f'scene={scene} flag={flag} pointer={pointer:08X} gfx_offset={address:08X}')
    print(struct.unpack_from('<32H',gfx,address))
    if args.output:
        args.output.mkdir(parents=True,exist_ok=True)
        image,report=decode(gfx,address)
        image.save(args.output/f'original_mk3_scene_{scene}.png')
        (args.output/f'original_mk3_scene_{scene}.json').write_text(json.dumps(report,indent=2)+'\n')
