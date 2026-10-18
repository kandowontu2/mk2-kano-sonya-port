"""Append original Kano/Sonya photos as typed native DMA image data.

Preparation only until linked into native ending code and runtime qualified.
No compressed-picture emulator extension or executable binary payload.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys
import zipfile

PORT=Path(__file__).resolve().parent
ROOT=PORT.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_native_ending_reference import reference

sha=lambda data:hashlib.sha256(data).hexdigest().upper()

def build(target=None,prefix_path=None):
    output=Path(target) if target else PORT/'generated_ending'
    assert not output.exists(), 'Do not overwrite an existing graphics generation'
    prefix=(Path(prefix_path) if prefix_path else PORT/'generated_morph/fighter_ui_finish_morph_graphics.bin').read_bytes()
    gfx=bytearray(0x1200000)
    inputs={}
    with zipfile.ZipFile(ROOT/'mk3.zip') as archive:
        for bank in range(5):
            for lane in range(4):
                chip=133-bank*4-lane
                name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
                data=archive.read(name)
                at=bank*0x400000+lane
                gfx[at:at+len(data)*4:4]=data
                inputs[name]=sha(data)
    packed=bytearray(prefix)
    lines=['; Original donor photos, native typed image/palette records only.',
           '; Generated reproducibly from user-supplied MK3 graphics ROMs.',
           '        .data']
    images=[]
    output.mkdir(parents=True)
    for fighter,name in enumerate(('kano','sonya')):
        for page in range(2):
            record,preview,origin=reference(gfx,fighter,page)
            width,height,frames,count=struct.unpack_from('<4H',record)
            assert frames==1 and count==256
            palette=struct.unpack_from('<256H',record,8)
            pixels=record[520:]
            assert len(pixels)==width*height and min(pixels)>0
            # Keep every original photo pixel nontransparent. Index zero is
            # reserved for the engine; black areas use a nonzero black index.
            start=len(packed)
            packed.extend(pixels)
            label=f'ks_end_{name}_picture{page+1}'
            lines += [f'        .def {label}',label,
                f'        .word {width},{height},0,0',
                f'        .long 0{((0xc00000+start)*8):08x}h',
                '        .word 00000h ; eight-bit, uncompressed native DMA',
                f'        .long {label}_palette',label+'_palette',
                '        .word 256']
            for at in range(0,256,8):
                lines.append('        .word '+','.join(f'0{value:04x}h' for value in palette[at:at+8]))
            preview.save(output/f'{name}_page{page+1}.png')
            images.append(dict(actor=name,page=page+1,label=label,width=width,height=height,
                packedOffset=start,bytes=len(pixels),pixelsSHA256=sha(pixels),
                paletteSHA256=sha(record[8:520]),sourcePicture=origin,
                independentReferenceSHA256=sha(record)))
    assert packed[:len(prefix)]==prefix and len(packed)<0x600000
    source=('\n'.join(lines)+'\n').encode()
    (output/'KSENDART.ASM').write_bytes(source)
    (output/'fighter_ui_finish_ending_graphics.bin').write_bytes(packed)
    report=dict(prefixSHA256=sha(prefix),prefixBytes=len(prefix),packedSHA256=sha(packed),
        appendedBytes=len(packed)-len(prefix),totalGraphicsBytes=len(packed),
        sourceSHA256=sha(source),images=images,donorGraphicsSHA256=inputs,
        decoderSHA256=sha((ROOT/'tools/decode_native_picture.py').read_bytes()),
        layoutGeneratorSHA256=sha((ROOT/'tools/build_native_ending_reference.py').read_bytes()),
        nativeDataOnly=True,originalPixelsDerivedByNearestNeighbourLayout=True,
        linkedIntoGame=False,runtimeVerified=False,releaseReady=False)
    (output/'ENDING_ART.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def emit_sockets():
    output=PORT/'generated_ending'
    report=json.loads((output/'ENDING_ART.json').read_text())
    packed=(output/'fighter_ui_finish_ending_graphics.bin').read_bytes()
    assert sha(packed)==report['packedSHA256']
    assert sha((output/'KSENDART.ASM').read_bytes())==report['sourceSHA256']
    region=packed+bytes(0x600000-len(packed))
    rebuilt=bytearray(len(region));sockets={}
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip=121-bank*4-lane;start=bank*0x400000+lane
            name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            assert not (output/name).exists()
            raw=region[start:start+size*4:4]
            assert len(raw)==size
            (output/name).write_bytes(raw)
            rebuilt[start:start+size*4:4]=raw;sockets[name]=sha(raw)
    assert rebuilt==region
    report.update(sockets=sockets,socketsEmitted=True,stockSocketRoundTripVerified=True)
    (output/'ENDING_ART.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    report=emit_sockets() if '--emit-sockets' in sys.argv else build()
    print(json.dumps({key:value for key,value in report.items() if key not in ('images','donorGraphicsSHA256')},indent=2))
