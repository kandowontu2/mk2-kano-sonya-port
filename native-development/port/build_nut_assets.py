"""Encode the authored Kano low-blow reaction as native typed ROM data."""
import json
from pathlib import Path
import struct
import sys
from PIL import Image
from generate_head_sources import PORT,sha
import import_character_art as art
OUT=PORT/'generated_nut';SOURCE=PORT/'assets/nut'
def main(prefix_path=None,output=None,source_output=None,emit_sockets=True):
    global OUT,SOURCE
    if output is not None:OUT=Path(output)
    if source_output is not None:
        SOURCE=Path(source_output)
        assert not SOURCE.exists()
    assert not OUT.exists() or '--refresh-generated' in sys.argv
    OUT.mkdir(exist_ok=True);SOURCE.mkdir(exist_ok=True)
    draft=PORT/'assets/nut_draft'
    manifest=json.loads((draft/'DRAFT_MANIFEST.json').read_text())
    path=draft/manifest['asset'];assert sha(path.read_bytes())==manifest['SHA256']
    program=(art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    colors=struct.unpack_from('<64H',program,0x92bbc+4)
    palette=[(0,0,0)]+[((v>>10&31)*255//31,(v>>5&31)*255//31,(v&31)*255//31) for v in colors[:63]]
    prefix=(Path(prefix_path) if prefix_path is not None else PORT/'generated_torso/fighter_ui_finish_torso_graphics.bin').read_bytes()
    packed=bytearray(prefix);frames=[];nearest={}
    lines=['; Authored own Kano nut-punch sprite DATA.', '        .include mainequ.asm',
           '        .ref ks_kano_primary_palette','        .data']
    preview=Image.new('RGBA',(320,150),(35,35,40,255))
    scale=125/(manifest['frames'][0]['alpha128Bounds'][3]-manifest['frames'][0]['alpha128Bounds'][1])
    with Image.open(path) as atlas:
        assert atlas.mode=='RGBA'
        for frame in manifest['frames']:
            assert not frame['touchesCellEdge']
            phase=frame['phase'];cell=atlas.crop(frame['cell']);box=frame['alpha128Bounds']
            crop=cell.crop(box);w,h=round(crop.width*scale),round(crop.height*scale)
            scaled=crop.resize((w,h),Image.Resampling.LANCZOS);indices=[]
            for r,g,b,a in scaled.getdata():
                if a<128:indices.append(0);continue
                key=(r,g,b)
                if key not in nearest:
                    nearest[key]=min(range(1,64),key=lambda i:sum((key[c]-palette[i][c])**2 for c in range(3)))
                indices.append(nearest[key])
            feet=[i%w for i in range((h-3)*w,h*w) if indices[i]];assert feet
            xo=round((min(feet)+max(feet))/2);yo=h-131
            filename=f'kano_{phase}.pgm'
            text=f'P2\n# Native palette indices, not grayscale luminance.\n{w} {h}\n63\n'
            text+='\n'.join(' '.join(map(str,indices[y*w:(y+1)*w])) for y in range(h))+'\n'
            (SOURCE/filename).write_text(text,encoding='ascii')
            payload=bytearray((w*h*6+7)//8)
            for i,v in enumerate(indices):
                at,shift=divmod(i*6,8);payload[at]|=v<<shift&255
                if shift>2:payload[at+1]|=v>>(8-shift)
            scalar=int.from_bytes(payload,'little')
            assert bytes(scalar>>(i*6)&63 for i in range(w*h))==bytes(indices)
            offset=len(packed);packed.extend(payload)
            label=f'ks_nut_kano_frame{phase}';pose=f'ks_nut_kano_pose{phase}'
            lines += [f'        .def {label},{pose}',label,f'        .word {w},{h},{xo},{yo}',
                f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 06000h',
                '        .long ks_kano_primary_palette',pose,f'        .long {label},0']
            frames.append(dict(phase=phase,file=filename,width=w,height=h,xOffset=xo,yOffset=yo,
                indexSHA256=sha(bytes(indices)),fileSHA256=sha((SOURCE/filename).read_bytes()),
                packedByteOffset=offset,packedSHA256=sha(payload),uniformScale=scale))
            decoded=Image.new('RGBA',(w,h));decoded.putdata([(*palette[i],255) if i else (0,0,0,0) for i in indices])
            preview.alpha_composite(decoded,(phase*160+30,140-h))
    lines += ['        .def ks_kano_nutcrunched','ks_kano_nutcrunched',
              '        .long ks_nut_kano_pose0,ks_nut_kano_pose1,0',
              '        .long ks_nut_kano_pose0,0']
    assert packed[:len(prefix)]==prefix and len(packed)<0x600000
    (OUT/'KSNUTART.ASM').write_text('\n'.join(lines)+'\n')
    (OUT/'fighter_ui_finish_nut_graphics.bin').write_bytes(packed)
    region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(0x600000);sockets={}
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane;payload=region[start:start+size*4:4]
            assert len(payload)==size
            if emit_sockets:
                (OUT/name).write_bytes(payload)
            rebuilt[start:start+size*4:4]=payload;sockets[name]=sha(payload)
    assert rebuilt==region
    report=dict(frames=frames,sockets=sockets,sourceDraftSHA256=manifest['SHA256'],
        prefixSHA256=sha(prefix),prefixBytes=len(prefix),appendedBytes=len(packed)-len(prefix),
        independentIndexDecodeVerified=True,stockSocketRoundTripVerified=True,
        runtimeVerified=False,fullVisualAcceptance=False,fullPortVerified=False)
    (OUT/'NUT_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    (SOURCE/'NUT_SOURCE.json').write_text(json.dumps(dict(frames=frames,sourceDraftSHA256=manifest['SHA256'],runtimeVerified=False),indent=2)+'\n')
    preview.resize((640,300),Image.Resampling.NEAREST).save(SOURCE/'palette_preview.png')
    print(json.dumps({k:v for k,v in report.items() if k not in ('frames','sockets')}))
if __name__=='__main__':main()
