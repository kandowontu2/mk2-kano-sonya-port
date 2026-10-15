"""Import complete character-owned Friendship artwork into the MKII donor.

This changes typed group/component fields only, never command or action code.
It is not playable finisher acceptance: native MKII scene integration follows.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import build_mk2ks_mk3 as animation

KANO_BODY=tuple(range(0xff9d1c30,0xff9d1c31,0x20))+(0xff9d1c90,
    0xff9d1d10,0xff9d1d90,0xff9d1e10,0xff9d1e90,0xff9d1f10,0xff9d1f90,
    0xff9d2010,0xff9d20b0,0xff9d2150,0xff9d21f0,0xff9d2290,0xff9d2330,
    0xff9d23d0,0xff9d2470,0xff9d2510,0xff9d2590)
KANO_BUBBLE=(0xff9d2610,0xff9d2650,0xff9d2690,0xff9d26d0,
    0xff9d2710,0xff9d2750,0xff9d2790)
SONYA_BODY=(0xff9d2b90,0xff9d2bf0,0xff9d2c70,0xff9d2d10,0xff9d2db0,
    0xff9d2e50,0xff9d2ef0,0xff9d2f70,0xff9d2ff0,0xff9d3070,0xff9d30f0)
GROUPS=KANO_BODY+KANO_BUBBLE+SONYA_BODY

def sha(data):return hashlib.sha256(data).hexdigest().upper()
def check(value,message):
    if not value:raise ValueError(message)

def build(payload,original):
    check(len(payload)==0x200000 and len(original)==0x100000,'Complete original and donor required')
    check(sha(original)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651',
          'Unsupported original MK3 revision')
    before=bytes(payload);changed_fields=[];frames=set();records=[]
    def pointer(at,wanted,kind):
        old=struct.unpack_from('<I',payload,at)[0]
        native=animation.relocate_pointer(wanted)
        check(old in(wanted,native),f'Occupied {kind} field at {at:06X}')
        if old!=native:
            struct.pack_into('<I',payload,at,native)
            changed_fields.append({'offset':at,'before':old,'after':native,'kind':kind})
    for group in GROUPS:
        components=animation.frame_group(original,group,group,group+0x200)
        check(components,'Malformed original Friendship group')
        at=animation.stock_file(group)
        for index,frame in enumerate(components):
            pointer(at+index*4,frame,'group_component');frames.add(frame)
        check(struct.unpack_from('<I',payload,at+len(components)*4)[0]==0,'Lost group terminator')
        records.append({'original_group':group,'native_group':animation.relocate_pointer(group),
                        'frames':components,'effect':group in KANO_BUBBLE})
    for frame in sorted(frames):
        at=animation.stock_file(frame)
        check(payload[at:at+8]==original[at:at+8] and payload[at+12:at+14]==original[at+12:at+14],
              'Native descriptor geometry/DMA command changed')
        source=struct.unpack_from('<I',original,at+8)[0]
        old=struct.unpack_from('<I',payload,at+8)[0];native=source+animation.GFX_REBASE
        check(old in(source,native),'Native frame graphics source already changed')
        if old!=native:
            struct.pack_into('<I',payload,at+8,native)
            changed_fields.append({'offset':at+8,'before':old,'after':native,'kind':'graphics_source'})
        tail=struct.unpack_from('<I',original,at+14)[0]
        if animation.TMS_ROM_BASE<=tail<=0xffffffff and tail%16==0:
            pointer(at+14,tail,'palette_pointer')
    # The first separate bubble component owns this native 16-pen palette.
    palette=animation.stock_file(0xffcdf710)
    check(original[palette:palette+2]==struct.pack('<H',16),'Original bubble palette changed')
    check(payload[palette:palette+34]==original[palette:palette+34],'Bubble palette was overwritten')
    # Every changed byte must be explained by one typed field. No MK3 script
    # opcode, callback, command table or second-MiB gameplay data may change.
    expected=bytearray(before)
    for field in changed_fields:struct.pack_into('<I',expected,field['offset'],field['after'])
    check(expected==payload,'Unaccounted-for donor mutation')
    check(payload[0x100000:]==before[0x100000:],'Existing gameplay payload changed')
    return {'groups':records,'unique_frames':len(frames),'changed_fields':changed_fields,
            'changed_bytes':sum(a!=b for a,b in zip(before,payload)),
            'before_sha256':sha(before),'after_sha256':sha(payload),
            'bubble_palette_address':0xfecdf710,'bubble_palette_hex':original[palette:palette+34].hex(),
            'fullPortAcceptance':False,'fullFinisherAcceptance':False,
            'scope':'artwork-only import; no MK3 action code is executed'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original',type=Path);parser.add_argument('payload',type=Path)
    parser.add_argument('output',type=Path);args=parser.parse_args()
    check(not args.output.exists(),'Do not overwrite imported artwork evidence')
    donor=bytearray(args.payload.read_bytes());report=build(donor,args.original.read_bytes())
    report['input_hashes']={str(path.resolve()):sha(path.read_bytes())for path in(args.original,args.payload,Path(__file__),Path(animation.__file__))}
    args.output.mkdir(parents=True)
    (args.output/'mk2ks_friendship_art_only.mdata').write_bytes(donor)
    (args.output/'import.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key]for key in('unique_frames','changed_bytes','after_sha256','scope')},indent=2))

if __name__=='__main__':main()
