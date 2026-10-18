"""Independent own nut-punch graphics/socket/linked-header verification."""
import hashlib
import json
from pathlib import Path
import re
import struct
from current_graphics import graphics_metadata
PORT=Path(__file__).resolve().parent;BUILD=PORT.parent/'baseline/mk2-rebuild-main/srcp'
graphics_metadata() # Validate the authoritative latest graphics chain separately.
metadata=json.loads((PORT/'generated_nut/NUT_DATA.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
lanes=[b''.join((BUILD/f'rom/P12{p}.{i}').read_bytes() for p in ('F8','FC')) for i in (0,1)]
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
def read(a,fmt):return struct.unpack_from('<'+fmt,program,(a-0xff800000)//8)
folder=PORT/'generated_nut';region=bytearray(0x600000)
for bank,size in ((0,0x100000),(1,0x80000)):
    for lane in range(4):
        chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
        raw=(folder/name).read_bytes();assert len(raw)==size
        start=bank*0x400000+lane;region[start:start+size*4:4]=raw
packed=(folder/'fighter_ui_finish_nut_graphics.bin').read_bytes()
assert region[:len(packed)]==packed and not any(region[len(packed):])
for frame in metadata['frames']:
    phase=frame['phase'];path=PORT/'assets/nut'/frame['file'];raw=path.read_bytes()
    assert sha(raw)==frame['fileSHA256']
    words=' '.join(line.split('#',1)[0] for line in raw.decode('ascii').splitlines()).split()
    assert words[0]=='P2'
    w,h,maximum=map(int,words[1:4]);indices=bytes(map(int,words[4:]))
    assert (w,h,maximum)==(frame['width'],frame['height'],63) and len(indices)==w*h
    assert sha(indices)==frame['indexSHA256'] and max(indices)<=63
    pointer=symbols[f'ks_nut_kano_frame{phase}']
    assert read(symbols[f'ks_nut_kano_pose{phase}'],'II')==(pointer,0)
    header=read(pointer,'HHhhIHI')
    assert header==(w,h,frame['xOffset'],frame['yOffset'],(0xc00000+frame['packedByteOffset'])*8,0x6000,symbols['ks_kano_primary_palette'])
    assert h-header[3]==131
    start=header[4]//8-0xc00000;size=(w*h*6+7)//8
    payload=region[start:start+size];assert sha(payload)==frame['packedSHA256']
    bits=int.from_bytes(payload,'little')
    assert bytes(bits>>(i*6)&63 for i in range(w*h))==indices
poses=[symbols[f'ks_nut_kano_pose{i}'] for i in range(2)]
root=symbols['ks_kano_nutcrunched']
assert read(symbols['ks_kano_anitab1']+54*32,'I')==(root,)
assert read(root,'IIIII')==(poses[0],poses[1],0,poses[0],0)
assert metadata['frames'][0]['uniformScale']==metadata['frames'][1]['uniformScale']
report=dict(ownFrames=2,independentSixBitDecodeVerified=True,stockSocketReassemblyVerified=True,
    nativeHeadersAndPaletteVerified=True,ownGroundPlane=131,nativeTwoPartScriptVerified=True,
    fullVisualAcceptance=False,fullPortVerified=False)
(folder/'NUT_ASSET_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
