"""Native typed morph frames/palettes; append only, no emulator game code."""
import json
from pathlib import Path
from build_arm_rip_assets import read_pgm,sha
from build_inflation_assets import pack6,unpack6

PORT=Path(__file__).resolve().parent
SOURCE=PORT/'assets/morph'
OUT=PORT/'generated_morph'

def main(prefix_path=None,output=None,emit_sockets=True):
    target=Path(output) if output is not None else OUT
    assert not target.exists(),'Never overwrite generated candidate data'
    manifest_path=SOURCE/'MORPH_SOURCES.json'
    source=json.loads(manifest_path.read_text())
    prefix_path=Path(prefix_path) if prefix_path is not None else PORT/'generated_split/fighter_ui_finish_split_graphics.bin'
    prefix=prefix_path.read_bytes();packed=bytearray(prefix)
    lines=['; Authored own morph intermediate DATA, acceptance tracked separately.','        .include mainequ.asm','        .data']
    for actor in ('kano','sonya'):
        colors=source['palettes'][actor]
        assert len(colors)==64 and colors[0]==0 and all(0<=v<0x8000 for v in colors)
        label=f'ks_{actor}_morph_palette'
        lines += [f'        .def {label}',label,'        .word 65']
        # Native palette count is 65: transparent slot + 63 colors + trailing slot.
        for at in range(0,64,8):lines += ['        .word '+','.join(f'0{v:04x}h' for v in colors[at:at+8])]
        lines += ['        .word 0']
    frames=[]
    for frame in source['frames']:
        path=SOURCE/frame['file'];assert sha(path.read_bytes())==frame['SHA256']
        w,h,pixels=read_pgm(path);assert (w,h)==(frame['width'],frame['height'])
        payload=pack6(pixels);assert unpack6(payload,w*h)==pixels
        label=f'ks_mo_{frame["actor"]}_frame{frame["phase"]}'
        pose=f'ks_mo_{frame["actor"]}_pose{frame["phase"]}'
        offset=len(packed);packed.extend(payload)
        lines += [f'        .def {label},{pose}',label,
            f'        .word {w},{h},{frame["xOffset"]},{frame["yOffset"]}',
            f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 06000h',
            f'        .long {frame["paletteLabel"]}',pose,f'        .long {label},0']
        frames.append(dict(**frame,imageLabel=label,poseLabel=pose,packedByteOffset=offset,
            packedBytes=len(payload),packedSHA256=sha(payload),sixBitRoundTripVerified=True))
    assert len(frames)==6 and len(packed)<0x600000
    assembly=('\n'.join(lines)+'\n').encode('ascii')
    region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(len(region));sockets={}
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip=121-bank*4-lane;start=bank*0x400000+lane
            name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            data=region[start:start+size*4:4];assert len(data)==size
            sockets[name]=data;rebuilt[start:start+size*4:4]=data
    assert rebuilt==region
    target.mkdir()
    (target/'KSMOART.ASM').write_bytes(assembly)
    (target/'fighter_ui_finish_morph_graphics.bin').write_bytes(packed)
    if emit_sockets:
        for name,data in sockets.items():(target/name).write_bytes(data)
    report=dict(frames=frames,palettes=source['palettes'],sourceManifestSHA256=sha(manifest_path.read_bytes()),
        assemblySHA256=sha(assembly),prefixSHA256=sha(prefix),prefixBytes=len(prefix),
        packedSHA256=sha(packed),appendedBytes=len(packed)-len(prefix),prefixPreservedByteIdentical=True,
        sockets={name:sha(data) for name,data in sockets.items()},socketsEmitted=emit_sockets,
        stockSocketRoundTripVerified=True,sixBitRoundTripVerified=True,
        linkedIntoROM=False,runtimeVerified=False,finalVisualAcceptance=False,releaseReady=False)
    (target/'MORPH_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(frames=6,appendedBytes=report['appendedBytes'],linkedIntoROM=False)))

if __name__=='__main__':main()
