"""Encode own impalement drafts as typed native ROM data, never driver payloads."""
import json
import struct
import sys
from pathlib import Path
from PIL import Image
from generate_head_sources import PORT, sha
import import_character_art as art

OUT = PORT/'generated_impale'
SOURCE = PORT/'assets/impale'

def main(prefix_path=None,output=None,source_output=None,emit_sockets=True):
    global OUT,SOURCE
    if output is not None:OUT=Path(output)
    if source_output is not None:
        SOURCE=Path(source_output)
        assert not SOURCE.exists()
    assert not OUT.exists() or '--refresh-generated' in sys.argv
    OUT.mkdir(exist_ok=True)
    SOURCE.mkdir(exist_ok=True)
    draft = PORT/'assets/impale_draft'
    manifest = json.loads((draft/'DRAFT_MANIFEST.json').read_text())
    prefix = (Path(prefix_path) if prefix_path is not None else PORT/'generated_nut/fighter_ui_finish_nut_graphics.bin').read_bytes()
    packed = bytearray(prefix)
    program = (art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    lines = ['; Authored impalement victim artwork and native two-part animation DATA.',
             '        .include mainequ.asm', '        .ref ks_kano_primary_palette',
             '        .ref ks_sonya_primary_palette', '        .data']
    frames = []
    preview = Image.new('RGBA', (360,330), (35,35,40,255))
    for actor_index, source in enumerate(manifest['actors']):
        actor = source['actor']
        path = draft/source['asset']
        assert sha(path.read_bytes()) == source['SHA256']
        assert sha((draft/source['promptFile']).read_bytes()) == source['promptSHA256']
        colors = struct.unpack_from('<64H', program, (0x92bbc if actor=='kano' else 0x92cf2)+4)
        palette = [(0,0,0)]+[((v>>10&31)*255//31,(v>>5&31)*255//31,(v&31)*255//31) for v in colors[:63]]
        nearest = {}
        bounds = source['frames'][0]['alpha128Bounds']
        scale = 143/(bounds[3]-bounds[1])
        with Image.open(path) as atlas:
            assert atlas.mode == 'RGBA'
            for frame in source['frames']:
                assert not frame['touchesCellEdge']
                phase = frame['phase']
                crop = atlas.crop(frame['cell']).crop(frame['alpha128Bounds'])
                w,h = round(crop.width*scale),round(crop.height*scale)
                scaled = crop.resize((w,h), Image.Resampling.LANCZOS)
                indices = []
                for r,g,b,a in scaled.getdata():
                    if a < 128:
                        indices.append(0)
                        continue
                    key = (r,g,b)
                    if key not in nearest:
                        nearest[key] = min(range(1,64), key=lambda i:sum((key[c]-palette[i][c])**2 for c in range(3)))
                    indices.append(nearest[key])
                # Preserve reference phase bounds around the native suspended origin.
                # All three poses share one scale; do not independently stretch poses.
                xo = round(w/2)-(6,10,9)[phase]
                yo = h-(142,136,140)[phase]
                filename = f'{actor}_{phase}.pgm'
                pgm = f'P2\n# Native palette indices, not grayscale luminance.\n{w} {h}\n63\n'
                pgm += '\n'.join(' '.join(map(str,indices[y*w:(y+1)*w])) for y in range(h))+'\n'
                (SOURCE/filename).write_text(pgm,encoding='ascii')
                payload = bytearray((w*h*6+7)//8)
                for i,v in enumerate(indices):
                    at,shift = divmod(i*6,8)
                    payload[at] |= v<<shift&255
                    if shift>2: payload[at+1] |= v>>(8-shift)
                offset = len(packed)
                packed.extend(payload)
                label,pose = f'ks_im_{actor}_frame{phase}',f'ks_im_{actor}_pose{phase}'
                lines += [f'        .def {label},{pose}',label,f'        .word {w},{h},{xo},{yo}',
                    f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 06000h',
                    f'        .long ks_{actor}_primary_palette',pose,f'        .long {label},0']
                frames.append(dict(actor=actor,phase=phase,file=filename,width=w,height=h,
                    xOffset=xo,yOffset=yo,uniformScale=scale,indexSHA256=sha(bytes(indices)),
                    fileSHA256=sha((SOURCE/filename).read_bytes()),packedByteOffset=offset,
                    packedSHA256=sha(payload),sourceDraftSHA256=source['SHA256']))
                decoded = Image.new('RGBA',(w,h))
                decoded.putdata([(*palette[i],255) if i else (0,0,0,0) for i in indices])
                preview.alpha_composite(decoded,(phase*120+20,actor_index*165+155-h))
        p = [f'ks_im_{actor}_pose{i}' for i in range(3)]
        lines += [f'        .def ks_{actor}_impaled',f'ks_{actor}_impaled',
            f'        .long ani_adjustxy,0010ffa0h,{p[0]}',
            f'        .long ani_adjustxy,0ffe80000h,{p[0]}',
            f'        .long ani_adjustxy,0ffe80000h,{p[0]}',
            f'        .long ani_adjustxy,0ffe80010h,{p[0]},0',
            f'        .long {p[0]},{p[1]},{p[2]},{p[1]},{p[0]},{p[1]},{p[2]},0']
    assert packed[:len(prefix)] == prefix and len(packed)<0x600000
    (OUT/'KSIMART.ASM').write_text('\n'.join(lines)+'\n')
    (OUT/'fighter_ui_finish_impale_graphics.bin').write_bytes(packed)
    region = packed+bytes(0x600000-len(packed))
    rebuilt = bytearray(0x600000)
    sockets = {}
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip = 121-bank*4-lane
            name = f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start = bank*0x400000+lane
            payload = region[start:start+size*4:4]
            assert len(payload)==size
            if emit_sockets:
                (OUT/name).write_bytes(payload)
            rebuilt[start:start+size*4:4] = payload
            sockets[name] = sha(payload)
    assert rebuilt == region
    report = dict(frames=frames,sockets=sockets,prefixSHA256=sha(prefix),prefixBytes=len(prefix),
        appendedBytes=len(packed)-len(prefix),stockSocketRoundTripVerified=True,
        runtimeVerified=False,fullVisualAcceptance=False,fullPortVerified=False)
    (OUT/'IMPALE_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    (SOURCE/'IMPALE_SOURCE.json').write_text(json.dumps(dict(frames=frames,runtimeVerified=False),indent=2)+'\n')
    preview.resize((720,660),Image.Resampling.NEAREST).save(SOURCE/'palette_preview.png')
    print(json.dumps({k:v for k,v in report.items() if k not in ('frames','sockets')}))

if __name__=='__main__': main()
