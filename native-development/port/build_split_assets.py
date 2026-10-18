"""Encode dedicated split components and synchronized own-half scripts."""
import json
from pathlib import Path
from build_arm_rip_assets import read_pgm,sha
from build_inflation_assets import pack6,unpack6

PORT=Path(__file__).resolve().parent
SOURCE=PORT/'assets/split_v2'
OUT=PORT/'generated_split'


def main(prefix_path=None,output=None,emit_sockets=True):
    target=Path(output) if output is not None else OUT
    assert not target.exists()
    manifest_path=SOURCE/'SPLIT_SOURCES.json'
    manifest=json.loads(manifest_path.read_text())
    assert manifest['kanoHalfContinuityRevision'] and manifest['unchangedOtherFrames']==20
    prefix_path=Path(prefix_path) if prefix_path is not None else PORT/'generated_ingestion/fighter_ui_finish_ingest_graphics.bin'
    prefix=prefix_path.read_bytes()
    packed=bytearray(prefix)
    lines=['; Dedicated own vertical-split DATA. Visual acceptance tracked separately.',
        '        .include mainequ.asm','        .ref ks_kano_primary_palette,ks_sonya_primary_palette','        .data']
    frames=[]
    for frame in manifest['frames']:
        path=SOURCE/frame['file']
        assert sha(path.read_bytes())==frame['SHA256']
        w,h,pixels=read_pgm(path)
        assert (w,h)==(frame['width'],frame['height'])
        payload=pack6(pixels)
        assert unpack6(payload,w*h)==pixels
        role={'whole':'whole','viewer_left':'left','viewer_right':'right'}[frame['role']]
        stem=f'ks_sp_{frame["actor"]}_{role}'
        label=f'{stem}_frame{frame["phase"]}'
        pose=f'{stem}_pose{frame["phase"]}'
        offset=len(packed)
        packed.extend(payload)
        lines += [f'        .def {label},{pose}',label,
            f'        .word {w},{h},{frame["xOffset"]},{frame["yOffset"]}',
            f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 06000h',
            f'        .long ks_{frame["actor"]}_primary_palette',pose,f'        .long {label},0']
        frames.append(dict(**frame,imageLabel=label,poseLabel=pose,packedByteOffset=offset,
            packedBytes=len(payload),packedSHA256=sha(payload),sixBitRoundTripVerified=True))
    for actor in ('kano','sonya'):
        label=f'ks_{actor}_split'
        lines += [f'        .def {label}',label]
        lines += [f'        .long ks_sp_{actor}_whole_pose{i}' for i in range(3)]
        lines += ['        .long 0']
        lines += [f'        .long ks_sp_{actor}_left_pose{i}' for i in range(3,10)]
        lines += ['        .long 0',f'        .def ks_{actor}_split_other',f'ks_{actor}_split_other']
        lines += [f'        .long ks_sp_{actor}_right_pose{i}' for i in range(3,10)]
        lines += ['        .long 0']
    assert len(frames)==34 and len(packed)<0x600000
    assembly=('\n'.join(lines)+'\n').encode('ascii')
    region=packed+bytes(0x600000-len(packed))
    rebuilt=bytearray(len(region))
    socket_data={}
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip=121-bank*4-lane
            name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane
            data=region[start:start+size*4:4]
            assert len(data)==size
            socket_data[name]=data
            rebuilt[start:start+size*4:4]=data
    assert rebuilt==region
    target.mkdir()
    (target/'KSPLART.ASM').write_bytes(assembly)
    (target/'fighter_ui_finish_split_graphics.bin').write_bytes(packed)
    if emit_sockets:
        for name,data in socket_data.items():(target/name).write_bytes(data)
    report=dict(format='MK2KS-SPLIT-TYPED-DATA-1',frames=frames,
        sourceManifestSHA256=sha(manifest_path.read_bytes()),assemblySHA256=sha(assembly),
        prefixSHA256=sha(prefix),prefixBytes=len(prefix),packedSHA256=sha(packed),
        appendedBytes=len(packed)-len(prefix),prefixPreservedByteIdentical=True,
        sockets={name:sha(data) for name,data in socket_data.items()},socketsEmitted=emit_sockets,
        stockSocketRoundTripVerified=True,sixBitRoundTripVerified=True,
        dedicatedSecondaryScripts=True,runtimeVerified=False,visualAcceptance=False,releaseReady=False)
    (target/'SPLIT_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(frames=34,appendedBytes=report['appendedBytes'],runtimeVerified=False)))


if __name__=='__main__':main()
