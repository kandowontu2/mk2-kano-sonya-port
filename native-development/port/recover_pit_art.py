"""Recover ONLY existing authored Pit sprite DATA, never old game/driver code."""
import io
import json
import re
import struct
import sys
import zipfile
from PIL import Image
import import_character_art as art

HERE=art.HERE
SRC=HERE.parent/'baseline/mk2-rebuild-main/srcp'
PACKAGE=art.ROOT/'release_mk2_kano_sonya_20261015_player/MK2_Kano_Sonya_20261015_PLAYER.zip'

def main():
    out=HERE/'generated_pit'
    assert not out.exists() or not any(out.iterdir()) or '--refresh-generated' in sys.argv
    with zipfile.ZipFile(PACKAGE) as z:
        with zipfile.ZipFile(io.BytesIO(z.read('MK2_Kano_Sonya/roms/mk2ks.zip'))) as roms:
            donor=roms.read('mk2ks.mdata')
    assert art.sha(donor)=='A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3'
    assert donor[0x130000:0x130004]==b'KPT2'
    pixel_at,pixel_size,gfx_dest,table,seq0,seq1,count,frame_count,coordinates=struct.unpack_from('<9I',donor,0x130004)
    assert (pixel_at,gfx_dest,count,frame_count)==(0x134000,0x1e80000,19,12)
    def old_at(address):
        assert 0xfe800000<=address<0xff800000 and address%8==0
        return (address-0xfe800000)//8
    symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
    rom=bytearray(1048576)
    for lane in [0,1]:rom[lane::2]=b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
    prefix=(HERE/'generated_friendship/fighter_ui_finish_friend_graphics.bin').read_bytes()
    packed=bytearray(prefix);lines=['; Recovered authored dedicated Pit sprite DATA only, no old executable payload.',
                                  '        .include mainequ.asm',
                                  '        .ref ks_kano_primary_palette,ks_sonya_primary_palette','        .data']
    records={};out.mkdir(exist_ok=True)
    for actor,name,sequence in [(17,'kano',seq0),(18,'sonya',seq1)]:
        assert struct.unpack_from('<I',donor,old_at(table)+actor*4)[0]==sequence
        words=struct.unpack_from('<10I',donor,old_at(sequence))
        assert words[5:8]==(1,sequence,0) and words[-1]==0
        groups=list(words[:5])+[words[8]]
        assert len(set(groups))==6
        coordinate=struct.unpack_from('<I',donor,old_at(coordinates)+actor*4)[0]
        assert coordinate==(64<<16)|192
        pal_at=(symbols[f'ks_{name}_primary_palette']-0xff800000)//8
        assert struct.unpack_from('<H',rom,pal_at)[0]==65
        colors=struct.unpack_from('<65H',rom,pal_at+2)
        assert colors[0]==0
        frames=[]
        for phase,group in enumerate(groups):
            frame,zero=struct.unpack_from('<2I',donor,old_at(group));assert zero==0
            w,h,x,y,sag,ctrl=struct.unpack_from('<4hIH',donor,old_at(frame))
            assert 0<w<256 and 0<h<256 and ctrl==0x6000 and sag%8==0
            start=pixel_at+(sag//8-gfx_dest);size=(w*h*6+7)//8
            assert pixel_at<=start and start+size<=pixel_at+pixel_size
            raw=donor[start:start+size];offset=len(packed);packed.extend(raw)
            label=f'ks_pit_{name}_frame{phase}'
            lines += [label,f'        .word {w},{h},{x},{y}',f'        .long 0{(0xc00000+offset)*8:08x}h',
                      '        .word 06000h',f'        .long ks_{name}_primary_palette',
                      f'ks_pit_{name}_pose{phase}',f'        .long {label},0']
            rgba=[]
            for i in range(w*h):
                bit=i*6;index=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit&7))&63
                c=colors[index]
                rgba.append(tuple(((c>>s)&31)*8+((c>>s)&31)//4 for s in (10,5,0))+(255 if index else 0,))
            image=Image.new('RGBA',(w,h));image.putdata(rgba);image.save(out/f'{name}_{phase}.png')
            frames.append(dict(phase=phase,width=w,height=h,xOffset=x,yOffset=y,sourceFrame=hex(frame),
                               packedByteOffset=offset,compressedSHA256=art.sha(raw),pixelSHA256=art.sha(bytes(v for px in rgba for v in px))))
        lines += [f'        .def ks_pit_{name}_sequence',f'ks_pit_{name}_sequence']
        lines += [f'        .long ks_pit_{name}_pose{i}' for i in range(5)]
        lines += [f'        .long ani_jump,ks_pit_{name}_sequence,0',f'        .long ks_pit_{name}_pose5,0']
        records[name]=dict(actorID=actor,coordinate=coordinate,frames=frames)
    assert packed[:len(prefix)]==prefix and len(packed)<0x600000
    source=('\n'.join(lines)+'\n').encode();(out/'KSPITART.ASM').write_bytes(source)
    (out/'fighter_ui_finish_pit_graphics.bin').write_bytes(packed)
    region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(0x600000);sockets={}
    for bank,size in [(0,0x100000),(1,0x80000)]:
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane;raw=region[start:start+size*4:4]
            assert len(raw)==size
            (out/name).write_bytes(raw);rebuilt[start:start+size*4:4]=raw;sockets[name]=art.sha(raw)
    assert rebuilt==region
    report=dict(sourceKind='recovered previously authored Pit draft sprites; NOT original MK3 digitized poses',
                sourcePayloadSHA256=art.sha(donor),sourceSHA256=art.sha(source),records=records,
                prefixSHA256=art.sha(prefix),prefixBytes=len(prefix),appendedBytes=len(packed)-len(prefix),
                totalGraphicsBytes=len(packed),stockSocketRoundTripVerified=True,sockets=sockets,
                oldExecutableCodeImported=False,visualAcceptance=False,runtimeVerified=False,releaseReady=False)
    (out/'PIT_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('records','sockets')},indent=2))

if __name__=='__main__':main()
