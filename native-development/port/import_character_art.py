"""Generate typed TI assembly DATA from user-supplied MK3 character art.

This is not an opcode dump. Image records, palettes and composite pose lists
are separately named and linked. No FE800000 memory region, tagged DMA address,
CPU palette interception or MAME initialization converter is required by them.
Not yet connected to the rebuilt roster; animation control translation follows.
"""
import hashlib
import json
from pathlib import Path
import struct
import zipfile
import native_art_records as parser

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def sha(b): return hashlib.sha256(b).hexdigest().upper()
def word(v): return f'0{v & 65535:04x}h'
def bitstream(gfx, source, width, height, control):
    bpp=(control>>12)&7 or 8
    cursor=source
    if control&0x80:
        for _ in range(height):
            byte=cursor>>3
            skip=((gfx[byte]|(gfx[byte+1]<<8))>>(cursor&7))&255
            pre=(skip&15)<<((control>>8)&3)
            post=(skip>>4)<<((control>>10)&3)
            cursor+=8+max(0,width-pre-post)*bpp
    else: cursor+=width*height*bpp
    bits=cursor-source
    assert bits>0 and cursor<=len(gfx)*8
    payload=(int.from_bytes(gfx[source//8:(cursor+7)//8],'little')>>(source&7))&((1<<bits)-1)
    return payload.to_bytes((bits+7)//8,'little'),bits
def main(output=None):
    gfx=bytearray(0x1200000)
    with zipfile.ZipFile(ROOT/'mk3.zip') as z:
        lo=z.read('mk321u54.bin'); hi=z.read('mk321u63.bin')
        for bank in range(5):
            for lane in range(4):
                chip=133-bank*4-lane
                payload=z.read(f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}')
                base=bank*0x400000+lane
                gfx[base:base+len(payload)*4:4]=payload
    data=bytearray(len(lo)+len(hi)); data[::2]=lo; data[1::2]=hi
    assert len(data)==0x100000
    report=dict(inputProgramSHA256=sha(data),hardware='unmodified Wolf-unit',
                metadataInProgramROM=True,customCPUHooks=False,customDMAHooks=False,fighters={})
    generated=Path(output) if output is not None else HERE/'generated_packed'
    packed=bytearray(); streams={}; verified=0
    for fighter,block,offsets in [('kano',parser.KANO_BLOCK,(0x92bbc,0x92c3e)),('sonya',parser.SONYA_BLOCK,(0x92cf2,0x92d74))]:
        out=generated/f'{fighter.upper()}ART.ASM'
        assert not out.exists(), 'Do not silently overwrite generated source'
        groups=parser.group_references(data,*block)
        poses={address:frames for _,address,frames in groups}
        frames=sorted({p for values in poses.values() for p in values})
        assert poses and frames
        prefix=f'ks_{fighter}'
        lines=['; Generated typed image/palette/composite DATA. No executable opcode words.',
               '; Input and record counts: ART_IMPORT.json. Original bit addresses remain',
               '; in label names for traceability, not as runtime addresses.',
               '; Graphics ROM bytes are appended after MKII at byte 0x00c00000.',
               '        .data']
        for variant,offset in zip(('primary','alternate'),offsets):
            count=struct.unpack_from('<I',data,offset)[0]; assert count==64
            colors=struct.unpack_from('<64H',data,offset+4)
            label=f'{prefix}_{variant}_palette'
            lines += [f'        .def {label}',f'{label}', '        .word 65,0']
            for i in range(0,64,8): lines.append('        .word '+','.join(word(x) for x in colors[i:i+8]))
        for address in frames:
            at=parser.stock_file(address)
            width,height,x,y,sag,control=struct.unpack_from('<HHHHIH',data,at)
            assert parser.looks_like_frame(data,at)
            payload,bits=bitstream(gfx,sag,width,height,control)
            key=(bits,sha(payload))
            if key not in streams:
                streams[key]=len(packed); packed.extend(payload)
            new_offset=streams[key]
            check=bytes(packed[new_offset:new_offset+len(payload)])
            assert check==payload
            verified+=1
            native_sag=(0xc00000+new_offset)*8
            assert native_sag < 0x10000000, 'Cannot fit on normal Wolf graphics bus'
            label=f'{prefix}_frame_{address:08x}'
            lines += [f'{label}',f'        .word {width},{height},{parser.signed(x)},{parser.signed(y)}',
                      f'        .long 0{native_sag:08x}h',f'        .word {word(control)}',
                      f'        .long {prefix}_primary_palette']
        for address,values in sorted(poses.items()):
            label=f'{prefix}_pose_{address:08x}'
            lines += [f'        .def {label}',label]
            lines += [f'        .long {prefix}_frame_{p:08x}' for p in values]
            lines += ['        .long 0']
        out.parent.mkdir(exist_ok=True)
        contents=('\n'.join(lines)+'\n').encode(); out.write_bytes(contents)
        report['fighters'][fighter]=dict(source=str(out.relative_to(ROOT)),sourceSHA256=sha(contents),
            frameRecords=len(frames),compositePoses=len(poses),palettes=2,
            expectedDataBytes=2*132+18*len(frames)+sum(4*(len(v)+1) for v in poses.values()))
    assert len(packed)<=0x600000, 'Exceeds six MiB available in STOCK MK3 socket layout'
    (generated/'fighter_graphics.bin').write_bytes(packed)
    # Standard MK3 sockets after the three MKII banks: 4 MiB + 2 MiB.
    region=packed+bytes(0x600000-len(packed))
    socket_hashes={}
    for bank,size in [(0,0x100000),(1,0x80000)]:
        for lane in range(4):
            chip=121-bank*4-lane
            name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            payload=region[bank*0x400000+lane:bank*0x400000+lane+size*4:4]
            assert len(payload)==size
            (generated/name).write_bytes(payload); socket_hashes[name]=sha(payload)
    report['graphicsPacking']=dict(bytes=len(packed),capacity=0x600000,
        stockMK3SocketLayoutFits=True,uniqueStreams=len(streams),verifiedFrameBitstreams=verified,
        SHA256=sha(packed),sockets=socket_hashes)
    (generated/'ART_IMPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
